ints = {
"UInt8"  : ( "01010100-0000-0000-060e-2b3401040101", 1, False),
"UInt16" : ( "01010200-0000-0000-060e-2b3401040101", 2, False),
"UInt32" : ( "01010300-0000-0000-060e-2b3401040101", 4, False),
"UInt64" : ( "01010400-0000-0000-060e-2b3401040101", 8, False),
"Int8"   : ( "01010500-0000-0000-060e-2b3401040101", 1, True),
"Int16"  : ( "01010600-0000-0000-060e-2b3401040101", 2, True),
"Int32"  : ( "01010700-0000-0000-060e-2b3401040101", 4, True),
"Int64"  : ( "01010800-0000-0000-060e-2b3401040101", 8, True),
}

enums = {
"Boolean" : ( "01040100-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "False",
    1  : "True",
    }
),
"ProductReleaseType" : ( "02010101-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "VersionUnknown",
    1  : "VersionReleased",
    2  : "VersionDebug",
    3  : "VersionPatched",
    4  : "VersionBeta",
    5  : "VersionPrivateBuild",
    }
),
"TapeFormatType" : ( "02010102-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "TapeFormatNull",
    1  : "BetacamFormat",
    2  : "BetacamSPFormat",
    3  : "VHSFormat",
    4  : "SVHSFormat",
    5  : "8mmFormat",
    6  : "Hi8Format",
    }
),
"VideoSignalType" : ( "02010103-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "VideoSignalNull",
    1  : "NTSCSignal",
    2  : "PALSignal",
    }
),
"TapeCaseType" : ( "02010104-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "TapeCaseNull",
    1  : "ThreeFourthInchVideoTape",
    2  : "VHSVideoTape",
    3  : "8mmVideoTape",
    4  : "BetacamVideoTape",
    5  : "CompactCassette",
    6  : "DATCartridge",
    7  : "NagraAudioTape",
    }
),
"ColorSitingType" : ( "02010105-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "CoSiting",
    1  : "Averaging",
    2  : "ThreeTap",
    3  : "Quincunx",
    4  : "Rec601",
    255: "UnknownSiting",
    }
),
"EditHintType" : ( "02010106-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "NoEditHint",
    1  : "Proportional",
    2  : "RelativeLeft",
    3  : "RelativeRight",
    4  : "RelativeFixed",
    }
),
"FadeType" : ( "02010107-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "FadeNone",
    1  : "FadeLinearAmp",
    2  : "FadeLinearPower",
    }
),
"LayoutType" : ( "02010108-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "FullFrame",
    1  : "SeparateFields",
    2  : "OneField",
    3  : "MixedFields",
    4  : "SegmentedFrame",
    }
),
"TCSource" : ( "02010109-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "TimecodeLTC",
    1  : "TimecodeVITC",
    }
),
"PulldownDirectionType" : ( "0201010a-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "TapeToFilmSpeed",
    1  : "FilmToTapeSpeed",
    }
),
"PulldownKindType" : ( "0201010b-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "TwoThreePD",
    1  : "PALPD",
    2  : "OneToOneNTSC",
    3  : "OneToOnePAL",
    4  : "VideoTapNTSC",
    5  : "OneToOneHDSixty",
    6  : "TwentyFourToSixtyPD",
    7  : "TwoToOnePD",
    }
),
"EdgeType" : ( "0201010c-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "EtNull",
    1  : "EtKeycode",
    2  : "EtEdgenum4",
    3  : "EtEdgenum5",
    8  : "EtHeaderSize",
    }
),
"FilmType" : ( "0201010d-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "FtNull",
    1  : "Ft35MM",
    2  : "Ft16MM",
    3  : "Ft8MM",
    4  : "Ft65MM",
    }
),
"RGBAComponentKind" : ( "0201010e-0000-0000-060e-2b3401040101", "UInt8", {
    0x30: "CompNone",
    0x41: "CompAlpha",
    0x42: "CompBlue",
    0x46: "CompFill",
    0x47: "CompGreen",
    0x50: "CompPalette",
    0x52: "CompRed",
    0x00: "CompNull",
    }
),
"ReferenceType" : ( "0201010f-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "RefLimitMinimum",
    1  : "RefLimitMaximum",
    2  : "RefMinimum",
    3  : "RefMaximum",
    4  : "RefEnumvalue",
    }
),
"AlphaTransparencyType" : ( "02010120-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "MinValueTransparent",
    1  : "MaxValueTransparent",
    }
),
"FieldNumber" : ( "02010121-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "UnspecifiedField",
    1  : "FieldOne",
    2  : "FieldTwo",
    }
),
"ElectroSpatialFormulation" : ( "02010122-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "ElectroSpatialFormulation_Default",
    1  : "ElectroSpatialFormulation_TwoChannelMode",
    2  : "ElectroSpatialFormulation_SingleChannelMode",
    3  : "ElectroSpatialFormulation_PrimarySecondaryMode",
    4  : "ElectroSpatialFormulation_StereophonicMode",
    7  : "ElectroSpatialFormulation_SingleChannelDoubleSamplingFrequencyMode",
    8  : "ElectroSpatialFormulation_StereoLeftChannelDoubleSamplingFrequencyMode",
    9  : "ElectroSpatialFormulation_StereoRightChannelDoubleSamplingFrequencyMode",
    15 : "ElectroSpatialFormulation_MultiChannelMode",
    }
),
"EmphasisType" : ( "02010123-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "Emphasis_Unknown",
    1  : "Emphasis_Reserved0",
    2  : "Emphasis_Reserved1",
    3  : "Emphasis_Reserved2",
    4  : "Emphasis_None",
    5  : "Emphasis_Reserved3",
    6  : "Emphasis_15and50",
    7  : "Emphasis_ITU",
    }
),
"AuxBitsModeType" : ( "02010124-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "AuxBitsMode_NotDefined",
    1  : "AuxBitsMode_MainAudioSampleData",
    2  : "AuxBitsMode_SingleCoordinationSignal",
    3  : "AuxBitsMode_UserDefined",
    4  : "AuxBitsMode_Reserved0",
    5  : "AuxBitsMode_Reserved1",
    6  : "AuxBitsMode_Reserved2",
    7  : "AuxBitsMode_Reserved3",
    }
),
"ChannelStatusModeType" : ( "02010125-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "ChannelStatusMode_None",
    1  : "ChannelStatusMode_Minimum",
    2  : "ChannelStatusMode_Standard",
    3  : "ChannelStatusMode_Fixed",
    4  : "ChannelStatusMode_Stream",
    5  : "ChannelStatusMode_Essence",
    }
),
"UserDataModeType" : ( "02010126-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "UserDataMode_NotDefined",
    1  : "UserDataMode_192BitBlockStructure",
    2  : "UserDataMode_AES18",
    3  : "UserDataMode_UserDefined",
    4  : "UserDataMode_IEC",
    5  : "UserDataMode_Metadata",
    6  : "UserDataMode_Reserved0",
    7  : "UserDataMode_Reserved1",
    8  : "UserDataMode_Reserved2",
    9  : "UserDataMode_Reserved3",
    10 : "UserDataMode_Reserved4",
    11 : "UserDataMode_Reserved5",
    12 : "UserDataMode_Reserved6",
    13 : "UserDataMode_Reserved7",
    14 : "UserDataMode_Reserved8",
    15 : "UserDataMode_Reserved9",
    }
),
"SignalStandardType" : ( "02010127-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "SignalStandard_None",
    1  : "SignalStandard_ITU601",
    2  : "SignalStandard_ITU1358",
    3  : "SignalStandard_SMPTE347M",
    4  : "SignalStandard_SMPTE274M",
    5  : "SignalStandard_SMPTE296M",
    6  : "SignalStandard_SMPTE349M",
    }
),
"ScanningDirectionType" : ( "02010128-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "ScanningDirection_LeftToRightTopToBottom",
    1  : "ScanningDirection_RightToLeftTopToBottom",
    2  : "ScanningDirection_LeftToRightBottomToTop",
    3  : "ScanningDirection_RightToLeftBottomToTop",
    4  : "ScanningDirection_TopToBottomLeftToRight",
    5  : "ScanningDirection_TopToBottomRightToLeft",
    6  : "ScanningDirection_BottomToTopLeftToRight",
    7  : "ScanningDirection_BottomToTopRightToLeft",
    }
),
"ContentScanningType" : ( "0201012a-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "ContentScanning_NotKnown",
    1  : "ContentScanning_Progressive",
    2  : "ContentScanning_Interlace",
    3  : "ContentScanning_Mixed",
    }
),
"TitleAlignmentType" : ( "0201012b-0000-0000-060e-2b3401040101", "UInt8", {
    0  : "TitleAlignment_Left",
    1  : "TitleAlignment_Center",
    2  : "TitleAlignment_Right",
    }
),
}

