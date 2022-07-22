ints = {
"aafUInt8"   : ("01010100-0000-0000-060e-2b3401040101", 1, False, ),
"aafUInt16"  : ("01010200-0000-0000-060e-2b3401040101", 2, False, ),
"aafUInt32"  : ("01010300-0000-0000-060e-2b3401040101", 4, False, ),
"aafUInt64"  : ("01010400-0000-0000-060e-2b3401040101", 8, False, ),
"aafInt8"    : ("01010500-0000-0000-060e-2b3401040101", 1, True, ),
"aafInt16"   : ("01010600-0000-0000-060e-2b3401040101", 2, True, ),
"aafInt32"   : ("01010700-0000-0000-060e-2b3401040101", 4, True, ),
"aafInt64"   : ("01010800-0000-0000-060e-2b3401040101", 8, True, ),
}

enums = {
"Boolean"                  : ("01040100-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "False",
   1  : "True",
   }
),
"ProductReleaseType"       : ("02010101-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "VersionUnknown",
   1  : "VersionReleased",
   2  : "VersionDebug",
   3  : "VersionPatched",
   4  : "VersionBeta",
   5  : "VersionPrivateBuild",
   }
),
"TapeFormatType"           : ("02010102-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "TapeFormatNull",
   1  : "BetacamFormat",
   2  : "BetacamSPFormat",
   3  : "VHSFormat",
   4  : "SVHSFormat",
   5  : "8mmFormat",
   6  : "Hi8Format",
   }
),
"VideoSignalType"          : ("02010103-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "VideoSignalNull",
   1  : "NTSCSignal",
   2  : "PALSignal",
   }
),
"TapeCaseType"             : ("02010104-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"ColorSitingType"          : ("02010105-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "CoSiting",
   1  : "Averaging",
   2  : "ThreeTap",
   3  : "Quincunx",
   4  : "Rec601",
   5  : "LineAlternating",
   6  : "VerticalMidpoint",
   255: "UnknownSiting",
   }
),
"EditHintType"             : ("02010106-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "NoEditHint",
   1  : "Proportional",
   2  : "RelativeLeft",
   3  : "RelativeRight",
   4  : "RelativeFixed",
   }
),
"FadeType"                 : ("02010107-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "FadeNone",
   1  : "FadeLinearAmp",
   2  : "FadeLinearPower",
   }
),
"LayoutType"               : ("02010108-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "FullFrame",
   1  : "SeparateFields",
   2  : "OneField",
   3  : "MixedFields",
   4  : "SegmentedFrame",
   }
),
"TCSource"                 : ("02010109-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "TimecodeLTC",
   1  : "TimecodeVITC",
   }
),
"PulldownDirectionType"    : ("0201010a-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "TapeToFilmSpeed",
   1  : "FilmToTapeSpeed",
   }
),
"PulldownKindType"         : ("0201010b-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"EdgeType"                 : ("0201010c-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "EtNull",
   1  : "EtKeycode",
   2  : "EtEdgenum4",
   3  : "EtEdgenum5",
   8  : "EtHeaderSize",
   }
),
"FilmType"                 : ("0201010d-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "FtNull",
   1  : "Ft35MM",
   2  : "Ft16MM",
   3  : "Ft8MM",
   4  : "Ft65MM",
   }
),
"RGBAComponentKind"        : ("0201010e-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0x30: "CompNone",
   0x41: "CompAlpha",
   0x42: "CompBlue",
   0x46: "CompFill",
   0x47: "CompGreen",
   0x50: "CompPalette",
   0x52: "CompRed",
   0x00: "CompNull",
   0x72: "CompRedLSBs",
   0x67: "CompGreenLSBs",
   0x62: "CompBlueLSBs",
   0x61: "CompAlphaLSBs",
   0x55: "CompColorDifferenceU",
   0x56: "CompColorDifferenceV",
   0x57: "CompComposite",
   0x58: "CompNonCoSitedLuma",
   0x59: "CompLuma",
   0x5A: "CompDepth",
   0x75: "CompColorDifferenceULSBs",
   0x76: "CompColorDifferenceVLSBs",
   0x77: "CompCompositeLSBs",
   0x78: "CompNonCoSitedLumaLSBs",
   0x79: "CompLumaLSBs",
   0x7A: "CompDepthLSBs",
   0xD8: "CompColorX",
   0xD9: "CompColorY",
   0xDA: "CompColorZ",
   }
),
"ReferenceType"            : ("0201010f-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "RefLimitMinimum",
   1  : "RefLimitMaximum",
   2  : "RefMinimum",
   3  : "RefMaximum",
   4  : "RefEnumvalue",
   }
),
"AlphaTransparencyType"    : ("02010120-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "MinValueTransparent",
   1  : "MaxValueTransparent",
   }
),
"FieldNumber"              : ("02010121-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "UnspecifiedField",
   1  : "FieldOne",
   2  : "FieldTwo",
   }
),
"ElectroSpatialFormulation": ("02010122-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"EmphasisType"             : ("02010123-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"AuxBitsModeType"          : ("02010124-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"ChannelStatusModeType"    : ("02010125-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "ChannelStatusMode_None",
   1  : "ChannelStatusMode_Minimum",
   2  : "ChannelStatusMode_Standard",
   3  : "ChannelStatusMode_Fixed",
   4  : "ChannelStatusMode_Stream",
   5  : "ChannelStatusMode_Essence",
   }
),
"UserDataModeType"         : ("02010126-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"SignalStandardType"       : ("02010127-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "SignalStandard_None",
   1  : "SignalStandard_ITU601",
   2  : "SignalStandard_ITU1358",
   3  : "SignalStandard_SMPTE347M",
   4  : "SignalStandard_SMPTE274M",
   5  : "SignalStandard_SMPTE296M",
   6  : "SignalStandard_SMPTE349M",
   7  : "SignalStandard_SMPTE428_1",
   }
),
"ScanningDirectionType"    : ("02010128-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
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
"ContentScanningType"      : ("0201012a-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "ContentScanning_NotKnown",
   1  : "ContentScanning_Progressive",
   2  : "ContentScanning_Interlace",
   3  : "ContentScanning_Mixed",
   }
),
"TitleAlignmentType"       : ("0201012b-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "TitleAlignment_Left",
   1  : "TitleAlignment_Center",
   2  : "TitleAlignment_Right",
   }
),
"AVCContentScanningType"   : ("0201012c-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "AVCContentScanning_NotKnown",
   1  : "AVCContentScanning_ProgressiveFramePicture",
   2  : "AVCContentScanning_InterlaceFieldPicture",
   3  : "AVCContentScanning_InterlaceFramePicture",
   4  : "AVCContentScanning_Interlace_FrameFieldPicture",
   }
),
"MPEG4VisualCodedContentType": ("0201012d-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", {
   0  : "MPEG4VisualCodedContent_Unknown",
   1  : "MPEG4VisualCodedContent_Progressive",
   2  : "MPEG4VisualCodedContent_Interlaced",
   3  : "MPEG4VisualCodedContent_Mixed",
   }
),
}

