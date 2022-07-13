"""

Excerpt from SMPTE ST 330 (Focus on Basic UMID)::

    5 General Specification

    A unique material identifier (UMID) provides for the globally unique identification of any audiovisual material.
    This standard defines a dual approach through the specification of a basic UMID and an extended UMID.
    The basic UMID provides a globally unique identification for audiovisual material that comprises an integer
    number of one or more contiguous material units. The basic UMID has no embedded mechanism to
    distinguish between individual material units within a single instance of audiovisual material. The data in the
    basic UMID can be created through automatic generation.

    The extended UMID comprises the basic UMID followed immediately by a source pack that provides a
    signature for material units. The source pack comprises a fixed length metadata pack of 32 bytes that
    provides sufficient metadata by which source ?when, where and who (or what)? information can be identified
    regardless of current ownership or status. The extended UMID also provides a mechanism to distinguish
    between individual material units within a single instance of audiovisual material.

    The basic UMID is 32 bytes long and the extended UMID is 64 bytes long.
    Both UMID types use the key-length-value construct defined by SMPTE ST 336. The key is a 16-byte
    universal label truncated to 12 bytes.
    In the case of the basic UMID, the length field has a value of 13h and the value is formed by the combination
    of a material number and an instance number.
    In the case of the extended UMID, the length field has a value of 33h and the value is formed by the
    combination of the material and the instance numbers followed by the source pack.
    All components of the UMID have a defined byte order for consistent application in storage and streaming
    environments.

    The components of the basic UMID are:
    1. A 12-byte universal label,
    2. A 1-byte length value,
    3. A 3-byte instance number, and
    4. A 16-byte material number.

    The combination of the instance and material numbers can be treated as a dumb number.
    Note: The material number does not indicate the status of the material (such as copy number) or its representation
    (such as the compression kind). The material number can be identical in copies and in different representations of
    the material. The purpose of the instance number is to separately identify different representations or instances of
    audiovisual material. Thus, for example, a high-resolution picture and a thumbnail can both have the same
    material number because they both represent the same picture but, because they are different instances, they will
    have different instance numbers for the different representations. Guidance for the consistent application of new
    material numbers and instance numbers is given in SMPTE RP 205.


    UMID universal label (SMPTELabel)

    Byte No.   Description            Value (hex)                 Meaning
    ----------------------------------------------------------------------------------------
    1          Object identifier      06h                         Universal label start
    2          Label size             0Ah                         12-byte Universal label
    3          Designation: ISO       2Bh                         ISO registered
    4          Designation: SMPTE     34h                         SMPTE registered
    5          Registry category      01h                         Dictionaries
    6          Specific category      01h                         Metadata dictionaries
    7          Structure              01h                         Dictionary standard (SMPTE ST 335)
    8          Version number         05h                         Version of the metadata dictionary (defined in SMPTE RP 210)
    9          Class                  01h                         Identifiers and locators
    10         Subclass               01h                         Globally unique identifiers
    11         Material type          XXh                         See Section 6.1.2.1
    12         Number creation method YYh                         See Section 6.1.2.2

    6.1.2.1 - Material type identification

    Byte 11 of the UL shall define the material type being identified using one of the values defined in Table 2.
    The use of material types '01h', '02h', '03h' and '04h' shall be deprecated for use in implementations using
    this revised standard. These values are preserved only for compatibility with systems implemented using
    SMPTE ST 330:2000#

    Table 2

    Byte value    Meaning                                                            Examples and notes
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    01h           picture material                                                   Deprecated
    02h           audio material                                                     Deprecated
    03h           data material                                                      Deprecated
    04h           other material                                                     Deprecated (originally not only picture, audio, or data material, but also a combination of material types)
    05h           single picture component                                           e.g. Y component
    06h           Two or more picture components in a single container               e.g. interleaved Y, Cb and Cr components
    08h           single audio component                                             e.g mono audio
    09h           two or more audio components in a single container                 e.g. AES3 audio pair
    0Bh           single auxiliary (or data) component                               e.g. sub-titles only
    0Ch           two or more auxiliary (or data) components in a single container   e.g. multiple sub-titles streams in different languages
    0Dh           mixed group of components in a single container                    e.g. video & stereo audio pair
    0Fh           material type is not identified

    6.1.2.2 Number creation method identification

    Byte 12 of the UL shall define the method by which the material and instance numbers are created. This byte
    is divided into top and bottom nibbles for the purpose of this definition.
    The top nibble shall occupy the 4 most significant bits (MSBs) of the byte and the value shall be used to
    define the method of material number creation. The values used by this nibble shall be limited to the range 0
    to 7h so that byte 12 conforms to the ASN.1 BER short form coding rules used by SMPTE ST 298.
    The methods of material number generation shall be as defined in table 3 and the specification of the each
    method shall be as defined in Annex A.
    Note: New material number generation methods can be added by amendment or revision of this document. Each
    addition will provide the proposed value (within the range of values currently identified as "Reserved but not
    defined") for inclusion in Table 3 together with the supporting definition to be added to Annex A.

    Table 3 - Identification of material number generation method::

        Value (hex)   Method
        -------------------------------------------------------------
        0             No defined method
        1             SMPTE method
        2             UUID/UL method
        3             Masked method
        4             IEEE 1394 network method
        5~7           Reserved but not defined


Notes from Pixar 10/30/17

Final note of discussion with Avid engineers how the top nibble in the 12th byte in the SMPTELabel should be set.
(In the past we always had it set to 00, i.e. "no defined method", we had some confusion about how to set it when using a uuid for the material)

Avid Engineer:

"The specification of number creation identification is very clear about using the 4 MSBs for the material
number so I am pretty sure that the numbers in the sub-titles of Annex A (e.g. 02h) should not be interpreted literally as values of byte 12.
20h is the correct value of the byte 12 for UL/UUID method/No defined method.

By the way, I don't see anything wrong with setting byte 12 to 00h (No defined method / No defined method)"

We at Pixar decided to set the byte to 20h, since it (even if already very minimal) completely eliminates the possibility to collide with any
MOB ID created by our old MOB ID generation algorithm.
"""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import uuid
import struct
from .utils import (int_from_bytes, bytes_from_int, unpack_u16le_from, unpack_u32le_from)
from . import auid