records = {
"AUID"   : ("01030100-0000-0000-060e-2b3401040101", (
    ("Data1"             , "UInt32"),
    ("Data2"             , "UInt16"),
    ("Data3"             , "UInt16"),
    ("Data4"             , "UInt8Array8"),
    )
),
"MobIDType": ("01030200-0000-0000-060e-2b3401040101", (
    ("SMPTELabel"        , "UInt8Array12"),
    ("length"            , "UInt8"),
    ("instanceHigh"      , "UInt8"),
    ("instanceMid"       , "UInt8"),
    ("instanceLow"       , "UInt8"),
    ("material"          , "AUID"),
    )
),
"Rational": ("03010100-0000-0000-060e-2b3401040101", (
    ("Numerator"         , "Int32"),
    ("Denominator"       , "Int32"),
    )
),
"ProductVersion": ("03010200-0000-0000-060e-2b3401040101", (
    ("major"             , "UInt16"),
    ("minor"             , "UInt16"),
    ("tertiary"          , "UInt16"),
    ("patchLevel"        , "UInt16"),
    ("type"              , "ProductReleaseType"),
    )
),
"VersionType": ("03010300-0000-0000-060e-2b3401040101", (
    ("major"             , "Int8"),
    ("minor"             , "Int8"),
    )
),
"RGBAComponent": ("03010400-0000-0000-060e-2b3401040101", (
    ("Code"              , "RGBAComponentKind"),
    ("Size"              , "UInt8"),
    )
),
"DateStruct": ("03010500-0000-0000-060e-2b3401040101", (
    ("year"              , "Int16"),
    ("month"             , "UInt8"),
    ("day"               , "UInt8"),
    )
),
"TimeStruct": ("03010600-0000-0000-060e-2b3401040101", (
    ("hour"              , "UInt8"),
    ("minute"            , "UInt8"),
    ("second"            , "UInt8"),
    ("fraction"          , "UInt8"),
    )
),
"TimeStamp": ("03010700-0000-0000-060e-2b3401040101", (
    ("date"              , "DateStruct"),
    ("time"              , "TimeStruct"),
    )
),
}