records = {
"AUID"   : ("01030100-0000-0000-060e-2b3401040101", (
    ("Data1"             , "01010300-0000-0000-060e-2b3401040101"),
    ("Data2"             , "01010200-0000-0000-060e-2b3401040101"),
    ("Data3"             , "01010200-0000-0000-060e-2b3401040101"),
    ("Data4"             , "04010800-0000-0000-060e-2b3401040101"),
    )
),
"MobIDType": ("01030200-0000-0000-060e-2b3401040101", (
    ("SMPTELabel"        , "04010200-0000-0000-060e-2b3401040101"),
    ("length"            , "01010100-0000-0000-060e-2b3401040101"),
    ("instanceHigh"      , "01010100-0000-0000-060e-2b3401040101"),
    ("instanceMid"       , "01010100-0000-0000-060e-2b3401040101"),
    ("instanceLow"       , "01010100-0000-0000-060e-2b3401040101"),
    ("material"          , "01030100-0000-0000-060e-2b3401040101"),
    )
),
"Rational": ("03010100-0000-0000-060e-2b3401040101", (
    ("Numerator"         , "01010700-0000-0000-060e-2b3401040101"),
    ("Denominator"       , "01010700-0000-0000-060e-2b3401040101"),
    )
),
"ProductVersion": ("03010200-0000-0000-060e-2b3401040101", (
    ("major"             , "01010200-0000-0000-060e-2b3401040101"),
    ("minor"             , "01010200-0000-0000-060e-2b3401040101"),
    ("tertiary"          , "01010200-0000-0000-060e-2b3401040101"),
    ("patchLevel"        , "01010200-0000-0000-060e-2b3401040101"),
    ("type"              , "02010101-0000-0000-060e-2b3401040101"),
    )
),
"VersionType": ("03010300-0000-0000-060e-2b3401040101", (
    ("major"             , "01010500-0000-0000-060e-2b3401040101"),
    ("minor"             , "01010500-0000-0000-060e-2b3401040101"),
    )
),
"RGBAComponent": ("03010400-0000-0000-060e-2b3401040101", (
    ("Code"              , "0201010e-0000-0000-060e-2b3401040101"),
    ("Size"              , "01010100-0000-0000-060e-2b3401040101"),
    )
),
"DateStruct": ("03010500-0000-0000-060e-2b3401040101", (
    ("year"              , "01010600-0000-0000-060e-2b3401040101"),
    ("month"             , "01010100-0000-0000-060e-2b3401040101"),
    ("day"               , "01010100-0000-0000-060e-2b3401040101"),
    )
),
"TimeStruct": ("03010600-0000-0000-060e-2b3401040101", (
    ("hour"              , "01010100-0000-0000-060e-2b3401040101"),
    ("minute"            , "01010100-0000-0000-060e-2b3401040101"),
    ("second"            , "01010100-0000-0000-060e-2b3401040101"),
    ("fraction"          , "01010100-0000-0000-060e-2b3401040101"),
    )
),
"TimeStamp": ("03010700-0000-0000-060e-2b3401040101", (
    ("date"              , "03010500-0000-0000-060e-2b3401040101"),
    ("time"              , "03010600-0000-0000-060e-2b3401040101"),
    )
),
}

