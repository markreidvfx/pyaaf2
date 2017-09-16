from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import uuid
import struct

MOBID_STRUCT = struct.Struct(''.join(( '<',
   '12B',  # UInt8Array12   SMPTELabel
   'B',    # UInt8          length
   'B',    # UInt8          instanceHigh
   'B',    # UInt8          instanceMid
   'B',    # UInt8          instanceLow
   'I',    # UInt32         Data1
   'H',    # UInt16         Data2
   'H',    # UInt16         Data3
   '8B',   # UInt8Array8    Data4
 )))

class MobID(object):
    def __init__(self, mobid=None, bytes_le=None):

        self.SMPTELabel = [0 for i in range(12)]
        self.length = 0
        self.instanceHigh = 0
        self.instanceMid = 0
        self.instanceLow = 0
        self.Data1 = 0
        self.Data2 = 0
        self.Data3 = 0
        self.Data4 = [0 for i in range(8)]

        if bytes_le:
            self.bytes_le = bytes_le

        if mobid:
            self.urn = mobid

    @staticmethod
    def new():
        m = MobID()
        m.SMPTELabel = [0x06, 0x0a, 0x2b, 0x34, 0x01, 0x01, 0x01, 0x05, 0x01, 0x01, 0x0f, 0x00]
        m.length = 0x13
        m.instanceHigh = 0x00
        m.instanceMid = 0x00
        m.instanceLow = 0x00
        m.material = uuid.uuid4()
        return m

    @property
    def material(self):
        return uuid.UUID(bytes_le=self.bytes_le[16:])

    @material.setter
    def material(self, value):
        self.Data1 = value.time_low
        self.Data2 = value.time_mid
        self.Data3 = value.time_hi_version
        self.Data4 = list(struct.unpack("8B", value.bytes[8:]))

    @property
    def bytes_le(self):
        return MOBID_STRUCT.pack(
        self.SMPTELabel[0],
        self.SMPTELabel[1],
        self.SMPTELabel[2],
        self.SMPTELabel[3],
        self.SMPTELabel[4],
        self.SMPTELabel[5],
        self.SMPTELabel[6],
        self.SMPTELabel[7],
        self.SMPTELabel[8],
        self.SMPTELabel[9],
        self.SMPTELabel[10],
        self.SMPTELabel[11],
        self.length,
        self.instanceHigh,
        self.instanceMid,
        self.instanceLow,
        self.Data1,
        self.Data2,
        self.Data3,
        self.Data4[0],
        self.Data4[1],
        self.Data4[2],
        self.Data4[3],
        self.Data4[4],
        self.Data4[5],
        self.Data4[6],
        self.Data4[7])

    @bytes_le.setter
    def bytes_le(self, data):

        (
        self.SMPTELabel[0],
        self.SMPTELabel[1],
        self.SMPTELabel[2],
        self.SMPTELabel[3],
        self.SMPTELabel[4],
        self.SMPTELabel[5],
        self.SMPTELabel[6],
        self.SMPTELabel[7],
        self.SMPTELabel[8],
        self.SMPTELabel[9],
        self.SMPTELabel[10],
        self.SMPTELabel[11],
        self.length,
        self.instanceHigh,
        self.instanceMid,
        self.instanceLow,
        self.Data1,
        self.Data2,
        self.Data3,
        self.Data4[0],
        self.Data4[1],
        self.Data4[2],
        self.Data4[3],
        self.Data4[4],
        self.Data4[5],
        self.Data4[6],
        self.Data4[7],
        ) = MOBID_STRUCT.unpack(data)

    def _from_dict(self, d):
        self.length = d.get("length", 0)
        self.instanceHigh = d.get("instanceHigh", 0)
        self.instanceMid = d.get("instanceMid", 0)
        self.instanceLow = d.get("instanceLow", 0)

        material = d.get("material", {'Data1':0, 'Data2':0, 'Data3':0})

        self.Data1 = material.get('Data1', 0)
        self.Data2 = material.get('Data2', 0)
        self.Data3 = material.get('Data3', 0)

        Data4 = material.get("Data4", [0 for i in xrange(8)])

        for i in xrange(8):
            if i >= len(Data4):
                break
            self.Data4[i] = Data4[i]

        SMPTELabel = d.get("SMPTELabel", [0 for i in xrange(12)])
        for i in xrange(12):
            if i >= len(SMPTELabel):
                break
            self.SMPTELabel[i] = SMPTELabel[i]

    def to_dict(self):

        material = {'Data1': self.Data1,
                    'Data2': self.Data2,
                    'Data3': self.Data3,
                    'Data4': [self.Data4[i] for i in xrange(8)]
                    }
        SMPTELabel = [self.SMPTELabel[i] for i in xrange(12)]

        return {'material':material,
                'length': self.length,
                'instanceHigh': self.instanceHigh,
                'instanceMid': self.instanceMid,
                'instanceLow': self.instanceLow,
                'SMPTELabel': SMPTELabel
                }
    @property
    def int(self):
        data = bytearray(self.bytes_le)
        num = 0
        for offset, byte in enumerate(data):
            num += byte << (offset * 8)
        return num

    def __int__(self):
        return self.int

    def __eq__(self, other):
        if isinstance(other, MobID):
            return self.int == other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)


    @property
    def urn(self):

        # handle case UMIDs where the material number is half swapped
        if self.SMPTELabel[11] == 0x00 and \
                 self.Data4[0] == 0x06 and \
                 self.Data4[1] == 0x0E and \
                 self.Data4[2] == 0x2B and \
                 self.Data4[3] == 0x34 and \
                 self.Data4[4] == 0x7F and \
                 self.Data4[5] == 0x7F:
            # print("case 1")
            f = "urn:smpte:umid:%02x%02x%02x%02x.%02x%02x%02x%02x.%02x%02x%02x%02x." + \
             "%02x"  + \
             "%02x%02x%02x." + \
             "%02x%02x%02x%02x.%02x%02x%02x%02x.%08x.%04x%04x"

            return f % (
                 self.SMPTELabel[0], self.SMPTELabel[1], self.SMPTELabel[2],  self.SMPTELabel[3],
                 self.SMPTELabel[4], self.SMPTELabel[5], self.SMPTELabel[6],  self.SMPTELabel[7],
                 self.SMPTELabel[8], self.SMPTELabel[9], self.SMPTELabel[10], self.SMPTELabel[11],
                 self.length,
                 self.instanceHigh, self.instanceMid, self.instanceLow,
                 self.Data4[0], self.Data4[1], self.Data4[2], self.Data4[3],
                 self.Data4[4], self.Data4[5], self.Data4[6], self.Data4[7],
                 self.Data1, self.Data2, self.Data3)
        else:
            # print("case 2")
            f = "urn:smpte:umid:%02x%02x%02x%02x.%02x%02x%02x%02x.%02x%02x%02x%02x." + \
             "%02x"  + \
             "%02x%02x%02x." + \
             "%08x.%04x%04x.%02x%02x%02x%02x.%02x%02x%02x%02x"

            return f % (
                 self.SMPTELabel[0], self.SMPTELabel[1], self.SMPTELabel[2],  self.SMPTELabel[3],
                 self.SMPTELabel[4], self.SMPTELabel[5], self.SMPTELabel[6],  self.SMPTELabel[7],
                 self.SMPTELabel[8], self.SMPTELabel[9], self.SMPTELabel[10], self.SMPTELabel[11],
                 self.length,
                 self.instanceHigh, self.instanceMid, self.instanceLow,
                 self.Data1, self.Data2, self.Data3,
                 self.Data4[0], self.Data4[1], self.Data4[2], self.Data4[3],
                 self.Data4[4], self.Data4[5], self.Data4[6], self.Data4[7])

    @urn.setter
    def urn(self, value):
        s = str(value).lower()
        for item in ("urn:smpte:umid:", ".", '-', '0x'):
            s = s.replace(item, '')
        assert len(s) == 64

        SMPTELabel = [0 for i in range(12)]
        start = 0
        for i in range(12):
            end = start + 2
            v = s[start:end]
            SMPTELabel[i] = int(v, 16)
            start = end
        self.SMPTELabel = SMPTELabel
        self.length = int(s[24:26], 16)
        self.instanceHigh = int(s[26:28], 16)
        self.instanceMid = int(s[28:30], 16)
        self.instanceLow = int(s[30:32], 16)

        start = 32
        data = [0 for i in range(6)]
        for i in range(6):
            end = start + 2
            v = s[start:end]
            data[i] = int(v, 16)
            start = end
        # print(s[32:start])
        if SMPTELabel[11] == 0x00 and \
                  data[0] == 0x06 and \
                  data[1] == 0x0E and \
                  data[2] == 0x2B and \
                  data[3] == 0x34 and \
                  data[4] == 0x7F and \
                  data[5] == 0x7F:

            start = 32
            data4 = [0 for i in range(8)]
            for i in range(8):
                end = start + 2
                v = s[start:end]
                data4[i] = int(v, 16)
                start = end

            self.Data4 = data4
            self.Data1 = int(s[48:56], 16)
            self.Data2 = int(s[56:60], 16)
            self.Data3 = int(s[60:64], 16)

        else:
            self.Data1 = int(s[32:40], 16)
            self.Data2 = int(s[40:44], 16)
            self.Data3 = int(s[44:48], 16)

            start = 48
            data4 = [0 for i in range(8)]
            for i in range(8):
                end = start + 2
                v = s[start:end]
                data4[i] = int(v, 16)
                start = end
            self.Data4 = data4

    def __repr__(self):
        return str(self.urn)

if __name__ == "__main__":

    t = "urn:smpte:umid:060a2b34.01010101.01010f00.13000000.060e2b34.7f7f2a80.4fa5c20f.4e301e50"
    m = MobID(t)
    print(t)
    print(m)
    assert str(m) == t