arrays = {
"UInt8Array"            : ("04010100-0000-0000-060e-2b3401040101", "UInt8", None),
"UInt8Array12"          : ("04010200-0000-0000-060e-2b3401040101", "UInt8", 12),
"Int32Array"            : ("04010300-0000-0000-060e-2b3401040101", "Int32", None),
"Int64Array"            : ("04010400-0000-0000-060e-2b3401040101", "Int64", None),
"StringArray"           : ("04010500-0000-0000-060e-2b3401040101", "Character", None),
"AUIDArray"             : ("04010600-0000-0000-060e-2b3401040101", "AUID", None),
"PositionArray"         : ("04010700-0000-0000-060e-2b3401040101", "UInt8", None),
"UInt8Array8"           : ("04010800-0000-0000-060e-2b3401040101", "UInt8", 8),
"UInt32Array"           : ("04010900-0000-0000-060e-2b3401040101", "UInt32", None),
"ChannelStatusModeArray": ("04010a00-0000-0000-060e-2b3401040101", "ChannelStatusModeType", None),
"UserDataModeArray"     : ("04010b00-0000-0000-060e-2b3401040101", "UserDataModeType", None),
"RGBALayout"            : ("04020100-0000-0000-060e-2b3401040101", "RGBAComponent", 8),
"DataValue"             : ("04100100-0000-0000-060e-2b3401040101", "UInt8", None),
}