fixed_arrays = {
"aafUUID"         : ("01030300-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", 16),
"aafUInt8Array12" : ("04010200-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", 12),
"aafUInt8Array8"  : ("04010800-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101", 8),
"aafRGBALayout"   : ("04020100-0000-0000-060e-2b3401040101", "03010400-0000-0000-060e-2b3401040101", 8),
}

var_arrays = {
"aafUUIDArray"                : ("04011500-0000-0000-060e-2b3401040101", "01030300-0000-0000-060e-2b3401040101"),
"aafUInt8Array"               : ("04010100-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101"),
"aafInt32Array"               : ("04010300-0000-0000-060e-2b3401040101", "01010700-0000-0000-060e-2b3401040101"),
"aafInt64Array"               : ("04010400-0000-0000-060e-2b3401040101", "01010800-0000-0000-060e-2b3401040101"),
"aafStringArray"              : ("04010500-0000-0000-060e-2b3401040101", "01100100-0000-0000-060e-2b3401040101"),
"aafAUIDArray"                : ("04010600-0000-0000-060e-2b3401040101", "01030100-0000-0000-060e-2b3401040101"),
"aafPositionArray"            : ("04010700-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101"),
"aafUInt32Array"              : ("04010900-0000-0000-060e-2b3401040101", "01010300-0000-0000-060e-2b3401040101"),
"aafChannelStatusModeArray"   : ("04010a00-0000-0000-060e-2b3401040101", "02010125-0000-0000-060e-2b3401040101"),
"aafUserDataModeArray"        : ("04010b00-0000-0000-060e-2b3401040101", "02010126-0000-0000-060e-2b3401040101"),
"aafDataValue"                : ("04100100-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101"),
"kAAFTypeID_ComponentStrongReferenceVector"              : ("05060100-0000-0000-060e-2b3401040101", "05020b00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_ControlPointStrongReferenceVector"           : ("05060200-0000-0000-060e-2b3401040101", "05020d00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_IdentificationStrongReferenceVector"         : ("05060300-0000-0000-060e-2b3401040101", "05021000-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_LocatorStrongReferenceVector"                : ("05060400-0000-0000-060e-2b3401040101", "05021200-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_MobSlotStrongReferenceVector"                : ("05060500-0000-0000-060e-2b3401040101", "05021400-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_SegmentStrongReferenceVector"                : ("05060600-0000-0000-060e-2b3401040101", "05020600-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_SourceReferenceStrongReferenceVector"        : ("05060700-0000-0000-060e-2b3401040101", "05020800-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_TaggedValueStrongReferenceVector"            : ("05060800-0000-0000-060e-2b3401040101", "05021a00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_KLVDataStrongReferenceVector"                : ("05060900-0000-0000-060e-2b3401040101", "05021c00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_ParameterStrongReferenceVector"              : ("05060a00-0000-0000-060e-2b3401040101", "05021600-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_FileDescriptorStrongReferenceVector"         : ("05060b00-0000-0000-060e-2b3401040101", "05021d00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_RIFFChunkStrongReferenceVector"              : ("05060c00-0000-0000-060e-2b3401040101", "05021e00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_DescriptiveObjectStrongReferenceVector"      : ("05060d00-0000-0000-060e-2b3401040101", "05022200-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_SubDescriptorStrongReferenceVector"          : ("05060e00-0000-0000-060e-2b3401040101", "05022600-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_OperationDefinitionWeakReferenceVector" : ("05040100-0000-0000-060e-2b3401040101", "05010700-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_TypeDefinitionWeakReferenceVector"      : ("05040200-0000-0000-060e-2b3401040101", "05010900-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_DataDefinitionWeakReferenceVector"      : ("05040300-0000-0000-060e-2b3401040101", "05010300-0000-0000-060e-2b3401040101" ),
}

renames = {
"aafPositionType"     : ("01012001-0000-0000-060e-2b3401040101", "01010800-0000-0000-060e-2b3401040101"),
"aafLengthType"       : ("01012002-0000-0000-060e-2b3401040101", "01010800-0000-0000-060e-2b3401040101"),
"aafJPEGTableIDType"  : ("01012003-0000-0000-060e-2b3401040101", "01010700-0000-0000-060e-2b3401040101"),
"aafPhaseFrameType"   : ("01012300-0000-0000-060e-2b3401040101", "01010700-0000-0000-060e-2b3401040101"),
}

strings = {
"aafString"           : ("01100200-0000-0000-060e-2b3401040101", "01100100-0000-0000-060e-2b3401040101"),
"aafISO7"             : ("01100400-0000-0000-060e-2b3401040101", "01100300-0000-0000-060e-2b3401040101"),
}

streams = {
"Stream" : "04100200-0000-0000-060e-2b3401040101",
}

opaques = {
"aafOpaque" : "04100400-0000-0000-060e-2b3401040101",
}

extenums = {
"OperationCategoryType": ("02020101-0000-0000-060e-2b3401040101", {
    "0d010102-0101-0100-060e-2b3404010101" : "OperationCategory_Effect",
    }
),
"TransferCharacteristicType": ("02020102-0000-0000-060e-2b3401040101", {
    "04010101-0101-0000-060e-2b3404010101" : "TransferCharacteristic_ITU470_PAL",
    "04010101-0102-0000-060e-2b3404010101" : "TransferCharacteristic_ITU709",
    "04010101-0103-0000-060e-2b3404010101" : "TransferCharacteristic_SMPTE240M",
    "04010101-0104-0000-060e-2b3404010101" : "TransferCharacteristic_274M_296M",
    "04010101-0105-0000-060e-2b3404010101" : "TransferCharacteristic_ITU1361",
    "04010101-0106-0000-060e-2b3404010101" : "TransferCharacteristic_linear",
    "04010101-0107-0000-060e-2b3404010108" : "TransferCharacteristic_SMPTE_DCDM",
    "04010101-0108-0000-060e-2b340401010d" : "TransferCharacteristic_IEC6196624_xvYCC",
    "04010101-0109-0000-060e-2b340401010e" : "TransferCharacteristic_ITU2020",
    "04010101-010a-0000-060e-2b340401010d" : "TransferCharacteristic_SMPTEST2084",
    "04010101-010b-0000-060e-2b340401010d" : "TransferCharacteristic_HLG_OETF",
    }
),
"PluginCategoryType": ("02020103-0000-0000-060e-2b3401040101", {
    "0d010102-0101-0200-060e-2b3404010101" : "PluginCategory_Effect",
    "0d010102-0101-0300-060e-2b3404010101" : "PluginCategory_Codec",
    "0d010102-0101-0400-060e-2b3404010101" : "PluginCategory_Interpolation",
    }
),
"UsageType"        : ("02020104-0000-0000-060e-2b3401040101", {
    "0d010102-0101-0500-060e-2b3404010101" : "Usage_SubClip",
    "0d010102-0101-0600-060e-2b3404010101" : "Usage_AdjustedClip",
    "0d010102-0101-0700-060e-2b3404010101" : "Usage_TopLevel",
    "0d010102-0101-0800-060e-2b3404010101" : "Usage_LowerLevel",
    "0d010102-0101-0900-060e-2b3404010101" : "Usage_Template",
    }
),
"ColorPrimariesType": ("02020105-0000-0000-060e-2b3401040101", {
    "04010101-0301-0000-060e-2b3404010106" : "ColorPrimaries_SMPTE170M",
    "04010101-0302-0000-060e-2b3404010106" : "ColorPrimaries_ITU470_PAL",
    "04010101-0303-0000-060e-2b3404010106" : "ColorPrimaries_ITU709",
    "04010101-0304-0000-060e-2b340401010d" : "ColorPrimaries_ITU2020",
    "04010101-0305-0000-060e-2b340401010d" : "ColorPrimaries_SMPTE_DCDM",
    "04010101-0306-0000-060e-2b340401010d" : "ColorPrimaries_P3D65",
    }
),
"CodingEquationsType": ("02020106-0000-0000-060e-2b3401040101", {
    "04010101-0201-0000-060e-2b3404010101" : "CodingEquations_ITU601",
    "04010101-0202-0000-060e-2b3404010101" : "CodingEquations_ITU709",
    "04010101-0203-0000-060e-2b3404010101" : "CodingEquations_SMPTE240M",
    "04010101-0204-0000-060e-2b340401010d" : "CodingEquations_YCgCo",
    "04010101-0205-0000-060e-2b340401010d" : "CodingEquations_GBR",
    "04010101-0206-0000-060e-2b340401010d" : "CodingEquations_ITU2020_NCL",
    }
),
}

chars = {
"aafCharacter" : "01100100-0000-0000-060e-2b3401040101",
}

generic_chars = {
"aafChar" : ("01100300-0000-0000-060e-2b3401040101", 1),
}

indirects = {
"aafIndirect" : "04100300-0000-0000-060e-2b3401040101",
}

sets = {
"AUIDSet": ("04030100-0000-0000-060e-2b3401040101", "01030100-0000-0000-060e-2b3401040101"),
"UInt32Set": ("04030200-0000-0000-060e-2b3401040101", "01010300-0000-0000-060e-2b3401040101"),
"kAAFTypeID_ClassDefinitionStrongReferenceSet"           : ("05050100-0000-0000-060e-2b3401040101", "05020900-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_CodecDefinitionStrongReferenceSet"           : ("05050200-0000-0000-060e-2b3401040101", "05020a00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_ContainerDefinitionStrongReferenceSet"       : ("05050300-0000-0000-060e-2b3401040101", "05020c00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_DataDefinitionStrongReferenceSet"            : ("05050400-0000-0000-060e-2b3401040101", "05020e00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_EssenceDataStrongReferenceSet"               : ("05050500-0000-0000-060e-2b3401040101", "05020f00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_InterpolationDefinitionStrongReferenceSet"   : ("05050600-0000-0000-060e-2b3401040101", "05021100-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_MobStrongReferenceSet"                       : ("05050700-0000-0000-060e-2b3401040101", "05021300-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_OperationDefinitionStrongReferenceSet"       : ("05050800-0000-0000-060e-2b3401040101", "05021500-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_ParameterDefinitionStrongReferenceSet"       : ("05050900-0000-0000-060e-2b3401040101", "05021700-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_PluginDefinitionStrongReferenceSet"          : ("05050a00-0000-0000-060e-2b3401040101", "05021800-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_PropertyDefinitionStrongReferenceSet"        : ("05050b00-0000-0000-060e-2b3401040101", "05021900-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_TypeDefinitionStrongReferenceSet"            : ("05050c00-0000-0000-060e-2b3401040101", "05021b00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_KLVDataDefinitionStrongReferenceSet"         : ("05050d00-0000-0000-060e-2b3401040101", "05022000-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_TaggedValueDefinitionStrongReferenceSet"     : ("05050e00-0000-0000-060e-2b3401040101", "05022100-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_DescriptiveObjectStrongReferenceSet"         : ("05050f00-0000-0000-060e-2b3401040101", "05022200-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_DataDefinitionWeakReferenceSet"         : ("05030d00-0000-0000-060e-2b3401040101", "05010300-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_ParameterDefinitionWeakReferenceSet"    : ("05030e00-0000-0000-060e-2b3401040101", "05010800-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_PluginDefinitionWeakReferenceSet"       : ("05030f00-0000-0000-060e-2b3401040101", "05010a00-0000-0000-060e-2b3401040101" ),
"kAAFTypeID_PropertyDefinitionWeakReferenceSet"     : ("05031000-0000-0000-060e-2b3401040101", "05010c00-0000-0000-060e-2b3401040101" ),
}

strongrefs = {
"kAAFTypeID_ContentStorageStrongReference"          : ("05020100-0000-0000-060e-2b3401040101", "0d010101-0101-1800-060e-2b3402060101" ),
"kAAFTypeID_DictionaryStrongReference"              : ("05020200-0000-0000-060e-2b3401040101", "0d010101-0101-2200-060e-2b3402060101" ),
"kAAFTypeID_EssenceDescriptorStrongReference"       : ("05020300-0000-0000-060e-2b3401040101", "0d010101-0101-2400-060e-2b3402060101" ),
"kAAFTypeID_NetworkLocatorStrongReference"          : ("05020400-0000-0000-060e-2b3401040101", "0d010101-0101-3200-060e-2b3402060101" ),
"kAAFTypeID_OperationGroupStrongReference"          : ("05020500-0000-0000-060e-2b3401040101", "0d010101-0101-0a00-060e-2b3402060101" ),
"kAAFTypeID_SegmentStrongReference"                 : ("05020600-0000-0000-060e-2b3401040101", "0d010101-0101-0300-060e-2b3402060101" ),
"kAAFTypeID_SourceClipStrongReference"              : ("05020700-0000-0000-060e-2b3401040101", "0d010101-0101-1100-060e-2b3402060101" ),
"kAAFTypeID_SourceReferenceStrongReference"         : ("05020800-0000-0000-060e-2b3401040101", "0d010101-0101-1000-060e-2b3402060101" ),
"kAAFTypeID_ClassDefinitionStrongReference"         : ("05020900-0000-0000-060e-2b3401040101", "0d010101-0201-0000-060e-2b3402060101" ),
"kAAFTypeID_CodecDefinitionStrongReference"         : ("05020a00-0000-0000-060e-2b3401040101", "0d010101-0101-1f00-060e-2b3402060101" ),
"kAAFTypeID_ComponentStrongReference"               : ("05020b00-0000-0000-060e-2b3401040101", "0d010101-0101-0200-060e-2b3402060101" ),
"kAAFTypeID_ContainerDefinitionStrongReference"     : ("05020c00-0000-0000-060e-2b3401040101", "0d010101-0101-2000-060e-2b3402060101" ),
"kAAFTypeID_ControlPointStrongReference"            : ("05020d00-0000-0000-060e-2b3401040101", "0d010101-0101-1900-060e-2b3402060101" ),
"kAAFTypeID_DataDefinitionStrongReference"          : ("05020e00-0000-0000-060e-2b3401040101", "0d010101-0101-1b00-060e-2b3402060101" ),
"kAAFTypeID_EssenceDataStrongReference"             : ("05020f00-0000-0000-060e-2b3401040101", "0d010101-0101-2300-060e-2b3402060101" ),
"kAAFTypeID_IdentificationStrongReference"          : ("05021000-0000-0000-060e-2b3401040101", "0d010101-0101-3000-060e-2b3402060101" ),
"kAAFTypeID_InterpolationDefinitionStrongReference" : ("05021100-0000-0000-060e-2b3401040101", "0d010101-0101-2100-060e-2b3402060101" ),
"kAAFTypeID_LocatorStrongReference"                 : ("05021200-0000-0000-060e-2b3401040101", "0d010101-0101-3100-060e-2b3402060101" ),
"kAAFTypeID_MobStrongReference"                     : ("05021300-0000-0000-060e-2b3401040101", "0d010101-0101-3400-060e-2b3402060101" ),
"kAAFTypeID_MobSlotStrongReference"                 : ("05021400-0000-0000-060e-2b3401040101", "0d010101-0101-3800-060e-2b3402060101" ),
"kAAFTypeID_OperationDefinitionStrongReference"     : ("05021500-0000-0000-060e-2b3401040101", "0d010101-0101-1c00-060e-2b3402060101" ),
"kAAFTypeID_ParameterStrongReference"               : ("05021600-0000-0000-060e-2b3401040101", "0d010101-0101-3c00-060e-2b3402060101" ),
"kAAFTypeID_ParameterDefinitionStrongReference"     : ("05021700-0000-0000-060e-2b3401040101", "0d010101-0101-1d00-060e-2b3402060101" ),
"kAAFTypeID_PluginDefinitionStrongReference"        : ("05021800-0000-0000-060e-2b3401040101", "0d010101-0101-1e00-060e-2b3402060101" ),
"kAAFTypeID_PropertyDefinitionStrongReference"      : ("05021900-0000-0000-060e-2b3401040101", "0d010101-0202-0000-060e-2b3402060101" ),
"kAAFTypeID_TaggedValueStrongReference"             : ("05021a00-0000-0000-060e-2b3401040101", "0d010101-0101-3f00-060e-2b3402060101" ),
"kAAFTypeID_TypeDefinitionStrongReference"          : ("05021b00-0000-0000-060e-2b3401040101", "0d010101-0203-0000-060e-2b3402060101" ),
"kAAFTypeID_KLVDataStrongReference"                 : ("05021c00-0000-0000-060e-2b3401040101", "0d010101-0101-4000-060e-2b3402060101" ),
"kAAFTypeID_FileDescriptorStrongReference"          : ("05021d00-0000-0000-060e-2b3401040101", "0d010101-0101-2500-060e-2b3402060101" ),
"kAAFTypeID_RIFFChunkStrongReference"               : ("05021e00-0000-0000-060e-2b3401040101", "0d010101-0101-4f00-060e-2b3402060101" ),
"kAAFTypeID_DescriptiveFrameworkStrongReference"    : ("05021f00-0000-0000-060e-2b3401040101", "0d010401-0000-0000-060e-2b3402060101" ),
"kAAFTypeID_KLVDataDefinitionStrongReference"       : ("05022000-0000-0000-060e-2b3401040101", "0d010101-0101-4d00-060e-2b3402060101" ),
"kAAFTypeID_TaggedValueDefinitionStrongReference"   : ("05022100-0000-0000-060e-2b3401040101", "0d010101-0101-4c00-060e-2b3402060101" ),
"kAAFTypeID_DescriptiveObjectStrongReference"       : ("05022200-0000-0000-060e-2b3401040101", "0d010400-0000-0000-060e-2b3402060101" ),
"kAAFTypeID_SubDescriptorStrongReference"           : ("05022600-0000-0000-060e-2b3401040101", "0d010101-0101-5900-060e-2b3402060101" ),
}

weakrefs = {
"ClassDefinitionWeakReference"            : ("05010100-0000-0000-060e-2b3401040101", "0d010101-0201-0000-060e-2b3402060101",
   ("0d010301-0101-0100-060e-2b3401010102", "06010107-0700-0000-060e-2b3401010102", )
),
"ContainerDefinitionWeakReference"        : ("05010200-0000-0000-060e-2b3401040101", "0d010101-0101-2000-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0508-0000-060e-2b3401010102", )
),
"DataDefinitionWeakReference"             : ("05010300-0000-0000-060e-2b3401040101", "0d010101-0101-1b00-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0505-0000-060e-2b3401010102", )
),
"InterpolationDefinitionWeakReference"    : ("05010500-0000-0000-060e-2b3401040101", "0d010101-0101-2100-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0509-0000-060e-2b3401010102", )
),
"MobWeakReference"                        : ("05010600-0000-0000-060e-2b3401040101", "0d010101-0101-3400-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0201-0000-060e-2b3401010102", "06010104-0501-0000-060e-2b3401010102", )
),
"OperationDefinitionWeakReference"        : ("05010700-0000-0000-060e-2b3401040101", "0d010101-0101-1c00-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0503-0000-060e-2b3401010102", )
),
"ParameterDefinitionWeakReference"        : ("05010800-0000-0000-060e-2b3401040101", "0d010101-0101-1d00-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0504-0000-060e-2b3401010102", )
),
"TypeDefinitionWeakReference"             : ("05010900-0000-0000-060e-2b3401040101", "0d010101-0203-0000-060e-2b3402060101",
   ("0d010301-0101-0100-060e-2b3401010102", "06010107-0800-0000-060e-2b3401010102", )
),
"PluginDefinitionWeakReference"           : ("05010a00-0000-0000-060e-2b3401040101", "0d010101-0101-1e00-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0506-0000-060e-2b3401010102", )
),
"CodecDefinitionWeakReference"            : ("05010b00-0000-0000-060e-2b3401040101", "0d010101-0101-1f00-060e-2b3402060101",
   ("0d010301-0102-0100-060e-2b3401010102", "06010104-0202-0000-060e-2b3401010102", "06010104-0507-0000-060e-2b3401010102", )
),
"PropertyDefinitionWeakReference"         : ("05010c00-0000-0000-060e-2b3401040101", "0d010101-0202-0000-060e-2b3402060101",
   ("0d010301-0101-0100-060e-2b3401010102", "06010107-0700-0000-060e-2b3401010102", "06010107-0200-0000-060e-2b3401010102", )
),
}

