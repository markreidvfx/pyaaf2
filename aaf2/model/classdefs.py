classdefs = {
"InterchangeObject" : ("0d010101-0101-0100-060e-2b3402060101" ,"Root", False, {
    "ObjClass"              : ("06010104-0101-0000-060e-2b3401010102", 0x0101, "ClassDefinitionWeakReference", True, False),
    "Generation"            : ("05200701-0800-0000-060e-2b3401010102", 0x0102, "AUID", False, False),
    }
),
"Component"      : ("0d010101-0101-0200-060e-2b3402060101" ,"InterchangeObject", False, {
    "DataDefinition"        : ("04070100-0000-0000-060e-2b3401010102", 0x0201, "DataDefinitionWeakReference", True, False),
    "Length"                : ("07020201-0103-0000-060e-2b3401010102", 0x0202, "LengthType", False, False),
    "KLVData"               : ("03010210-0400-0000-060e-2b3401010102", 0x0203, "KLVDataStrongReferenceVector", False, False),
    "UserComments"          : ("03020102-1600-0000-060e-2b3401010107", 0x0204, "TaggedValueStrongReferenceVector", False, False),
    "Attributes"            : ("03010210-0800-0000-060e-2b3401010107", 0x0205, "TaggedValueStrongReferenceVector", False, False),
    }
),
"Segment"        : ("0d010101-0101-0300-060e-2b3402060101" ,"Component", False, {
    }
),
"EdgeCode"       : ("0d010101-0101-0400-060e-2b3402060101" ,"Segment", True, {
    "Start"                 : ("01040901-0000-0000-060e-2b3401010102", 0x0401, "PositionType", True, False),
    "FilmKind"              : ("04100103-0109-0000-060e-2b3401010102", 0x0402, "FilmType", True, False),
    "CodeFormat"            : ("04100103-0102-0000-060e-2b3401010101", 0x0403, "EdgeType", True, False),
    "Header"                : ("01030201-0200-0000-060e-2b3401010102", 0x0404, "DataValue", False, False),
    }
),
"EssenceGroup"   : ("0d010101-0101-0500-060e-2b3402060101" ,"Segment", True, {
    "Choices"               : ("06010104-0601-0000-060e-2b3401010102", 0x0501, "SourceReferenceStrongReferenceVector", True, False),
    "StillFrame"            : ("06010104-0208-0000-060e-2b3401010102", 0x0502, "SourceReferenceStrongReference", False, False),
    }
),
"Event"          : ("0d010101-0101-0600-060e-2b3402060101" ,"Segment", False, {
    "Position"              : ("07020103-0303-0000-060e-2b3401010102", 0x0601, "PositionType", True, False),
    "Comment"               : ("05300404-0100-0000-060e-2b3401010102", 0x0602, "String", False, False),
    }
),
"GPITrigger"     : ("0d010101-0101-0700-060e-2b3402060101" ,"Event", True, {
    "ActiveState"           : ("05300401-0000-0000-060e-2b3401010101", 0x0801, "Boolean", True, False),
    }
),
"CommentMarker"  : ("0d010101-0101-0800-060e-2b3402060101" ,"Event", True, {
    "Annotation"            : ("06010104-020a-0000-060e-2b3401010102", 0x0901, "SourceReferenceStrongReference", False, False),
    }
),
"Filler"         : ("0d010101-0101-0900-060e-2b3402060101" ,"Segment", True, {
    }
),
"OperationGroup" : ("0d010101-0101-0a00-060e-2b3402060101" ,"Segment", True, {
    "Operation"             : ("05300506-0000-0000-060e-2b3401010102", 0x0b01, "OperationDefinitionWeakReference", True, False),
    "InputSegments"         : ("06010104-0602-0000-060e-2b3401010102", 0x0b02, "SegmentStrongReferenceVector", False, False),
    "Parameters"            : ("06010104-060a-0000-060e-2b3401010102", 0x0b03, "ParameterStrongReferenceVector", False, False),
    "BypassOverride"        : ("0530050c-0000-0000-060e-2b3401010102", 0x0b04, "UInt32", False, False),
    "Rendering"             : ("06010104-0206-0000-060e-2b3401010102", 0x0b05, "SourceReferenceStrongReference", False, False),
    }
),
"NestedScope"    : ("0d010101-0101-0b00-060e-2b3402060101" ,"Segment", True, {
    "Slots"                 : ("06010104-0607-0000-060e-2b3401010102", 0x0c01, "SegmentStrongReferenceVector", True, False),
    }
),
"Pulldown"       : ("0d010101-0101-0c00-060e-2b3402060101" ,"Segment", True, {
    "InputSegment"          : ("06010104-0207-0000-060e-2b3401010102", 0x0d01, "SegmentStrongReference", True, False),
    "PulldownKind"          : ("05401001-0200-0000-060e-2b3401010102", 0x0d02, "PulldownKindType", True, False),
    "PulldownDirection"     : ("05401001-0100-0000-060e-2b3401010102", 0x0d03, "PulldownDirectionType", True, False),
    "PhaseFrame"            : ("05401001-0300-0000-060e-2b3401010102", 0x0d04, "PhaseFrameType", True, False),
    }
),
"ScopeReference" : ("0d010101-0101-0d00-060e-2b3402060101" ,"Segment", True, {
    "RelativeScope"         : ("06010103-0300-0000-060e-2b3401010102", 0x0e01, "UInt32", True, False),
    "RelativeSlot"          : ("06010103-0400-0000-060e-2b3401010102", 0x0e02, "UInt32", True, False),
    }
),
"Selector"       : ("0d010101-0101-0e00-060e-2b3402060101" ,"Segment", True, {
    "Selected"              : ("06010104-0209-0000-060e-2b3401010102", 0x0f01, "SegmentStrongReference", True, False),
    "Alternates"            : ("06010104-0608-0000-060e-2b3401010102", 0x0f02, "SegmentStrongReferenceVector", False, False),
    }
),
"Sequence"       : ("0d010101-0101-0f00-060e-2b3402060101" ,"Segment", True, {
    "Components"            : ("06010104-0609-0000-060e-2b3401010102", 0x1001, "ComponentStrongReferenceVector", True, False),
    }
),
"SourceReference" : ("0d010101-0101-1000-060e-2b3402060101" ,"Segment", False, {
    "SourceID"              : ("06010103-0100-0000-060e-2b3401010102", 0x1101, "MobIDType", False, False),
    "SourceMobSlotID"       : ("06010103-0200-0000-060e-2b3401010102", 0x1102, "UInt32", True, False),
    "ChannelIDs"            : ("06010103-0700-0000-060e-2b3401010107", 0x1103, "UInt32Array", False, False),
    "MonoSourceSlotIDs"     : ("06010103-0800-0000-060e-2b3401010108", 0x1104, "UInt32Array", False, False),
    }
),
"SourceClip"     : ("0d010101-0101-1100-060e-2b3402060101" ,"SourceReference", True, {
    "StartTime"             : ("07020103-0104-0000-060e-2b3401010102", 0x1201, "PositionType", False, False),
    "FadeInLength"          : ("07020201-0105-0200-060e-2b3401010102", 0x1202, "LengthType", False, False),
    "FadeInType"            : ("05300501-0000-0000-060e-2b3401010101", 0x1203, "FadeType", False, False),
    "FadeOutLength"         : ("07020201-0105-0300-060e-2b3401010102", 0x1204, "LengthType", False, False),
    "FadeOutType"           : ("05300502-0000-0000-060e-2b3401010101", 0x1205, "FadeType", False, False),
    }
),
"TextClip"       : ("0d010101-0101-1200-060e-2b3402060101" ,"SourceReference", False, {
    }
),
"HTMLClip"       : ("0d010101-0101-1300-060e-2b3402060101" ,"TextClip", True, {
    "BeginAnchor"           : ("05300601-0100-0000-060e-2b3401010102", 0x1401, "String", False, False),
    "EndAnchor"             : ("05300602-0100-0000-060e-2b3401010102", 0x1402, "String", False, False),
    }
),
"Timecode"       : ("0d010101-0101-1400-060e-2b3402060101" ,"Segment", True, {
    "Start"                 : ("07020103-0105-0000-060e-2b3401010102", 0x1501, "PositionType", True, False),
    "FPS"                   : ("04040101-0206-0000-060e-2b3401010102", 0x1502, "UInt16", True, False),
    "Drop"                  : ("04040101-0500-0000-060e-2b3401010101", 0x1503, "Boolean", True, False),
    }
),
"TimecodeStream" : ("0d010101-0101-1500-060e-2b3402060101" ,"Segment", False, {
    "SampleRate"            : ("04040101-0201-0000-060e-2b3401010102", 0x1601, "Rational", True, False),
    "Source"                : ("04070300-0000-0000-060e-2b3401010102", 0x1602, "Stream", True, False),
    "SourceType"            : ("04040201-0000-0000-060e-2b3401010101", 0x1603, "TCSource", True, False),
    }
),
"TimecodeStream12M" : ("0d010101-0101-1600-060e-2b3402060101" ,"TimecodeStream", True, {
    "IncludeSync"           : ("04040101-0400-0000-060e-2b3401010101", 0x1701, "Boolean", True, False),
    }
),
"Transition"     : ("0d010101-0101-1700-060e-2b3402060101" ,"Component", True, {
    "OperationGroup"        : ("06010104-0205-0000-060e-2b3401010102", 0x1801, "OperationGroupStrongReference", True, False),
    "CutPoint"              : ("07020103-0106-0000-060e-2b3401010102", 0x1802, "PositionType", True, False),
    }
),
"ContentStorage" : ("0d010101-0101-1800-060e-2b3402060101" ,"InterchangeObject", True, {
    "Mobs"                  : ("06010104-0501-0000-060e-2b3401010102", 0x1901, "MobStrongReferenceSet", True, False),
    "EssenceData"           : ("06010104-0502-0000-060e-2b3401010102", 0x1902, "EssenceDataStrongReferenceSet", False, False),
    }
),
"ControlPoint"   : ("0d010101-0101-1900-060e-2b3402060101" ,"InterchangeObject", True, {
    "Value"                 : ("0530050d-0000-0000-060e-2b3401010102", 0x1a02, "Indirect", True, False),
    "Time"                  : ("07020103-1002-0100-060e-2b3401010102", 0x1a03, "Rational", True, False),
    "EditHint"              : ("05300508-0000-0000-060e-2b3401010102", 0x1a04, "EditHintType", False, False),
    }
),
"DefinitionObject" : ("0d010101-0101-1a00-060e-2b3402060101" ,"InterchangeObject", False, {
    "Identification"        : ("01011503-0000-0000-060e-2b3401010102", 0x1b01, "AUID", True, True),
    "Name"                  : ("01070102-0301-0000-060e-2b3401010102", 0x1b02, "String", True, False),
    "Description"           : ("03020301-0201-0000-060e-2b3401010102", 0x1b03, "String", False, False),
    }
),
"DataDefinition" : ("0d010101-0101-1b00-060e-2b3402060101" ,"DefinitionObject", True, {
    }
),
"OperationDefinition" : ("0d010101-0101-1c00-060e-2b3402060101" ,"DefinitionObject", True, {
    "DataDefinition"        : ("05300509-0000-0000-060e-2b3401010102", 0x1e01, "DataDefinitionWeakReference", True, False),
    "IsTimeWarp"            : ("05300503-0000-0000-060e-2b3401010101", 0x1e02, "Boolean", False, False),
    "DegradeTo"             : ("06010104-0401-0000-060e-2b3401010102", 0x1e03, "OperationDefinitionWeakReferenceVector", False, False),
    "OperationCategory"     : ("0530050a-0000-0000-060e-2b3401010102", 0x1e06, "OperationCategoryType", False, False),
    "NumberInputs"          : ("05300504-0000-0000-060e-2b3401010101", 0x1e07, "Int32", True, False),
    "Bypass"                : ("05300505-0000-0000-060e-2b3401010101", 0x1e08, "UInt32", False, False),
    "ParametersDefined"     : ("06010104-0302-0000-060e-2b3401010102", 0x1e09, "ParameterDefinitionWeakReferenceSet", False, False),
    }
),
"ParameterDefinition" : ("0d010101-0101-1d00-060e-2b3402060101" ,"DefinitionObject", True, {
    "Type"                  : ("06010104-0106-0000-060e-2b3401010102", 0x1f01, "TypeDefinitionWeakReference", True, False),
    "DisplayUnits"          : ("0530050b-0100-0000-060e-2b3401010102", 0x1f03, "String", False, False),
    }
),
"PluginDefinition" : ("0d010101-0101-1e00-060e-2b3402060101" ,"DefinitionObject", True, {
    "PluginCategory"        : ("05200901-0000-0000-060e-2b3401010102", 0x2203, "PluginCategoryType", True, False),
    "VersionNumber"         : ("03030301-0300-0000-060e-2b3401010102", 0x2204, "VersionType", True, False),
    "VersionString"         : ("03030301-0201-0000-060e-2b3401010102", 0x2205, "String", False, False),
    "Manufacturer"          : ("010a0101-0101-0000-060e-2b3401010102", 0x2206, "String", False, False),
    "ManufacturerInfo"      : ("06010104-020b-0000-060e-2b3401010102", 0x2207, "NetworkLocatorStrongReference", False, False),
    "ManufacturerID"        : ("010a0101-0300-0000-060e-2b3401010102", 0x2208, "AUID", False, False),
    "Platform"              : ("05200902-0000-0000-060e-2b3401010102", 0x2209, "AUID", False, False),
    "MinPlatformVersion"    : ("05200903-0000-0000-060e-2b3401010102", 0x220a, "VersionType", False, False),
    "MaxPlatformVersion"    : ("05200904-0000-0000-060e-2b3401010102", 0x220b, "VersionType", False, False),
    "Engine"                : ("05200905-0000-0000-060e-2b3401010102", 0x220c, "AUID", False, False),
    "MinEngineVersion"      : ("05200906-0000-0000-060e-2b3401010102", 0x220d, "VersionType", False, False),
    "MaxEngineVersion"      : ("05200907-0000-0000-060e-2b3401010102", 0x220e, "VersionType", False, False),
    "PluginAPI"             : ("05200908-0000-0000-060e-2b3401010102", 0x220f, "AUID", False, False),
    "MinPluginAPI"          : ("05200909-0000-0000-060e-2b3401010102", 0x2210, "VersionType", False, False),
    "MaxPluginAPI"          : ("0520090a-0000-0000-060e-2b3401010102", 0x2211, "VersionType", False, False),
    "SoftwareOnly"          : ("0520090b-0000-0000-060e-2b3401010102", 0x2212, "Boolean", False, False),
    "Accelerator"           : ("0520090c-0000-0000-060e-2b3401010102", 0x2213, "Boolean", False, False),
    "Locators"              : ("0520090d-0000-0000-060e-2b3401010102", 0x2214, "LocatorStrongReferenceVector", False, False),
    "Authentication"        : ("0520090e-0000-0000-060e-2b3401010102", 0x2215, "Boolean", False, False),
    "DefinitionObject"      : ("0520090f-0000-0000-060e-2b3401010102", 0x2216, "AUID", False, False),
    }
),
"CodecDefinition" : ("0d010101-0101-1f00-060e-2b3402060101" ,"DefinitionObject", True, {
    "FileDescriptorClass"   : ("06010104-0107-0000-060e-2b3401010102", 0x2301, "ClassDefinitionWeakReference", True, False),
    "DataDefinitions"       : ("06010104-0301-0000-060e-2b3401010102", 0x2302, "DataDefinitionWeakReferenceVector", True, False),
    }
),
"ContainerDefinition" : ("0d010101-0101-2000-060e-2b3402060101" ,"DefinitionObject", True, {
    "EssenceIsIdentified"   : ("03010201-0300-0000-060e-2b3401010101", 0x2401, "Boolean", False, False),
    }
),
"InterpolationDefinition" : ("0d010101-0101-2100-060e-2b3402060101" ,"DefinitionObject", True, {
    }
),
"Dictionary"     : ("0d010101-0101-2200-060e-2b3402060101" ,"InterchangeObject", True, {
    "OperationDefinitions"  : ("06010104-0503-0000-060e-2b3401010102", 0x2603, "OperationDefinitionStrongReferenceSet", False, False),
    "ParameterDefinitions"  : ("06010104-0504-0000-060e-2b3401010102", 0x2604, "ParameterDefinitionStrongReferenceSet", False, False),
    "DataDefinitions"       : ("06010104-0505-0000-060e-2b3401010102", 0x2605, "DataDefinitionStrongReferenceSet", False, False),
    "PluginDefinitions"     : ("06010104-0506-0000-060e-2b3401010102", 0x2606, "PluginDefinitionStrongReferenceSet", False, False),
    "CodecDefinitions"      : ("06010104-0507-0000-060e-2b3401010102", 0x2607, "CodecDefinitionStrongReferenceSet", False, False),
    "ContainerDefinitions"  : ("06010104-0508-0000-060e-2b3401010102", 0x2608, "ContainerDefinitionStrongReferenceSet", False, False),
    "InterpolationDefinitions": ("06010104-0509-0000-060e-2b3401010102", 0x2609, "InterpolationDefinitionStrongReferenceSet", False, False),
    "KLVDataDefinitions"    : ("06010104-050a-0000-060e-2b3401010107", 0x260a, "KLVDataDefinitionStrongReferenceSet", False, False),
    "TaggedValueDefinitions": ("06010104-050b-0000-060e-2b3401010107", 0x260b, "TaggedValueDefinitionStrongReferenceSet", False, False),
    }
),
"EssenceData"    : ("0d010101-0101-2300-060e-2b3402060101" ,"InterchangeObject", True, {
    "MobID"                 : ("06010106-0100-0000-060e-2b3401010102", 0x2701, "MobIDType", True, True),
    "Data"                  : ("04070200-0000-0000-060e-2b3401010102", 0x2702, "Stream", True, False),
    "SampleIndex"           : ("06010102-0100-0000-060e-2b3401010102", 0x2b01, "Stream", False, False),
    }
),
"EssenceDescriptor" : ("0d010101-0101-2400-060e-2b3402060101" ,"InterchangeObject", False, {
    "Locator"               : ("06010104-0603-0000-060e-2b3401010102", 0x2f01, "LocatorStrongReferenceVector", False, False),
    }
),
"FileDescriptor" : ("0d010101-0101-2500-060e-2b3402060101" ,"EssenceDescriptor", False, {
    "SampleRate"            : ("04060101-0000-0000-060e-2b3401010101", 0x3001, "Rational", True, False),
    "Length"                : ("04060102-0000-0000-060e-2b3401010101", 0x3002, "LengthType", True, False),
    "ContainerFormat"       : ("06010104-0102-0000-060e-2b3401010102", 0x3004, "ContainerDefinitionWeakReference", False, False),
    "CodecDefinition"       : ("06010104-0103-0000-060e-2b3401010102", 0x3005, "CodecDefinitionWeakReference", False, False),
    "LinkedSlotID"          : ("06010103-0500-0000-060e-2b3401010105", 0x3006, "UInt32", False, False),
    }
),
"AIFCDescriptor" : ("0d010101-0101-2600-060e-2b3402060101" ,"FileDescriptor", True, {
    "Summary"               : ("03030302-0200-0000-060e-2b3401010102", 0x3101, "DataValue", True, False),
    }
),
"DigitalImageDescriptor" : ("0d010101-0101-2700-060e-2b3402060101" ,"FileDescriptor", False, {
    "Compression"           : ("04010601-0000-0000-060e-2b3401010102", 0x3201, "AUID", False, False),
    "StoredHeight"          : ("04010502-0100-0000-060e-2b3401010101", 0x3202, "UInt32", True, False),
    "StoredWidth"           : ("04010502-0200-0000-060e-2b3401010101", 0x3203, "UInt32", True, False),
    "SampledHeight"         : ("04010501-0700-0000-060e-2b3401010101", 0x3204, "UInt32", False, False),
    "SampledWidth"          : ("04010501-0800-0000-060e-2b3401010101", 0x3205, "UInt32", False, False),
    "SampledXOffset"        : ("04010501-0900-0000-060e-2b3401010101", 0x3206, "Int32", False, False),
    "SampledYOffset"        : ("04010501-0a00-0000-060e-2b3401010101", 0x3207, "Int32", False, False),
    "DisplayHeight"         : ("04010501-0b00-0000-060e-2b3401010101", 0x3208, "UInt32", False, False),
    "DisplayWidth"          : ("04010501-0c00-0000-060e-2b3401010101", 0x3209, "UInt32", False, False),
    "DisplayXOffset"        : ("04010501-0d00-0000-060e-2b3401010101", 0x320a, "Int32", False, False),
    "DisplayYOffset"        : ("04010501-0e00-0000-060e-2b3401010101", 0x320b, "Int32", False, False),
    "FrameLayout"           : ("04010301-0400-0000-060e-2b3401010101", 0x320c, "LayoutType", True, False),
    "VideoLineMap"          : ("04010302-0500-0000-060e-2b3401010102", 0x320d, "Int32Array", True, False),
    "ImageAspectRatio"      : ("04010101-0100-0000-060e-2b3401010101", 0x320e, "Rational", True, False),
    "AlphaTransparency"     : ("05200102-0000-0000-060e-2b3401010102", 0x320f, "AlphaTransparencyType", False, False),
    "TransferCharacteristic": ("04010201-0101-0200-060e-2b3401010102", 0x3210, "TransferCharacteristicType", False, False),
    "ColorPrimaries"        : ("04010201-0106-0100-060e-2b3401010109", 0x3219, "ColorPrimariesType", False, False),
    "CodingEquations"       : ("04010201-0103-0100-060e-2b3401010102", 0x321a, "CodingEquationsType", False, False),
    "ImageAlignmentFactor"  : ("04180101-0000-0000-060e-2b3401010102", 0x3211, "UInt32", False, False),
    "FieldDominance"        : ("04010301-0600-0000-060e-2b3401010102", 0x3212, "FieldNumber", False, False),
    "FieldStartOffset"      : ("04180102-0000-0000-060e-2b3401010102", 0x3213, "UInt32", False, False),
    "FieldEndOffset"        : ("04180103-0000-0000-060e-2b3401010102", 0x3214, "UInt32", False, False),
    "SignalStandard"        : ("04050113-0000-0000-060e-2b3401010105", 0x3215, "SignalStandardType", False, False),
    "StoredF2Offset"        : ("04010302-0800-0000-060e-2b3401010105", 0x3216, "Int32", False, False),
    "DisplayF2Offset"       : ("04010302-0700-0000-060e-2b3401010105", 0x3217, "Int32", False, False),
    "ActiveFormatDescriptor": ("04010302-0900-0000-060e-2b3401010105", 0x3218, "UInt8", False, False),
    }
),
"CDCIDescriptor" : ("0d010101-0101-2800-060e-2b3402060101" ,"DigitalImageDescriptor", True, {
    "ComponentWidth"        : ("04010503-0a00-0000-060e-2b3401010102", 0x3301, "UInt32", True, False),
    "HorizontalSubsampling" : ("04010501-0500-0000-060e-2b3401010101", 0x3302, "UInt32", True, False),
    "ColorSiting"           : ("04010501-0600-0000-060e-2b3401010101", 0x3303, "ColorSitingType", False, False),
    "BlackReferenceLevel"   : ("04010503-0300-0000-060e-2b3401010101", 0x3304, "UInt32", False, False),
    "WhiteReferenceLevel"   : ("04010503-0400-0000-060e-2b3401010101", 0x3305, "UInt32", False, False),
    "ColorRange"            : ("04010503-0500-0000-060e-2b3401010102", 0x3306, "UInt32", False, False),
    "PaddingBits"           : ("04180104-0000-0000-060e-2b3401010102", 0x3307, "Int16", False, False),
    "VerticalSubsampling"   : ("04010501-1000-0000-060e-2b3401010102", 0x3308, "UInt32", False, False),
    "AlphaSamplingWidth"    : ("04010503-0700-0000-060e-2b3401010102", 0x3309, "UInt32", False, False),
    "ReversedByteOrder"     : ("03010201-0a00-0000-060e-2b3401010105", 0x330b, "Boolean", False, False),
    }
),
"RGBADescriptor" : ("0d010101-0101-2900-060e-2b3402060101" ,"DigitalImageDescriptor", True, {
    "PixelLayout"           : ("04010503-0600-0000-060e-2b3401010102", 0x3401, "RGBALayout", True, False),
    "Palette"               : ("04010503-0800-0000-060e-2b3401010102", 0x3403, "DataValue", False, False),
    "PaletteLayout"         : ("04010503-0900-0000-060e-2b3401010102", 0x3404, "RGBALayout", False, False),
    "ScanningDirection"     : ("04010404-0100-0000-060e-2b3401010105", 0x3405, "ScanningDirectionType", False, False),
    "ComponentMaxRef"       : ("04010503-0b00-0000-060e-2b3401010105", 0x3406, "UInt32", False, False),
    "ComponentMinRef"       : ("04010503-0c00-0000-060e-2b3401010105", 0x3407, "UInt32", False, False),
    "AlphaMaxRef"           : ("04010503-0d00-0000-060e-2b3401010105", 0x3408, "UInt32", False, False),
    "AlphaMinRef"           : ("04010503-0e00-0000-060e-2b3401010105", 0x3409, "UInt32", False, False),
    }
),
"HTMLDescriptor" : ("0d010101-0101-2a00-060e-2b3402060101" ,"FileDescriptor", True, {
    }
),
"TIFFDescriptor" : ("0d010101-0101-2b00-060e-2b3402060101" ,"FileDescriptor", True, {
    "IsUniform"             : ("05020103-0101-0000-060e-2b3401010102", 0x3701, "Boolean", True, False),
    "IsContiguous"          : ("06080201-0000-0000-060e-2b3401010101", 0x3702, "Boolean", True, False),
    "LeadingLines"          : ("04010302-0300-0000-060e-2b3401010101", 0x3703, "Int32", False, False),
    "TrailingLines"         : ("04010302-0400-0000-060e-2b3401010101", 0x3704, "Int32", False, False),
    "JPEGTableID"           : ("05020103-0102-0000-060e-2b3401010102", 0x3705, "JPEGTableIDType", False, False),
    "Summary"               : ("03030302-0300-0000-060e-2b3401010102", 0x3706, "DataValue", True, False),
    }
),
"WAVEDescriptor" : ("0d010101-0101-2c00-060e-2b3402060101" ,"FileDescriptor", True, {
    "Summary"               : ("03030302-0100-0000-060e-2b3401010102", 0x3801, "DataValue", True, False),
    }
),
"FilmDescriptor" : ("0d010101-0101-2d00-060e-2b3402060101" ,"EssenceDescriptor", True, {
    "FilmFormat"            : ("04100103-0108-0000-060e-2b3401010102", 0x3901, "FilmType", False, False),
    "FrameRate"             : ("04010802-0300-0000-060e-2b3401010102", 0x3902, "UInt32", False, False),
    "PerforationsPerFrame"  : ("04100103-0103-0000-060e-2b3401010102", 0x3903, "UInt8", False, False),
    "FilmAspectRatio"       : ("04100103-0203-0000-060e-2b3401010102", 0x3904, "Rational", False, False),
    "Manufacturer"          : ("04100103-0106-0100-060e-2b3401010102", 0x3905, "String", False, False),
    "Model"                 : ("04100103-0105-0100-060e-2b3401010102", 0x3906, "String", False, False),
    "FilmGaugeFormat"       : ("04100103-0104-0100-060e-2b3401010102", 0x3907, "String", False, False),
    "FilmBatchNumber"       : ("04100103-0107-0100-060e-2b3401010102", 0x3908, "String", False, False),
    }
),
"TapeDescriptor" : ("0d010101-0101-2e00-060e-2b3402060101" ,"EssenceDescriptor", True, {
    "FormFactor"            : ("04100101-0101-0000-060e-2b3401010102", 0x3a01, "TapeCaseType", False, False),
    "VideoSignal"           : ("04010401-0100-0000-060e-2b3401010102", 0x3a02, "VideoSignalType", False, False),
    "TapeFormat"            : ("0d010101-0101-0100-060e-2b3401010102", 0x3a03, "TapeFormatType", False, False),
    "Length"                : ("04100101-0300-0000-060e-2b3401010102", 0x3a04, "UInt32", False, False),
    "ManufacturerID"        : ("04100101-0401-0000-060e-2b3401010102", 0x3a05, "String", False, False),
    "Model"                 : ("04100101-0201-0000-060e-2b3401010102", 0x3a06, "String", False, False),
    "TapeBatchNumber"       : ("04100101-0601-0000-060e-2b3401010102", 0x3a07, "String", False, False),
    "TapeStock"             : ("04100101-0501-0000-060e-2b3401010102", 0x3a08, "String", False, False),
    }
),
"Header"         : ("0d010101-0101-2f00-060e-2b3402060101" ,"InterchangeObject", True, {
    "ByteOrder"             : ("03010201-0200-0000-060e-2b3401010101", 0x3b01, "Int16", True, False),
    "LastModified"          : ("07020110-0204-0000-060e-2b3401010102", 0x3b02, "TimeStamp", True, False),
    "Content"               : ("06010104-0201-0000-060e-2b3401010102", 0x3b03, "ContentStorageStrongReference", True, False),
    "Dictionary"            : ("06010104-0202-0000-060e-2b3401010102", 0x3b04, "DictionaryStrongReference", True, False),
    "Version"               : ("03010201-0500-0000-060e-2b3401010102", 0x3b05, "VersionType", True, False),
    "IdentificationList"    : ("06010104-0604-0000-060e-2b3401010102", 0x3b06, "IdentificationStrongReferenceVector", True, False),
    "ObjectModelVersion"    : ("03010201-0400-0000-060e-2b3401010102", 0x3b07, "UInt32", False, False),
    "OperationalPattern"    : ("01020203-0000-0000-060e-2b3401010105", 0x3b09, "AUID", False, False),
    "EssenceContainers"     : ("01020210-0201-0000-060e-2b3401010105", 0x3b0a, "AUIDSet", False, False),
    "DescriptiveSchemes"    : ("01020210-0202-0000-060e-2b3401010105", 0x3b0b, "AUIDSet", False, False),
    }
),
"Identification" : ("0d010101-0101-3000-060e-2b3402060101" ,"InterchangeObject", True, {
    "CompanyName"           : ("05200701-0201-0000-060e-2b3401010102", 0x3c01, "String", True, False),
    "ProductName"           : ("05200701-0301-0000-060e-2b3401010102", 0x3c02, "String", True, False),
    "ProductVersion"        : ("05200701-0400-0000-060e-2b3401010102", 0x3c03, "ProductVersion", False, False),
    "ProductVersionString"  : ("05200701-0501-0000-060e-2b3401010102", 0x3c04, "String", True, False),
    "ProductID"             : ("05200701-0700-0000-060e-2b3401010102", 0x3c05, "AUID", True, False),
    "Date"                  : ("07020110-0203-0000-060e-2b3401010102", 0x3c06, "TimeStamp", True, False),
    "ToolkitVersion"        : ("05200701-0a00-0000-060e-2b3401010102", 0x3c07, "ProductVersion", False, False),
    "Platform"              : ("05200701-0601-0000-060e-2b3401010102", 0x3c08, "String", False, False),
    "GenerationAUID"        : ("05200701-0100-0000-060e-2b3401010102", 0x3c09, "AUID", True, False),
    }
),
"Locator"        : ("0d010101-0101-3100-060e-2b3402060101" ,"InterchangeObject", False, {
    }
),
"NetworkLocator" : ("0d010101-0101-3200-060e-2b3402060101" ,"Locator", True, {
    "URLString"             : ("01020101-0100-0000-060e-2b3401010101", 0x4001, "String", True, False),
    }
),
"TextLocator"    : ("0d010101-0101-3300-060e-2b3402060101" ,"Locator", True, {
    "Name"                  : ("01040102-0100-0000-060e-2b3401010102", 0x4101, "String", True, False),
    }
),
"Mob"            : ("0d010101-0101-3400-060e-2b3402060101" ,"InterchangeObject", False, {
    "MobID"                 : ("01011510-0000-0000-060e-2b3401010101", 0x4401, "MobIDType", True, True),
    "Name"                  : ("01030302-0100-0000-060e-2b3401010101", 0x4402, "String", False, False),
    "Slots"                 : ("06010104-0605-0000-060e-2b3401010102", 0x4403, "MobSlotStrongReferenceVector", True, False),
    "LastModified"          : ("07020110-0205-0000-060e-2b3401010102", 0x4404, "TimeStamp", True, False),
    "CreationTime"          : ("07020110-0103-0000-060e-2b3401010102", 0x4405, "TimeStamp", True, False),
    "UserComments"          : ("03020102-0c00-0000-060e-2b3401010102", 0x4406, "TaggedValueStrongReferenceVector", False, False),
    "KLVData"               : ("03010210-0300-0000-060e-2b3401010102", 0x4407, "KLVDataStrongReferenceVector", False, False),
    "Attributes"            : ("03010210-0700-0000-060e-2b3401010107", 0x4409, "TaggedValueStrongReferenceVector", False, False),
    "UsageCode"             : ("05010108-0000-0000-060e-2b3401010107", 0x4408, "UsageType", False, False),
    }
),
"CompositionMob" : ("0d010101-0101-3500-060e-2b3402060101" ,"Mob", True, {
    "DefaultFadeLength"     : ("07020201-0105-0100-060e-2b3401010102", 0x4501, "LengthType", False, False),
    "DefFadeType"           : ("05300201-0000-0000-060e-2b3401010101", 0x4502, "FadeType", False, False),
    "DefFadeEditUnit"       : ("05300403-0000-0000-060e-2b3401010102", 0x4503, "Rational", False, False),
    "Rendering"             : ("06010104-010a-0000-060e-2b3401010108", 0x4504, "MobIDType", False, False),
    }
),
"MasterMob"      : ("0d010101-0101-3600-060e-2b3402060101" ,"Mob", True, {
    }
),
"SourceMob"      : ("0d010101-0101-3700-060e-2b3402060101" ,"Mob", True, {
    "EssenceDescription"    : ("06010104-0203-0000-060e-2b3401010102", 0x4701, "EssenceDescriptorStrongReference", True, False),
    }
),
"MobSlot"        : ("0d010101-0101-3800-060e-2b3402060101" ,"InterchangeObject", False, {
    "SlotID"                : ("01070101-0000-0000-060e-2b3401010102", 0x4801, "UInt32", True, False),
    "SlotName"              : ("01070102-0100-0000-060e-2b3401010102", 0x4802, "String", False, False),
    "Segment"               : ("06010104-0204-0000-060e-2b3401010102", 0x4803, "SegmentStrongReference", True, False),
    "PhysicalTrackNumber"   : ("01040103-0000-0000-060e-2b3401010102", 0x4804, "UInt32", False, False),
    }
),
"EventMobSlot"   : ("0d010101-0101-3900-060e-2b3402060101" ,"MobSlot", True, {
    "EditRate"              : ("05300402-0000-0000-060e-2b3401010102", 0x4901, "Rational", True, False),
    "EventSlotOrigin"       : ("07020103-010b-0000-060e-2b3401010105", 0x4902, "PositionType", False, False),
    }
),
"StaticMobSlot"  : ("0d010101-0101-3a00-060e-2b3402060101" ,"MobSlot", True, {
    }
),
"TimelineMobSlot" : ("0d010101-0101-3b00-060e-2b3402060101" ,"MobSlot", True, {
    "EditRate"              : ("05300405-0000-0000-060e-2b3401010102", 0x4b01, "Rational", True, False),
    "Origin"                : ("07020103-0103-0000-060e-2b3401010102", 0x4b02, "PositionType", True, False),
    "MarkIn"                : ("07020103-010c-0000-060e-2b3401010107", 0x4b03, "PositionType", False, False),
    "MarkOut"               : ("07020103-0203-0000-060e-2b3401010107", 0x4b04, "PositionType", False, False),
    "UserPos"               : ("07020103-010d-0000-060e-2b3401010107", 0x4b05, "PositionType", False, False),
    }
),
"Parameter"      : ("0d010101-0101-3c00-060e-2b3402060101" ,"InterchangeObject", False, {
    "Definition"            : ("06010104-0104-0000-060e-2b3401010102", 0x4c01, "AUID", True, False),
    }
),
"ConstantValue"  : ("0d010101-0101-3d00-060e-2b3402060101" ,"Parameter", True, {
    "Value"                 : ("05300507-0000-0000-060e-2b3401010102", 0x4d01, "Indirect", True, False),
    }
),
"VaryingValue"   : ("0d010101-0101-3e00-060e-2b3402060101" ,"Parameter", True, {
    "Interpolation"         : ("06010104-0105-0000-060e-2b3401010102", 0x4e01, "InterpolationDefinitionWeakReference", True, False),
    "PointList"             : ("06010104-0606-0000-060e-2b3401010102", 0x4e02, "ControlPointStrongReferenceVector", True, False),
    }
),
"TaggedValue"    : ("0d010101-0101-3f00-060e-2b3402060101" ,"InterchangeObject", True, {
    "Name"                  : ("03020102-0901-0000-060e-2b3401010102", 0x5001, "String", True, False),
    "Value"                 : ("03020102-0a01-0000-060e-2b3401010102", 0x5003, "Indirect", True, False),
    }
),
"KLVData"        : ("0d010101-0101-4000-060e-2b3402060101" ,"InterchangeObject", True, {
    "Value"                 : ("03010210-0200-0000-060e-2b3401010102", 0x5101, "Opaque", True, False),
    }
),
"DescriptiveMarker" : ("0d010101-0101-4100-060e-2b3402060101" ,"CommentMarker", True, {
    "DescribedSlots"        : ("01070105-0000-0000-060e-2b3401010104", 0x6102, "UInt32Set", False, False),
    "Description"           : ("06010104-020c-0000-060e-2b3401010105", 0x6101, "DescriptiveFrameworkStrongReference", False, False),
    }
),
"SoundDescriptor" : ("0d010101-0101-4200-060e-2b3402060101" ,"FileDescriptor", True, {
    "AudioSamplingRate"     : ("04020301-0101-0000-060e-2b3401010105", 0x3d03, "Rational", True, False),
    "Locked"                : ("04020301-0400-0000-060e-2b3401010104", 0x3d02, "Boolean", False, False),
    "AudioRefLevel"         : ("04020101-0300-0000-060e-2b3401010101", 0x3d04, "Int8", False, False),
    "ElectroSpatial"        : ("04020101-0100-0000-060e-2b3401010101", 0x3d05, "ElectroSpatialFormulation", False, False),
    "Channels"              : ("04020101-0400-0000-060e-2b3401010105", 0x3d07, "UInt32", True, False),
    "QuantizationBits"      : ("04020303-0400-0000-060e-2b3401010104", 0x3d01, "UInt32", True, False),
    "DialNorm"              : ("04020701-0000-0000-060e-2b3401010105", 0x3d0c, "Int8", False, False),
    "Compression"           : ("04020402-0000-0000-060e-2b3401010102", 0x3d06, "AUID", False, False),
    }
),
"DataEssenceDescriptor" : ("0d010101-0101-4300-060e-2b3402060101" ,"FileDescriptor", True, {
    "DataEssenceCoding"     : ("04030302-0000-0000-060e-2b3401010103", 0x3e01, "AUID", False, False),
    }
),
"MultipleDescriptor" : ("0d010101-0101-4400-060e-2b3402060101" ,"FileDescriptor", True, {
    "FileDescriptors"       : ("06010104-060b-0000-060e-2b3401010104", 0x3f01, "FileDescriptorStrongReferenceVector", True, False),
    }
),
"DescriptiveClip" : ("0d010101-0101-4500-060e-2b3402060101" ,"SourceClip", True, {
    "DescribedSlotIDs"      : ("01070106-0000-0000-060e-2b3401010105", 0x6103, "UInt32Set", False, False),
    }
),
"PCMDescriptor"  : ("0d010101-0101-4800-060e-2b3402060101" ,"SoundDescriptor", True, {
    "BlockAlign"            : ("04020302-0100-0000-060e-2b3401010105", 0x3d0a, "UInt16", True, False),
    "SequenceOffset"        : ("04020302-0200-0000-060e-2b3401010105", 0x3d0b, "UInt8", False, False),
    "AverageBPS"            : ("04020303-0500-0000-060e-2b3401010105", 0x3d09, "UInt32", True, False),
    "ChannelAssignment"     : ("04020101-0500-0000-060e-2b3401010107", 0x3d32, "AUID", False, False),
    "PeakEnvelopeVersion"   : ("04020301-0600-0000-060e-2b3401010108", 0x3d29, "UInt32", False, False),
    "PeakEnvelopeFormat"    : ("04020301-0700-0000-060e-2b3401010108", 0x3d2a, "UInt32", False, False),
    "PointsPerPeakValue"    : ("04020301-0800-0000-060e-2b3401010108", 0x3d2b, "UInt32", False, False),
    "PeakEnvelopeBlockSize" : ("04020301-0900-0000-060e-2b3401010108", 0x3d2c, "UInt32", False, False),
    "PeakChannels"          : ("04020301-0a00-0000-060e-2b3401010108", 0x3d2d, "UInt32", False, False),
    "PeakFrames"            : ("04020301-0b00-0000-060e-2b3401010108", 0x3d2e, "UInt32", False, False),
    "PeakOfPeaksPosition"   : ("04020301-0c00-0000-060e-2b3401010108", 0x3d2f, "PositionType", False, False),
    "PeakEnvelopeTimestamp" : ("04020301-0d00-0000-060e-2b3401010108", 0x3d30, "TimeStamp", False, False),
    "PeakEnvelopeData"      : ("04020301-0e00-0000-060e-2b3401010108", 0x3d31, "Stream", False, False),
    }
),
"AES3PCMDescriptor" : ("0d010101-0101-4700-060e-2b3402060101" ,"PCMDescriptor", True, {
    "Emphasis"              : ("04020501-0600-0000-060e-2b3401010105", 0x3d0d, "EmphasisType", False, False),
    "BlockStartOffset"      : ("04020302-0300-0000-060e-2b3401010105", 0x3d0f, "UInt16", False, False),
    "AuxBitsMode"           : ("04020501-0100-0000-060e-2b3401010105", 0x3d08, "AuxBitsModeType", False, False),
    "ChannelStatusMode"     : ("04020501-0200-0000-060e-2b3401010105", 0x3d10, "ChannelStatusModeArray", False, False),
    "FixedChannelStatusData": ("04020501-0300-0000-060e-2b3401010105", 0x3d11, "UInt8Array", False, False),
    "UserDataMode"          : ("04020501-0400-0000-060e-2b3401010105", 0x3d12, "UserDataModeArray", False, False),
    "FixedUserData"         : ("04020501-0500-0000-060e-2b3401010105", 0x3d13, "UInt8Array", False, False),
    }
),
"PhysicalDescriptor" : ("0d010101-0101-4900-060e-2b3402060101" ,"EssenceDescriptor", False, {
    }
),
"ImportDescriptor" : ("0d010101-0101-4a00-060e-2b3402060101" ,"PhysicalDescriptor", True, {
    }
),
"RecordingDescriptor" : ("0d010101-0101-4b00-060e-2b3402060101" ,"PhysicalDescriptor", True, {
    }
),
"TaggedValueDefinition" : ("0d010101-0101-4c00-060e-2b3402060101" ,"DefinitionObject", True, {
    }
),
"KLVDataDefinition" : ("0d010101-0101-4d00-060e-2b3402060101" ,"DefinitionObject", True, {
    "KLVDataType"           : ("06010104-0109-0000-060e-2b3401010107", 0x4d12, "TypeDefinitionWeakReference", False, False),
    }
),
"AuxiliaryDescriptor" : ("0d010101-0101-4e00-060e-2b3402060101" ,"PhysicalDescriptor", True, {
    "MimeType"              : ("04090201-0000-0000-060e-2b3401010107", 0x4e11, "String", True, False),
    "CharSet"               : ("04090300-0000-0000-060e-2b3401010108", 0x4e12, "String", False, False),
    }
),
"RIFFChunk"      : ("0d010101-0101-4f00-060e-2b3402060101" ,"InterchangeObject", True, {
    "ChunkID"               : ("04060802-0000-0000-060e-2b3401010108", 0x4f01, "UInt32", True, False),
    "ChunkLength"           : ("04060903-0000-0000-060e-2b3401010108", 0x4f02, "UInt32", True, False),
    "ChunkData"             : ("04070400-0000-0000-060e-2b3401010108", 0x4f03, "Stream", True, False),
    }
),
"BWFImportDescriptor" : ("0d010101-0101-5000-060e-2b3402060101" ,"ImportDescriptor", True, {
    "QltyFileSecurityReport": ("04020302-0500-0000-060e-2b3401010105", 0x3d15, "UInt32", False, False),
    "QltyFileSecurityWave"  : ("04020302-0600-0000-060e-2b3401010105", 0x3d16, "UInt32", False, False),
    "BextCodingHistory"     : ("04020502-0101-0000-060e-2b3401010105", 0x3d21, "String", False, False),
    "QltyBasicData"         : ("04020502-0201-0000-060e-2b3401010105", 0x3d22, "String", False, False),
    "QltyStartOfModulation" : ("04020502-0301-0000-060e-2b3401010105", 0x3d23, "String", False, False),
    "QltyQualityEvent"      : ("04020502-0401-0000-060e-2b3401010105", 0x3d24, "String", False, False),
    "QltyEndOfModulation"   : ("04020502-0501-0000-060e-2b3401010105", 0x3d25, "String", False, False),
    "QltyQualityParameter"  : ("04020502-0601-0000-060e-2b3401010105", 0x3d26, "String", False, False),
    "QltyOperatorComment"   : ("04020502-0701-0000-060e-2b3401010105", 0x3d27, "String", False, False),
    "QltyCueSheet"          : ("04020502-0801-0000-060e-2b3401010105", 0x3d28, "String", False, False),
    "UnknownBWFChunks"      : ("06010104-060f-0000-060e-2b3401010108", 0x3d33, "RIFFChunkStrongReferenceVector", False, False),
    }
),
"MPEGVideoDescriptor" : ("0d010101-0101-5100-060e-2b3402060101" ,"CDCIDescriptor", True, {
    "SingleSequence"        : ("04010602-0102-0000-060e-2b3401010105", 0x0000, "Boolean", False, False),
    "ConstantBPictureCount" : ("04010602-0103-0000-060e-2b3401010105", 0x0000, "Boolean", False, False),
    "CodedContentScanning"  : ("04010602-0104-0000-060e-2b3401010105", 0x0000, "ContentScanningType", False, False),
    "LowDelay"              : ("04010602-0105-0000-060e-2b3401010105", 0x0000, "Boolean", False, False),
    "ClosedGOP"             : ("04010602-0106-0000-060e-2b3401010105", 0x0000, "Boolean", False, False),
    "IdenticalGOP"          : ("04010602-0107-0000-060e-2b3401010105", 0x0000, "Boolean", False, False),
    "MaxGOP"                : ("04010602-0108-0000-060e-2b3401010105", 0x0000, "UInt16", False, False),
    "MaxBPictureCount"      : ("04010602-0109-0000-060e-2b3401010105", 0x0000, "UInt16", False, False),
    "BitRate"               : ("04010602-010b-0000-060e-2b3401010105", 0x0000, "UInt32", False, False),
    "ProfileAndLevel"       : ("04010602-010a-0000-060e-2b3401010105", 0x0000, "UInt8", False, False),
    }
),
"MetaDefinition" : ("0d010101-0224-0000-060e-2b3402060101" ,"Root", False, {
    "Identification"        : ("06010107-1300-0000-060e-2b3401010102", 0x0005, "AUID", True, True),
    "Name"                  : ("03020401-0201-0000-060e-2b3401010102", 0x0006, "String", True, False),
    "Description"           : ("06010107-1401-0000-060e-2b3401010102", 0x0007, "String", False, False),
    }
),
"ClassDefinition" : ("0d010101-0201-0000-060e-2b3402060101" ,"MetaDefinition", True, {
    "ParentClass"           : ("06010107-0100-0000-060e-2b3401010102", 0x0008, "ClassDefinitionWeakReference", True, False),
    "Properties"            : ("06010107-0200-0000-060e-2b3401010102", 0x0009, "PropertyDefinitionStrongReferenceSet", False, False),
    "IsConcrete"            : ("06010107-0300-0000-060e-2b3401010102", 0x000a, "Boolean", True, False),
    }
),
"PropertyDefinition" : ("0d010101-0202-0000-060e-2b3402060101" ,"MetaDefinition", True, {
    "Type"                  : ("06010107-0400-0000-060e-2b3401010102", 0x000b, "AUID", True, False),
    "IsOptional"            : ("03010202-0100-0000-060e-2b3401010102", 0x000c, "Boolean", True, False),
    "LocalIdentification"   : ("06010107-0500-0000-060e-2b3401010102", 0x000d, "UInt16", True, False),
    "IsUniqueIdentifier"    : ("06010107-0600-0000-060e-2b3401010102", 0x000e, "Boolean", False, False),
    }
),
"TypeDefinition" : ("0d010101-0203-0000-060e-2b3402060101" ,"MetaDefinition", False, {
    }
),
"TypeDefinitionInteger" : ("0d010101-0204-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "Size"                  : ("03010203-0100-0000-060e-2b3401010102", 0x000f, "UInt8", True, False),
    "IsSigned"              : ("03010203-0200-0000-060e-2b3401010102", 0x0010, "Boolean", True, False),
    }
),
"TypeDefinitionStrongObjectReference" : ("0d010101-0205-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ReferencedType"        : ("06010107-0900-0000-060e-2b3401010102", 0x0011, "ClassDefinitionWeakReference", True, False),
    }
),
"TypeDefinitionWeakObjectReference" : ("0d010101-0206-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ReferencedType"        : ("06010107-0a00-0000-060e-2b3401010102", 0x0012, "ClassDefinitionWeakReference", True, False),
    "TargetSet"             : ("03010203-0b00-0000-060e-2b3401010102", 0x0013, "AUIDArray", True, False),
    }
),
"TypeDefinitionEnumeration" : ("0d010101-0207-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ElementType"           : ("06010107-0b00-0000-060e-2b3401010102", 0x0014, "TypeDefinitionWeakReference", True, False),
    "ElementNames"          : ("03010203-0400-0000-060e-2b3401010102", 0x0015, "StringArray", True, False),
    "ElementValues"         : ("03010203-0500-0000-060e-2b3401010102", 0x0016, "Int64Array", True, False),
    }
),
"TypeDefinitionFixedArray" : ("0d010101-0208-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ElementType"           : ("06010107-0c00-0000-060e-2b3401010102", 0x0017, "TypeDefinitionWeakReference", True, False),
    "ElementCount"          : ("03010203-0300-0000-060e-2b3401010102", 0x0018, "UInt32", True, False),
    }
),
"TypeDefinitionVariableArray" : ("0d010101-0209-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ElementType"           : ("06010107-0d00-0000-060e-2b3401010102", 0x0019, "TypeDefinitionWeakReference", True, False),
    }
),
"TypeDefinitionSet" : ("0d010101-020a-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ElementType"           : ("06010107-0e00-0000-060e-2b3401010102", 0x001a, "TypeDefinitionWeakReference", True, False),
    }
),
"TypeDefinitionString" : ("0d010101-020b-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ElementType"           : ("06010107-0f00-0000-060e-2b3401010102", 0x001b, "TypeDefinitionWeakReference", True, False),
    }
),
"TypeDefinitionStream" : ("0d010101-020c-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    }
),
"TypeDefinitionRecord" : ("0d010101-020d-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "MemberTypes"           : ("06010107-1100-0000-060e-2b3401010102", 0x001c, "TypeDefinitionWeakReferenceVector", True, False),
    "MemberNames"           : ("03010203-0600-0000-060e-2b3401010102", 0x001d, "StringArray", True, False),
    }
),
"TypeDefinitionRename" : ("0d010101-020e-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "RenamedType"           : ("06010107-1200-0000-060e-2b3401010102", 0x001e, "TypeDefinitionWeakReference", True, False),
    }
),
"TypeDefinitionExtendibleEnumeration" : ("0d010101-0220-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    "ElementNames"          : ("03010203-0700-0000-060e-2b3401010102", 0x001f, "StringArray", True, False),
    "ElementValues"         : ("03010203-0800-0000-060e-2b3401010102", 0x0020, "AUIDArray", True, False),
    }
),
"TypeDefinitionIndirect" : ("0d010101-0221-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    }
),
"TypeDefinitionOpaque" : ("0d010101-0222-0000-060e-2b3402060101" ,"TypeDefinitionIndirect", True, {
    }
),
"TypeDefinitionCharacter" : ("0d010101-0223-0000-060e-2b3402060101" ,"TypeDefinition", True, {
    }
),
"MetaDictionary" : ("0d010101-0225-0000-060e-2b3402060101" ,"Root", True, {
    "ClassDefinitions"      : ("06010107-0700-0000-060e-2b3401010102", 0x0003, "ClassDefinitionStrongReferenceSet", False, False),
    "TypeDefinitions"       : ("06010107-0800-0000-060e-2b3401010102", 0x0004, "TypeDefinitionStrongReferenceSet", False, False),
    }
),
"DescriptiveObject" : ("0d010400-0000-0000-060e-2b3402060101" ,"InterchangeObject", False, {
    }
),
"DescriptiveFramework" : ("0d010401-0000-0000-060e-2b3402060101" ,"InterchangeObject", False, {
    }
)}

