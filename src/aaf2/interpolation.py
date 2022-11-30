from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import math
import sys

EPSILON = 1e-10 # sys.float_info.epsilon

def lerp(a, b, t):
    return a + (b - a) * t

def cubic_bezier(p0, p1, p2, p3, t):
    u = 1.0 - t
    w1 = u * u * u
    w2 = 3.0 * u * u * t
    w3 = 3.0 * u * t * t
    w4 = t * t * t
    return w1 * p0 + w2 * p1 + w3 * p2 + w4 * p3

def valid_root(v):
    # there can be floating point error
    return v >= -EPSILON and v <= 1.0 + EPSILON

def cube_root(x):
    if x < 0.0:
        x = abs(x)
        cube_root = x**(1/3)*(-1)
    else:
        cube_root = x**(1/3)
    return cube_root

# Cardano's algorithm
# https://pomax.github.io/bezierinfo/#extremities
def bezier_cubic_roots(pa, pb, pc, pd):
    a = 3.0 * pa - 6.0 * pb + 3.0 * pc
    b = -3.0 * pa + 3.0 * pb
    c = pa
    d = -pa + 3.0*pb - 3.0*pc + pd

    result = []
    if abs(d) < EPSILON:
        # this is not a cubic curve.
        if abs(a) < EPSILON:
            # this is not a quadratic curve either.
            if abs(b) < EPSILON:
                # there are no solutions.
                return []

            # linear solution
            root = -c / b
            if valid_root(root):
                result.append(root)
            return result

        # quadratic solution
        q = math.sqrt(b*b - 4*a*c)
        a2 = 2.0*a
        root = (q-b)/a2
        if valid_root(root):
            result.append(root)

        root = (-b-q)/a2
        if valid_root(root):
            result.append(root)

        return result

    # at this point, we know we need a cubic solution.
    a /= d
    b /= d
    c /= d

    p = (3*b - a*a)/3.0
    p3 = p/3.0
    q = (2.0*a*a*a - 9*a*b + 27.0*c)/27.0
    q2 = q/2.0
    discriminant = q2*q2 + p3*p3*p3

    if discriminant < 0.0:
        mp3  = -p / 3.0
        mp33 = mp3*mp3*mp3
        r    = math.sqrt( mp33 )
        t    = -q / (2.0*r)

        cosphi = max(-1.0, min(1.0, t))

        phi  = math.acos(cosphi)
        crtr = cube_root(r)
        t1   = 2.0*crtr

        root = t1 * math.cos(phi / 3.0) - a / 3.0
        if valid_root(root):
            result.append(root)

        root = t1 * math.cos((phi + 2.0 * math.pi)/3.0) - a/3.0
        if valid_root(root):
            result.append(root)

        root = t1 * math.cos((phi + 4.0 * math.pi)/3.0) - a/3.0
        if valid_root(root):
            result.append(root)

        return result

    # three real roots, but two of them are equal:
    if discriminant == 0.0:
        if q2 < 0.0:
            u1 = cube_root(-q2)
        else:
            u1 = -cube_root(q2)

        root = 2.0 * u1 - a / 3.0
        if valid_root(root):
            result.append(root)

        root = -u1 - a / 3.0
        if valid_root(root):
            result.append(root)

        return result

    # one real root, two complex roots
    sd = math.sqrt(discriminant)
    u1 = cube_root(sd - q2)
    v1 = cube_root(sd + q2)
    root = u1 - v1 - a / 3.0

    if valid_root(root):
        result.append(root)

    return result

def scale_handle(p0, p1, p2):
    # scale using similar triangles
    #         o <- p1
    #        /
    #       /
    #      /|<- result
    #     / |
    #    /  |
    #   /   |
    #  /    |
    # /p0---p2
    y = (p1[1] - p0[1]) * (p2[0] - p0[0]) / (p1[0] - p0[0])
    return [p2[0], p0[1] + y]

