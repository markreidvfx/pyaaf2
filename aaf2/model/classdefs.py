classdefs = {
"InterchangeObject"     : ("0d010101-0101-0100-060e-2b3402060101", None, False, {
    "ObjClass"              : ("06010104-0101-0000-060e-2b3401010102", 0x0101, "ClassDefinitionWeakReference", False, False),
    "Generation"            : ("05200701-0800-0000-060e-2b3401010102", 0x0102, "AUID", True, False),
    }
),
"Component"             : ("0d010101-0101-0200-060e-2b3402060101", "InterchangeObject", False, {
    "DataDefinition"        : ("04070100-0000-0000-060e-2b3401010102", 0x0201, "DataDefinitionWeakReference", False, False),
    "Length"                : ("07020201-0103-0000-060e-2b3401010102", 0x0202, "aafLengthType", True, False),
    "KLVData"               : ("03010210-0400-0000-060e-2b3401010102", 0x0203, "kAAFTypeID_KLVDataStrongReferenceVector", True, False),
    "UserComments"          : ("03020102-1600-0000-060e-2b3401010107", 0x0204, "kAAFTypeID_TaggedValueStrongReferenceVector", True, False),
    "Attributes"            : ("03010210-0800-0000-060e-2b3401010107", 0x0205, "kAAFTypeID_TaggedValueStrongReferenceVector", True, False),
    }
),
"Segment"               : ("0d010101-0101-0300-060e-2b3402060101", "Component", False, {
    }
),
"EdgeCode"              : ("0d010101-0101-0400-060e-2b3402060101", "Segment", True, {
    "Start"                 : ("01040901-0000-0000-060e-2b3401010102", 0x0401, "aafPositionType", False, False),
    "FilmKind"              : ("04100103-0109-0000-060e-2b3401010102", 0x0402, "FilmType", False, False),
    "CodeFormat"            : ("04100103-0102-0000-060e-2b3401010101", 0x0403, "EdgeType", False, False),
    "Header"                : ("01030201-0200-0000-060e-2b3401010102", 0x0404, "aafDataValue", True, False),
    }
),
"EssenceGroup"          : ("0d010101-0101-0500-060e-2b3402060101", "Segment", True, {
    "Choices"               : ("06010104-0601-0000-060e-2b3401010102", 0x0501, "kAAFTypeID_SourceReferenceStrongReferenceVector", False, False),
    "StillFrame"            : ("06010104-0208-0000-060e-2b3401010102", 0x0502, "kAAFTypeID_SourceReferenceStrongReference", True, False),
    }
),
"Event"                 : ("0d010101-0101-0600-060e-2b3402060101", "Segment", False, {
    "Position"              : ("07020103-0303-0000-060e-2b3401010102", 0x0601, "aafPositionType", False, False),
    "Comment"               : ("05300404-0100-0000-060e-2b3401010102", 0x0602, "aafString", True, False),
    }
),
"GPITrigger"            : ("0d010101-0101-0700-060e-2b3402060101", "Event", True, {
    "ActiveState"           : ("05300401-0000-0000-060e-2b3401010101", 0x0801, "Boolean", False, False),
    }
),
"CommentMarker"         : ("0d010101-0101-0800-060e-2b3402060101", "Event", True, {
    "Annotation"            : ("06010104-020a-0000-060e-2b3401010102", 0x0901, "kAAFTypeID_SourceReferenceStrongReference", True, False),
    }
),
"Filler"                : ("0d010101-0101-0900-060e-2b3402060101", "Segment", True, {
    }
),
"OperationGroup"        : ("0d010101-0101-0a00-060e-2b3402060101", "Segment", True, {
    "Operation"             : ("05300506-0000-0000-060e-2b3401010102", 0x0b01, "OperationDefinitionWeakReference", False, False),
    "InputSegments"         : ("06010104-0602-0000-060e-2b3401010102", 0x0b02, "kAAFTypeID_SegmentStrongReferenceVector", True, False),
    "Parameters"            : ("06010104-060a-0000-060e-2b3401010102", 0x0b03, "kAAFTypeID_ParameterStrongReferenceVector", True, False),
    "BypassOverride"        : ("0530050c-0000-0000-060e-2b3401010102", 0x0b04, "aafUInt32", True, False),
    "Rendering"             : ("06010104-0206-0000-060e-2b3401010102", 0x0b05, "kAAFTypeID_SourceReferenceStrongReference", True, False),
    }
),
"NestedScope"           : ("0d010101-0101-0b00-060e-2b3402060101", "Segment", True, {
    "Slots"                 : ("06010104-0607-0000-060e-2b3401010102", 0x0c01, "kAAFTypeID_SegmentStrongReferenceVector", False, False),
    }
),
"Pulldown"              : ("0d010101-0101-0c00-060e-2b3402060101", "Segment", True, {
    "InputSegment"          : ("06010104-0207-0000-060e-2b3401010102", 0x0d01, "kAAFTypeID_SegmentStrongReference", False, False),
    "PulldownKind"          : ("05401001-0200-0000-060e-2b3401010102", 0x0d02, "PulldownKindType", False, False),
    "PulldownDirection"     : ("05401001-0100-0000-060e-2b3401010102", 0x0d03, "PulldownDirectionType", False, False),
    "PhaseFrame"            : ("05401001-0300-0000-060e-2b3401010102", 0x0d04, "aafPhaseFrameType", False, False),
    }
),
"ScopeReference"        : ("0d010101-0101-0d00-060e-2b3402060101", "Segment", True, {
    "RelativeScope"         : ("06010103-0300-0000-060e-2b3401010102", 0x0e01, "aafUInt32", False, False),
    "RelativeSlot"          : ("06010103-0400-0000-060e-2b3401010102", 0x0e02, "aafUInt32", False, False),
    }
),
"Selector"              : ("0d010101-0101-0e00-060e-2b3402060101", "Segment", True, {
    "Selected"              : ("06010104-0209-0000-060e-2b3401010102", 0x0f01, "kAAFTypeID_SegmentStrongReference", False, False),
    "Alternates"            : ("06010104-0608-0000-060e-2b3401010102", 0x0f02, "kAAFTypeID_SegmentStrongReferenceVector", True, False),
    }
),
"Sequence"              : ("0d010101-0101-0f00-060e-2b3402060101", "Segment", True, {
    "Components"            : ("06010104-0609-0000-060e-2b3401010102", 0x1001, "kAAFTypeID_ComponentStrongReferenceVector", False, False),
    }
),
"SourceReference"       : ("0d010101-0101-1000-060e-2b3402060101", "Segment", False, {
    "SourceID"              : ("06010103-0100-0000-060e-2b3401010102", 0x1101, "MobIDType", True, False),
    "SourceMobSlotID"       : ("06010103-0200-0000-060e-2b3401010102", 0x1102, "aafUInt32", False, False),
    "ChannelIDs"            : ("06010103-0700-0000-060e-2b3401010107", 0x1103, "aafUInt32Array", True, False),
    "MonoSourceSlotIDs"     : ("06010103-0800-0000-060e-2b3401010108", 0x1104, "aafUInt32Array", True, False),
    }
),
"SourceClip"            : ("0d010101-0101-1100-060e-2b3402060101", "SourceReference", True, {
    "StartTime"             : ("07020103-0104-0000-060e-2b3401010102", 0x1201, "aafPositionType", True, False),
    "FadeInLength"          : ("07020201-0105-0200-060e-2b3401010102", 0x1202, "aafLengthType", True, False),
    "FadeInType"            : ("05300501-0000-0000-060e-2b3401010101", 0x1203, "FadeType", True, False),
    "FadeOutLength"         : ("07020201-0105-0300-060e-2b3401010102", 0x1204, "aafLengthType", True, False),
    "FadeOutType"           : ("05300502-0000-0000-060e-2b3401010101", 0x1205, "FadeType", True, False),
    }
),
"TextClip"              : ("0d010101-0101-1200-060e-2b3402060101", "SourceReference", False, {
    }
),
"HTMLClip"              : ("0d010101-0101-1300-060e-2b3402060101", "TextClip", True, {
    "BeginAnchor"           : ("05300601-0100-0000-060e-2b3401010102", 0x1401, "aafString", True, False),
    "EndAnchor"             : ("05300602-0100-0000-060e-2b3401010102", 0x1402, "aafString", True, False),
    }
),
"Timecode"              : ("0d010101-0101-1400-060e-2b3402060101", "Segment", True, {
    "Start"                 : ("07020103-0105-0000-060e-2b3401010102", 0x1501, "aafPositionType", False, False),
    "FPS"                   : ("04040101-0206-0000-060e-2b3401010102", 0x1502, "aafUInt16", False, False),
    "Drop"                  : ("04040101-0500-0000-060e-2b3401010101", 0x1503, "Boolean", False, False),
    }
),
"TimecodeStream"        : ("0d010101-0101-1500-060e-2b3402060101", "Segment", False, {
    "SampleRate"            : ("04040101-0201-0000-060e-2b3401010102", 0x1601, "Rational", False, False),
    "Source"                : ("04070300-0000-0000-060e-2b3401010102", 0x1602, "Stream", False, False),
    "SourceType"            : ("04040201-0000-0000-060e-2b3401010101", 0x1603, "TCSource", False, False),
    }
),
"TimecodeStream12M"     : ("0d010101-0101-1600-060e-2b3402060101", "TimecodeStream", True, {
    "IncludeSync"           : ("04040101-0400-0000-060e-2b3401010101", 0x1701, "Boolean", False, False),
    }
),
"Transition"            : ("0d010101-0101-1700-060e-2b3402060101", "Component", True, {
    "OperationGroup"        : ("06010104-0205-0000-060e-2b3401010102", 0x1801, "kAAFTypeID_OperationGroupStrongReference", False, False),
    "CutPoint"              : ("07020103-0106-0000-060e-2b3401010102", 0x1802, "aafPositionType", False, False),
    }
),
"ContentStorage"        : ("0d010101-0101-1800-060e-2b3402060101", "InterchangeObject", True, {
    "Mobs"                  : ("06010104-0501-0000-060e-2b3401010102", 0x1901, "kAAFTypeID_MobStrongReferenceSet", False, False),
    "EssenceData"           : ("06010104-0502-0000-060e-2b3401010102", 0x1902, "kAAFTypeID_EssenceDataStrongReferenceSet", True, False),
    }
),
"ControlPoint"          : ("0d010101-0101-1900-060e-2b3402060101", "InterchangeObject", True, {
    "Value"                 : ("0530050d-0000-0000-060e-2b3401010102", 0x1a02, "aafIndirect", False, False),
    "Time"                  : ("07020103-1002-0100-060e-2b3401010102", 0x1a03, "Rational", False, False),
    "EditHint"              : ("05300508-0000-0000-060e-2b3401010102", 0x1a04, "EditHintType", True, False),
    }
),
"DefinitionObject"      : ("0d010101-0101-1a00-060e-2b3402060101", "InterchangeObject", False, {
    "Identification"        : ("01011503-0000-0000-060e-2b3401010102", 0x1b01, "AUID", False, True),
    "Name"                  : ("01070102-0301-0000-060e-2b3401010102", 0x1b02, "aafString", False, False),
    "Description"           : ("03020301-0201-0000-060e-2b3401010102", 0x1b03, "aafString", True, False),
    }
),
"DataDefinition"        : ("0d010101-0101-1b00-060e-2b3402060101", "DefinitionObject", True, {
    }
),
"OperationDefinition"   : ("0d010101-0101-1c00-060e-2b3402060101", "DefinitionObject", True, {
    "DataDefinition"        : ("05300509-0000-0000-060e-2b3401010102", 0x1e01, "DataDefinitionWeakReference", False, False),
    "IsTimeWarp"            : ("05300503-0000-0000-060e-2b3401010101", 0x1e02, "Boolean", True, False),
    "DegradeTo"             : ("06010104-0401-0000-060e-2b3401010102", 0x1e03, "kAAFTypeID_OperationDefinitionWeakReferenceVector", True, False),
    "OperationCategory"     : ("0530050a-0000-0000-060e-2b3401010102", 0x1e06, "aafOperationCategoryType", True, False),
    "NumberInputs"          : ("05300504-0000-0000-060e-2b3401010101", 0x1e07, "aafInt32", False, False),
    "Bypass"                : ("05300505-0000-0000-060e-2b3401010101", 0x1e08, "aafUInt32", True, False),
    "ParametersDefined"     : ("06010104-0302-0000-060e-2b3401010102", 0x1e09, "kAAFTypeID_ParameterDefinitionWeakReferenceSet", True, False),
    }
),
"ParameterDefinition"   : ("0d010101-0101-1d00-060e-2b3402060101", "DefinitionObject", True, {
    "Type"                  : ("06010104-0106-0000-060e-2b3401010102", 0x1f01, "TypeDefinitionWeakReference", False, False),
    "DisplayUnits"          : ("0530050b-0100-0000-060e-2b3401010102", 0x1f03, "aafString", True, False),
    }
),
"PluginDefinition"      : ("0d010101-0101-1e00-060e-2b3402060101", "DefinitionObject", True, {
    "PluginCategory"        : ("05200901-0000-0000-060e-2b3401010102", 0x2203, "aafPluginCategoryType", False, False),
    "VersionNumber"         : ("03030301-0300-0000-060e-2b3401010102", 0x2204, "VersionType", False, False),
    "VersionString"         : ("03030301-0201-0000-060e-2b3401010102", 0x2205, "aafString", True, False),
    "Manufacturer"          : ("010a0101-0101-0000-060e-2b3401010102", 0x2206, "aafString", True, False),
    "ManufacturerInfo"      : ("06010104-020b-0000-060e-2b3401010102", 0x2207, "kAAFTypeID_NetworkLocatorStrongReference", True, False),
    "ManufacturerID"        : ("010a0101-0300-0000-060e-2b3401010102", 0x2208, "AUID", True, False),
    "Platform"              : ("05200902-0000-0000-060e-2b3401010102", 0x2209, "AUID", True, False),
    "MinPlatformVersion"    : ("05200903-0000-0000-060e-2b3401010102", 0x220a, "VersionType", True, False),
    "MaxPlatformVersion"    : ("05200904-0000-0000-060e-2b3401010102", 0x220b, "VersionType", True, False),
    "Engine"                : ("05200905-0000-0000-060e-2b3401010102", 0x220c, "AUID", True, False),
    "MinEngineVersion"      : ("05200906-0000-0000-060e-2b3401010102", 0x220d, "VersionType", True, False),
    "MaxEngineVersion"      : ("05200907-0000-0000-060e-2b3401010102", 0x220e, "VersionType", True, False),
    "PluginAPI"             : ("05200908-0000-0000-060e-2b3401010102", 0x220f, "AUID", True, False),
    "MinPluginAPI"          : ("05200909-0000-0000-060e-2b3401010102", 0x2210, "VersionType", True, False),
    "MaxPluginAPI"          : ("0520090a-0000-0000-060e-2b3401010102", 0x2211, "VersionType", True, False),
    "SoftwareOnly"          : ("0520090b-0000-0000-060e-2b3401010102", 0x2212, "Boolean", True, False),
    "Accelerator"           : ("0520090c-0000-0000-060e-2b3401010102", 0x2213, "Boolean", True, False),
    "Locators"              : ("0520090d-0000-0000-060e-2b3401010102", 0x2214, "kAAFTypeID_LocatorStrongReferenceVector", True, False),
    "Authentication"        : ("0520090e-0000-0000-060e-2b3401010102", 0x2215, "Boolean", True, False),
    "DefinitionObject"      : ("0520090f-0000-0000-060e-2b3401010102", 0x2216, "AUID", True, False),
    }
),
"CodecDefinition"       : ("0d010101-0101-1f00-060e-2b3402060101", "DefinitionObject", True, {
    "FileDescriptorClass"   : ("06010104-0107-0000-060e-2b3401010102", 0x2301, "ClassDefinitionWeakReference", False, False),
    "DataDefinitions"       : ("06010104-0301-0000-060e-2b3401010102", 0x2302, "kAAFTypeID_DataDefinitionWeakReferenceVector", False, False),
    }
),
"ContainerDefinition"   : ("0d010101-0101-2000-060e-2b3402060101", "DefinitionObject", True, {
    "EssenceIsIdentified"   : ("03010201-0300-0000-060e-2b3401010101", 0x2401, "Boolean", True, False),
    }
),
"InterpolationDefinition" : ("0d010101-0101-2100-060e-2b3402060101", "DefinitionObject", True, {
    }
),
"Dictionary"            : ("0d010101-0101-2200-060e-2b3402060101", "InterchangeObject", True, {
    "OperationDefinitions"  : ("06010104-0503-0000-060e-2b3401010102", 0x2603, "kAAFTypeID_OperationDefinitionStrongReferenceSet", True, False),
    "ParameterDefinitions"  : ("06010104-0504-0000-060e-2b3401010102", 0x2604, "kAAFTypeID_ParameterDefinitionStrongReferenceSet", True, False),
    "DataDefinitions"       : ("06010104-0505-0000-060e-2b3401010102", 0x2605, "kAAFTypeID_DataDefinitionStrongReferenceSet", True, False),
    "PluginDefinitions"     : ("06010104-0506-0000-060e-2b3401010102", 0x2606, "kAAFTypeID_PluginDefinitionStrongReferenceSet", True, False),
    "CodecDefinitions"      : ("06010104-0507-0000-060e-2b3401010102", 0x2607, "kAAFTypeID_CodecDefinitionStrongReferenceSet", True, False),
    "ContainerDefinitions"  : ("06010104-0508-0000-060e-2b3401010102", 0x2608, "kAAFTypeID_ContainerDefinitionStrongReferenceSet", True, False),
    "InterpolationDefinitions": ("06010104-0509-0000-060e-2b3401010102", 0x2609, "kAAFTypeID_InterpolationDefinitionStrongReferenceSet", True, False),
    "KLVDataDefinitions"    : ("06010104-050a-0000-060e-2b3401010107", 0x260a, "kAAFTypeID_KLVDataDefinitionStrongReferenceSet", True, False),
    "TaggedValueDefinitions": ("06010104-050b-0000-060e-2b3401010107", 0x260b, "kAAFTypeID_TaggedValueDefinitionStrongReferenceSet", True, False),
    }
),
"EssenceData"           : ("0d010101-0101-2300-060e-2b3402060101", "InterchangeObject", True, {
    "MobID"                 : ("06010106-0100-0000-060e-2b3401010102", 0x2701, "MobIDType", False, True),
    "Data"                  : ("04070200-0000-0000-060e-2b3401010102", 0x2702, "Stream", False, False),
    "SampleIndex"           : ("06010102-0100-0000-060e-2b3401010102", 0x2b01, "Stream", True, False),
    }
),
"EssenceDescriptor"     : ("0d010101-0101-2400-060e-2b3402060101", "InterchangeObject", False, {
    "Locator"               : ("06010104-0603-0000-060e-2b3401010102", 0x2f01, "kAAFTypeID_LocatorStrongReferenceVector", True, False),
    }
),
"FileDescriptor"        : ("0d010101-0101-2500-060e-2b3402060101", "EssenceDescriptor", False, {
    "SampleRate"            : ("04060101-0000-0000-060e-2b3401010101", 0x3001, "Rational", False, False),
    "Length"                : ("04060102-0000-0000-060e-2b3401010101", 0x3002, "aafLengthType", False, False),
    "ContainerFormat"       : ("06010104-0102-0000-060e-2b3401010102", 0x3004, "ContainerDefinitionWeakReference", True, False),
    "CodecDefinition"       : ("06010104-0103-0000-060e-2b3401010102", 0x3005, "CodecDefinitionWeakReference", True, False),
    "LinkedSlotID"          : ("06010103-0500-0000-060e-2b3401010105", 0x3006, "aafUInt32", True, False),
    }
),
"AIFCDescriptor"        : ("0d010101-0101-2600-060e-2b3402060101", "FileDescriptor", True, {
    "Summary"               : ("03030302-0200-0000-060e-2b3401010102", 0x3101, "aafDataValue", False, False),
    }
),
"DigitalImageDescriptor" : ("0d010101-0101-2700-060e-2b3402060101", "FileDescriptor", False, {
    "Compression"           : ("04010601-0000-0000-060e-2b3401010102", 0x3201, "AUID", True, False),
    "StoredHeight"          : ("04010502-0100-0000-060e-2b3401010101", 0x3202, "aafUInt32", False, False),
    "StoredWidth"           : ("04010502-0200-0000-060e-2b3401010101", 0x3203, "aafUInt32", False, False),
    "SampledHeight"         : ("04010501-0700-0000-060e-2b3401010101", 0x3204, "aafUInt32", True, False),
    "SampledWidth"          : ("04010501-0800-0000-060e-2b3401010101", 0x3205, "aafUInt32", True, False),
    "SampledXOffset"        : ("04010501-0900-0000-060e-2b3401010101", 0x3206, "aafInt32", True, False),
    "SampledYOffset"        : ("04010501-0a00-0000-060e-2b3401010101", 0x3207, "aafInt32", True, False),
    "DisplayHeight"         : ("04010501-0b00-0000-060e-2b3401010101", 0x3208, "aafUInt32", True, False),
    "DisplayWidth"          : ("04010501-0c00-0000-060e-2b3401010101", 0x3209, "aafUInt32", True, False),
    "DisplayXOffset"        : ("04010501-0d00-0000-060e-2b3401010101", 0x320a, "aafInt32", True, False),
    "DisplayYOffset"        : ("04010501-0e00-0000-060e-2b3401010101", 0x320b, "aafInt32", True, False),
    "FrameLayout"           : ("04010301-0400-0000-060e-2b3401010101", 0x320c, "LayoutType", False, False),
    "VideoLineMap"          : ("04010302-0500-0000-060e-2b3401010102", 0x320d, "aafInt32Array", False, False),
    "ImageAspectRatio"      : ("04010101-0100-0000-060e-2b3401010101", 0x320e, "Rational", False, False),
    "AlphaTransparency"     : ("05200102-0000-0000-060e-2b3401010102", 0x320f, "AlphaTransparencyType", True, False),
    "TransferCharacteristic": ("04010201-0101-0200-060e-2b3401010102", 0x3210, "aafTransferCharacteristicType", True, False),
    "ColorPrimaries"        : ("04010201-0106-0100-060e-2b3401010109", 0x3219, "aafColorPrimariesType", True, False),
    "CodingEquations"       : ("04010201-0103-0100-060e-2b3401010102", 0x321a, "aafCodingEquationsType", True, False),
    "ImageAlignmentFactor"  : ("04180101-0000-0000-060e-2b3401010102", 0x3211, "aafUInt32", True, False),
    "FieldDominance"        : ("04010301-0600-0000-060e-2b3401010102", 0x3212, "FieldNumber", True, False),
    "FieldStartOffset"      : ("04180102-0000-0000-060e-2b3401010102", 0x3213, "aafUInt32", True, False),
    "FieldEndOffset"        : ("04180103-0000-0000-060e-2b3401010102", 0x3214, "aafUInt32", True, False),
    "SignalStandard"        : ("04050113-0000-0000-060e-2b3401010105", 0x3215, "SignalStandardType", True, False),
    "StoredF2Offset"        : ("04010302-0800-0000-060e-2b3401010105", 0x3216, "aafInt32", True, False),
    "DisplayF2Offset"       : ("04010302-0700-0000-060e-2b3401010105", 0x3217, "aafInt32", True, False),
    "ActiveFormatDescriptor": ("04010302-0900-0000-060e-2b3401010105", 0x3218, "aafUInt8", True, False),
    }
),
"CDCIDescriptor"        : ("0d010101-0101-2800-060e-2b3402060101", "DigitalImageDescriptor", True, {
    "ComponentWidth"        : ("04010503-0a00-0000-060e-2b3401010102", 0x3301, "aafUInt32", False, False),
    "HorizontalSubsampling" : ("04010501-0500-0000-060e-2b3401010101", 0x3302, "aafUInt32", False, False),
    "ColorSiting"           : ("04010501-0600-0000-060e-2b3401010101", 0x3303, "ColorSitingType", True, False),
    "BlackReferenceLevel"   : ("04010503-0300-0000-060e-2b3401010101", 0x3304, "aafUInt32", True, False),
    "WhiteReferenceLevel"   : ("04010503-0400-0000-060e-2b3401010101", 0x3305, "aafUInt32", True, False),
    "ColorRange"            : ("04010503-0500-0000-060e-2b3401010102", 0x3306, "aafUInt32", True, False),
    "PaddingBits"           : ("04180104-0000-0000-060e-2b3401010102", 0x3307, "aafInt16", True, False),
    "VerticalSubsampling"   : ("04010501-1000-0000-060e-2b3401010102", 0x3308, "aafUInt32", True, False),
    "AlphaSamplingWidth"    : ("04010503-0700-0000-060e-2b3401010102", 0x3309, "aafUInt32", True, False),
    "ReversedByteOrder"     : ("03010201-0a00-0000-060e-2b3401010105", 0x330b, "Boolean", True, False),
    }
),
"RGBADescriptor"        : ("0d010101-0101-2900-060e-2b3402060101", "DigitalImageDescriptor", True, {
    "PixelLayout"           : ("04010503-0600-0000-060e-2b3401010102", 0x3401, "aafRGBALayout", False, False),
    "Palette"               : ("04010503-0800-0000-060e-2b3401010102", 0x3403, "aafDataValue", True, False),
    "PaletteLayout"         : ("04010503-0900-0000-060e-2b3401010102", 0x3404, "aafRGBALayout", True, False),
    "ScanningDirection"     : ("04010404-0100-0000-060e-2b3401010105", 0x3405, "ScanningDirectionType", True, False),
    "ComponentMaxRef"       : ("04010503-0b00-0000-060e-2b3401010105", 0x3406, "aafUInt32", True, False),
    "ComponentMinRef"       : ("04010503-0c00-0000-060e-2b3401010105", 0x3407, "aafUInt32", True, False),
    "AlphaMaxRef"           : ("04010503-0d00-0000-060e-2b3401010105", 0x3408, "aafUInt32", True, False),
    "AlphaMinRef"           : ("04010503-0e00-0000-060e-2b3401010105", 0x3409, "aafUInt32", True, False),
    }
),
"HTMLDescriptor"        : ("0d010101-0101-2a00-060e-2b3402060101", "FileDescriptor", True, {
    }
),
"TIFFDescriptor"        : ("0d010101-0101-2b00-060e-2b3402060101", "FileDescriptor", True, {
    "IsUniform"             : ("05020103-0101-0000-060e-2b3401010102", 0x3701, "Boolean", False, False),
    "IsContiguous"          : ("06080201-0000-0000-060e-2b3401010101", 0x3702, "Boolean", False, False),
    "LeadingLines"          : ("04010302-0300-0000-060e-2b3401010101", 0x3703, "aafInt32", True, False),
    "TrailingLines"         : ("04010302-0400-0000-060e-2b3401010101", 0x3704, "aafInt32", True, False),
    "JPEGTableID"           : ("05020103-0102-0000-060e-2b3401010102", 0x3705, "aafJPEGTableIDType", True, False),
    "Summary"               : ("03030302-0300-0000-060e-2b3401010102", 0x3706, "aafDataValue", False, False),
    }
),
"WAVEDescriptor"        : ("0d010101-0101-2c00-060e-2b3402060101", "FileDescriptor", True, {
    "Summary"               : ("03030302-0100-0000-060e-2b3401010102", 0x3801, "aafDataValue", False, False),
    }
),
"FilmDescriptor"        : ("0d010101-0101-2d00-060e-2b3402060101", "EssenceDescriptor", True, {
    "FilmFormat"            : ("04100103-0108-0000-060e-2b3401010102", 0x3901, "FilmType", True, False),
    "FrameRate"             : ("04010802-0300-0000-060e-2b3401010102", 0x3902, "aafUInt32", True, False),
    "PerforationsPerFrame"  : ("04100103-0103-0000-060e-2b3401010102", 0x3903, "aafUInt8", True, False),
    "FilmAspectRatio"       : ("04100103-0203-0000-060e-2b3401010102", 0x3904, "Rational", True, False),
    "Manufacturer"          : ("04100103-0106-0100-060e-2b3401010102", 0x3905, "aafString", True, False),
    "Model"                 : ("04100103-0105-0100-060e-2b3401010102", 0x3906, "aafString", True, False),
    "FilmGaugeFormat"       : ("04100103-0104-0100-060e-2b3401010102", 0x3907, "aafString", True, False),
    "FilmBatchNumber"       : ("04100103-0107-0100-060e-2b3401010102", 0x3908, "aafString", True, False),
    }
),
"TapeDescriptor"        : ("0d010101-0101-2e00-060e-2b3402060101", "EssenceDescriptor", True, {
    "FormFactor"            : ("04100101-0101-0000-060e-2b3401010102", 0x3a01, "TapeCaseType", True, False),
    "VideoSignal"           : ("04010401-0100-0000-060e-2b3401010102", 0x3a02, "VideoSignalType", True, False),
    "TapeFormat"            : ("0d010101-0101-0100-060e-2b3401010102", 0x3a03, "TapeFormatType", True, False),
    "Length"                : ("04100101-0300-0000-060e-2b3401010102", 0x3a04, "aafUInt32", True, False),
    "ManufacturerID"        : ("04100101-0401-0000-060e-2b3401010102", 0x3a05, "aafString", True, False),
    "Model"                 : ("04100101-0201-0000-060e-2b3401010102", 0x3a06, "aafString", True, False),
    "TapeBatchNumber"       : ("04100101-0601-0000-060e-2b3401010102", 0x3a07, "aafString", True, False),
    "TapeStock"             : ("04100101-0501-0000-060e-2b3401010102", 0x3a08, "aafString", True, False),
    }
),
"Header"                : ("0d010101-0101-2f00-060e-2b3402060101", "InterchangeObject", True, {
    "ByteOrder"             : ("03010201-0200-0000-060e-2b3401010101", 0x3b01, "aafInt16", False, False),
    "LastModified"          : ("07020110-0204-0000-060e-2b3401010102", 0x3b02, "TimeStamp", False, False),
    "Content"               : ("06010104-0201-0000-060e-2b3401010102", 0x3b03, "kAAFTypeID_ContentStorageStrongReference", False, False),
    "Dictionary"            : ("06010104-0202-0000-060e-2b3401010102", 0x3b04, "kAAFTypeID_DictionaryStrongReference", False, False),
    "Version"               : ("03010201-0500-0000-060e-2b3401010102", 0x3b05, "VersionType", False, False),
    "IdentificationList"    : ("06010104-0604-0000-060e-2b3401010102", 0x3b06, "kAAFTypeID_IdentificationStrongReferenceVector", False, False),
    "ObjectModelVersion"    : ("03010201-0400-0000-060e-2b3401010102", 0x3b07, "aafUInt32", True, False),
    "OperationalPattern"    : ("01020203-0000-0000-060e-2b3401010105", 0x3b09, "AUID", True, False),
    "EssenceContainers"     : ("01020210-0201-0000-060e-2b3401010105", 0x3b0a, "kAAFTypeID_AUIDSet", True, False),
    "DescriptiveSchemes"    : ("01020210-0202-0000-060e-2b3401010105", 0x3b0b, "kAAFTypeID_AUIDSet", True, False),
    }
),
"Identification"        : ("0d010101-0101-3000-060e-2b3402060101", "InterchangeObject", True, {
    "CompanyName"           : ("05200701-0201-0000-060e-2b3401010102", 0x3c01, "aafString", False, False),
    "ProductName"           : ("05200701-0301-0000-060e-2b3401010102", 0x3c02, "aafString", False, False),
    "ProductVersion"        : ("05200701-0400-0000-060e-2b3401010102", 0x3c03, "ProductVersion", True, False),
    "ProductVersionString"  : ("05200701-0501-0000-060e-2b3401010102", 0x3c04, "aafString", False, False),
    "ProductID"             : ("05200701-0700-0000-060e-2b3401010102", 0x3c05, "AUID", False, False),
    "Date"                  : ("07020110-0203-0000-060e-2b3401010102", 0x3c06, "TimeStamp", False, False),
    "ToolkitVersion"        : ("05200701-0a00-0000-060e-2b3401010102", 0x3c07, "ProductVersion", True, False),
    "Platform"              : ("05200701-0601-0000-060e-2b3401010102", 0x3c08, "aafString", True, False),
    "GenerationAUID"        : ("05200701-0100-0000-060e-2b3401010102", 0x3c09, "AUID", False, False),
    }
),
"Locator"               : ("0d010101-0101-3100-060e-2b3402060101", "InterchangeObject", False, {
    }
),
"NetworkLocator"        : ("0d010101-0101-3200-060e-2b3402060101", "Locator", True, {
    "URLString"             : ("01020101-0100-0000-060e-2b3401010101", 0x4001, "aafString", False, False),
    }
),
"TextLocator"           : ("0d010101-0101-3300-060e-2b3402060101", "Locator", True, {
    "Name"                  : ("01040102-0100-0000-060e-2b3401010102", 0x4101, "aafString", False, False),
    }
),
"Mob"                   : ("0d010101-0101-3400-060e-2b3402060101", "InterchangeObject", False, {
    "MobID"                 : ("01011510-0000-0000-060e-2b3401010101", 0x4401, "MobIDType", False, True),
    "Name"                  : ("01030302-0100-0000-060e-2b3401010101", 0x4402, "aafString", True, False),
    "Slots"                 : ("06010104-0605-0000-060e-2b3401010102", 0x4403, "kAAFTypeID_MobSlotStrongReferenceVector", False, False),
    "LastModified"          : ("07020110-0205-0000-060e-2b3401010102", 0x4404, "TimeStamp", False, False),
    "CreationTime"          : ("07020110-0103-0000-060e-2b3401010102", 0x4405, "TimeStamp", False, False),
    "UserComments"          : ("03020102-0c00-0000-060e-2b3401010102", 0x4406, "kAAFTypeID_TaggedValueStrongReferenceVector", True, False),
    "KLVData"               : ("03010210-0300-0000-060e-2b3401010102", 0x4407, "kAAFTypeID_KLVDataStrongReferenceVector", True, False),
    "Attributes"            : ("03010210-0700-0000-060e-2b3401010107", 0x4409, "kAAFTypeID_TaggedValueStrongReferenceVector", True, False),
    "UsageCode"             : ("05010108-0000-0000-060e-2b3401010107", 0x4408, "aafUsageType", True, False),
    }
),
"CompositionMob"        : ("0d010101-0101-3500-060e-2b3402060101", "Mob", True, {
    "DefaultFadeLength"     : ("07020201-0105-0100-060e-2b3401010102", 0x4501, "aafLengthType", True, False),
    "DefFadeType"           : ("05300201-0000-0000-060e-2b3401010101", 0x4502, "FadeType", True, False),
    "DefFadeEditUnit"       : ("05300403-0000-0000-060e-2b3401010102", 0x4503, "Rational", True, False),
    "Rendering"             : ("06010104-010a-0000-060e-2b3401010108", 0x4504, "MobIDType", True, False),
    }
),
"MasterMob"             : ("0d010101-0101-3600-060e-2b3402060101", "Mob", True, {
    }
),
"SourceMob"             : ("0d010101-0101-3700-060e-2b3402060101", "Mob", True, {
    "EssenceDescription"    : ("06010104-0203-0000-060e-2b3401010102", 0x4701, "kAAFTypeID_EssenceDescriptorStrongReference", False, False),
    }
),
"MobSlot"               : ("0d010101-0101-3800-060e-2b3402060101", "InterchangeObject", False, {
    "SlotID"                : ("01070101-0000-0000-060e-2b3401010102", 0x4801, "aafUInt32", False, False),
    "SlotName"              : ("01070102-0100-0000-060e-2b3401010102", 0x4802, "aafString", True, False),
    "Segment"               : ("06010104-0204-0000-060e-2b3401010102", 0x4803, "kAAFTypeID_SegmentStrongReference", False, False),
    "PhysicalTrackNumber"   : ("01040103-0000-0000-060e-2b3401010102", 0x4804, "aafUInt32", True, False),
    }
),
"EventMobSlot"          : ("0d010101-0101-3900-060e-2b3402060101", "MobSlot", True, {
    "EditRate"              : ("05300402-0000-0000-060e-2b3401010102", 0x4901, "Rational", False, False),
    "EventSlotOrigin"       : ("07020103-010b-0000-060e-2b3401010105", 0x4902, "aafPositionType", True, False),
    }
),
"StaticMobSlot"         : ("0d010101-0101-3a00-060e-2b3402060101", "MobSlot", True, {
    }
),
"TimelineMobSlot"       : ("0d010101-0101-3b00-060e-2b3402060101", "MobSlot", True, {
    "EditRate"              : ("05300405-0000-0000-060e-2b3401010102", 0x4b01, "Rational", False, False),
    "Origin"                : ("07020103-0103-0000-060e-2b3401010102", 0x4b02, "aafPositionType", False, False),
    "MarkIn"                : ("07020103-010c-0000-060e-2b3401010107", 0x4b03, "aafPositionType", True, False),
    "MarkOut"               : ("07020103-0203-0000-060e-2b3401010107", 0x4b04, "aafPositionType", True, False),
    "UserPos"               : ("07020103-010d-0000-060e-2b3401010107", 0x4b05, "aafPositionType", True, False),
    }
),
"Parameter"             : ("0d010101-0101-3c00-060e-2b3402060101", "InterchangeObject", False, {
    "Definition"            : ("06010104-0104-0000-060e-2b3401010102", 0x4c01, "AUID", False, False),
    }
),
"ConstantValue"         : ("0d010101-0101-3d00-060e-2b3402060101", "Parameter", True, {
    "Value"                 : ("05300507-0000-0000-060e-2b3401010102", 0x4d01, "aafIndirect", False, False),
    }
),
"VaryingValue"          : ("0d010101-0101-3e00-060e-2b3402060101", "Parameter", True, {
    "Interpolation"         : ("06010104-0105-0000-060e-2b3401010102", 0x4e01, "InterpolationDefinitionWeakReference", False, False),
    "PointList"             : ("06010104-0606-0000-060e-2b3401010102", 0x4e02, "kAAFTypeID_ControlPointStrongReferenceVector", False, False),
    }
),
"TaggedValue"           : ("0d010101-0101-3f00-060e-2b3402060101", "InterchangeObject", True, {
    "Name"                  : ("03020102-0901-0000-060e-2b3401010102", 0x5001, "aafString", False, False),
    "Value"                 : ("03020102-0a01-0000-060e-2b3401010102", 0x5003, "aafIndirect", False, False),
    }
),
"KLVData"               : ("0d010101-0101-4000-060e-2b3402060101", "InterchangeObject", True, {
    "Value"                 : ("03010210-0200-0000-060e-2b3401010102", 0x5101, "aafOpaque", False, False),
    }
),
"DescriptiveMarker"     : ("0d010101-0101-4100-060e-2b3402060101", "CommentMarker", True, {
    "DescribedSlots"        : ("01070105-0000-0000-060e-2b3401010104", 0x6102, "kAAFTypeID_UInt32Set", True, False),
    "Description"           : ("06010104-020c-0000-060e-2b3401010105", 0x6101, "kAAFTypeID_DescriptiveFrameworkStrongReference", True, False),
    }
),
"SoundDescriptor"       : ("0d010101-0101-4200-060e-2b3402060101", "FileDescriptor", True, {
    "AudioSamplingRate"     : ("04020301-0101-0000-060e-2b3401010105", 0x3d03, "Rational", False, False),
    "Locked"                : ("04020301-0400-0000-060e-2b3401010104", 0x3d02, "Boolean", True, False),
    "AudioRefLevel"         : ("04020101-0300-0000-060e-2b3401010101", 0x3d04, "aafInt8", True, False),
    "ElectroSpatial"        : ("04020101-0100-0000-060e-2b3401010101", 0x3d05, "ElectroSpatialFormulation", True, False),
    "Channels"              : ("04020101-0400-0000-060e-2b3401010105", 0x3d07, "aafUInt32", False, False),
    "QuantizationBits"      : ("04020303-0400-0000-060e-2b3401010104", 0x3d01, "aafUInt32", False, False),
    "DialNorm"              : ("04020701-0000-0000-060e-2b3401010105", 0x3d0c, "aafInt8", True, False),
    "Compression"           : ("04020402-0000-0000-060e-2b3401010102", 0x3d06, "AUID", True, False),
    }
),
"DataEssenceDescriptor" : ("0d010101-0101-4300-060e-2b3402060101", "FileDescriptor", True, {
    "DataEssenceCoding"     : ("04030302-0000-0000-060e-2b3401010103", 0x3e01, "AUID", True, False),
    }
),
"MultipleDescriptor"    : ("0d010101-0101-4400-060e-2b3402060101", "FileDescriptor", True, {
    "FileDescriptors"       : ("06010104-060b-0000-060e-2b3401010104", 0x3f01, "kAAFTypeID_FileDescriptorStrongReferenceVector", False, False),
    }
),
"DescriptiveClip"       : ("0d010101-0101-4500-060e-2b3402060101", "SourceClip", True, {
    "DescribedSlotIDs"      : ("01070106-0000-0000-060e-2b3401010105", 0x6103, "kAAFTypeID_UInt32Set", True, False),
    }
),
"PCMDescriptor"         : ("0d010101-0101-4800-060e-2b3402060101", "SoundDescriptor", True, {
    "BlockAlign"            : ("04020302-0100-0000-060e-2b3401010105", 0x3d0a, "aafUInt16", False, False),
    "SequenceOffset"        : ("04020302-0200-0000-060e-2b3401010105", 0x3d0b, "aafUInt8", True, False),
    "AverageBPS"            : ("04020303-0500-0000-060e-2b3401010105", 0x3d09, "aafUInt32", False, False),
    "ChannelAssignment"     : ("04020101-0500-0000-060e-2b3401010107", 0x3d32, "AUID", True, False),
    "PeakEnvelopeVersion"   : ("04020301-0600-0000-060e-2b3401010108", 0x3d29, "aafUInt32", True, False),
    "PeakEnvelopeFormat"    : ("04020301-0700-0000-060e-2b3401010108", 0x3d2a, "aafUInt32", True, False),
    "PointsPerPeakValue"    : ("04020301-0800-0000-060e-2b3401010108", 0x3d2b, "aafUInt32", True, False),
    "PeakEnvelopeBlockSize" : ("04020301-0900-0000-060e-2b3401010108", 0x3d2c, "aafUInt32", True, False),
    "PeakChannels"          : ("04020301-0a00-0000-060e-2b3401010108", 0x3d2d, "aafUInt32", True, False),
    "PeakFrames"            : ("04020301-0b00-0000-060e-2b3401010108", 0x3d2e, "aafUInt32", True, False),
    "PeakOfPeaksPosition"   : ("04020301-0c00-0000-060e-2b3401010108", 0x3d2f, "aafPositionType", True, False),
    "PeakEnvelopeTimestamp" : ("04020301-0d00-0000-060e-2b3401010108", 0x3d30, "TimeStamp", True, False),
    "PeakEnvelopeData"      : ("04020301-0e00-0000-060e-2b3401010108", 0x3d31, "Stream", True, False),
    }
),
"AES3PCMDescriptor"     : ("0d010101-0101-4700-060e-2b3402060101", "PCMDescriptor", True, {
    "Emphasis"              : ("04020501-0600-0000-060e-2b3401010105", 0x3d0d, "EmphasisType", True, False),
    "BlockStartOffset"      : ("04020302-0300-0000-060e-2b3401010105", 0x3d0f, "aafUInt16", True, False),
    "AuxBitsMode"           : ("04020501-0100-0000-060e-2b3401010105", 0x3d08, "AuxBitsModeType", True, False),
    "ChannelStatusMode"     : ("04020501-0200-0000-060e-2b3401010105", 0x3d10, "aafChannelStatusModeArray", True, False),
    "FixedChannelStatusData": ("04020501-0300-0000-060e-2b3401010105", 0x3d11, "aafUInt8Array", True, False),
    "UserDataMode"          : ("04020501-0400-0000-060e-2b3401010105", 0x3d12, "aafUserDataModeArray", True, False),
    "FixedUserData"         : ("04020501-0500-0000-060e-2b3401010105", 0x3d13, "aafUInt8Array", True, False),
    }
),
"PhysicalDescriptor"    : ("0d010101-0101-4900-060e-2b3402060101", "EssenceDescriptor", False, {
    }
),
"ImportDescriptor"      : ("0d010101-0101-4a00-060e-2b3402060101", "PhysicalDescriptor", True, {
    }
),
"RecordingDescriptor"   : ("0d010101-0101-4b00-060e-2b3402060101", "PhysicalDescriptor", True, {
    }
),
"TaggedValueDefinition" : ("0d010101-0101-4c00-060e-2b3402060101", "DefinitionObject", True, {
    }
),
"KLVDataDefinition"     : ("0d010101-0101-4d00-060e-2b3402060101", "DefinitionObject", True, {
    "KLVDataType"           : ("06010104-0109-0000-060e-2b3401010107", 0x4d12, "TypeDefinitionWeakReference", True, False),
    }
),
"AuxiliaryDescriptor"   : ("0d010101-0101-4e00-060e-2b3402060101", "PhysicalDescriptor", True, {
    "MimeType"              : ("04090201-0000-0000-060e-2b3401010107", 0x4e11, "aafString", False, False),
    "CharSet"               : ("04090300-0000-0000-060e-2b3401010108", 0x4e12, "aafString", True, False),
    }
),
"RIFFChunk"             : ("0d010101-0101-4f00-060e-2b3402060101", "InterchangeObject", True, {
    "ChunkID"               : ("04060802-0000-0000-060e-2b3401010108", 0x4f01, "aafUInt32", False, False),
    "ChunkLength"           : ("04060903-0000-0000-060e-2b3401010108", 0x4f02, "aafUInt32", False, False),
    "ChunkData"             : ("04070400-0000-0000-060e-2b3401010108", 0x4f03, "Stream", False, False),
    }
),
"BWFImportDescriptor"   : ("0d010101-0101-5000-060e-2b3402060101", "ImportDescriptor", True, {
    "QltyFileSecurityReport": ("04020302-0500-0000-060e-2b3401010105", 0x3d15, "aafUInt32", True, False),
    "QltyFileSecurityWave"  : ("04020302-0600-0000-060e-2b3401010105", 0x3d16, "aafUInt32", True, False),
    "BextCodingHistory"     : ("04020502-0101-0000-060e-2b3401010105", 0x3d21, "aafString", True, False),
    "QltyBasicData"         : ("04020502-0201-0000-060e-2b3401010105", 0x3d22, "aafString", True, False),
    "QltyStartOfModulation" : ("04020502-0301-0000-060e-2b3401010105", 0x3d23, "aafString", True, False),
    "QltyQualityEvent"      : ("04020502-0401-0000-060e-2b3401010105", 0x3d24, "aafString", True, False),
    "QltyEndOfModulation"   : ("04020502-0501-0000-060e-2b3401010105", 0x3d25, "aafString", True, False),
    "QltyQualityParameter"  : ("04020502-0601-0000-060e-2b3401010105", 0x3d26, "aafString", True, False),
    "QltyOperatorComment"   : ("04020502-0701-0000-060e-2b3401010105", 0x3d27, "aafString", True, False),
    "QltyCueSheet"          : ("04020502-0801-0000-060e-2b3401010105", 0x3d28, "aafString", True, False),
    "UnknownBWFChunks"      : ("06010104-060f-0000-060e-2b3401010108", 0x3d33, "kAAFTypeID_RIFFChunkStrongReferenceVector", True, False),
    }
),
"MPEGVideoDescriptor"   : ("0d010101-0101-5100-060e-2b3402060101", "CDCIDescriptor", True, {
    "SingleSequence"        : ("04010602-0102-0000-060e-2b3401010105", 0x0000, "Boolean", True, False),
    "ConstantBPictureCount" : ("04010602-0103-0000-060e-2b3401010105", 0x0000, "Boolean", True, False),
    "CodedContentScanning"  : ("04010602-0104-0000-060e-2b3401010105", 0x0000, "ContentScanningType", True, False),
    "LowDelay"              : ("04010602-0105-0000-060e-2b3401010105", 0x0000, "Boolean", True, False),
    "ClosedGOP"             : ("04010602-0106-0000-060e-2b3401010105", 0x0000, "Boolean", True, False),
    "IdenticalGOP"          : ("04010602-0107-0000-060e-2b3401010105", 0x0000, "Boolean", True, False),
    "MaxGOP"                : ("04010602-0108-0000-060e-2b3401010105", 0x0000, "aafUInt16", True, False),
    "MaxBPictureCount"      : ("04010602-0109-0000-060e-2b3401010105", 0x0000, "aafUInt16", True, False),
    "BitRate"               : ("04010602-010b-0000-060e-2b3401010105", 0x0000, "aafUInt32", True, False),
    "ProfileAndLevel"       : ("04010602-010a-0000-060e-2b3401010105", 0x0000, "aafUInt8", True, False),
    }
),
"MetaDefinition"        : ("0d010101-0224-0000-060e-2b3402060101", None, False, {
    "Identification"        : ("06010107-1300-0000-060e-2b3401010102", 0x0005, "AUID", False, True),
    "Name"                  : ("03020401-0201-0000-060e-2b3401010102", 0x0006, "aafString", False, False),
    "Description"           : ("06010107-1401-0000-060e-2b3401010102", 0x0007, "aafString", True, False),
    }
),
"ClassDefinition"       : ("0d010101-0201-0000-060e-2b3402060101", "MetaDefinition", True, {
    "ParentClass"           : ("06010107-0100-0000-060e-2b3401010102", 0x0008, "ClassDefinitionWeakReference", False, False),
    "Properties"            : ("06010107-0200-0000-060e-2b3401010102", 0x0009, "kAAFTypeID_PropertyDefinitionStrongReferenceSet", True, False),
    "IsConcrete"            : ("06010107-0300-0000-060e-2b3401010102", 0x000a, "Boolean", False, False),
    }
),
"PropertyDefinition"    : ("0d010101-0202-0000-060e-2b3402060101", "MetaDefinition", True, {
    "Type"                  : ("06010107-0400-0000-060e-2b3401010102", 0x000b, "AUID", False, False),
    "IsOptional"            : ("03010202-0100-0000-060e-2b3401010102", 0x000c, "Boolean", False, False),
    "LocalIdentification"   : ("06010107-0500-0000-060e-2b3401010102", 0x000d, "aafUInt16", False, False),
    "IsUniqueIdentifier"    : ("06010107-0600-0000-060e-2b3401010102", 0x000e, "Boolean", True, False),
    }
),
"TypeDefinition"        : ("0d010101-0203-0000-060e-2b3402060101", "MetaDefinition", False, {
    }
),
"TypeDefinitionInteger" : ("0d010101-0204-0000-060e-2b3402060101", "TypeDefinition", True, {
    "Size"                  : ("03010203-0100-0000-060e-2b3401010102", 0x000f, "aafUInt8", False, False),
    "IsSigned"              : ("03010203-0200-0000-060e-2b3401010102", 0x0010, "Boolean", False, False),
    }
),
"TypeDefinitionStrongObjectReference" : ("0d010101-0205-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ReferencedType"        : ("06010107-0900-0000-060e-2b3401010102", 0x0011, "ClassDefinitionWeakReference", False, False),
    }
),
"TypeDefinitionWeakObjectReference" : ("0d010101-0206-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ReferencedType"        : ("06010107-0a00-0000-060e-2b3401010102", 0x0012, "ClassDefinitionWeakReference", False, False),
    "TargetSet"             : ("03010203-0b00-0000-060e-2b3401010102", 0x0013, "aafAUIDArray", False, False),
    }
),
"TypeDefinitionEnumeration" : ("0d010101-0207-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ElementType"           : ("06010107-0b00-0000-060e-2b3401010102", 0x0014, "TypeDefinitionWeakReference", False, False),
    "ElementNames"          : ("03010203-0400-0000-060e-2b3401010102", 0x0015, "aafStringArray", False, False),
    "ElementValues"         : ("03010203-0500-0000-060e-2b3401010102", 0x0016, "aafInt64Array", False, False),
    }
),
"TypeDefinitionFixedArray" : ("0d010101-0208-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ElementType"           : ("06010107-0c00-0000-060e-2b3401010102", 0x0017, "TypeDefinitionWeakReference", False, False),
    "ElementCount"          : ("03010203-0300-0000-060e-2b3401010102", 0x0018, "aafUInt32", False, False),
    }
),
"TypeDefinitionVariableArray" : ("0d010101-0209-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ElementType"           : ("06010107-0d00-0000-060e-2b3401010102", 0x0019, "TypeDefinitionWeakReference", False, False),
    }
),
"TypeDefinitionSet"     : ("0d010101-020a-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ElementType"           : ("06010107-0e00-0000-060e-2b3401010102", 0x001a, "TypeDefinitionWeakReference", False, False),
    }
),
"TypeDefinitionString"  : ("0d010101-020b-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ElementType"           : ("06010107-0f00-0000-060e-2b3401010102", 0x001b, "TypeDefinitionWeakReference", False, False),
    }
),
"TypeDefinitionStream"  : ("0d010101-020c-0000-060e-2b3402060101", "TypeDefinition", True, {
    }
),
"TypeDefinitionRecord"  : ("0d010101-020d-0000-060e-2b3402060101", "TypeDefinition", True, {
    "MemberTypes"           : ("06010107-1100-0000-060e-2b3401010102", 0x001c, "kAAFTypeID_TypeDefinitionWeakReferenceVector", False, False),
    "MemberNames"           : ("03010203-0600-0000-060e-2b3401010102", 0x001d, "aafStringArray", False, False),
    }
),
"TypeDefinitionRename"  : ("0d010101-020e-0000-060e-2b3402060101", "TypeDefinition", True, {
    "RenamedType"           : ("06010107-1200-0000-060e-2b3401010102", 0x001e, "TypeDefinitionWeakReference", False, False),
    }
),
"TypeDefinitionExtendibleEnumeration" : ("0d010101-0220-0000-060e-2b3402060101", "TypeDefinition", True, {
    "ElementNames"          : ("03010203-0700-0000-060e-2b3401010102", 0x001f, "aafStringArray", False, False),
    "ElementValues"         : ("03010203-0800-0000-060e-2b3401010102", 0x0020, "aafAUIDArray", False, False),
    }
),
"TypeDefinitionIndirect" : ("0d010101-0221-0000-060e-2b3402060101", "TypeDefinition", True, {
    }
),
"TypeDefinitionOpaque"  : ("0d010101-0222-0000-060e-2b3402060101", "TypeDefinitionIndirect", True, {
    }
),
"TypeDefinitionCharacter" : ("0d010101-0223-0000-060e-2b3402060101", "TypeDefinition", True, {
    }
),
"MetaDictionary"        : ("0d010101-0225-0000-060e-2b3402060101", None, True, {
    "ClassDefinitions"      : ("06010107-0700-0000-060e-2b3401010102", 0x0003, "kAAFTypeID_ClassDefinitionStrongReferenceSet", True, False),
    "TypeDefinitions"       : ("06010107-0800-0000-060e-2b3401010102", 0x0004, "kAAFTypeID_TypeDefinitionStrongReferenceSet", True, False),
    }
),
"DescriptiveObject"     : ("0d010400-0000-0000-060e-2b3402060101", "InterchangeObject", False, {
    }
),
"DescriptiveFramework"  : ("0d010401-0000-0000-060e-2b3402060101", "InterchangeObject", False, {
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