renames = {
"PositionType"     : ("01012001-0000-0000-060e-2b3401040101", "Int64"),
"LengthType"       : ("01012002-0000-0000-060e-2b3401040101", "Int64"),
"JPEGTableIDType"  : ("01012003-0000-0000-060e-2b3401040101", "Int32"),
"PhaseFrameType"   : ("01012300-0000-0000-060e-2b3401040101", "Int32"),
}

strings = {
"String"           : ("01100200-0000-0000-060e-2b3401040101", "Character"),
}

extenums = {
"OperationCategoryType": ("02020101-0000-0000-060e-2b3401040101", {
    "0d010102-0101-0100-060e-2b3404010101": "OperationCategory_Effect",
    }
),
"TransferCharacteristicType": ("02020102-0000-0000-060e-2b3401040101", {
    "04010101-0101-0000-060e-2b3404010101": "TransferCharacteristic_ITU470_PAL",
    "04010101-0102-0000-060e-2b3404010101": "TransferCharacteristic_ITU709",
    "04010101-0103-0000-060e-2b3404010101": "TransferCharacteristic_SMPTE240M",
    "04010101-0104-0000-060e-2b3404010101": "TransferCharacteristic_274M_296M",
    "04010101-0105-0000-060e-2b3404010101": "TransferCharacteristic_ITU1361",
    "04010101-0106-0000-060e-2b3404010101": "TransferCharacteristic_linear",
    }
),
"PluginCategoryType": ("02020103-0000-0000-060e-2b3401040101", {
    "0d010102-0101-0200-060e-2b3404010101": "PluginCategory_Effect",
    "0d010102-0101-0300-060e-2b3404010101": "PluginCategory_Codec",
    "0d010102-0101-0400-060e-2b3404010101": "PluginCategory_Interpolation",
    }
),
"UsageType"        : ("02020104-0000-0000-060e-2b3401040101", {
    "0d010102-0101-0500-060e-2b3404010101": "Usage_SubClip",
    "0d010102-0101-0600-060e-2b3404010101": "Usage_AdjustedClip",
    "0d010102-0101-0700-060e-2b3404010101": "Usage_TopLevel",
    "0d010102-0101-0800-060e-2b3404010101": "Usage_LowerLevel",
    "0d010102-0101-0900-060e-2b3404010101": "Usage_Template",
    }
),
"ColorPrimariesType": ("02020105-0000-0000-060e-2b3401040101", {
    "04010101-0301-0000-060e-2b3404010106": "ColorPrimaries_SMPTE170M",
    "04010101-0302-0000-060e-2b3404010106": "ColorPrimaries_ITU470_PAL",
    "04010101-0303-0000-060e-2b3404010106": "ColorPrimaries_ITU709",
    }
),
"CodingEquationsType": ("02020106-0000-0000-060e-2b3401040101", {
    "04010101-0201-0000-060e-2b3404010101": "CodingEquations_ITU601",
    "04010101-0202-0000-060e-2b3404010101": "CodingEquations_ITU709",
    "04010101-0203-0000-060e-2b3404010101": "CodingEquations_SMPTE240M",
    }
),
}

chars = {
"Character" : "01100100-0000-0000-060e-2b3401040101",
}

indirects = {
"Indirect" : "04100300-0000-0000-060e-2b3401040101",
}

opaques = {
"Opaque" : "04100400-0000-0000-060e-2b3401040101",
}