def bezier_interpolate(p0, p1, p2, p3, x):

    # degenerate cases 1
    # p0 is after p3
    if p0[0] >= p3[0]:
        return p[1]

    # degenerate cases 2
    # p1 after p3 or before p0
    if p1[0] > p3[0]:
        p1 = scale_handle(p0, p1, p3)
    elif p1[0] < p0[0]:
        p1 = [p0[0], p1[1]]

    # degenerate cases 3
    # p2 before p0 or after p3
    if p2[0] < p0[0]:
        p2 = scale_handle(p3, p2, p0)
    elif p2[0] > p3[0]:
        p2 = [p3[0], p2[1]]

    # offset points so x is the x axis
    pa = p0[0] - x
    pb = p1[0] - x
    pc = p2[0] - x
    pd = p3[0] - x

    # solve for x = 0
    roots = bezier_cubic_roots(pa, pb, pc, pd)
    if not roots:
        # fall back to old method or decrease EPSILON precision?
        assert False

    # use the root as t for y
    y = cubic_bezier(p0[1], p1[1], p2[1], p3[1], min(1.0, max(0, roots[0])))
    return y

def bezier_interpolate_old(p0, p1, p2, p3, t):

    t_len = p3[0] - p0[0]
    t_diff = t - p0[0]
    t_mix = t_diff/t_len

    guess_t = t_mix

    # approximate the correct t value,
    # maybe this is the newtonian method?
    # I kind of made it up, its slow but seems to work
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

    y = cubic_bezier(p0[1], p1[1], p2[1], p3[1], guess_t)
    return y

def sign_no_zero(v):
    if v >= 0:
        return 1
    return -1

def calculate_tangent(p0, p1, p2, in_tangent=False):

    # Note:
    # This code was a lot of guess work
    # MC docs refer to spline as "Natural Spline" or "Cardinal Spline"
    # and AAF files export it with CubicInterpolator definition
    # MC has some wacky way of calculating the y coord of tangents

    # in_tangent <---- x ----> out_tangent

    x = p1[0]
    y = p1[1]

    px = p0[0]
    nx = p2[0]

    py = p0[1]
    ny = p2[1]

    if in_tangent:
        tan_x = 0.4 * (x - px)
    else:
        tan_x = 0.4 * (nx - x)

    slope = (ny - py) / (nx - px)
    prev_slope = (y - py) / (x - px)
    next_slope = (ny - y) / (nx - x)

    if sign_no_zero(prev_slope) != sign_no_zero(next_slope) or sign_no_zero(slope) != sign_no_zero(next_slope) or ny == py:
        tan_y = 0
    else:
        height = abs(ny - py)

        h1 = abs(ny - y)
        h2 = abs(y - py)

        # took me ages to figure this out
        scale = min(h1, h2) / height * 2.0
        tan_y = scale * slope * tan_x

    if in_tangent:
        tan_x *= -1.0
        tan_y *= -1.0

    return (tan_x, tan_y)

def cubic_interpolate(p0, p1, p2, p3, t):
    tan_x0, tan_y0 = calculate_tangent(p0, p1, p2, False)
    tan_x1, tan_y1 = calculate_tangent(p1, p2, p3, True)

    p0 = p1
    p3 = p2

    p1 = (p0[0] + tan_x0, p0[1] + tan_y0)
    p2 = (p3[0] + tan_x1, p3[1] + tan_y1)

    return bezier_interpolate(p0, p1, p2, p3, t)

def mc_trapezoidal_integrate(value_at_func, a, b, n=5):
    # this attempts to integrate a function the same way MC does.
    # for most correct results abs(a-b) == 0.5 and n = 5

    h = float(b - a) / n
    pv = value_at_func(a-h)
    result = 0
    for i in range(n):
        v =  value_at_func(a + (i * h))
        result += (v + pv) * h * 0.5
        pv = v
    return result

def integrate_iter(value_at_func, start, end):
    # func is a value_at(time) function that takes a time arg
    pos = 0
    for i in range(start, end-1):
        t = float(i)
        pos += mc_trapezoidal_integrate(value_at_func, t-0.5, t)
        yield t, pos
        t += 0.5
        pos += mc_trapezoidal_integrate(value_at_func, t-0.5, t)
        yield t, pos

    t += 0.5
    pos += mc_trapezoidal_integrate(value_at_func, t-0.5, t)
    yield t, pos