aliases = {
"ClassDef"               : "ClassDefinition",
"CodecDef"               : "CodecDefinition",
"DataDef"                : "DataDefinition",
"DefObject"              : "DefinitionObject",
"Edgecode"               : "EdgeCode",
"OperationDef"           : "OperationDefinition",
"Object"                 : "InterchangeObject",
"ParameterDef"           : "ParameterDefinition",
"InterpolationDef"       : "InterpolationDefinition",
"PropertyDef"            : "PropertyDefinition",
"TypeDef"                : "TypeDefinition",
"TypeDefCharacter"       : "TypeDefinitionCharacter",
"TypeDefEnum"            : "TypeDefinitionEnumeration",
"TypeDefExtEnum"         : "TypeDefinitionExtendibleEnumeration",
"TypeDefFixedArray"      : "TypeDefinitionFixedArray",
"TypeDefInt"             : "TypeDefinitionInteger",
"TypeDefRecord"          : "TypeDefinitionRecord",
"TypeDefRename"          : "TypeDefinitionRename",
"TypeDefSet"             : "TypeDefinitionSet",
"TypeDefStream"          : "TypeDefinitionStream",
"TypeDefString"          : "TypeDefinitionString",
"TypeDefIndirect"        : "TypeDefinitionIndirect",
"TypeDefOpaque"          : "TypeDefinitionOpaque",
"TypeDefStrongObjRef"    : "TypeDefinitionStrongObjectReference",
"TypeDefVariableArray"   : "TypeDefinitionVariableArray",
"TypeDefWeakObjRef"      : "TypeDefinitionWeakObjectReference",
"ContainerDef"           : "ContainerDefinition",
"PluginDef"              : "PluginDefinition",
}