MOBID_STRUCT = struct.Struct(str(''.join(( '<',
   '12B',  # UInt8Array12   SMPTELabel      0
   'B',    # UInt8          length         12
   'B',    # UInt8          instanceHigh   13
   'B',    # UInt8          instanceMid    14
   'B',    # UInt8          instanceLow    15
   'I',    # UInt32         Data1          16
   'H',    # UInt16         Data2          20
   'H',    # UInt16         Data3          22
   '8B',   # UInt8Array8    Data4          24
 ))))

def UniqueMobID():
    m = MobID()              # Description              Meaning
    m.SMPTELabel = [0x06,    # Object identifier        Universal label start
                    0x0a,    # Label size               12-byte Universal label
                    0x2b,    # Designation: ISO         ISO registered
                    0x34,    # Designation: SMPTE       SMPTE registered
                    0x01,    # Registry category        Dictionaries
                    0x01,    # Specific category        Metadata dictionaries
                    0x01,    # Structure                Dictionary standard (SMPTE ST 335)
                    0x05,    # Version number           Version of the metadata dictionary (defined in SMPTE RP 210)
                    0x01,    # Class                    Identifiers and locators
                    0x01,    # Subclass                 Globally unique identifiers
                    0x0f,    # Material type            See Section 6.1.2.1
                    0x20     # Number creation method   See Section 6.1.2.2     # Using UUID/UL method, Note 10/30/17 - matching pixar recommendation
                   ]
    m.length = 0x13          # Length, 13h = Basic UMID, 33h = Extended UMID
    m.instanceHigh = 0x00
    m.instanceMid = 0x00
    m.instanceLow = 0x00
    m.material = uuid.uuid4() # 16 byte material slot, filled with uuid according to RFC4122
    return m

