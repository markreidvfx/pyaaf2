from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import sys
import logging
from fractions import Fraction, _RATIONAL_FORMAT
from decimal import Decimal
import numbers
Rational = numbers.Rational

if sys.version_info.major >= 3:
    unicode = str

class AAFRational(Fraction):
    """
    Subclass of fractions.Fraction from the standard library. Behaves exactly the same, except
    doesn't round to the Greatest Common Divisor at the end.
    """

    def __new__(cls, numerator=0, denominator=None):

        self = super(AAFRational, cls).__new__(cls)

        if denominator is None:
            if isinstance(numerator, Rational):
                self._numerator = numerator.numerator
                self._denominator = numerator.denominator
                return self

            elif isinstance(numerator, float):
                # Exact conversion from float
                value = Fraction.from_float(numerator)

                # make sure fraction can fit in a int32
                value = value.limit_denominator(0x7FFFFFFF)
                if value._numerator > 0x7FFFFFFF or value._numerator < -0x7FFFFFFF:
                    value._denominator = int(value._denominator * (0x7FFFFFFF / float(value._numerator)))
                    value._numerator = 0x7FFFFFFF

                self._numerator = value._numerator
                self._denominator = value._denominator
                return self

            elif isinstance(numerator, Decimal):
                value = Fraction.from_decimal(numerator)
                self._numerator = value._numerator
                self._denominator = value._denominator
                return self

            elif isinstance(numerator, (str, unicode)):
                # Handle construction from strings.
                m = _RATIONAL_FORMAT.match(numerator)
                if m is None:
                    raise ValueError('Invalid literal for Fraction: %r' %
                                     numerator)
                numerator = int(m.group('num') or '0')
                denom = m.group('denom')
                if denom:
                    denominator = int(denom)
                else:
                    denominator = 1
                    decimal = m.group('decimal')
                    if decimal:
                        scale = 10**len(decimal)
                        numerator = numerator * scale + int(decimal)
                        denominator *= scale
                    exp = m.group('exp')
                    if exp:
                        exp = int(exp)
                        if exp >= 0:
                            numerator *= 10**exp
                        else:
                            denominator *= 10**-exp
                if m.group('sign') == '-':
                    numerator = -numerator

            else:
                raise TypeError("argument should be a string " +
                                "or a Rational instance")

        elif (isinstance(numerator, Rational) and
            isinstance(denominator, Rational)):
            numerator, denominator = (
                numerator.numerator * denominator.denominator,
                denominator.numerator * numerator.denominator
                )
        else:
            raise TypeError("both arguments should be " +
                            "Rational instances")

        if denominator == 0:
            if numerator == 0:
                # AAF seemingly can have valid 0/0 property values,
                # which we default to 0/1, which is mathematically not
                # correct but works around this weird AAF behaviour (observed in
                # AAF files exported from Storyboard Pro)
                logging.warning("Fraction(0,0) not mathematically plausible, "
                                "use Fraction(0,1) instead.")
                self._numerator = 0
                self._denominator = 1
                return self
            raise ZeroDivisionError('Fraction(%s, 0)' % numerator)
        # don't find the gcd
        #g = gcd(numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self
