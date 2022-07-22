from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
from datetime import datetime
import io

from . import core
from . utils import register_class
from .auid import AUID
from .rational import AAFRational
from .interpolation import integrate_iter, lerp, cubic_interpolate, bezier_interpolate


ConstantInterp     = AUID("5b6c85a5-0ede-11d3-80a9-006008143e6f")
LinearInterp       = AUID("5b6c85a4-0ede-11d3-80a9-006008143e6f")
BezierInterpolator = AUID("df394eda-6ac6-4566-8dbe-f28b0bdd781a")
CubicInterpolator  = AUID("a04a5439-8a0e-4cb7-975f-a5b255866883")

class TaggedValueHelper(object):
    def __init__(self, poperty_vector):
        self.p = poperty_vector

    def get(self, key, default=None):
        for item in self.p:
            if item['Name'].value == key:
                return item
        return default

    def __contains__(self, key):
        return not self.get(key, None) is None

    def __getitem__(self, key):
        p = self.get(key, None)
        if p:
            return p['Value'].value

        raise IndexError(key)

    def items(self):
        for item in self.p:
            yield item['Name'].value, item["Value"].value

    def append(self, value):
        self.p.append(value)

    def __setitem__(self, key, value):
        tag = self.get(key, None)
        if tag is None:
            tag = self.p.parent.root.create.TaggedValue()
            tag['Name'].value = key
            self.p.append(tag)

        tag['Value'].value = value

@register_class
class TaggedValue(core.AAFObject):
    class_id = AUID("0d010101-0101-3f00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, name=None, value=None, value_typedef=None):
        self.name = name
        if value is not None:
            self.encode_value(value, value_typedef)

    @property
    def name(self):
        return self['Name'].value

    @name.setter
    def name(self, value):
        self['Name'].value = value

    @property
    def value(self):
        return self['Value'].value

    @value.setter
    def value(self, value):
        self['Value'].value = value

    @property
    def value_typedef(self):
        if self['Value'].data:
            return self['Value'].typedef.decode_typedef(self['Value'].data)

    def encode_value(self, value, value_typedef=None):
        if value_typedef is None:
            self.value = value
            return
        self['Value'].add_pid_entry()
        self['Value'].data = self['Value'].typedef.encode(value, value_typedef)
        self['Value'].mark_modified()

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                                self.__class__.__name__)

        value_typedef = self.value_typedef
        if value_typedef:
            s += ' %s' % repr(value_typedef)

        name = self.name
        if name:
            s += ' %s' % name

        s += " = " + repr(self.value)

        return '<%s at 0x%x>' % (s, id(self))

class Parameter(core.AAFObject):
    class_id = AUID("0d010101-0101-3c00-060e-2b3402060101")
    __slots__ = ()

    @property
    def auid(self):
        return self['Definition'].value
    @auid.setter
    def auid(self, value):
        self['Definition'].value = value

    @property
    def parameterdef(self):
        return self.root.dictionary.lookup_parameterdef(self['Definition'].value)

    @parameterdef.setter
    def parameterdef(self, value):
        self['Definition'].value = value.auid

    @property
    def name(self):
        return self.parameterdef.name

    @property
    def unique_property(self):
        return self['Definition']

    @property
    def unique_key(self):
        return self.unique_property.value

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                                self.__class__.__name__)

        parameterdef = self.parameterdef
        if parameterdef:
            s += ' %s' % parameterdef.name

        return '<%s at 0x%x>' % (s, id(self))