sets = {
"AUIDSet"     : ("04030100-0000-0000-060e-2b3401040101", "AUID"),
"UInt32Set"   : ("04030200-0000-0000-060e-2b3401040101", "UInt32"),
}

strongrefs = {
"ContentStorageStrongReference"             : ("05020100-0000-0000-060e-2b3401040101", "ContentStorage"),
"DictionaryStrongReference"                 : ("05020200-0000-0000-060e-2b3401040101", "Dictionary"),
"EssenceDescriptorStrongReference"          : ("05020300-0000-0000-060e-2b3401040101", "EssenceDescriptor"),
"NetworkLocatorStrongReference"             : ("05020400-0000-0000-060e-2b3401040101", "NetworkLocator"),
"OperationGroupStrongReference"             : ("05020500-0000-0000-060e-2b3401040101", "OperationGroup"),
"SegmentStrongReference"                    : ("05020600-0000-0000-060e-2b3401040101", "Segment"),
"SourceClipStrongReference"                 : ("05020700-0000-0000-060e-2b3401040101", "SourceClip"),
"SourceReferenceStrongReference"            : ("05020800-0000-0000-060e-2b3401040101", "SourceReference"),
"ClassDefinitionStrongReference"            : ("05020900-0000-0000-060e-2b3401040101", "ClassDefinition"),
"CodecDefinitionStrongReference"            : ("05020a00-0000-0000-060e-2b3401040101", "CodecDefinition"),
"ComponentStrongReference"                  : ("05020b00-0000-0000-060e-2b3401040101", "Component"),
"ContainerDefinitionStrongReference"        : ("05020c00-0000-0000-060e-2b3401040101", "ContainerDefinition"),
"ControlPointStrongReference"               : ("05020d00-0000-0000-060e-2b3401040101", "ControlPoint"),
"DataDefinitionStrongReference"             : ("05020e00-0000-0000-060e-2b3401040101", "DataDefinition"),
"EssenceDataStrongReference"                : ("05020f00-0000-0000-060e-2b3401040101", "EssenceData"),
"IdentificationStrongReference"             : ("05021000-0000-0000-060e-2b3401040101", "Identification"),
"InterpolationDefinitionStrongReference"    : ("05021100-0000-0000-060e-2b3401040101", "InterpolationDefinition"),
"LocatorStrongReference"                    : ("05021200-0000-0000-060e-2b3401040101", "Locator"),
"MobStrongReference"                        : ("05021300-0000-0000-060e-2b3401040101", "Mob"),
"MobSlotStrongReference"                    : ("05021400-0000-0000-060e-2b3401040101", "MobSlot"),
"OperationDefinitionStrongReference"        : ("05021500-0000-0000-060e-2b3401040101", "OperationDefinition"),
"ParameterStrongReference"                  : ("05021600-0000-0000-060e-2b3401040101", "Parameter"),
"ParameterDefinitionStrongReference"        : ("05021700-0000-0000-060e-2b3401040101", "ParameterDefinition"),
"PluginDefinitionStrongReference"           : ("05021800-0000-0000-060e-2b3401040101", "PluginDefinition"),
"PropertyDefinitionStrongReference"         : ("05021900-0000-0000-060e-2b3401040101", "PropertyDefinition"),
"TaggedValueStrongReference"                : ("05021a00-0000-0000-060e-2b3401040101", "TaggedValue"),
"TypeDefinitionStrongReference"             : ("05021b00-0000-0000-060e-2b3401040101", "TypeDefinition"),
"KLVDataStrongReference"                    : ("05021c00-0000-0000-060e-2b3401040101", "KLVData"),
"FileDescriptorStrongReference"             : ("05021d00-0000-0000-060e-2b3401040101", "FileDescriptor"),
"RIFFChunkStrongReference"                  : ("05021e00-0000-0000-060e-2b3401040101", "RIFFChunk"),
"DescriptiveFrameworkStrongReference"       : ("05021f00-0000-0000-060e-2b3401040101", "DescriptiveFramework"),
"KLVDataDefinitionStrongReference"          : ("05022000-0000-0000-060e-2b3401040101", "KLVDataDefinition"),
"TaggedValueDefinitionStrongReference"      : ("05022100-0000-0000-060e-2b3401040101", "TaggedValueDefinition"),
"DescriptiveObjectStrongReference"          : ("05022200-0000-0000-060e-2b3401040101", "DescriptiveObject"),
}

