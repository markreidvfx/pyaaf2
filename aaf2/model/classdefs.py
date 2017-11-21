classdefs = {
"InterchangeObject"  : ( "0d010101-0101-0100-060e-2b3402060101" , "InterchangeObject" , False , {
     "Generation" : ( "05200701-0800-0000-060e-2b3401010102" ,  0x0102 ,  "AUID" , True ,  False ),
     "ObjClass" : ( "06010104-0101-0000-060e-2b3401010102" ,  0x0101 ,  "ClassDefinitionWeakReference" , False ,  False ),
     }
),
"Component"  : ( "0d010101-0101-0200-060e-2b3402060101" , "InterchangeObject" , False , {
     "ComponentAttributeList" : ( "60958184-47b1-11d4-a01c-0004ac969f50" ,  0xFFCC ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "Length" : ( "07020201-0103-0000-060e-2b3401010102" ,  0x0202 ,  "aafLengthType" , True ,  False ),
     "KLVData" : ( "03010210-0400-0000-060e-2b3401010102" ,  0x0203 ,  "kAAFTypeID_KLVDataStrongReferenceVector" , True ,  False ),
     "Attributes" : ( "03010210-0800-0000-060e-2b3401010107" ,  0x0205 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "DataDefinition" : ( "04070100-0000-0000-060e-2b3401010102" ,  0x0201 ,  "DataDefinitionWeakReference" , False ,  False ),
     "UserComments" : ( "03020102-1600-0000-060e-2b3401010107" ,  0x0204 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     }
),
"Segment"  : ( "0d010101-0101-0300-060e-2b3402060101" , "Component" , False , {
     }
),
"EdgeCode"  : ( "0d010101-0101-0400-060e-2b3402060101" , "Segment" , True , {
     "Start" : ( "01040901-0000-0000-060e-2b3401010102" ,  0x0401 ,  "aafPositionType" , False ,  False ),
     "FilmKind" : ( "04100103-0109-0000-060e-2b3401010102" ,  0x0402 ,  "FilmType" , False ,  False ),
     "AvFilmType" : ( "067da182-a750-48ba-995b-b7fd88f3b838" ,  0xFFB4 ,  "aafInt16" , True ,  False ),
     "AvBasePerf" : ( "1fb0160a-6907-45fe-a997-c6818820970e" ,  0xFFB2 ,  "aafUInt8" , True ,  False ),
     "CodeFormat" : ( "04100103-0102-0000-060e-2b3401010101" ,  0x0403 ,  "EdgeType" , False ,  False ),
     "AvEdgeType" : ( "4d783cfa-35da-4566-9a52-2190d5078616" ,  0xFFB3 ,  "aafInt16" , True ,  False ),
     "Header" : ( "01030201-0200-0000-060e-2b3401010102" ,  0x0404 ,  "aafDataValue" , True ,  False ),
     }
),
"EssenceGroup"  : ( "0d010101-0101-0500-060e-2b3402060101" , "Segment" , True , {
     "Choices" : ( "06010104-0601-0000-060e-2b3401010102" ,  0x0501 ,  "kAAFTypeID_SourceReferenceStrongReferenceVector" , False ,  False ),
     "StillFrame" : ( "06010104-0208-0000-060e-2b3401010102" ,  0x0502 ,  "kAAFTypeID_SourceReferenceStrongReference" , True ,  False ),
     "EssenceGroupType" : ( "d9c9bf24-f6b8-11d3-a083-006094eb75cb" ,  0xFFB5 ,  "aafInt32" , True ,  False ),
     }
),
"Event"  : ( "0d010101-0101-0600-060e-2b3402060101" , "Segment" , False , {
     "Comment" : ( "05300404-0100-0000-060e-2b3401010102" ,  0x0602 ,  "aafString" , True ,  False ),
     "Position" : ( "07020103-0303-0000-060e-2b3401010102" ,  0x0601 ,  "aafPositionType" , False ,  False ),
     }
),
"CommentMarker"  : ( "0d010101-0101-0800-060e-2b3402060101" , "Event" , True , {
     "CommentMarkerColor" : ( "e96e6d44-c383-11d3-a069-006094eb75cb" ,  0xFFDE ,  "RGBColor" , True ,  False ),
     "CommentMarkerUSer" : ( "c4c45d9a-0967-11d4-a08a-006094eb75cb" ,  0xFFDD ,  "aafString" , True ,  False ),
     "CommentMarkerTime" : ( "c4c45d9c-0967-11d4-a08a-006094eb75cb" ,  0xFFDB ,  "aafString" , True ,  False ),
     "CommentMarkerIcon" : ( "c4c45d9d-0967-11d4-a08a-006094eb75cb" ,  0xFFD9 ,  "aafInt32" , True ,  False ),
     "CommentMarkerStatus" : ( "c4c45d9e-0967-11d4-a08a-006094eb75cb" ,  0xFFD8 ,  "aafInt32" , True ,  False ),
     "CommentMarkerDate" : ( "c4c45d9b-0967-11d4-a08a-006094eb75cb" ,  0xFFDC ,  "aafString" , True ,  False ),
     "CommentMarkerAttributeList" : ( "c72cc817-aac5-499b-af34-bc47fec1eaa8" ,  0xFFD7 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "Annotation" : ( "06010104-020a-0000-060e-2b3401010102" ,  0x0901 ,  "kAAFTypeID_SourceReferenceStrongReference" , True ,  False ),
     "CommentMarkerAnnotationList" : ( "6d64dd66-e5c7-488f-b0e4-272c932378a6" ,  0xFFDA ,  "aafString" , True ,  False ),
     }
),
"Filler"  : ( "0d010101-0101-0900-060e-2b3402060101" , "Segment" , True , {
     }
),
"OperationGroup"  : ( "0d010101-0101-0a00-060e-2b3402060101" , "Segment" , True , {
     "Rendering" : ( "06010104-0206-0000-060e-2b3401010102" ,  0x0B05 ,  "kAAFTypeID_SourceReferenceStrongReference" , True ,  False ),
     "OpGrpTKMNTrackedParamSetng" : ( "30a42452-069e-11d4-9ffb-0004ac969f50" ,  0xFFC5 ,  "AvidBagOfBits" , True ,  False ),
     "OpGroupLeftLength" : ( "7cd5da62-6a1c-4490-9f6c-f57204ec7dba" ,  0xFFC0 ,  "aafInt32" , True ,  False ),
     "OpGrpTKMNTrackedParamAry" : ( "30a42451-069e-11d4-9ffb-0004ac969f50" ,  0xFFC6 ,  "AvidTKMNTrackedParamArray" , True ,  False ),
     "OpGroupMotionCtlSourceParams" : ( "614406f1-d8e7-469b-bd99-0e70a9a9cd60" ,  0xFFC3 ,  "kAAFTypeID_ParameterStrongReferenceVector" , True ,  False ),
     "OpGroupRightLength" : ( "a7da7356-2021-4f89-97d2-e683307c8dd7" ,  0xFFBF ,  "aafInt32" , True ,  False ),
     "OpGroupMotionCtlOffsetMapAdjust" : ( "77ad6841-08fc-4f53-bd0a-2a6b0b5f94d9" ,  0xFFC4 ,  "Rational" , True ,  False ),
     "Operation" : ( "05300506-0000-0000-060e-2b3401010102" ,  0x0B01 ,  "OperationDefinitionWeakReference" , False ,  False ),
     "BypassOverride" : ( "0530050c-0000-0000-060e-2b3401010102" ,  0x0B04 ,  "aafUInt32" , True ,  False ),
     "OpGroupGraphicsParamStream" : ( "73fe71c5-15f3-4f0e-acb8-b70edfe6ca5c" ,  0xFFC2 ,  "Stream" , True ,  False ),
     "OpGroupAVXParamStream" : ( "b045db5e-87d7-47fb-b862-2a548a1cad60" ,  0xFFC1 ,  "Stream" , True ,  False ),
     "Parameters" : ( "06010104-060a-0000-060e-2b3401010102" ,  0x0B03 ,  "kAAFTypeID_ParameterStrongReferenceVector" , True ,  False ),
     "InputSegments" : ( "06010104-0602-0000-060e-2b3401010102" ,  0x0B02 ,  "kAAFTypeID_SegmentStrongReferenceVector" , True ,  False ),
     "OpGrpTKMNTrackerDataAry" : ( "af913551-04c3-11d4-9ff9-0004ac969f50" ,  0xFFC7 ,  "AvidTKMNTrackerDataArray" , True ,  False ),
     }
),
"NestedScope"  : ( "0d010101-0101-0b00-060e-2b3402060101" , "Segment" , True , {
     "Slots" : ( "06010104-0607-0000-060e-2b3401010102" ,  0x0C01 ,  "kAAFTypeID_SegmentStrongReferenceVector" , False ,  False ),
     }
),
"Pulldown"  : ( "0d010101-0101-0c00-060e-2b3402060101" , "Segment" , True , {
     "PulldownKind" : ( "05401001-0200-0000-060e-2b3401010102" ,  0x0D02 ,  "PulldownKindType" , False ,  False ),
     "PulldownDirection" : ( "05401001-0100-0000-060e-2b3401010102" ,  0x0D03 ,  "PulldownDirectionType" , False ,  False ),
     "PhaseFrame" : ( "05401001-0300-0000-060e-2b3401010102" ,  0x0D04 ,  "aafPhaseFrameType" , False ,  False ),
     "InputSegment" : ( "06010104-0207-0000-060e-2b3401010102" ,  0x0D01 ,  "kAAFTypeID_SegmentStrongReference" , False ,  False ),
     }
),
"ScopeReference"  : ( "0d010101-0101-0d00-060e-2b3402060101" , "Segment" , True , {
     "RelativeScope" : ( "06010103-0300-0000-060e-2b3401010102" ,  0x0E01 ,  "aafUInt32" , False ,  False ),
     "RelativeSlot" : ( "06010103-0400-0000-060e-2b3401010102" ,  0x0E02 ,  "aafUInt32" , False ,  False ),
     "Avid Scope" : ( "9dc9c6cb-479d-4ff6-988a-b6784b90dc43" ,  0xFFCD ,  "aafUInt32" , True ,  False ),
     }
),
"Selector"  : ( "0d010101-0101-0e00-060e-2b3402060101" , "Segment" , True , {
     "Selected" : ( "06010104-0209-0000-060e-2b3401010102" ,  0x0F01 ,  "kAAFTypeID_SegmentStrongReference" , False ,  False ),
     "Alternates" : ( "06010104-0608-0000-060e-2b3401010102" ,  0x0F02 ,  "kAAFTypeID_SegmentStrongReferenceVector" , True ,  False ),
     }
),
"Sequence"  : ( "0d010101-0101-0f00-060e-2b3402060101" , "Segment" , True , {
     "Components" : ( "06010104-0609-0000-060e-2b3401010102" ,  0x1001 ,  "kAAFTypeID_ComponentStrongReferenceVector" , False ,  False ),
     }
),
"SourceReference"  : ( "0d010101-0101-1000-060e-2b3402060101" , "Segment" , False , {
     "ChannelIDs" : ( "06010103-0700-0000-060e-2b3401010107" ,  0x1103 ,  "aafUInt32Array" , True ,  False ),
     "SourceID" : ( "06010103-0100-0000-060e-2b3401010102" ,  0x1101 ,  "MobIDType" , True ,  False ),
     "SourceMobSlotID" : ( "06010103-0200-0000-060e-2b3401010102" ,  0x1102 ,  "aafUInt32" , False ,  False ),
     "MonoSourceSlotIDs" : ( "06010103-0800-0000-060e-2b3401010108" ,  0x1104 ,  "aafUInt32Array" , True ,  False ),
     }
),
"SourceClip"  : ( "0d010101-0101-1100-060e-2b3402060101" , "SourceReference" , True , {
     "FadeOutType" : ( "05300502-0000-0000-060e-2b3401010101" ,  0x1205 ,  "FadeType" , True ,  False ),
     "SubclipFullLength" : ( "660162e5-bbef-4618-8e0b-4b149b661a12" ,  0xFFD6 ,  "aafInt64" , True ,  False ),
     "FadeInLength" : ( "07020201-0105-0200-060e-2b3401010102" ,  0x1202 ,  "aafLengthType" , True ,  False ),
     "FadeInType" : ( "05300501-0000-0000-060e-2b3401010101" ,  0x1203 ,  "FadeType" , True ,  False ),
     "FadeOutLength" : ( "07020201-0105-0300-060e-2b3401010102" ,  0x1204 ,  "aafLengthType" , True ,  False ),
     "StartTime" : ( "07020103-0104-0000-060e-2b3401010102" ,  0x1201 ,  "aafPositionType" , True ,  False ),
     }
),
"Timecode"  : ( "0d010101-0101-1400-060e-2b3402060101" , "Segment" , True , {
     "Start" : ( "07020103-0105-0000-060e-2b3401010102" ,  0x1501 ,  "aafPositionType" , False ,  False ),
     "Drop" : ( "04040101-0500-0000-060e-2b3401010101" ,  0x1503 ,  "Boolean" , False ,  False ),
     "FPS" : ( "04040101-0206-0000-060e-2b3401010102" ,  0x1502 ,  "aafUInt16" , False ,  False ),
     }
),
"Transition"  : ( "0d010101-0101-1700-060e-2b3402060101" , "Component" , True , {
     "OperationGroup" : ( "06010104-0205-0000-060e-2b3401010102" ,  0x1801 ,  "kAAFTypeID_OperationGroupStrongReference" , False ,  False ),
     "CutPoint" : ( "07020103-0106-0000-060e-2b3401010102" ,  0x1802 ,  "aafPositionType" , False ,  False ),
     "TranTKMNTrackedParamAry" : ( "2c04d7ec-179d-11d4-a003-0004ac969f50" ,  0xFFBB ,  "AvidTKMNTrackedParamArray" , True ,  False ),
     "TranTKMNTrackedParamSetngs" : ( "2c04d7ed-179d-11d4-a003-0004ac969f50" ,  0xFFBA ,  "AvidBagOfBits" , True ,  False ),
     "TranTKMNTrackerDataAry" : ( "2c04d7eb-179d-11d4-a003-0004ac969f50" ,  0xFFBC ,  "AvidTKMNTrackerDataArray" , True ,  False ),
     }
),
"ContentStorage"  : ( "0d010101-0101-1800-060e-2b3402060101" , "InterchangeObject" , True , {
     "EssenceData" : ( "06010104-0502-0000-060e-2b3401010102" ,  0x1902 ,  "kAAFTypeID_EssenceDataStrongReferenceSet" , True ,  False ),
     "Mobs" : ( "06010104-0501-0000-060e-2b3401010102" ,  0x1901 ,  "kAAFTypeID_MobStrongReferenceSet" , False ,  False ),
     }
),
"ControlPoint"  : ( "0d010101-0101-1900-060e-2b3402060101" , "InterchangeObject" , True , {
     "Value" : ( "0530050d-0000-0000-060e-2b3401010102" ,  0x1A02 ,  "aafIndirect" , False ,  False ),
     "ControlPointPointProperties" : ( "3c1b48d0-c32c-4ea9-bb9d-35b898527283" ,  0xFFBE ,  "kAAFTypeID_ParameterStrongReferenceVector" , True ,  False ),
     "Time" : ( "07020103-1002-0100-060e-2b3401010102" ,  0x1A03 ,  "Rational" , False ,  False ),
     "EditHint" : ( "05300508-0000-0000-060e-2b3401010102" ,  0x1A04 ,  "EditHintType" , True ,  False ),
     "ControlPointSource" : ( "0e040101-0101-010a-060e-2b3401010101" ,  0xFFBD ,  "aafInt32" , True ,  False ),
     }
),
"DefinitionObject"  : ( "0d010101-0101-1a00-060e-2b3402060101" , "InterchangeObject" , False , {
     "Identification" : ( "01011503-0000-0000-060e-2b3401010102" ,  0x1B01 ,  "AUID" , False ,  True ),
     "Description" : ( "03020301-0201-0000-060e-2b3401010102" ,  0x1B03 ,  "aafString" , True ,  False ),
     "Name" : ( "01070102-0301-0000-060e-2b3401010102" ,  0x1B02 ,  "aafString" , False ,  False ),
     }
),
"DataDefinition"  : ( "0d010101-0101-1b00-060e-2b3402060101" , "DefinitionObject" , True , {
     }
),
"OperationDefinition"  : ( "0d010101-0101-1c00-060e-2b3402060101" , "DefinitionObject" , True , {
     "IsTimeWarp" : ( "05300503-0000-0000-060e-2b3401010101" ,  0x1E02 ,  "Boolean" , True ,  False ),
     "OperationCategory" : ( "0530050a-0000-0000-060e-2b3401010102" ,  0x1E06 ,  "OperationCategoryType" , True ,  False ),
     "ParametersDefined" : ( "06010104-0302-0000-060e-2b3401010102" ,  0x1E09 ,  "kAAFTypeID_ParameterDefinitionWeakReferenceSet" , True ,  False ),
     "DegradeTo" : ( "06010104-0401-0000-060e-2b3401010102" ,  0x1E03 ,  "kAAFTypeID_OperationDefinitionWeakReferenceVector" , True ,  False ),
     "NumberInputs" : ( "05300504-0000-0000-060e-2b3401010101" ,  0x1E07 ,  "aafInt32" , False ,  False ),
     "DataDefinition" : ( "05300509-0000-0000-060e-2b3401010102" ,  0x1E01 ,  "DataDefinitionWeakReference" , False ,  False ),
     "Bypass" : ( "05300505-0000-0000-060e-2b3401010101" ,  0x1E08 ,  "aafUInt32" , True ,  False ),
     }
),
"ParameterDefinition"  : ( "0d010101-0101-1d00-060e-2b3402060101" , "DefinitionObject" , True , {
     "Type" : ( "06010104-0106-0000-060e-2b3401010102" ,  0x1F01 ,  "TypeDefinitionWeakReference" , False ,  False ),
     "DisplayUnits" : ( "0530050b-0100-0000-060e-2b3401010102" ,  0x1F03 ,  "aafString" , True ,  False ),
     }
),
"PluginDefinition"  : ( "0d010101-0101-1e00-060e-2b3402060101" , "DefinitionObject" , True , {
     "Manufacturer" : ( "010a0101-0101-0000-060e-2b3401010102" ,  0x2206 ,  "aafString" , True ,  False ),
     "MinPluginAPI" : ( "05200909-0000-0000-060e-2b3401010102" ,  0x2210 ,  "VersionType" , True ,  False ),
     "VersionString" : ( "03030301-0201-0000-060e-2b3401010102" ,  0x2205 ,  "aafString" , True ,  False ),
     "Platform" : ( "05200902-0000-0000-060e-2b3401010102" ,  0x2209 ,  "AUID" , True ,  False ),
     "MaxPlatformVersion" : ( "05200904-0000-0000-060e-2b3401010102" ,  0x220B ,  "VersionType" , True ,  False ),
     "MaxEngineVersion" : ( "05200907-0000-0000-060e-2b3401010102" ,  0x220E ,  "VersionType" , True ,  False ),
     "DefinitionObject" : ( "0520090f-0000-0000-060e-2b3401010102" ,  0x2216 ,  "AUID" , True ,  False ),
     "ManufacturerID" : ( "010a0101-0300-0000-060e-2b3401010102" ,  0x2208 ,  "AUID" , True ,  False ),
     "Locators" : ( "0520090d-0000-0000-060e-2b3401010102" ,  0x2214 ,  "kAAFTypeID_LocatorStrongReferenceVector" , True ,  False ),
     "Authentication" : ( "0520090e-0000-0000-060e-2b3401010102" ,  0x2215 ,  "Boolean" , True ,  False ),
     "ManufacturerInfo" : ( "06010104-020b-0000-060e-2b3401010102" ,  0x2207 ,  "kAAFTypeID_NetworkLocatorStrongReference" , True ,  False ),
     "Accelerator" : ( "0520090c-0000-0000-060e-2b3401010102" ,  0x2213 ,  "Boolean" , True ,  False ),
     "SoftwareOnly" : ( "0520090b-0000-0000-060e-2b3401010102" ,  0x2212 ,  "Boolean" , True ,  False ),
     "MinEngineVersion" : ( "05200906-0000-0000-060e-2b3401010102" ,  0x220D ,  "VersionType" , True ,  False ),
     "MinPlatformVersion" : ( "05200903-0000-0000-060e-2b3401010102" ,  0x220A ,  "VersionType" , True ,  False ),
     "MaxPluginAPI" : ( "0520090a-0000-0000-060e-2b3401010102" ,  0x2211 ,  "VersionType" , True ,  False ),
     "PluginAPI" : ( "05200908-0000-0000-060e-2b3401010102" ,  0x220F ,  "AUID" , True ,  False ),
     "VersionNumber" : ( "03030301-0300-0000-060e-2b3401010102" ,  0x2204 ,  "VersionType" , False ,  False ),
     "PluginCategory" : ( "05200901-0000-0000-060e-2b3401010102" ,  0x2203 ,  "PluginCategoryType" , False ,  False ),
     "Engine" : ( "05200905-0000-0000-060e-2b3401010102" ,  0x220C ,  "AUID" , True ,  False ),
     }
),
"CodecDefinition"  : ( "0d010101-0101-1f00-060e-2b3402060101" , "DefinitionObject" , True , {
     "DataDefinitions" : ( "06010104-0301-0000-060e-2b3401010102" ,  0x2302 ,  "kAAFTypeID_DataDefinitionWeakReferenceVector" , False ,  False ),
     "FileDescriptorClass" : ( "06010104-0107-0000-060e-2b3401010102" ,  0x2301 ,  "ClassDefinitionWeakReference" , False ,  False ),
     }
),
"ContainerDefinition"  : ( "0d010101-0101-2000-060e-2b3402060101" , "DefinitionObject" , True , {
     "EssenceIsIdentified" : ( "03010201-0300-0000-060e-2b3401010101" ,  0x2401 ,  "Boolean" , True ,  False ),
     }
),
"InterpolationDefinition"  : ( "0d010101-0101-2100-060e-2b3402060101" , "DefinitionObject" , True , {
     }
),
"Dictionary"  : ( "0d010101-0101-2200-060e-2b3402060101" , "InterchangeObject" , True , {
     "OperationDefinitions" : ( "06010104-0503-0000-060e-2b3401010102" ,  0x2603 ,  "kAAFTypeID_OperationDefinitionStrongReferenceSet" , True ,  False ),
     "KLVDataDefinitions" : ( "06010104-050a-0000-060e-2b3401010107" ,  0x260A ,  "kAAFTypeID_KLVDataDefinitionStrongReferenceSet" , True ,  False ),
     "InterpolationDefinitions" : ( "06010104-0509-0000-060e-2b3401010102" ,  0x2609 ,  "kAAFTypeID_InterpolationDefinitionStrongReferenceSet" , True ,  False ),
     "ParameterDefinitions" : ( "06010104-0504-0000-060e-2b3401010102" ,  0x2604 ,  "kAAFTypeID_ParameterDefinitionStrongReferenceSet" , True ,  False ),
     "PluginDefinitions" : ( "06010104-0506-0000-060e-2b3401010102" ,  0x2606 ,  "kAAFTypeID_PluginDefinitionStrongReferenceSet" , True ,  False ),
     "ContainerDefinitions" : ( "06010104-0508-0000-060e-2b3401010102" ,  0x2608 ,  "kAAFTypeID_ContainerDefinitionStrongReferenceSet" , True ,  False ),
     "DataDefinitions" : ( "06010104-0505-0000-060e-2b3401010102" ,  0x2605 ,  "kAAFTypeID_DataDefinitionStrongReferenceSet" , True ,  False ),
     "CodecDefinitions" : ( "06010104-0507-0000-060e-2b3401010102" ,  0x2607 ,  "kAAFTypeID_CodecDefinitionStrongReferenceSet" , True ,  False ),
     "TaggedValueDefinitions" : ( "06010104-050b-0000-060e-2b3401010107" ,  0x260B ,  "kAAFTypeID_TaggedValueDefinitionStrongReferenceSet" , True ,  False ),
     }
),
"EssenceData"  : ( "0d010101-0101-2300-060e-2b3402060101" , "InterchangeObject" , True , {
     "SampleIndex" : ( "06010102-0100-0000-060e-2b3401010102" ,  0x2B01 ,  "Stream" , True ,  False ),
     "MobID" : ( "06010106-0100-0000-060e-2b3401010102" ,  0x2701 ,  "MobIDType" , False ,  True ),
     "Data" : ( "04070200-0000-0000-060e-2b3401010102" ,  0x2702 ,  "Stream" , False ,  False ),
     }
),
"EssenceDescriptor"  : ( "0d010101-0101-2400-060e-2b3402060101" , "InterchangeObject" , False , {
     "SubDescriptors" : ( "06010104-0610-0000-060e-2b3401010109" ,  0xFFF3 ,  "kAAFTypeID_SubDescriptorStrongReferenceVector" , True ,  False ),
     "MediaContainer" : ( "13980e2b-2f30-44ec-bdb0-3b730da56562" ,  0xFFF1 ,  "aafString" , True ,  False ),
     "Locator" : ( "06010104-0603-0000-060e-2b3401010102" ,  0x2F01 ,  "kAAFTypeID_LocatorStrongReferenceVector" , True ,  False ),
     "MediaContainerGUID" : ( "92790417-0131-4a05-898d-167691e11ca1" ,  0xFFF2 ,  "AUID" , True ,  False ),
     }
),
"FileDescriptor"  : ( "0d010101-0101-2500-060e-2b3402060101" , "EssenceDescriptor" , False , {
     "ContainerFormat" : ( "06010104-0102-0000-060e-2b3401010102" ,  0x3004 ,  "ContainerDefinitionWeakReference" , True ,  False ),
     "CodecDefinition" : ( "06010104-0103-0000-060e-2b3401010102" ,  0x3005 ,  "CodecDefinitionWeakReference" , True ,  False ),
     "SampleRate" : ( "04060101-0000-0000-060e-2b3401010101" ,  0x3001 ,  "Rational" , False ,  False ),
     "LinkedSlotID" : ( "06010103-0500-0000-060e-2b3401010105" ,  0x3006 ,  "aafUInt32" , True ,  False ),
     "Length" : ( "04060102-0000-0000-060e-2b3401010101" ,  0x3002 ,  "aafLengthType" , False ,  False ),
     }
),
"DigitalImageDescriptor"  : ( "0d010101-0101-2700-060e-2b3402060101" , "FileDescriptor" , False , {
     "SourceBox" : ( "0e040101-0101-0108-060e-2b3401010101" ,  0xFFE6 ,  "BoundsBox" , True ,  False ),
     "SampledYOffset" : ( "04010501-0a00-0000-060e-2b3401010101" ,  0x3207 ,  "aafInt32" , True ,  False ),
     "ColorPrimaries" : ( "04010201-0106-0100-060e-2b3401010109" ,  0x3219 ,  "ColorPrimariesType" , True ,  False ),
     "ActiveFormatDescriptor" : ( "04010302-0900-0000-060e-2b3401010105" ,  0x3218 ,  "aafUInt8" , True ,  False ),
     "VideoLineMap" : ( "04010302-0500-0000-060e-2b3401010102" ,  0x320D ,  "aafInt32Array" , False ,  False ),
     "AvidEssenceElementSizeKind" : ( "0e040101-0101-0110-060e-2b3401010101" ,  0xFFE5 ,  "AvidEssenceElementSizeKind" , True ,  False ),
     "Compression" : ( "04010601-0000-0000-060e-2b3401010102" ,  0x3201 ,  "AUID" , True ,  False ),
     "FieldDominance" : ( "04010301-0600-0000-060e-2b3401010102" ,  0x3212 ,  "FieldNumber" , True ,  False ),
     "SampledHeight" : ( "04010501-0700-0000-060e-2b3401010101" ,  0x3204 ,  "aafUInt32" , True ,  False ),
     "ValidBox" : ( "0e040101-0101-0106-060e-2b3401010101" ,  0xFFE8 ,  "BoundsBox" , True ,  False ),
     "StoredHeight" : ( "04010502-0100-0000-060e-2b3401010101" ,  0x3202 ,  "aafUInt32" , False ,  False ),
     "SignalStandard" : ( "04050113-0000-0000-060e-2b3401010105" ,  0x3215 ,  "SignalStandardType" , True ,  False ),
     "DataOffset" : ( "bfde81e4-bcc8-4abd-a80e-214dc0f14684" ,  0xFFEB ,  "aafInt32" , True ,  False ),
     "FirstFrameOffset" : ( "ce2aca4e-51ab-11d3-a024-006094eb75cb" ,  0xFFEF ,  "aafInt32" , True ,  False ),
     "AlphaTransparency" : ( "05200102-0000-0000-060e-2b3401010102" ,  0x320F ,  "AlphaTransparencyType" , True ,  False ),
     "StoredWidth" : ( "04010502-0200-0000-060e-2b3401010101" ,  0x3203 ,  "aafUInt32" , False ,  False ),
     "FieldEndOffset" : ( "04180103-0000-0000-060e-2b3401010102" ,  0x3214 ,  "aafUInt32" , True ,  False ),
     "DisplayYOffset" : ( "04010501-0e00-0000-060e-2b3401010101" ,  0x320B ,  "aafInt32" , True ,  False ),
     "FramingBox" : ( "0e040101-0101-010c-060e-2b3401010101" ,  0xFFE9 ,  "BoundsBox" , True ,  False ),
     "FieldStartOffset" : ( "04180102-0000-0000-060e-2b3401010102" ,  0x3213 ,  "aafUInt32" , True ,  False ),
     "ImageAspectRatio" : ( "04010101-0100-0000-060e-2b3401010101" ,  0x320E ,  "Rational" , False ,  False ),
     "SampledWidth" : ( "04010501-0800-0000-060e-2b3401010101" ,  0x3205 ,  "aafUInt32" , True ,  False ),
     "DisplayXOffset" : ( "04010501-0d00-0000-060e-2b3401010101" ,  0x320A ,  "aafInt32" , True ,  False ),
     "CodingEquations" : ( "04010201-0103-0100-060e-2b3401010102" ,  0x321A ,  "CodingEquationsType" , True ,  False ),
     "DisplayWidth" : ( "04010501-0c00-0000-060e-2b3401010101" ,  0x3209 ,  "aafUInt32" , True ,  False ),
     "ResolutionID" : ( "ce2aca4d-51ab-11d3-a024-006094eb75cb" ,  0xFFF0 ,  "aafInt32" , True ,  False ),
     "DisplayHeight" : ( "04010501-0b00-0000-060e-2b3401010101" ,  0x3208 ,  "aafUInt32" , True ,  False ),
     "TransferCharacteristic" : ( "04010201-0101-0200-060e-2b3401010102" ,  0x3210 ,  "TransferCharacteristicType" , True ,  False ),
     "SampledXOffset" : ( "04010501-0900-0000-060e-2b3401010101" ,  0x3206 ,  "aafInt32" , True ,  False ),
     "FrameSampleSize" : ( "ce2aca50-51ab-11d3-a024-006094eb75cb" ,  0xFFED ,  "aafInt32" , True ,  False ),
     "DisplayF2Offset" : ( "04010302-0700-0000-060e-2b3401010105" ,  0x3217 ,  "aafInt32" , True ,  False ),
     "FrameLayout" : ( "04010301-0400-0000-060e-2b3401010101" ,  0x320C ,  "LayoutType" , False ,  False ),
     "FrameStartOffset" : ( "c8a0bd74-a247-4297-a52c-4458bffa1fc6" ,  0xFFEA ,  "aafInt32" , True ,  False ),
     "StoredF2Offset" : ( "04010302-0800-0000-060e-2b3401010105" ,  0x3216 ,  "aafInt32" , True ,  False ),
     "FrameIndexByteOrder" : ( "b57e925d-170d-11d4-a08f-006094eb75cb" ,  0xFFEC ,  "aafUInt16" , True ,  False ),
     "EssenceBox" : ( "0e040101-0101-0107-060e-2b3401010101" ,  0xFFE7 ,  "BoundsBox" , True ,  False ),
     "ImageAlignmentFactor" : ( "04180101-0000-0000-060e-2b3401010102" ,  0x3211 ,  "aafUInt32" , True ,  False ),
     "ImageSize" : ( "ce2aca4f-51ab-11d3-a024-006094eb75cb" ,  0xFFEE ,  "aafInt32" , True ,  False ),
     }
),
"CDCIDescriptor"  : ( "0d010101-0101-2800-060e-2b3402060101" , "DigitalImageDescriptor" , True , {
     "ImageStartAlignment" : ( "506f8de5-54a1-11d3-a029-006094eb75cb" ,  0xFFE2 ,  "aafUInt32" , True ,  False ),
     "WhiteReferenceLevel" : ( "04010503-0400-0000-060e-2b3401010101" ,  0x3305 ,  "aafUInt32" , True ,  False ),
     "HorizontalSubsampling" : ( "04010501-0500-0000-060e-2b3401010101" ,  0x3302 ,  "aafUInt32" , False ,  False ),
     "ComponentWidth" : ( "04010503-0a00-0000-060e-2b3401010102" ,  0x3301 ,  "aafUInt32" , False ,  False ),
     "OffsetToFrameIndexes" : ( "9d15fca3-54c5-11d3-a029-006094eb75cb" ,  0xFFE4 ,  "aafInt32" , True ,  False ),
     "BlackReferenceLevel" : ( "04010503-0300-0000-060e-2b3401010101" ,  0x3304 ,  "aafUInt32" , True ,  False ),
     "ReversedByteOrder" : ( "03010201-0a00-0000-060e-2b3401010105" ,  0x330B ,  "Boolean" , True ,  False ),
     "ColorRange" : ( "04010503-0500-0000-060e-2b3401010102" ,  0x3306 ,  "aafUInt32" , True ,  False ),
     "ColorSiting" : ( "04010501-0600-0000-060e-2b3401010101" ,  0x3303 ,  "ColorSitingType" , True ,  False ),
     "PaddingBits" : ( "04180104-0000-0000-060e-2b3401010102" ,  0x3307 ,  "aafInt16" , True ,  False ),
     "VerticalSubsampling" : ( "04010501-1000-0000-060e-2b3401010102" ,  0x3308 ,  "aafUInt32" , True ,  False ),
     "OffsetToFrameIndexes64" : ( "298eb260-30b6-4e30-8c90-cf63aa793c34" ,  0xFFE3 ,  "aafInt64" , True ,  False ),
     "AlphaSamplingWidth" : ( "04010503-0700-0000-060e-2b3401010102" ,  0x3309 ,  "aafUInt32" , True ,  False ),
     }
),
"RGBADescriptor"  : ( "0d010101-0101-2900-060e-2b3402060101" , "DigitalImageDescriptor" , True , {
     "Palette" : ( "04010503-0800-0000-060e-2b3401010102" ,  0x3403 ,  "aafDataValue" , True ,  False ),
     "AlphaMinRef" : ( "04010503-0e00-0000-060e-2b3401010105" ,  0x3409 ,  "aafUInt32" , True ,  False ),
     "OffsetToFrameIndexes" : ( "0e040101-0101-010d-060e-2b3401010101" ,  0xFFE1 ,  "aafInt64" , True ,  False ),
     "PixelLayout" : ( "04010503-0600-0000-060e-2b3401010102" ,  0x3401 ,  "aafRGBALayout" , False ,  False ),
     "AlphaMaxRef" : ( "04010503-0d00-0000-060e-2b3401010105" ,  0x3408 ,  "aafUInt32" , True ,  False ),
     "ScanningDirection" : ( "04010404-0100-0000-060e-2b3401010105" ,  0x3405 ,  "ScanningDirectionType" , True ,  False ),
     "ComponentMaxRef" : ( "04010503-0b00-0000-060e-2b3401010105" ,  0x3406 ,  "aafUInt32" , True ,  False ),
     "ComponentMinRef" : ( "04010503-0c00-0000-060e-2b3401010105" ,  0x3407 ,  "aafUInt32" , True ,  False ),
     "PaletteLayout" : ( "04010503-0900-0000-060e-2b3401010102" ,  0x3404 ,  "aafRGBALayout" , True ,  False ),
     }
),
"TapeDescriptor"  : ( "0d010101-0101-2e00-060e-2b3402060101" , "EssenceDescriptor" , True , {
     "TapeBatchNumber" : ( "04100101-0601-0000-060e-2b3401010102" ,  0x3A07 ,  "aafString" , True ,  False ),
     "ColorFrame" : ( "9548b03a-15fb-11d4-a08f-006094eb75cb" ,  0xFFDF ,  "aafInt32" , True ,  False ),
     "VideoSignal" : ( "04010401-0100-0000-060e-2b3401010102" ,  0x3A02 ,  "VideoSignalType" , True ,  False ),
     "Model" : ( "04100101-0201-0000-060e-2b3401010102" ,  0x3A06 ,  "aafString" , True ,  False ),
     "ManufacturerID" : ( "04100101-0401-0000-060e-2b3401010102" ,  0x3A05 ,  "aafString" , True ,  False ),
     "TapeStock" : ( "04100101-0501-0000-060e-2b3401010102" ,  0x3A08 ,  "aafString" , True ,  False ),
     "Length" : ( "04100101-0300-0000-060e-2b3401010102" ,  0x3A04 ,  "aafUInt32" , True ,  False ),
     "TapeFormat" : ( "0d010101-0101-0100-060e-2b3401010102" ,  0x3A03 ,  "TapeFormatType" , True ,  False ),
     "FormFactor" : ( "04100101-0101-0000-060e-2b3401010102" ,  0x3A01 ,  "TapeCaseType" , True ,  False ),
     }
),
"Header"  : ( "0d010101-0101-2f00-060e-2b3402060101" , "InterchangeObject" , True , {
     "EssenceFileMobID" : ( "abf1b771-8efd-4802-8b2f-680dff611381" ,  0xFFFE ,  "MobIDType" , True ,  False ),
     "IdentificationList" : ( "06010104-0604-0000-060e-2b3401010102" ,  0x3B06 ,  "kAAFTypeID_IdentificationStrongReferenceVector" , False ,  False ),
     "MasterMobID" : ( "ffdd41e1-ae2c-49c6-ae58-78e041454179" ,  0xFFFF ,  "MobIDType" , True ,  False ),
     "Version" : ( "03010201-0500-0000-060e-2b3401010102" ,  0x3B05 ,  "VersionType" , False ,  False ),
     "DescriptiveSchemes" : ( "01020210-0202-0000-060e-2b3401010105" ,  0x3B0B ,  "AUIDSet" , True ,  False ),
     "ByteOrder" : ( "03010201-0200-0000-060e-2b3401010101" ,  0x3B01 ,  "aafInt16" , False ,  False ),
     "Content" : ( "06010104-0201-0000-060e-2b3401010102" ,  0x3B03 ,  "kAAFTypeID_ContentStorageStrongReference" , False ,  False ),
     "OperationalPattern" : ( "01020203-0000-0000-060e-2b3401010105" ,  0x3B09 ,  "AUID" , True ,  False ),
     "LastModified" : ( "07020110-0204-0000-060e-2b3401010102" ,  0x3B02 ,  "TimeStamp" , False ,  False ),
     "AudioRateAdjustmentFactor" : ( "b7d51ad5-650b-4d3a-8596-99b579e177a6" ,  0xFFFB ,  "aafUInt16" , True ,  False ),
     "ObjectModelVersion" : ( "03010201-0400-0000-060e-2b3401010102" ,  0x3B07 ,  "aafUInt32" , True ,  False ),
     "ProjectEditRate" : ( "f36546b1-387c-4ee9-8c70-a718467ae486" ,  0xFFFC ,  "Rational" , True ,  False ),
     "ProjectName" : ( "62fc3717-492d-42bf-a5fb-7b25f61594b9" ,  0xFFFD ,  "aafString" , True ,  False ),
     "EssenceContainers" : ( "01020210-0201-0000-060e-2b3401010105" ,  0x3B0A ,  "AUIDSet" , True ,  False ),
     "Dictionary" : ( "06010104-0202-0000-060e-2b3401010102" ,  0x3B04 ,  "kAAFTypeID_DictionaryStrongReference" , False ,  False ),
     }
),
"Identification"  : ( "0d010101-0101-3000-060e-2b3402060101" , "InterchangeObject" , True , {
     "CompanyName" : ( "05200701-0201-0000-060e-2b3401010102" ,  0x3C01 ,  "aafString" , False ,  False ),
     "ProductVersion" : ( "05200701-0400-0000-060e-2b3401010102" ,  0x3C03 ,  "ProductVersion" , True ,  False ),
     "Platform" : ( "05200701-0601-0000-060e-2b3401010102" ,  0x3C08 ,  "aafString" , True ,  False ),
     "GenerationAUID" : ( "05200701-0100-0000-060e-2b3401010102" ,  0x3C09 ,  "AUID" , False ,  False ),
     "ProductID" : ( "05200701-0700-0000-060e-2b3401010102" ,  0x3C05 ,  "AUID" , False ,  False ),
     "Date" : ( "07020110-0203-0000-060e-2b3401010102" ,  0x3C06 ,  "TimeStamp" , False ,  False ),
     "ProductName" : ( "05200701-0301-0000-060e-2b3401010102" ,  0x3C02 ,  "aafString" , False ,  False ),
     "ProductVersionString" : ( "05200701-0501-0000-060e-2b3401010102" ,  0x3C04 ,  "aafString" , False ,  False ),
     "ToolkitVersion" : ( "05200701-0a00-0000-060e-2b3401010102" ,  0x3C07 ,  "ProductVersion" , True ,  False ),
     }
),
"Locator"  : ( "0d010101-0101-3100-060e-2b3402060101" , "InterchangeObject" , False , {
     }
),
"NetworkLocator"  : ( "0d010101-0101-3200-060e-2b3402060101" , "Locator" , True , {
     "URLString" : ( "01020101-0100-0000-060e-2b3401010101" ,  0x4001 ,  "aafString" , False ,  False ),
     }
),
"Mob"  : ( "0d010101-0101-3400-060e-2b3402060101" , "InterchangeObject" , False , {
     "Attributes" : ( "03010210-0700-0000-060e-2b3401010107" ,  0x4409 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "MobAttributeList" : ( "60958183-47b1-11d4-a01c-0004ac969f50" ,  0xFFF9 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "UserComments" : ( "03020102-0c00-0000-060e-2b3401010102" ,  0x4406 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "SubclipFullLength" : ( "1262bf7b-fce2-4dfe-a0f6-ceec047c80aa" ,  0xFFF7 ,  "aafInt64" , True ,  False ),
     "MobID" : ( "01011510-0000-0000-060e-2b3401010101" ,  0x4401 ,  "MobIDType" , False ,  True ),
     "Slots" : ( "06010104-0605-0000-060e-2b3401010102" ,  0x4403 ,  "kAAFTypeID_MobSlotStrongReferenceVector" , False ,  False ),
     "AppCode" : ( "96c46992-4f62-11d3-a022-006094eb75cb" ,  0xFFFA ,  "aafInt32" , True ,  False ),
     "FileMobRate" : ( "0e040101-0101-010f-060e-2b3401010101" ,  0xFFF5 ,  "Rational" , True ,  False ),
     "ConvertFrameRate" : ( "d4243bd4-0142-4595-a8f3-f2eba54244de" ,  0xFFF8 ,  "Boolean" , True ,  False ),
     "SubclipBegin" : ( "aa24b657-fcbb-4921-951d-3a2038396722" ,  0xFFF6 ,  "aafInt64" , True ,  False ),
     "LastModified" : ( "07020110-0205-0000-060e-2b3401010102" ,  0x4404 ,  "TimeStamp" , False ,  False ),
     "CreationTime" : ( "07020110-0103-0000-060e-2b3401010102" ,  0x4405 ,  "TimeStamp" , False ,  False ),
     "KLVData" : ( "03010210-0300-0000-060e-2b3401010102" ,  0x4407 ,  "kAAFTypeID_KLVDataStrongReferenceVector" , True ,  False ),
     "Name" : ( "01030302-0100-0000-060e-2b3401010101" ,  0x4402 ,  "aafString" , True ,  False ),
     "UsageCode" : ( "05010108-0000-0000-060e-2b3401010107" ,  0x4408 ,  "UsageType" , True ,  False ),
     }
),
"CompositionMob"  : ( "0d010101-0101-3500-060e-2b3402060101" , "Mob" , True , {
     "DefFadeType" : ( "05300201-0000-0000-060e-2b3401010101" ,  0x4502 ,  "FadeType" , True ,  False ),
     "DefaultFadeLength" : ( "07020201-0105-0100-060e-2b3401010102" ,  0x4501 ,  "aafLengthType" , True ,  False ),
     "Rendering" : ( "06010104-010a-0000-060e-2b3401010108" ,  0x4504 ,  "MobIDType" , True ,  False ),
     "DefFadeEditUnit" : ( "05300403-0000-0000-060e-2b3401010102" ,  0x4503 ,  "Rational" , True ,  False ),
     }
),
"MasterMob"  : ( "0d010101-0101-3600-060e-2b3402060101" , "Mob" , True , {
     }
),
"SourceMob"  : ( "0d010101-0101-3700-060e-2b3402060101" , "Mob" , True , {
     "EssenceDescription" : ( "06010104-0203-0000-060e-2b3401010102" ,  0x4701 ,  "kAAFTypeID_EssenceDescriptorStrongReference" , False ,  False ),
     }
),
"MobSlot"  : ( "0d010101-0101-3800-060e-2b3402060101" , "InterchangeObject" , False , {
     "SlotID" : ( "01070101-0000-0000-060e-2b3401010102" ,  0x4801 ,  "aafUInt32" , False ,  False ),
     "SlotName" : ( "01070102-0100-0000-060e-2b3401010102" ,  0x4802 ,  "aafString" , True ,  False ),
     "PhysicalTrackNumber" : ( "01040103-0000-0000-060e-2b3401010102" ,  0x4804 ,  "aafUInt32" , True ,  False ),
     "Segment" : ( "06010104-0204-0000-060e-2b3401010102" ,  0x4803 ,  "kAAFTypeID_SegmentStrongReference" , False ,  False ),
     }
),
"EventMobSlot"  : ( "0d010101-0101-3900-060e-2b3402060101" , "MobSlot" , True , {
     "EventSlotOrigin" : ( "07020103-010b-0000-060e-2b3401010105" ,  0x4902 ,  "aafPositionType" , True ,  False ),
     "EditRate" : ( "05300402-0000-0000-060e-2b3401010102" ,  0x4901 ,  "Rational" , False ,  False ),
     }
),
"StaticMobSlot" : ( "0d010101-0101-3a00-060e-2b3402060101", "MobSlot", True , {
    }
),
"TimelineMobSlot"  : ( "0d010101-0101-3b00-060e-2b3402060101" , "MobSlot" , True , {
     "TimelineMobAttributeList" : ( "107f8331-1914-4234-b2c4-5a3eb755b7ca" ,  0xFFF4 ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "MarkOut" : ( "07020103-0203-0000-060e-2b3401010107" ,  0x4B04 ,  "aafPositionType" , True ,  False ),
     "UserPos" : ( "07020103-010d-0000-060e-2b3401010107" ,  0x4B05 ,  "aafPositionType" , True ,  False ),
     "MarkIn" : ( "07020103-010c-0000-060e-2b3401010107" ,  0x4B03 ,  "aafPositionType" , True ,  False ),
     "EditRate" : ( "05300405-0000-0000-060e-2b3401010102" ,  0x4B01 ,  "Rational" , False ,  False ),
     "Origin" : ( "07020103-0103-0000-060e-2b3401010102" ,  0x4B02 ,  "aafPositionType" , False ,  False ),
     }
),
"Parameter"  : ( "0d010101-0101-3c00-060e-2b3402060101" , "InterchangeObject" , False , {
     "IsSilent" : ( "967dbcc7-4ba6-4b57-b8e8-3a0fbc550353" ,  0xFFD5 ,  "Boolean" , True ,  False ),
     "IsEnabled" : ( "0e040101-0101-010b-060e-2b3401010101" ,  0xFFD4 ,  "Boolean" , True ,  False ),
     "Definition" : ( "06010104-0104-0000-060e-2b3401010102" ,  0x4C01 ,  "AUID" , False ,  False ),
     }
),
"ConstantValue"  : ( "0d010101-0101-3d00-060e-2b3402060101" , "Parameter" , True , {
     "Value" : ( "05300507-0000-0000-060e-2b3401010102" ,  0x4D01 ,  "aafIndirect" , False ,  False ),
     }
),
"VaryingValue"  : ( "0d010101-0101-3e00-060e-2b3402060101" , "Parameter" , True , {
     "VVal_FieldCount" : ( "2902558b-acfa-439e-a1cd-9fa1e8f891ef" ,  0xFFB9 ,  "aafInt16" , True ,  False ),
     "Interpolation" : ( "06010104-0105-0000-060e-2b3401010102" ,  0x4E01 ,  "InterpolationDefinitionWeakReference" , False ,  False ),
     "VVal_Extrapolation" : ( "8f2b8bae-b685-4939-b3a5-6373633b3e6c" ,  0xFFB8 ,  "AUID" , True ,  False ),
     "PointList" : ( "06010104-0606-0000-060e-2b3401010102" ,  0x4E02 ,  "kAAFTypeID_ControlPointStrongReferenceVector" , False ,  False ),
     }
),
"TaggedValue"  : ( "0d010101-0101-3f00-060e-2b3402060101" , "InterchangeObject" , True , {
     "PortableObjectClassID" : ( "08835f4f-7b28-11d3-a044-006094eb75cb" ,  0xFFCA ,  "aafUInt32" , True ,  False ),
     "Value" : ( "03020102-0a01-0000-060e-2b3401010102" ,  0x5003 ,  "aafIndirect" , False ,  False ),
     "Name" : ( "03020102-0901-0000-060e-2b3401010102" ,  0x5001 ,  "aafString" , False ,  False ),
     "PortableObject" : ( "b6bb5f4e-7b37-11d3-a044-006094eb75cb" ,  0xFFC9 ,  "AvidStrongReference" , True ,  False ),
     "TaggedValueAttributeList" : ( "60958185-47b1-11d4-a01c-0004ac969f50" ,  0xFFCB ,  "kAAFTypeID_TaggedValueStrongReferenceVector" , True ,  False ),
     "TaggedValue_Stream" : ( "c12d81ac-bd68-4fef-a37f-562d28e37158" ,  0xFFC8 ,  "Stream" , True ,  False ),
     }
),
"KLVData"  : ( "0d010101-0101-4000-060e-2b3402060101" , "InterchangeObject" , True , {
     "Value" : ( "03010210-0200-0000-060e-2b3401010102" ,  0x5101 ,  "aafOpaque" , False ,  False ),
     }
),
"DescriptiveMarker"  : ( "0d010101-0101-4100-060e-2b3402060101" , "CommentMarker" , True , {
     "DescribedSlots" : ( "01070105-0000-0000-060e-2b3401010104" ,  0x6102 ,  "UInt32Set" , True ,  False ),
     "Description" : ( "06010104-020c-0000-060e-2b3401010105" ,  0x6101 ,  "kAAFTypeID_DescriptiveFrameworkStrongReference" , True ,  False ),
     }
),
"SoundDescriptor"  : ( "0d010101-0101-4200-060e-2b3402060101" , "FileDescriptor" , True , {
     "AudioSamplingRate" : ( "04020301-0101-0000-060e-2b3401010105" ,  0x3D03 ,  "Rational" , False ,  False ),
     "QuantizationBits" : ( "04020303-0400-0000-060e-2b3401010104" ,  0x3D01 ,  "aafUInt32" , False ,  False ),
     "ElectroSpatial" : ( "04020101-0100-0000-060e-2b3401010101" ,  0x3D05 ,  "ElectroSpatialFormulation" , True ,  False ),
     "AudioRefLevel" : ( "04020101-0300-0000-060e-2b3401010101" ,  0x3D04 ,  "aafInt8" , True ,  False ),
     "DialNorm" : ( "04020701-0000-0000-060e-2b3401010105" ,  0x3D0C ,  "aafInt8" , True ,  False ),
     "Locked" : ( "04020301-0400-0000-060e-2b3401010104" ,  0x3D02 ,  "Boolean" , True ,  False ),
     "Channels" : ( "04020101-0400-0000-060e-2b3401010105" ,  0x3D07 ,  "aafUInt32" , False ,  False ),
     "Compression" : ( "04020402-0000-0000-060e-2b3401010102" ,  0x3D06 ,  "AUID" , True ,  False ),
     }
),
"DataEssenceDescriptor"  : ( "0d010101-0101-4300-060e-2b3402060101" , "FileDescriptor" , True , {
     "FirstFrameOffset" : ( "0e040101-0101-0102-060e-2b3401010101" ,  0xFFD1 ,  "aafInt32" , True ,  False ),
     "DataEssenceCoding" : ( "04030302-0000-0000-060e-2b3401010103" ,  0x3E01 ,  "AUID" , True ,  False ),
     "DataOffset" : ( "0e040101-0101-0109-060e-2b3401010101" ,  0xFFD3 ,  "aafInt32" , True ,  False ),
     "MinSampleSize" : ( "0e040101-0101-0103-060e-2b3401010101" ,  0xFFD0 ,  "aafInt32" , True ,  False ),
     "MaxSampleSize" : ( "0e040101-0101-0104-060e-2b3401010101" ,  0xFFCF ,  "aafInt32" , True ,  False ),
     "OffsetToFrameIndexes" : ( "0e040101-0101-0101-060e-2b3401010101" ,  0xFFD2 ,  "aafInt64" , True ,  False ),
     }
),
"MultipleDescriptor"  : ( "0d010101-0101-4400-060e-2b3402060101" , "FileDescriptor" , True , {
     "FileDescriptors" : ( "06010104-060b-0000-060e-2b3401010104" ,  0x3F01 ,  "kAAFTypeID_FileDescriptorStrongReferenceVector" , False ,  False ),
     }
),
"PCMDescriptor"  : ( "0d010101-0101-4800-060e-2b3402060101" , "SoundDescriptor" , True , {
     "PeakFrames" : ( "04020301-0b00-0000-060e-2b3401010108" ,  0x3D2E ,  "aafUInt32" , True ,  False ),
     "PeakEnvelopeBlockSize" : ( "04020301-0900-0000-060e-2b3401010108" ,  0x3D2C ,  "aafUInt32" , True ,  False ),
     "BlockAlign" : ( "04020302-0100-0000-060e-2b3401010105" ,  0x3D0A ,  "aafUInt16" , False ,  False ),
     "ChannelAssignment" : ( "04020101-0500-0000-060e-2b3401010107" ,  0x3D32 ,  "AUID" , True ,  False ),
     "PeakEnvelopeFormat" : ( "04020301-0700-0000-060e-2b3401010108" ,  0x3D2A ,  "aafUInt32" , True ,  False ),
     "PeakChannels" : ( "04020301-0a00-0000-060e-2b3401010108" ,  0x3D2D ,  "aafUInt32" , True ,  False ),
     "PeakEnvelopeTimestamp" : ( "04020301-0d00-0000-060e-2b3401010108" ,  0x3D30 ,  "TimeStamp" , True ,  False ),
     "PeakEnvelopeData" : ( "04020301-0e00-0000-060e-2b3401010108" ,  0x3D31 ,  "Stream" , True ,  False ),
     "DataOffset" : ( "bb3fabdd-fcc0-43a8-9759-c727771fcc4a" ,  0xFFE0 ,  "aafInt32" , True ,  False ),
     "PeakOfPeaksPosition" : ( "04020301-0c00-0000-060e-2b3401010108" ,  0x3D2F ,  "aafPositionType" , True ,  False ),
     "PeakEnvelopeVersion" : ( "04020301-0600-0000-060e-2b3401010108" ,  0x3D29 ,  "aafUInt32" , True ,  False ),
     "SequenceOffset" : ( "04020302-0200-0000-060e-2b3401010105" ,  0x3D0B ,  "aafUInt8" , True ,  False ),
     "AverageBPS" : ( "04020303-0500-0000-060e-2b3401010105" ,  0x3D09 ,  "aafUInt32" , False ,  False ),
     "PointsPerPeakValue" : ( "04020301-0800-0000-060e-2b3401010108" ,  0x3D2B ,  "aafUInt32" , True ,  False ),
     }
),
"PhysicalDescriptor"  : ( "0d010101-0101-4900-060e-2b3402060101" , "EssenceDescriptor" , False , {
     }
),
"ImportDescriptor"  : ( "0d010101-0101-4a00-060e-2b3402060101" , "PhysicalDescriptor" , True , {
     }
),
"TaggedValueDefinition"  : ( "0d010101-0101-4c00-060e-2b3402060101" , "DefinitionObject" , True , {
     }
),
"KLVDataDefinition"  : ( "0d010101-0101-4d00-060e-2b3402060101" , "DefinitionObject" , True , {
     "KLVDataType" : ( "06010104-0109-0000-060e-2b3401010107" ,  0x4D12 ,  "TypeDefinitionWeakReference" , True ,  False ),
     }
),
"SubDescriptor"  : ( "0d010101-0101-5900-060e-2b3402060101" , "InterchangeObject" , False , {
     }
),
"AVCSubDescriptor"  : ( "0101010d-0101-006e-060e-2b3402060101" , "SubDescriptor" , True , {
     "AVCMaximumBitRate" : ( "06060104-0b01-0000-060e-2b340101010e" ,  0xFFAF ,  "aafUInt32" , True ,  False ),
     "AVCProfileConstraint" : ( "06060104-0c01-0000-060e-2b340101010e" ,  0xFFAE ,  "aafUInt8" , True ,  False ),
     "AVCLevel" : ( "06060104-0d01-0000-060e-2b340101010e" ,  0xFFAD ,  "aafUInt8" , True ,  False ),
     "AVCDecodingDelay" : ( "06060104-0e01-0000-060e-2b340101010e" ,  0xFFAC ,  "aafUInt8" , False ,  False ),
     "AVCMaximumRefFrames" : ( "06060104-0f01-0000-060e-2b340101010e" ,  0xFFAB ,  "aafUInt8" , True ,  False ),
     "AVCCodedContentKind" : ( "06060104-0401-0000-060e-2b340101010e" ,  0xFFB5 ,  "AVCContentScanningType" , True ,  False ),
     "AVCSequenceParameterSetFlag" : ( "06060104-1001-0000-060e-2b340101010e" ,  0xFFAA ,  "aafUInt8" , True ,  False ),
     "AVCPictureParameterSetFlag" : ( "06060104-1101-0000-060e-2b340101010e" ,  0xFFA9 ,  "aafUInt8" , True ,  False ),
     "AVCMaximumGOPSize" : ( "06060104-0801-0000-060e-2b340101010e" ,  0xFFB2 ,  "aafUInt16" , True ,  False ),
     "AVCConstantBPictureFlag" : ( "06060104-0301-0000-060e-2b340101010e" ,  0xFFB6 ,  "Boolean" , True ,  False ),
     "AVCIdenticalGOPIndicator" : ( "06060104-0701-0000-060e-2b340101010e" ,  0xFFB3 ,  "Boolean" , True ,  False ),
     "AVCClosedGOPIndicator" : ( "06060104-0601-0000-060e-2b340101010e" ,  0xFFB4 ,  "Boolean" , True ,  False ),
     "AVCMaximumBPictureCount" : ( "06060104-0901-0000-060e-2b340101010e" ,  0xFFB1 ,  "aafUInt16" , True ,  False ),
     "AVCAverageBitRate" : ( "06060104-1401-0000-060e-2b340101010e" ,  0xFFA8 ,  "aafUInt32" , True ,  False ),
     "AVCProfile" : ( "06060104-0a01-0000-060e-2b340101010e" ,  0xFFB0 ,  "aafUInt8" , True ,  False ),
     }
),
"ANCDataDescriptor"  : ( "0d010101-0101-5c00-060e-2b3402060101" , "DataEssenceDescriptor" , True , {
     "ManifestArray" : ( "0e040101-0101-0105-060e-2b3401010101" ,  0xFFCE ,  "AvidManifestArray" , True ,  False ),
     }
),
"ClassDefinition"  : ( "0d010101-0201-0000-060e-2b3402060101" , "MetaDefinition" , True , {
     "ParentClass" : ( "06010107-0100-0000-060e-2b3401010102" ,  0x0008 ,  "ClassDefinitionWeakReference" , False ,  False ),
     "Properties" : ( "06010107-0200-0000-060e-2b3401010102" ,  0x0009 ,  "kAAFTypeID_PropertyDefinitionStrongReferenceSet" , True ,  False ),
     "IsConcrete" : ( "06010107-0300-0000-060e-2b3401010102" ,  0x000A ,  "Boolean" , False ,  False ),
     }
),
"PropertyDefinition"  : ( "0d010101-0202-0000-060e-2b3402060101" , "MetaDefinition" , True , {
     "Type" : ( "06010107-0400-0000-060e-2b3401010102" ,  0x000B ,  "AUID" , False ,  False ),
     "IsOptional" : ( "03010202-0100-0000-060e-2b3401010102" ,  0x000C ,  "Boolean" , False ,  False ),
     "LocalIdentification" : ( "06010107-0500-0000-060e-2b3401010102" ,  0x000D ,  "aafUInt16" , False ,  False ),
     "IsUniqueIdentifier" : ( "06010107-0600-0000-060e-2b3401010102" ,  0x000E ,  "Boolean" , True ,  False ),
     }
),
"TypeDefinition"  : ( "0d010101-0203-0000-060e-2b3402060101" , "MetaDefinition" , False , {
     }
),
"TypeDefinitionInteger"  : ( "0d010101-0204-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "IsSigned" : ( "03010203-0200-0000-060e-2b3401010102" ,  0x0010 ,  "Boolean" , False ,  False ),
     "Size" : ( "03010203-0100-0000-060e-2b3401010102" ,  0x000F ,  "aafUInt8" , False ,  False ),
     }
),
"TypeDefinitionStrongObjectReference"  : ( "0d010101-0205-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ReferencedType" : ( "06010107-0900-0000-060e-2b3401010102" ,  0x0011 ,  "ClassDefinitionWeakReference" , False ,  False ),
     }
),
"TypeDefinitionWeakObjectReference"  : ( "0d010101-0206-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ReferencedType" : ( "06010107-0a00-0000-060e-2b3401010102" ,  0x0012 ,  "ClassDefinitionWeakReference" , False ,  False ),
     "TargetSet" : ( "03010203-0b00-0000-060e-2b3401010102" ,  0x0013 ,  "aafAUIDArray" , False ,  False ),
     }
),
"TypeDefinitionEnumeration"  : ( "0d010101-0207-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ElementType" : ( "06010107-0b00-0000-060e-2b3401010102" ,  0x0014 ,  "TypeDefinitionWeakReference" , False ,  False ),
     "ElementValues" : ( "03010203-0500-0000-060e-2b3401010102" ,  0x0016 ,  "aafInt64Array" , False ,  False ),
     "ElementNames" : ( "03010203-0400-0000-060e-2b3401010102" ,  0x0015 ,  "aafString" , False ,  False ),
     }
),
"TypeDefinitionFixedArray"  : ( "0d010101-0208-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ElementCount" : ( "03010203-0300-0000-060e-2b3401010102" ,  0x0018 ,  "aafUInt32" , False ,  False ),
     "ElementType" : ( "06010107-0c00-0000-060e-2b3401010102" ,  0x0017 ,  "TypeDefinitionWeakReference" , False ,  False ),
     }
),
"TypeDefinitionVariableArray"  : ( "0d010101-0209-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ElementType" : ( "06010107-0d00-0000-060e-2b3401010102" ,  0x0019 ,  "TypeDefinitionWeakReference" , False ,  False ),
     }
),
"TypeDefinitionSet"  : ( "0d010101-020a-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ElementType" : ( "06010107-0e00-0000-060e-2b3401010102" ,  0x001A ,  "TypeDefinitionWeakReference" , False ,  False ),
     }
),
"TypeDefinitionString"  : ( "0d010101-020b-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ElementType" : ( "06010107-0f00-0000-060e-2b3401010102" ,  0x001B ,  "TypeDefinitionWeakReference" , False ,  False ),
     }
),
"TypeDefinitionStream"  : ( "0d010101-020c-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     }
),
"TypeDefinitionRecord"  : ( "0d010101-020d-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "MemberNames" : ( "03010203-0600-0000-060e-2b3401010102" ,  0x001D ,  "aafString" , False ,  False ),
     "MemberTypes" : ( "06010107-1100-0000-060e-2b3401010102" ,  0x001C ,  "kAAFTypeID_TypeDefinitionWeakReferenceVector" , False ,  False ),
     }
),
"TypeDefinitionRename"  : ( "0d010101-020e-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "RenamedType" : ( "06010107-1200-0000-060e-2b3401010102" ,  0x001E ,  "TypeDefinitionWeakReference" , False ,  False ),
     }
),
"TypeDefinitionExtendibleEnumeration"  : ( "0d010101-0220-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     "ElementValues" : ( "03010203-0800-0000-060e-2b3401010102" ,  0x0020 ,  "aafAUIDArray" , False ,  False ),
     "ElementNames" : ( "03010203-0700-0000-060e-2b3401010102" ,  0x001F ,  "aafString" , False ,  False ),
     }
),
"TypeDefinitionIndirect"  : ( "0d010101-0221-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     }
),
"TypeDefinitionOpaque"  : ( "0d010101-0222-0000-060e-2b3402060101" , "TypeDefinitionIndirect" , True , {
     }
),
"TypeDefinitionCharacter"  : ( "0d010101-0223-0000-060e-2b3402060101" , "TypeDefinition" , True , {
     }
),
"MetaDefinition"  : ( "0d010101-0224-0000-060e-2b3402060101" , "InterchangeObject" , False , {
     "Identification" : ( "06010107-1300-0000-060e-2b3401010102" ,  0x0005 ,  "AUID" , False ,  True ),
     "Description" : ( "06010107-1401-0000-060e-2b3401010102" ,  0x0007 ,  "aafString" , True ,  False ),
     "Name" : ( "03020401-0201-0000-060e-2b3401010102" ,  0x0006 ,  "aafString" , False ,  False ),
     }
),
"MetaDictionary"  : ( "0d010101-0225-0000-060e-2b3402060101" , "InterchangeObject" , True , {
     "ClassDefinitions" : ( "06010107-0700-0000-060e-2b3401010102" ,  0x0003 ,  "kAAFTypeID_ClassDefinitionStrongReferenceSet" , True ,  False ),
     "TypeDefinitions" : ( "06010107-0800-0000-060e-2b3401010102" ,  0x0004 ,  "kAAFTypeID_TypeDefinitionStrongReferenceSet" , True ,  False ),
     }
),
"DescriptiveFramework"  : ( "0d010401-0000-0000-060e-2b3402060101" , "InterchangeObject" , False , {
     }
),
"AvidTrackManTrackedParamClass"  : ( "30a42454-069e-11d4-9ffb-0004ac969f50" , "InterchangeObject" , True , {
     "TKMNTrackedParamSetngs" : ( "30a42453-069e-11d4-9ffb-0004ac969f50" ,  0xFF9F ,  "AvidBagOfBits" , False ,  False ),
     }
),
"AvidTrackManTrackerDataClass"  : ( "13e0a981-0412-11d4-9ff9-0004ac969f50" , "InterchangeObject" , True , {
     "TKMNTrkDataBoxX" : ( "e3c9057c-311d-41c1-9a7d-41ae1de90150" ,  0xFFA1 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataConfidence" : ( "c63c3449-0412-11d4-9ff9-0004ac969f50" ,  0xFFAE ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataOffsetTrackingEnabled" : ( "875d33e9-f596-4daa-9730-3128a06b9763" ,  0xFFA5 ,  "Boolean" , True ,  False ),
     "TKMNTrkDataPatternH" : ( "c63c344d-0412-11d4-9ff9-0004ac969f50" ,  0xFFAA ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataOffsetY" : ( "c63c344b-0412-11d4-9ff9-0004ac969f50" ,  0xFFAC ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataSearchTH" : ( "c63c3450-0412-11d4-9ff9-0004ac969f50" ,  0xFFA7 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataBoxY" : ( "f15129da-7d1a-4f68-87ab-c0956f125654" ,  0xFFA0 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataSettings" : ( "c63c3452-0412-11d4-9ff9-0004ac969f50" ,  0xFFB1 ,  "AvidBagOfBits" , False ,  False ),
     "TKMNTrkDataSearchLW" : ( "c63c344e-0412-11d4-9ff9-0004ac969f50" ,  0xFFA9 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataSmoothingEnabled" : ( "75994f5f-e038-4769-9026-d8082cebc6e0" ,  0xFFA4 ,  "Boolean" , True ,  False ),
     "TKMNTrkDataFilterDataAmt" : ( "aab41ed6-07cc-4917-8119-a4bfeec607a0" ,  0xFFA2 ,  "Rational" , True ,  False ),
     "TKMNTrkDataSearchBH" : ( "c63c3451-0412-11d4-9ff9-0004ac969f50" ,  0xFFA6 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataPatternW" : ( "c63c344c-0412-11d4-9ff9-0004ac969f50" ,  0xFFAB ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataDataY" : ( "c63c3448-0412-11d4-9ff9-0004ac969f50" ,  0xFFAF ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataOffsetX" : ( "c63c344a-0412-11d4-9ff9-0004ac969f50" ,  0xFFAD ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataSearchRW" : ( "c63c344f-0412-11d4-9ff9-0004ac969f50" ,  0xFFA8 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataDataX" : ( "c63c3447-0412-11d4-9ff9-0004ac969f50" ,  0xFFB0 ,  "kAAFTypeID_ParameterStrongReference" , True ,  False ),
     "TKMNTrkDataJitterRemovalEnabled" : ( "d1f936be-6f3a-4b8d-8e7a-855ab8a8565f" ,  0xFFA3 ,  "Boolean" , True ,  False ),
     }
),
"Avid MC Mob Reference"  : ( "6619f8e0-fe77-11d3-a084-006094eb75cb" , "InterchangeObject" , True , {
     "Mob Reference Position" : ( "81110ea0-fe7c-11d3-a084-006094eb75cb" ,  0xFFB6 ,  "aafInt64" , False ,  False ),
     "Mob Reference MobID" : ( "81110e9f-fe7c-11d3-a084-006094eb75cb" ,  0xFFB7 ,  "MobIDType" , False ,  False ),
     }
),
}

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
