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

def lerp(p0, p1, t):
    value = ((1.0 - t) * p0) + (t * p1)
    return value

def cubic_bezier(p0, p1, p2, p3, t):
    value = pow(1.0 - t, 3.0) * p0 + \
            pow(1.0 - t, 2.0) * 3.0 * t * p1 + \
            (1.0 - t) * 3.0 * t * t * p2 + \
            t * t * t * p3
    return value

def cubic_bezier_interpolate(p0, p1, p2, p3, t):

    t_len = p3[0] - p0[0]
    t_diff = t - p0[0]
    t_mix = t_diff/t_len

    guess_t = t_mix

    # approxmate the correct t value,
    # not sure if this correct
    # its slow but seems to work..
    for i in range(20):
        x = cubic_bezier(p0[0], p1[0], p2[0], p3[0], guess_t)
        if x == t:
            break
        offset = x - t
        guess_t -= offset/t_len

        if guess_t < 0:
            guess_t = 0
        if guess_t > 1.0:
            guess_t = 1.0

        # print("  ", offset)

    y = cubic_bezier(p0[1], p1[1], p2[1], p3[1], guess_t)
    # print(t, x, y)

    return y

def sign_no_zero(v):
    if 0 < v:
        return -1
    return 1

def calculate_tanget(p0, p1, p2, in_tanget=False):

    # Note:
    # This code was a lot of guess work
    # MC docs refer to spline as "Natural Spline" or "Cardinal Spline"
    # and AAF files export it with CubicInterpolator definition
    # MC has some wacky way of calculating the y coord of tangets

    # in_tanget <---- x ----> out_tanget

    x = p1[0]
    y = p1[1]

    px = p0[0]
    nx = p2[0]

    py = p0[1]
    ny = p2[1]

    if in_tanget:
        tan_x = 0.4 * (x - px)
    else:
        tan_x = 0.4 * (nx - x)

    slope = (ny - py) / (nx - px)
    prev_slope = (y - py) / (x - px)
    next_slope = (ny - y) / (nx - x)

    if sign_no_zero(prev_slope) != sign_no_zero(next_slope) or sign_no_zero(slope) != sign_no_zero(next_slope):
        tan_y = 0
    else:
        height = abs(ny - py)

        h1 = abs(ny - y)
        h2 = abs(y - py)

        # took me ages to figure this out
        scale = min(h1, h2) / height * 2.0
        tan_y = scale * slope * tan_x

    if in_tanget:
        tan_x *= -1.0
        tan_y *= -1.0

    return (tan_x, tan_y)

def cubic_interpolate(p0, p1, p2, p3, t):

    tan_x0, tan_y0 = calculate_tanget(p0, p1, p2, False)
    tan_x1, tan_y1 = calculate_tanget(p1, p2, p3, True)

    p0 = p1
    p3 = p2

    p1 = (p0[0] + tan_x0, p0[1] + tan_y0)
    p2 = (p3[0] + tan_x1, p3[1] + tan_y1)

    return cubic_bezier_interpolate(p0, p1, p2, p3, t)


def mc_trapezoidal_integrate(f, a, b, n=5):
    # this attempts to integrate a function the same way MC does.
    # for most correct results abs(a-b) == 0.5 and n = 5

    h = float(b - a) / n
    pv = f(a-h)
    result = 0
    for i in range(n):
        v =  f(a + (i * h))
        result += (v + pv) * h * 0.5
        pv = v
    return result

def integrate_iter(speed_map, start, end):
    pos = 0
    for i in range(start, end-1):
        t = float(i)
        pos += mc_trapezoidal_integrate(speed_map.value_at, t-0.5, t)
        yield t, pos
        t += 0.5
        pos += mc_trapezoidal_integrate(speed_map.value_at, t-0.5, t)
        yield t, pos

    t += 0.5
    pos += mc_trapezoidal_integrate(speed_map.value_at, t-0.5, t)
    yield t, pos

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

    for i, (t,v) in enumerate(integrate_iter(speed_map, inter_start, inter_end)):
        time.append(t)
        value.append(v)

        if t == center:
            offset_index = i

    center_offset = value[offset_index]

    # not really sure what this base fream offset is about
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
    @interpolationdef.setter
    def interpolation(self, value):
        self['Interpolation'].value = value

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

        elif self.interpolationdef.auid  == BezierInterpolator:
            t0 = float(p1.time)
            v0 = float(p1.value)

            t3 = float(p2.time)
            v3 = float(p2.value)

            tangets = p1.tangets[1]
            t1 = t0 + tangets[0]
            v1 = v0 + tangets[1]

            tangets = p2.tangets[0]
            t2 = t3 + tangets[0]
            v2 = v3 + tangets[1]

            return cubic_bezier_interpolate((t0, v0),
                                            (t1, v1),
                                            (t2, v2),
                                            (t3, v3), t)

        elif self.interpolationdef.auid  == CubicInterpolator:

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
        self['Value'].value =  AAFRational(value)

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
    def tangets(self):
        props = self.point_properties
        return [(float(props.get("PP_IN_TANGENT_POS_U", 0)),
                 float(props.get("PP_IN_TANGENT_VAL_U", 0))),
                (float(props.get("PP_OUT_TANGENT_POS_U", 0)),
                 float(props.get("PP_OUT_TANGENT_VAL_U", 0)))]