strongref_sets = {
"ClassDefinitionStrongReferenceSet"         : ("05050100-0000-0000-060e-2b3401040101", "ClassDefinitionStrongReference"),
"CodecDefinitionStrongReferenceSet"         : ("05050200-0000-0000-060e-2b3401040101", "CodecDefinitionStrongReference"),
"ContainerDefinitionStrongReferenceSet"     : ("05050300-0000-0000-060e-2b3401040101", "ContainerDefinitionStrongReference"),
"DataDefinitionStrongReferenceSet"          : ("05050400-0000-0000-060e-2b3401040101", "DataDefinitionStrongReference"),
"EssenceDataStrongReferenceSet"             : ("05050500-0000-0000-060e-2b3401040101", "EssenceDataStrongReference"),
"InterpolationDefinitionStrongReferenceSet" : ("05050600-0000-0000-060e-2b3401040101", "InterpolationDefinitionStrongReference"),
"MobStrongReferenceSet"                     : ("05050700-0000-0000-060e-2b3401040101", "MobStrongReference"),
"OperationDefinitionStrongReferenceSet"     : ("05050800-0000-0000-060e-2b3401040101", "OperationDefinitionStrongReference"),
"ParameterDefinitionStrongReferenceSet"     : ("05050900-0000-0000-060e-2b3401040101", "ParameterDefinitionStrongReference"),
"PluginDefinitionStrongReferenceSet"        : ("05050a00-0000-0000-060e-2b3401040101", "PluginDefinitionStrongReference"),
"PropertyDefinitionStrongReferenceSet"      : ("05050b00-0000-0000-060e-2b3401040101", "PropertyDefinitionStrongReference"),
"TypeDefinitionStrongReferenceSet"          : ("05050c00-0000-0000-060e-2b3401040101", "TypeDefinitionStrongReference"),
"KLVDataDefinitionStrongReferenceSet"       : ("05050d00-0000-0000-060e-2b3401040101", "KLVDataDefinitionStrongReference"),
"TaggedValueDefinitionStrongReferenceSet"   : ("05050e00-0000-0000-060e-2b3401040101", "TaggedValueDefinitionStrongReference"),
"DescriptiveObjectStrongReferenceSet"       : ("05050f00-0000-0000-060e-2b3401040101", "DescriptiveObjectStrongReference"),
}

strongref_vectors = {
"ComponentStrongReferenceVector"            : ("05060100-0000-0000-060e-2b3401040101", "ComponentStrongReference"),
"ControlPointStrongReferenceVector"         : ("05060200-0000-0000-060e-2b3401040101", "ControlPointStrongReference"),
"IdentificationStrongReferenceVector"       : ("05060300-0000-0000-060e-2b3401040101", "IdentificationStrongReference"),
"LocatorStrongReferenceVector"              : ("05060400-0000-0000-060e-2b3401040101", "LocatorStrongReference"),
"MobSlotStrongReferenceVector"              : ("05060500-0000-0000-060e-2b3401040101", "MobSlotStrongReference"),
"SegmentStrongReferenceVector"              : ("05060600-0000-0000-060e-2b3401040101", "SegmentStrongReference"),
"SourceReferenceStrongReferenceVector"      : ("05060700-0000-0000-060e-2b3401040101", "SourceReferenceStrongReference"),
"TaggedValueStrongReferenceVector"          : ("05060800-0000-0000-060e-2b3401040101", "TaggedValueStrongReference"),
"KLVDataStrongReferenceVector"              : ("05060900-0000-0000-060e-2b3401040101", "KLVDataStrongReference"),
"ParameterStrongReferenceVector"            : ("05060a00-0000-0000-060e-2b3401040101", "ParameterStrongReference"),
"FileDescriptorStrongReferenceVector"       : ("05060b00-0000-0000-060e-2b3401040101", "FileDescriptorStrongReference"),
"RIFFChunkStrongReferenceVector"            : ("05060c00-0000-0000-060e-2b3401040101", "RIFFChunkStrongReference"),
"DescriptiveObjectStrongReferenceVector"    : ("05060d00-0000-0000-060e-2b3401040101", "DescriptiveObjectStrongReference"),
}