@register_class
class ConstantValue(Parameter):
    class_id = AUID("0d010101-0101-3d00-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, parameterdef=None, value=None):
        super(ConstantValue, self).__init__()

        if parameterdef is not None:
            self.parameterdef = self.root.dictionary.lookup_parameterdef(parameterdef)

        if value is not None:
            if parameterdef is None:
                raise ValueError("need parameterdef to initialize value")
            self.value = value

    @property
    def typedef(self):
        return self.parameterdef.typedef

    def value_at(self, t):
        return self.value

    @property
    def value(self):
        return self['Value'].value

    @value.setter
    def value(self, value):
        self['Value'].add_pid_entry()
        indirect_typedef = self['Value'].typedef
        parameter_typdef = self.typedef
        self['Value'].data = indirect_typedef.encode(value, parameter_typdef)
        self['Value'].mark_modified()


@register_class
class VaryingValue(Parameter):
    class_id = AUID("0d010101-0101-3e00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, parameterdef=None, interperlationdef=None):
        super(VaryingValue, self).__init__()
        if parameterdef:
            self.parameterdef = self.root.dictionary.lookup_parameterdef(parameterdef)

        if interperlationdef:
            self.interpolationdef = self.root.dictionary.lookup_interperlationdef(interperlationdef)

    @property
    def interpolationdef(self):
        return self['Interpolation'].value

    @interpolationdef.setter
    def interpolationdef(self, value):
        self['Interpolation'].value = value

    # TODO: Deprecate this
    @property
    def interpolation(self):
        return self['Interpolation'].value

    @interpolation.setter
    def interpolation(self, value):
        self['Interpolation'].value = value

    @property
    def pointlist(self):
        return self['PointList']

    @property
    def typedef(self):
        return self.parameterdef.typedef

    def add_keyframe(self, time, value, edit_hint=None):
        cp = self.root.create.ControlPoint()
        cp.time = time

        cp['Value'].add_pid_entry()
        cp['Value'].data = cp['Value'].typedef.encode(value, self.typedef)
        cp['Value'].mark_modified()

        if edit_hint:
            cp['EditHint'].value = edit_hint

        pointlist = self['PointList']

        if len(pointlist) > 0:
            index = self.nearest_index(time)
            nearest = pointlist[index]
            if float(nearest.time) == float(time):
                pointlist[index] = cp
            else:
                pointlist.insert(index+1, cp)
        else:
            pointlist.append(cp)

        return cp

    def value_at(self, t):
        t = float(t)

        index = self.nearest_index(t)
        pointlist = self['PointList']

        p1 = pointlist[index]

        # clamp if t outside of range
        if t < p1.time or index + 1 >= len(pointlist):
            return float(p1.value)

        if self.interpolationdef.auid == ConstantInterp:
            return float(p1.value)

        p2 = pointlist[index+1]

        if self.interpolationdef.auid == LinearInterp:
            t_len = float(p2.time) - float(p1.time)
            t_diff = t - float(p1.time)
            t_mix = t_diff/t_len

            v0 = float(p1.value)
            v1 = float(p2.value)
            return lerp(v0, v1, t_mix)

        elif self.interpolationdef.auid == BezierInterpolator:
            t0 = float(p1.time)
            v0 = float(p1.value)

            t3 = float(p2.time)
            v3 = float(p2.value)

            tangents = p1.tangents[1]
            t1 = t0 + tangents[0]
            v1 = v0 + tangents[1]

            tangents = p2.tangents[0]
            t2 = t3 + tangents[0]
            v2 = v3 + tangents[1]

            return bezier_interpolate((t0, v0),
                                      (t1, v1),
                                      (t2, v2),
                                      (t3, v3), t)

        elif self.interpolationdef.auid == CubicInterpolator:

            t1 = float(p1.time)
            v1 = float(p1.value)

            t2 = float(p2.time)
            v2 = float(p2.value)

            if index - 1 >= 0:
                p0 = pointlist[index - 1]
                t0 = float(p0.time)
                v0 = float(p0.value)
            else:
                t0 = t1 - ((t2 - t1) * 0.5)
                v0 = v1

            if index + 2 < len(pointlist):
                p3 = pointlist[index + 2]
                t3 = float(p3.time)
                v3 = float(p3.value)
            else:
                t3 = t2 + ((t2 - t1) * 0.5)
                v3 = v2

            return cubic_interpolate((t0, v0),
                                     (t1, v1),
                                     (t2, v2),
                                     (t3, v3), t)

        else:

            raise NotImplementedError("Interpolation not implemented for %s %s" %
                           (self.interpolationdef.name, str(self.interpolationdef.auid)))

    def nearest_index(self, t):
        """
        binary search for index of point.time <= t
        """
        pointlist = self['PointList']
        start = 0
        end = len(pointlist) - 1
        while True:
            if end < start:
                return max(0, end)

            m = (start + end) // 2
            p = pointlist[m]
            if p.time < t:
                start = m + 1
            elif p.time > t:
                end = m - 1
            else:
                return m

@register_class
class ControlPoint(core.AAFObject):
    class_id = AUID("0d010101-0101-1900-060e-2b3402060101")
    __slots__ = ()

    @property
    def time(self):
        return float(self['Time'].value)

    @time.setter
    def time(self, value):
        self['Time'].value = value

    @property
    def value(self):
        return float(self['Value'].value)

    @value.setter
    def value(self, value):
        self['Value'].value = AAFRational(value)

    @property
    def point_properties(self):
        props = {}
        if 'ControlPointPointProperties' in self:
            for p in self['ControlPointPointProperties'].value:
                props[p.name] = p.value
        return props

    @property
    def base_frame(self):
        return self.point_properties.get("PP_BASE_FRAME_U", 0)

    @property
    def tangents(self):
        props = self.point_properties
        return [(float(props.get("PP_IN_TANGENT_POS_U", 0)),
                 float(props.get("PP_IN_TANGENT_VAL_U", 0))),
                (float(props.get("PP_OUT_TANGENT_POS_U", 0)),
                 float(props.get("PP_OUT_TANGENT_VAL_U", 0)))]

def generate_offset_map(speed_map, start=0, end=None):
    pointlist = speed_map['PointList']

    # first speed map key frame is the zero point
    # of the offset map curve
    first = pointlist.value[0]
    center = int(first.time)
    if end is None:
        last = pointlist.value[-1]
        end = int(last.time)

    if start > end:
        raise ValueError("start needs to be less then end")

    time = []
    value = []
    offset_index = None

    inter_start = min(start, center)
    inter_end = max(center,  end+1)

    for i, (t,v) in enumerate(integrate_iter(speed_map.value_at, inter_start, inter_end)):
        time.append(t)
        value.append(v)

        if t == center:
            offset_index = i

    center_offset = value[offset_index]

    # not really sure what this base frame offset is about
    # but appears to contain the how much calculation is off...
    center_offset -= first.base_frame

    result = []
    for i, t in enumerate(time):
        if t > end:
            break

        if t >= start:
            v = value[i] - center_offset
            result.append((t, v))

    return result
