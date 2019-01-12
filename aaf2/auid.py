import uuid
import struct
import traceback

class AUID(object):
    __slots__ = ('bytes_le')
    def __init__(self, hex=None, bytes_le=None, bytes_be=None, int=None):
        if bytes_le:
            self.bytes_le = bytearray(bytes_le)
        elif isinstance(hex, (uuid.UUID, AUID)):
            self.bytes_le = bytearray(hex.bytes_le)
        elif hex is not None:
            hex = hex.replace('urn:', '').replace('uuid:', '')
            hex = hex.strip('{}').replace('-', '')
            if len(hex) != 32:
                raise ValueError('badly formed hexadecimal UUID string')
            b = bytearray.fromhex(hex)
            self.bytes_le = bytearray(b[4-1::-1] + b[6-1:4-1:-1] + b[8-1:6-1:-1] + b[8:])
        elif bytes_be is not None:
            self.bytes_be = bytes_be
        elif int is not None:
            if int is 0:
                self.bytes_le = bytearray(16)
            else:
                self.bytes_le = bytearray(uuid.UUID(int=int).bytes_le)
        else:
            raise TypeError('one of the hex, bytes_le, bytes_be '
                            'or int arguments must be given')

    @property
    def bytes_be(self):
        return bytearray(self.bytes_le[4-1::-1]    + self.bytes_le[6-1:4-1:-1] +
                         self.bytes_le[8-1:6-1:-1] + self.bytes_le[8:])

    @bytes_be.setter
    def bytes_be(self, value):
        self.bytes_le = bytearray(value[4-1::-1]    + value[6-1:4-1:-1] +
                                  value[8-1:6-1:-1] + value[8:])

    @property
    def int(self):
        num = 0
        for i, byte in enumerate(self.bytes_be[::-1]):
            num += byte << (i * 8)
        return num

    @property
    def hex(self):
        return '%032x' % self.int

    @property
    def uuid(self):
        return uuid.UUID(bytes_le=bytes(self.bytes_le))

    @property
    def data1(self):
        value  = self.bytes_le[0]
        value += self.bytes_le[1] << 8
        value += self.bytes_le[2] << 16
        value += self.bytes_le[3] << 24
        return value

    @property
    def data2(self):
        value  = self.bytes_le[4]
        value += self.bytes_le[5] << 8
        return value

    @property
    def data3(self):
        value  = self.bytes_le[6]
        value += self.bytes_le[7] << 8
        return value

    @property
    def data4(self):
        return self.bytes_le[8:]

    def __hash__(self):
        return hash(bytes(self.bytes_le))

    def __eq__(self, other):
        if isinstance(other, (AUID, uuid.UUID)):
            return self.bytes_le == other.bytes_le
        return NotImplemented

    def __repr__(self):
        data4 = self.data4
        f = "%08x-%04x-%04x-%02x%02x-%02x%02x%02x%02x%02x%02x"
        return f % (self.data1, self.data2, self.data3,
                    data4[0], data4[1], data4[2], data4[3],
                    data4[4], data4[5], data4[6], data4[7])
