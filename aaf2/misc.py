from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
from datetime import datetime
import io

from . import core
from . utils import register_class

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
    class_id = UUID("0d010101-0101-3f00-060e-2b3402060101")
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
        name = self.name
        if name:
            s += ' %s' % name

        s += " = " + str(self.value)

        return '<%s at 0x%x>' % (s, id(self))

class Parameter(core.AAFObject):
    class_id = UUID("0d010101-0101-3c00-060e-2b3402060101")
    __slots__ = ()

    @property
    def uuid(self):
        return self['Definition'].value
    @uuid.setter
    def uuid(self, value):
        self['Definition'].value = value

    @property
    def parameterdef(self):
        return self.root.dictionary.lookup_parameterdef(self['Definition'].value)

    @parameterdef.setter
    def parameterdef(self, value):
        self['Definition'].value = value.uuid

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
    class_id = UUID("0d010101-0101-3d00-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, parameterdef=None, value=None):
        super(ConstantValue, self).__init__()

        if parameterdef is not None:
            self.parameterdef = parameterdef

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

def cubic_catmullrom(p0, p1, p2, p3, t):

    tt = t * t
    ttt = tt * t

    q0 = -ttt + (2.0 * tt) - t
    q1 = (3.0 * ttt) - (5.0 * tt) + 2.0
    q2 = (-3.0 * ttt) + (4.0 * tt) + t
    q3 = ttt - tt

    value = (p0 * q0) + (p1 * q1) + (p2 * q2) + (p3 * q3)
    value *= 0.5
    return value

def cubic_interp(p0, p1, m0, m1, t,):
    t = float(t)
    tt = t * t
    ttt = tt * t

    q0 = (2.0 * ttt) - (3.0 * tt) + 1
    q1 = ttt - (2.0 * tt) + t
    q2 = (-2.0 * ttt) + (3.0 * tt)
    q3 = ttt - tt

    value = (q0 * p0) + (q1 * m0) + (q2 * p1) + (q3 * m1)
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

def cubic_catmullrom_interpolate(p0, p1, p2, p3, t):
    t_len = p2[0] - p1[0]
    t_diff = t - p1[0]
    t_mix = t_diff/t_len

    guess_t = t_mix

    for i in range(20):
        x = cubic_catmullrom(p0[0], p1[0], p2[0], p3[0], guess_t)
        if x == t:
            break
        offset = x - t
        guess_t -= offset/t_len
        # print("  ", offset)
    # print(p0, p1, p2, p3, t_mix)

    y = cubic_catmullrom(p0[1], p1[1], p2[1], p3[1], guess_t)
    # print(t, x, y)
    return y

def cubic_interpolate(p0, p1, p2, p3, t):
    # Note:
    # This code is a lot of guess work
    # not sure what Avid MC actually does
    # MC docs refer to spline as "Natural Spline" or "Cardinal Spline"
    # and AAF files export it with CubicInterpolator definition
    # This is a hacked Cardinal spline that "looks" pretty close...

    # Finite difference
    # https://en.wikipedia.org/wiki/Cubic_Hermite_spline#Finite_difference

    # m0x = (p2[0] - p1[0]) + (p1[0] - p0[0])
    # m0y = (p2[1] - p1[1]) + (p1[1] - p0[1])
    #
    # m1x = (p3[0] - p2[0]) + (p2[0] - p1[0])
    # m1y = (p3[1] - p2[1]) + (p2[1] - p1[1])

    # Cardinal spline
    # https://en.wikipedia.org/wiki/Cubic_Hermite_spline#Cardinal_spline

    # m0x = (p2[0] - p0[0])
    # m0y = (p2[1] - p0[1])
    #
    # m1x = (p3[0] - p2[0])
    # m1y = (p3[1] - p2[1])

    # Note: the tangets are both really the same??
    m0x = (p3[0] - p0[0])
    m0y = (p3[1] - p0[1])

    m1x = (p3[0] - p0[0])
    m1y = (p3[1] - p0[1])

    # tension control
    c = 0.75

    flatten = 0
    # MC appears to flatten tangets if point is
    # higher/lower the its neighbor points
    if p1[1] >= p0[1] and p1[1] >= p2[1]:
        m0y *= flatten

    if p1[1] <= p0[1] and p1[1] <= p2[1]:
        m0y *= flatten

    if p2[1] >= p3[1] and p2[1] >= p1[1]:
        m1y *= flatten

    if p2[1] <= p3[1] and p2[1] <= p1[1]:
        m1y *= flatten

    m0x *= c * 0.5
    m0y *= c * 0.5

    m1x *= c * 0.5
    m1y *= c * 0.5

    t_len = p2[0] - p1[0]
    t_diff = t - p1[0]
    t_mix = t_diff/t_len

    guess_t = t_mix

    for i in range(20):
        x =  cubic_interp(p1[0], p2[0], m0x, m1x, guess_t)
        if x == t:
            break
        offset = x - t
        guess_t -= offset/t_len

        if guess_t < 0:
            guess_t = 0
        if guess_t > 1.0:
            guess_t = 1.0

    c = c

    y = cubic_interp(p1[1], p2[1], m0y, m1y, guess_t)

    # print(t, x, y, i, t_mix, guess_t)
    return y


@register_class
class VaryingValue(Parameter):
    class_id = UUID("0d010101-0101-3e00-060e-2b3402060101")
    __slots__ = ()

    @property
    def interpolation(self):
        return self['Interpolation'].value

    def value_at(self, t):
        t = float(t)

        bounds = self.bounds(t)
        if not bounds:
            raise ValueError("No PointList property")

        if len(bounds) == 1:
            return float(bounds[0].value)

        #ConstantInterp
        if self.interpolation.uuid == UUID("5b6c85a5-0ede-11d3-80a9-006008143e6f"):
            return float(bounds[0].value)

        t_len = float(bounds[1].time) - float(bounds[0].time)
        t_diff = t - float(bounds[0].time)
        t_mix = t_diff/t_len

        # LinearInterp
        if self.interpolation.uuid == UUID("5b6c85a4-0ede-11d3-80a9-006008143e6f"):
            v0 = float(bounds[0].value)
            v1 = float(bounds[1].value)
            return lerp(v0, v1, t_mix)

        # BezierInterpolator
        elif self.interpolation.uuid  == UUID("df394eda-6ac6-4566-8dbe-f28b0bdd781a"):
            t0 = float(bounds[0].time)
            v0 = float(bounds[0].value)

            t3 = float(bounds[1].time)
            v3 = float(bounds[1].value)

            tangets = bounds[0].tangets[1]
            t1 = t0 + tangets[0]
            v1 = v0 + tangets[1]

            tangets = bounds[1].tangets[0]
            t2 = t3 + tangets[0]
            v2 = v3 + tangets[1]

            return cubic_bezier_interpolate((t0, v0),
                                            (t1, v1),
                                            (t2, v2),
                                            (t3, v3), t)

        # CubicInterpolator
        elif self.interpolation.uuid  == UUID("a04a5439-8a0e-4cb7-975f-a5b255866883"):

            t1 = float(bounds[0].time)
            v1 = float(bounds[0].value)

            t2 = float(bounds[1].time)
            v2 = float(bounds[1].value)

            start = self.bounds(t1 - .0001)
            end = self.bounds(t2 + .0001)

            # print('s', t, bounds[0].time, [float(item.time) for item in start])
            # print('e', t, bounds[1].time, [float(item.time) for item in end])

            if len(start) == 1:
                t0 = t1 - ((t2 - t1) * 0.5)
                v0 = v1
            else:
                t0 = float(start[0].time)
                v0 = float(start[0].value)

            if len(end) == 1:
                t3 = t2 + ((t2 - t1) * 0.5)
                v3 = v2
            else:
                t3 = float(end[1].time)
                v3 = float(end[1].value)

            # return lerp(v1, v2, t_mix)
            return cubic_interpolate((t0, v0),
                                     (t1, v1),
                                     (t2, v2),
                                     (t3, v3), t)


        else:

            raise NotImplementedError("Interpolation not implemented for %s %s" %
                           (self.interpolation.name, str(self.interpolation.uuid)))


    def bounds(self, t):
        t = float(t)
        min_point = None
        max_point = None

        for point in self['PointList']:

            if point.time > t:
                max_point = point
                break

            min_point = point

        if min_point is None:
            return [max_point]

        if max_point is None:
            return [min_point]

        return [min_point, max_point]

@register_class
class ControlPoint(core.AAFObject):
    class_id = UUID("0d010101-0101-1900-060e-2b3402060101")
    __slots__ = ()

    @property
    def time(self):
        return float(self['Time'].value)

    @property
    def value(self):
        return float(self['Value'].value)

    @property
    def tangets(self):
        props = {}
        if 'ControlPointPointProperties' in self:
            for p in self['ControlPointPointProperties'].value:
                props[p.name] = p.value

        return [(float(props.get("PP_IN_TANGENT_POS_U", 0)),
                 float(props.get("PP_IN_TANGENT_VAL_U", 0))),
                (float(props.get("PP_OUT_TANGENT_POS_U", 0)),
                 float(props.get("PP_OUT_TANGENT_VAL_U", 0)))]