class MobID(object):
    __slots__ = ('bytes_le')
    def __init__(self, mobid=None, bytes_le=None, int=None):

        if bytes_le:
            self.bytes_le = bytearray(bytes_le)
        else:
            self.bytes_le = bytearray(32)

            if mobid is not None:
                self.urn = mobid

            if int is not None:
                self.int = int

    @staticmethod
    def new():
        """
        Static method for generating unique MobIDs. Uses uuid.uuid4() for generation.
        """
        return UniqueMobID()

    @property
    def material(self):
        """
        MobID material representation as a UUID
        """
        return auid.AUID(bytes_le=self.bytes_le[16:])

    @material.setter
    def material(self, value):
        self.bytes_le[16:] = value.bytes_le

    @property
    def SMPTELabel(self):
        return self.bytes_le[0:12]

    @SMPTELabel.setter
    def SMPTELabel(self, value):
        struct.pack_into(str('12B'), self.bytes_le, 0, *value)

    @property
    def length(self):
        return self.bytes_le[12]

    @length.setter
    def length(self, value):
        self.bytes_le[12] = value

    @property
    def instanceHigh(self):
        return self.bytes_le[13]

    @instanceHigh.setter
    def instanceHigh(self, value):
        self.bytes_le[13] = value

    @property
    def instanceMid(self):
        return self.bytes_le[14]

    @instanceMid.setter
    def instanceMid(self, value):
        self.bytes_le[14] = value

    @property
    def instanceLow(self):
        return self.bytes_le[15]

    @instanceLow.setter
    def instanceLow(self, value):
        self.bytes_le[15] = value

    @property
    def Data1(self):
        return unpack_u32le_from(self.bytes_le, 16)

    @Data1.setter
    def Data1(self, value):
        struct.pack_into(str('<I'), self.bytes_le, 16, value)

    @property
    def Data2(self):
        return unpack_u16le_from(self.bytes_le, 20)

    @Data2.setter
    def Data2(self, value):
        struct.pack_into(str('<H'), self.bytes_le, 20, value)

    @property
    def Data3(self):
        return unpack_u16le_from(self.bytes_le, 22)

    @Data3.setter
    def Data3(self, value):
        struct.pack_into(str('<H'), self.bytes_le, 22, value)

    @property
    def Data4(self):
        return self.bytes_le[24:32]

    @Data4.setter
    def Data4(self, value):
        struct.pack_into(str('8B'), self.bytes_le, 24, *value)

    def from_dict(self, d):
        """
        Set MobID from a dict
        """
        self.length = d.get("length", 0)
        self.instanceHigh = d.get("instanceHigh", 0)
        self.instanceMid = d.get("instanceMid", 0)
        self.instanceLow = d.get("instanceLow", 0)

        material = d.get("material", {'Data1':0, 'Data2':0, 'Data3':0, 'Data4': [0 for i in range(8)]})

        self.Data1 = material.get('Data1', 0)
        self.Data2 = material.get('Data2', 0)
        self.Data3 = material.get('Data3', 0)

        self.Data4 = material.get("Data4", [0 for i in range(8)])
        self.SMPTELabel = d.get("SMPTELabel", [0 for i in range(12)])

    def to_dict(self):
        """
        MobID representation as dict
        """

        material = {'Data1': self.Data1,
                    'Data2': self.Data2,
                    'Data3': self.Data3,
                    'Data4': list(self.Data4)
                    }

        return {'material':material,
                'length': self.length,
                'instanceHigh': self.instanceHigh,
                'instanceMid': self.instanceMid,
                'instanceLow': self.instanceLow,
                'SMPTELabel': list(self.SMPTELabel)
                }
    @property
    def int(self):
        """
        MobID representation as a int
        """
        return int_from_bytes(self.bytes_le, byte_order='big')

    @int.setter
    def int(self, value):
        # NOTE: interpreted as big endian
        self.bytes_le = bytearray(bytes_from_int(value, 32, byte_order='big'))

    def __int__(self):
        return self.int

    def __eq__(self, other):
        if isinstance(other, MobID):
            return self.bytes_le == other.bytes_le
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, MobID):
            return self.int < other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, MobID):
            return self.int <= other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, MobID):
            return self.int > other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, MobID):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(bytes(self.bytes_le))

    @property
    def urn(self):
        """
        MobID Uniform Resource Name representation.
        https://en.wikipedia.org/wiki/Uniform_Resource_Name
        """

        SMPTELabel = self.SMPTELabel
        Data4 = self.Data4

        # handle case UMIDs where the material number is half swapped
        if (SMPTELabel[11] == 0x00 and
            Data4[0] == 0x06 and Data4[1] == 0x0E and
            Data4[2] == 0x2B and Data4[3] == 0x34 and
            Data4[4] == 0x7F and Data4[5] == 0x7F):

            # print("case 1")
            f = "urn:smpte:umid:%02x%02x%02x%02x.%02x%02x%02x%02x.%02x%02x%02x%02x." + \
             "%02x"  + \
             "%02x%02x%02x." + \
             "%02x%02x%02x%02x.%02x%02x%02x%02x.%08x.%04x%04x"

            return f % (
                 SMPTELabel[0], SMPTELabel[1], SMPTELabel[2],  SMPTELabel[3],
                 SMPTELabel[4], SMPTELabel[5], SMPTELabel[6],  SMPTELabel[7],
                 SMPTELabel[8], SMPTELabel[9], SMPTELabel[10], SMPTELabel[11],
                 self.length,
                 self.instanceHigh, self.instanceMid, self.instanceLow,
                 Data4[0], Data4[1], Data4[2], Data4[3],
                 Data4[4], Data4[5], Data4[6], Data4[7],
                 self.Data1, self.Data2, self.Data3)
        else:
            # print("case 2")
            f = "urn:smpte:umid:%02x%02x%02x%02x.%02x%02x%02x%02x.%02x%02x%02x%02x." + \
             "%02x"  + \
             "%02x%02x%02x." + \
             "%08x.%04x%04x.%02x%02x%02x%02x.%02x%02x%02x%02x"

            return f % (
                 SMPTELabel[0], SMPTELabel[1], SMPTELabel[2],  SMPTELabel[3],
                 SMPTELabel[4], SMPTELabel[5], SMPTELabel[6],  SMPTELabel[7],
                 SMPTELabel[8], SMPTELabel[9], SMPTELabel[10], SMPTELabel[11],
                 self.length,
                 self.instanceHigh, self.instanceMid, self.instanceLow,
                 self.Data1, self.Data2, self.Data3,
                 Data4[0], Data4[1], Data4[2], Data4[3],
                 Data4[4], Data4[5], Data4[6], Data4[7])

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
        if (SMPTELabel[11] == 0x00 and
                   data[0] == 0x06 and data[1] == 0x0E and
                   data[2] == 0x2B and data[3] == 0x34 and
                   data[4] == 0x7F and data[5] == 0x7F):

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