weakrefs = {
"ClassDefinitionWeakReference"              : ("05010100-0000-0000-060e-2b3401040101", "ClassDefinition",
    ("MetaDictionary", "ClassDefinitions", )
),
"ContainerDefinitionWeakReference"          : ("05010200-0000-0000-060e-2b3401040101", "ContainerDefinition",
    ("Header", "Dictionary", "ContainerDefinitions", )
),
"DataDefinitionWeakReference"               : ("05010300-0000-0000-060e-2b3401040101", "DataDefinition",
    ("Header", "Dictionary", "DataDefinitions", )
),
"InterpolationDefinitionWeakReference"      : ("05010500-0000-0000-060e-2b3401040101", "InterpolationDefinition",
    ("Header", "Dictionary", "InterpolationDefinitions", )
),
"MobWeakReference"                          : ("05010600-0000-0000-060e-2b3401040101", "Mob",
    ("Header", "Content", "Mobs", )
),
"OperationDefinitionWeakReference"          : ("05010700-0000-0000-060e-2b3401040101", "OperationDefinition",
    ("Header", "Dictionary", "OperationDefinitions", )
),
"ParameterDefinitionWeakReference"          : ("05010800-0000-0000-060e-2b3401040101", "ParameterDefinition",
    ("Header", "Dictionary", "ParameterDefinitions", )
),
"TypeDefinitionWeakReference"               : ("05010900-0000-0000-060e-2b3401040101", "TypeDefinition",
    ("MetaDictionary", "TypeDefinitions", )
),
"PluginDefinitionWeakReference"             : ("05010a00-0000-0000-060e-2b3401040101", "PluginDefinition",
    ("Header", "Dictionary", "PluginDefinitions", )
),
"CodecDefinitionWeakReference"              : ("05010b00-0000-0000-060e-2b3401040101", "CodecDefinition",
    ("Header", "Dictionary", "CodecDefinitions", )
),
"PropertyDefinitionWeakReference"           : ("05010c00-0000-0000-060e-2b3401040101", "PropertyDefinition",
    ("MetaDictionary", "ClassDefinitions", "Properties", )
),
}

weakref_sets = {
"DataDefinitionWeakReferenceSet"            : ("05030d00-0000-0000-060e-2b3401040101", "DataDefinitionWeakReference"),
"ParameterDefinitionWeakReferenceSet"       : ("05030e00-0000-0000-060e-2b3401040101", "ParameterDefinitionWeakReference"),
"PluginDefinitionWeakReferenceSet"          : ("05030f00-0000-0000-060e-2b3401040101", "PluginDefinitionWeakReference"),
"PropertyDefinitionWeakReferenceSet"        : ("05031000-0000-0000-060e-2b3401040101", "PropertyDefinitionWeakReference"),
}

weakref_vectors = {
"OperationDefinitionWeakReferenceVector"    : ("05040100-0000-0000-060e-2b3401040101", "OperationDefinitionWeakReference"),
"TypeDefinitionWeakReferenceVector"         : ("05040200-0000-0000-060e-2b3401040101", "TypeDefinitionWeakReference"),
"DataDefinitionWeakReferenceVector"         : ("05040300-0000-0000-060e-2b3401040101", "DataDefinitionWeakReference"),
}

streams = {
"Stream" : "04100200-0000-0000-060e-2b3401040101"
}

