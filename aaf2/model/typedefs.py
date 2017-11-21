
ints = {
"aafUInt8" : ( "01010100-0000-0000-060e-2b3401040101" , 1 , False ),
"aafUInt16" : ( "01010200-0000-0000-060e-2b3401040101" , 2 , False ),
"aafUInt32" : ( "01010300-0000-0000-060e-2b3401040101" , 4 , False ),
"aafInt8" : ( "01010500-0000-0000-060e-2b3401040101" , 1 , True ),
"aafInt16" : ( "01010600-0000-0000-060e-2b3401040101" , 2 , True ),
"aafInt32" : ( "01010700-0000-0000-060e-2b3401040101" , 4 , True ),
"aafInt64" : ( "01010800-0000-0000-060e-2b3401040101" , 8 , True ),
}

enums = {
"Boolean" : ( "01040100-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "False" ,
     1 : "True" ,
     }
),
"ProductReleaseType" : ( "02010101-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "VersionUnknown" ,
     1 : "VersionReleased" ,
     2 : "VersionDebug" ,
     3 : "VersionPatched" ,
     4 : "VersionBeta" ,
     5 : "VersionPrivateBuild" ,
     }
),
"AvidEssenceElementSizeKind" : ( "0e040201-0101-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "AvidEssenceElementSizeKind_Unknown" ,
     1 : "AvidEssenceElementSizeKind_CBE" ,
     2 : "AvidEssenceElementSizeKind_VBE" ,
     }
),
"TapeFormatType" : ( "02010102-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "TapeFormatNull" ,
     1 : "BetacamFormat" ,
     2 : "BetacamSPFormat" ,
     3 : "VHSFormat" ,
     4 : "SVHSFormat" ,
     5 : "8mmFormat" ,
     6 : "Hi8Format" ,
     }
),
"VideoSignalType" : ( "02010103-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "VideoSignalNull" ,
     1 : "NTSCSignal" ,
     2 : "PALSignal" ,
     }
),
"TapeCaseType" : ( "02010104-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "TapeCaseNull" ,
     1 : "ThreeFourthInchVideoTape" ,
     2 : "VHSVideoTape" ,
     3 : "8mmVideoTape" ,
     4 : "BetacamVideoTape" ,
     5 : "CompactCassette" ,
     6 : "DATCartridge" ,
     7 : "NagraAudioTape" ,
     }
),
"ColorSitingType" : ( "02010105-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "CoSiting" ,
     1 : "Averaging" ,
     2 : "ThreeTap" ,
     3 : "Quincunx" ,
     4 : "Rec601" ,
     255 : "UnknownSiting" ,
     }
),
"EditHintType" : ( "02010106-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "NoEditHint" ,
     1 : "Proportional" ,
     2 : "RelativeLeft" ,
     3 : "RelativeRight" ,
     4 : "RelativeFixed" ,
     }
),
"FadeType" : ( "02010107-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "FadeNone" ,
     1 : "FadeLinearAmp" ,
     2 : "FadeLinearPower" ,
     }
),
"LayoutType" : ( "02010108-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "FullFrame" ,
     1 : "SeparateFields" ,
     2 : "OneField" ,
     3 : "MixedFields" ,
     4 : "SegmentedFrame" ,
     }
),
"PulldownDirectionType" : ( "0201010a-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "TapeToFilmSpeed" ,
     1 : "FilmToTapeSpeed" ,
     }
),
"PulldownKindType" : ( "0201010b-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "TwoThreePD" ,
     1 : "PALPD" ,
     2 : "OneToOneNTSC" ,
     3 : "OneToOnePAL" ,
     4 : "VideoTapNTSC" ,
     5 : "OneToOneHDSixty" ,
     6 : "TwentyFourToSixtyPD" ,
     7 : "TwoToOnePD" ,
     }
),
"EdgeType" : ( "0201010c-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "EtNull" ,
     1 : "EtKeycode" ,
     2 : "EtEdgenum4" ,
     3 : "EtEdgenum5" ,
     8 : "EtHeaderSize" ,
     }
),
"FilmType" : ( "0201010d-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "FtNull" ,
     1 : "Ft35MM" ,
     2 : "Ft16MM" ,
     3 : "Ft8MM" ,
     4 : "Ft65MM" ,
     }
),
"RGBAComponentKind" : ( "0201010e-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "CompNull" ,
     65 : "CompAlpha" ,
     66 : "CompBlue" ,
     70 : "CompFill" ,
     71 : "CompGreen" ,
     80 : "CompPalette" ,
     48 : "CompNone" ,
     82 : "CompRed" ,
     }
),
"AlphaTransparencyType" : ( "02010120-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "MinValueTransparent" ,
     1 : "MaxValueTransparent" ,
     }
),
"FieldNumber" : ( "02010121-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "UnspecifiedField" ,
     1 : "FieldOne" ,
     2 : "FieldTwo" ,
     }
),
"ElectroSpatialFormulation" : ( "02010122-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "ElectroSpatialFormulation_Default" ,
     1 : "ElectroSpatialFormulation_TwoChannelMode" ,
     2 : "ElectroSpatialFormulation_SingleChannelMode" ,
     3 : "ElectroSpatialFormulation_PrimarySecondaryMode" ,
     4 : "ElectroSpatialFormulation_StereophonicMode" ,
     7 : "ElectroSpatialFormulation_SingleChannelDoubleSamplingFrequencyMode" ,
     8 : "ElectroSpatialFormulation_StereoLeftChannelDoubleSamplingFrequencyMode" ,
     9 : "ElectroSpatialFormulation_StereoRightChannelDoubleSamplingFrequencyMode" ,
     15 : "ElectroSpatialFormulation_MultiChannelMode" ,
     }
),
"SignalStandardType" : ( "02010127-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "SignalStandard_None" ,
     1 : "SignalStandard_ITU601" ,
     2 : "SignalStandard_ITU1358" ,
     3 : "SignalStandard_SMPTE347M" ,
     4 : "SignalStandard_SMPTE274M" ,
     5 : "SignalStandard_SMPTE296M" ,
     6 : "SignalStandard_SMPTE349M" ,
     }
),
"ScanningDirectionType" : ( "02010128-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "ScanningDirection_LeftToRightTopToBottom" ,
     1 : "ScanningDirection_RightToLeftTopToBottom" ,
     2 : "ScanningDirection_LeftToRightBottomToTop" ,
     3 : "ScanningDirection_RightToLeftBottomToTop" ,
     4 : "ScanningDirection_TopToBottomLeftToRight" ,
     5 : "ScanningDirection_TopToBottomRightToLeft" ,
     6 : "ScanningDirection_BottomToTopLeftToRight" ,
     7 : "ScanningDirection_BottomToTopRightToLeft" ,
     }
),
"AVCContentScanningType" : ( "0201012c-0000-0000-060e-2b3401040101" , "aafUInt8" , {
     0 : "AVCContentScanning_NotKnown" ,
     1 : "AVCContentScanning_ProgressiveFramePicture" ,
     2 : "AVCContentScanning_InterlaceFieldPicture" ,
     3 : "AVCContentScanning_InterlaceFramePicture" ,
     4 : "AVCContentScanning_Interlace_FrameFieldPicture" ,
     }
),
"AvidPannerKindType" : ( "3659b342-4f19-4316-9309-f139434a94e5" , "aafUInt32" , {
     1 : "AvidPannerKind_Stereo" ,
     2 : "AvidPannerKind_LCR" ,
     3 : "AvidPannerKind_Quad" ,
     4 : "AvidPannerKind_LCRS" ,
     5 : "AvidPannerKind_5dot0" ,
     6 : "AvidPannerKind_5dot1" ,
     7 : "AvidPannerKind_6dot0" ,
     8 : "AvidPannerKind_6dot1" ,
     9 : "AvidPannerKind_7dot0" ,
     10 : "AvidPannerKind_7dot1" ,
     }
),
}

records = {
"Rational" : ( "03010100-0000-0000-060e-2b3401040101" , (
     ( "Numerator" , "aafInt32" ),
     ( "Denominator" , "aafInt32" ),
     )
),
"AUID" : ( "01030100-0000-0000-060e-2b3401040101" , (
     ( "Data1" , "aafUInt32" ),
     ( "Data2" , "aafUInt16" ),
     ( "Data3" , "aafUInt16" ),
     ( "Data4" , "aafUInt8Array8" ),
     )
),
"ProductVersion" : ( "03010200-0000-0000-060e-2b3401040101" , (
     ( "major" , "aafUInt16" ),
     ( "minor" , "aafUInt16" ),
     ( "tertiary" , "aafUInt16" ),
     ( "patchLevel" , "aafUInt16" ),
     ( "type" , "ProductReleaseType" ),
     )
),
"MobIDType" : ( "01030200-0000-0000-060e-2b3401040101" , (
     ( "SMPTELabel" , "aafUInt8Array12" ),
     ( "length" , "aafUInt8" ),
     ( "instanceHigh" , "aafUInt8" ),
     ( "instanceMid" , "aafUInt8" ),
     ( "instanceLow" , "aafUInt8" ),
     ( "material" , "AUID" ),
     )
),
"VersionType" : ( "03010300-0000-0000-060e-2b3401040101" , (
     ( "major" , "aafInt8" ),
     ( "minor" , "aafInt8" ),
     )
),
"RGBAComponent" : ( "03010400-0000-0000-060e-2b3401040101" , (
     ( "Code" , "RGBAComponentKind" ),
     ( "Size" , "aafUInt8" ),
     )
),
"DateStruct" : ( "03010500-0000-0000-060e-2b3401040101" , (
     ( "year" , "aafInt16" ),
     ( "month" , "aafUInt8" ),
     ( "day" , "aafUInt8" ),
     )
),
"TimeStruct" : ( "03010600-0000-0000-060e-2b3401040101" , (
     ( "hour" , "aafUInt8" ),
     ( "minute" , "aafUInt8" ),
     ( "second" , "aafUInt8" ),
     ( "fraction" , "aafUInt8" ),
     )
),
"TimeStamp" : ( "03010700-0000-0000-060e-2b3401040101" , (
     ( "date" , "DateStruct" ),
     ( "time" , "TimeStruct" ),
     )
),
"AvidManifestElement" : ( "0e040301-0100-0000-060e-2b3401040101" , (
     ( "did" , "aafUInt8" ),
     ( "sdid" , "aafUInt8" ),
     )
),
"BoundsBox" : ( "0e040301-0200-0000-060e-2b3401040101" , (
     ( "PositionX" , "Rational" ),
     ( "PositionY" , "Rational" ),
     ( "Width" , "Rational" ),
     ( "Height" , "Rational" ),
     )
),
"RGBColor" : ( "e96e6d43-c383-11d3-a069-006094eb75cb" , (
     ( "red" , "aafUInt16" ),
     ( "green" , "aafUInt16" ),
     ( "blue" , "aafUInt16" ),
     )
),
"AudioSuitePlugInChunk" : ( "4e4d8f5f-eefd-11d3-9ff5-0004ac969f50" , (
     ( "Version" , "aafUInt32" ),
     ( "ManufacturerID" , "AvidString4" ),
     ( "ProductID" , "AvidString4" ),
     ( "PlugInID" , "AvidString4" ),
     ( "ChunkID" , "AvidString4" ),
     ( "Name" , "AvidWideString32" ),
     ( "ChunkDataUID" , "AUID" ),
     )
),
"EqualizationBand" : ( "c4c670c9-bd44-11d3-80e9-006008143e6f" , (
     ( "type" , "AUID" ),
     ( "frequency" , "aafUInt32" ),
     ( "gain" , "aafUInt32" ),
     ( "q" , "aafUInt32" ),
     ( "enable" , "Boolean" ),
     )
),
}

fixed_arrays = {
"aafRGBALayout" : ( "04020100-0000-0000-060e-2b3401040101" , "RGBAComponent" , 8 ),
"aafUInt8Array12" : ( "04010200-0000-0000-060e-2b3401040101" , "aafUInt8" , 12 ),
"aafUInt8Array8" : ( "04010800-0000-0000-060e-2b3401040101" , "aafUInt8" , 8 ),
"AvidPosition" : ( "8bc4272e-6bab-11d3-80cf-006008143e6f" , "aafUInt8" , 24 ),
"AvidCrop" : ( "8bc4272f-6bab-11d3-80cf-006008143e6f" , "aafUInt8" , 32 ),
"AvidScale" : ( "8bc42730-6bab-11d3-80cf-006008143e6f" , "aafUInt8" , 16 ),
"AvidSpillSupress" : ( "8bc42731-6bab-11d3-80cf-006008143e6f" , "aafUInt8" , 8 ),
"AvidBounds" : ( "8bc42732-6bab-11d3-80cf-006008143e6f" , "aafUInt8" , 48 ),
"AvidColor" : ( "8bc42733-6bab-11d3-80cf-006008143e6f" , "aafUInt8" , 68 ),
"AvidString4" : ( "0f96cb41-2aa8-11d4-a00f-0004ac969f50" , "aafUInt8" , 4 ),
"AvidWideString32" : ( "3271a34f-f3a1-11d3-9ff5-0004ac969f50" , "aafUInt16" , 32 ),
"AvidGlobalKeyFrame" : ( "09997778-960e-11d3-a04e-006094eb75cb" , "aafUInt8" , 16 ),
}

var_arrays = {
"kAAFTypeID_OperationDefinitionWeakReferenceVector" : ( "05040100-0000-0000-060e-2b3401040101" , "OperationDefinitionWeakReference" ),
"kAAFTypeID_ComponentStrongReferenceVector" : ( "05060100-0000-0000-060e-2b3401040101" , "kAAFTypeID_ComponentStrongReference" ),
"aafDataValue" : ( "04100100-0000-0000-060e-2b3401040101" , "aafUInt8" ),
"kAAFTypeID_TypeDefinitionWeakReferenceVector" : ( "05040200-0000-0000-060e-2b3401040101" , "TypeDefinitionWeakReference" ),
"kAAFTypeID_ControlPointStrongReferenceVector" : ( "05060200-0000-0000-060e-2b3401040101" , "kAAFTypeID_ControlPointStrongReference" ),
"aafInt32Array" : ( "04010300-0000-0000-060e-2b3401040101" , "aafInt32" ),
"kAAFTypeID_DataDefinitionWeakReferenceVector" : ( "05040300-0000-0000-060e-2b3401040101" , "DataDefinitionWeakReference" ),
"kAAFTypeID_IdentificationStrongReferenceVector" : ( "05060300-0000-0000-060e-2b3401040101" , "kAAFTypeID_IdentificationStrongReference" ),
"aafInt64Array" : ( "04010400-0000-0000-060e-2b3401040101" , "aafInt64" ),
"kAAFTypeID_LocatorStrongReferenceVector" : ( "05060400-0000-0000-060e-2b3401040101" , "kAAFTypeID_LocatorStrongReference" ),
"kAAFTypeID_MobSlotStrongReferenceVector" : ( "05060500-0000-0000-060e-2b3401040101" , "kAAFTypeID_MobSlotStrongReference" ),
"aafAUIDArray" : ( "04010600-0000-0000-060e-2b3401040101" , "AUID" ),
"kAAFTypeID_SegmentStrongReferenceVector" : ( "05060600-0000-0000-060e-2b3401040101" , "kAAFTypeID_SegmentStrongReference" ),
"kAAFTypeID_SourceReferenceStrongReferenceVector" : ( "05060700-0000-0000-060e-2b3401040101" , "kAAFTypeID_SourceReferenceStrongReference" ),
"kAAFTypeID_TaggedValueStrongReferenceVector" : ( "05060800-0000-0000-060e-2b3401040101" , "kAAFTypeID_TaggedValueStrongReference" ),
"aafUInt32Array" : ( "04010900-0000-0000-060e-2b3401040101" , "aafUInt32" ),
"kAAFTypeID_KLVDataStrongReferenceVector" : ( "05060900-0000-0000-060e-2b3401040101" , "kAAFTypeID_KLVDataStrongReference" ),
"kAAFTypeID_ParameterStrongReferenceVector" : ( "05060a00-0000-0000-060e-2b3401040101" , "kAAFTypeID_ParameterStrongReference" ),
"kAAFTypeID_FileDescriptorStrongReferenceVector" : ( "05060b00-0000-0000-060e-2b3401040101" , "kAAFTypeID_FileDescriptorStrongReference" ),
"kAAFTypeID_SubDescriptorStrongReferenceVector" : ( "05060e00-0000-0000-060e-2b3401040101" , "kAAFTypeID_SubDescriptorStrongReference" ),
"AvidManifestArray" : ( "0e040402-0100-0000-060e-2b3401040101" , "AvidManifestElement" ),
"AudioSuitePIChunkArray" : ( "4e4d8f60-eefd-11d3-9ff5-0004ac969f50" , "AudioSuitePlugInChunk" ),
"AudioSuitePIChunkData" : ( "5cf19caf-ef83-11d3-9ff5-0004ac969f50" , "aafUInt8" ),
"AvidTKMNTrackedParamArray" : ( "b56a2ec2-fc3b-11d3-9ff7-0004ac969f50" , "AvidStrongReference" ),
"AvidTKMNTrackerDataArray" : ( "b56a2ec3-fc3b-11d3-9ff7-0004ac969f50" , "AvidStrongReference" ),
"EqualizationBandArray" : ( "c4c670ca-bd44-11d3-80e9-006008143e6f" , "EqualizationBand" ),
"AvidBagOfBits" : ( "ccaa73d1-f538-11d3-a081-006094eb75cb" , "aafUInt8" ),
}

renames = {
"aafPhaseFrameType" : ( "01012300-0000-0000-060e-2b3401040101" , "aafInt32" ),
"aafPositionType" : ( "01012001-0000-0000-060e-2b3401040101" , "aafInt64" ),
"aafLengthType" : ( "01012002-0000-0000-060e-2b3401040101" , "aafInt64" ),
}

strings = {
"aafString" : ( "01100200-0000-0000-060e-2b3401040101" , "aafCharacter" ),
}

streams = {
"Stream" : "04100200-0000-0000-060e-2b3401040101" ,
}

opaques = {
}

extenums = {
"OperationCategoryType" : ( "02020101-0000-0000-060e-2b3401040101" , {
     "0d010102-0101-0100-060e-2b3404010101" : "OperationCategory_Effect" ,
     }
),
"TransferCharacteristicType" : ( "02020102-0000-0000-060e-2b3401040101" , {
     "0e040501-0106-0000-060e-2b3404010101" : "TransferCharacteristic_SMPTE_ST2084" ,
     "04010101-0106-0000-060e-2b3404010101" : "TransferCharacteristic_linear" ,
     "0e040501-0108-0000-060e-2b3404010101" : "TransferCharacteristic_ARIB_B67" ,
     "0e040501-0105-0000-060e-2b3404010101" : "TransferCharacteristic_SMPTE_RP431" ,
     "04010101-0101-0000-060e-2b3404010101" : "TransferCharacteristic_ITU470_PAL" ,
     "0e040501-010a-0000-060e-2b3404010101" : "TransferCharacteristic_ITU709_Extended2" ,
     "0e040501-0102-0000-060e-2b3404010101" : "TransferCharacteristic_DPXLogarithmic" ,
     "0e060401-0101-0605-060e-2b3404010106" : "TransferCharacteristic_Sony_SLog3" ,
     "04010101-0103-0000-060e-2b3404010101" : "TransferCharacteristic_SMPTE240M" ,
     "0e170000-0001-0101-060e-2b340401010c" : "TransferCharacteristic_ARRI_LogC" ,
     "0e040501-0101-0000-060e-2b3404010101" : "TransferCharacteristic_DPXPrintingDensity" ,
     "04010101-0102-0000-060e-2b3404010101" : "TransferCharacteristic_ITU709" ,
     "0e040501-0103-0000-060e-2b3404010101" : "TransferCharacteristic_SRGB" ,
     "04010101-0104-0000-060e-2b3404010101" : "TransferCharacteristic_274M_296M" ,
     "04010101-0105-0000-060e-2b3404010101" : "TransferCharacteristic_ITU1361",
     }
),
"PluginCategoryType" : ( "02020103-0000-0000-060e-2b3401040101" , {
     "0d010102-0101-0200-060e-2b3404010101" : "PluginCategory_Effect" ,
     "0d010102-0101-0400-060e-2b3404010101" : "PluginCategory_Interpolation" ,
     "0d010102-0101-0300-060e-2b3404010101" : "PluginCategory_Codec" ,
     }
),
"UsageType" : ( "02020104-0000-0000-060e-2b3401040101" , {
     "0d010102-0101-0800-060e-2b3404010101" : "Usage_LowerLevel" ,
     "0d010102-0101-0500-060e-2b3404010101" : "Usage_SubClip" ,
     "0d010102-0101-0900-060e-2b3404010101" : "Usage_Template" ,
     "0d010102-0101-0700-060e-2b3404010101" : "Usage_TopLevel" ,
     "0d010102-0101-0600-060e-2b3404010101" : "Usage_AdjustedClip" ,
     }
),
"ColorPrimariesType" : ( "02020105-0000-0000-060e-2b3401040101" , {
     "0e040501-0301-0000-060e-2b3404010101" : "ColorPrimaries_SMPTE_RP431" ,
     "04010101-0301-0000-060e-2b3404010106" : "ColorPrimaries_SMPTE170M" ,
     "04010101-0302-0000-060e-2b3404010106" : "ColorPrimaries_ITU470_PAL" ,
     "04010101-0303-0000-060e-2b3404010106" : "ColorPrimaries_ITU709" ,
     "0e040501-0302-0000-060e-2b3404010101" : "ColorPrimaries_Sony_SGamut3" ,
     "0e040501-0303-0000-060e-2b3404010101" : "ColorPrimaries_Sony_SGamut3_Cine" ,
     "04010101-0304-0000-060e-2b340401010d" : "ColorPrimaries_ITU2020" ,
     }
),
"CodingEquationsType" : ( "02020106-0000-0000-060e-2b3401040101" , {
     "04010101-0201-0000-060e-2b3404010101" : "CodingEquations_ITU601" ,
     "04010101-0203-0000-060e-2b3404010101" : "CodingEquations_SMPTE240M" ,
     "0e040501-0201-0000-060e-2b3404010101" : "CodingEquations_ITU2020" ,
     "04010101-0202-0000-060e-2b3404010101" : "CodingEquations_ITU709" ,
     }
),
}

chars = {
"aafCharacter" : "01100100-0000-0000-060e-2b3401040101" ,
}

indirects = {
"aafIndirect" : "04100300-0000-0000-060e-2b3401040101" ,
"aafOpaque" : "04100400-0000-0000-060e-2b3401040101" ,
}

sets = {
"AUIDSet" : ( "04030100-0000-0000-060e-2b3401040101" , "AUID" ),
"kAAFTypeID_ClassDefinitionStrongReferenceSet" : ( "05050100-0000-0000-060e-2b3401040101" , "kAAFTypeID_ClassDefinitionStrongReference" ),
"UInt32Set" : ( "04030200-0000-0000-060e-2b3401040101" , "aafUInt32" ),
"kAAFTypeID_CodecDefinitionStrongReferenceSet" : ( "05050200-0000-0000-060e-2b3401040101" , "kAAFTypeID_CodecDefinitionStrongReference" ),
"kAAFTypeID_ContainerDefinitionStrongReferenceSet" : ( "05050300-0000-0000-060e-2b3401040101" , "kAAFTypeID_ContainerDefinitionStrongReference" ),
"kAAFTypeID_DataDefinitionStrongReferenceSet" : ( "05050400-0000-0000-060e-2b3401040101" , "kAAFTypeID_DataDefinitionStrongReference" ),
"kAAFTypeID_EssenceDataStrongReferenceSet" : ( "05050500-0000-0000-060e-2b3401040101" , "kAAFTypeID_EssenceDataStrongReference" ),
"kAAFTypeID_InterpolationDefinitionStrongReferenceSet" : ( "05050600-0000-0000-060e-2b3401040101" , "kAAFTypeID_InterpolationDefinitionStrongReference" ),
"kAAFTypeID_MobStrongReferenceSet" : ( "05050700-0000-0000-060e-2b3401040101" , "kAAFTypeID_MobStrongReference" ),
"kAAFTypeID_OperationDefinitionStrongReferenceSet" : ( "05050800-0000-0000-060e-2b3401040101" , "kAAFTypeID_OperationDefinitionStrongReference" ),
"kAAFTypeID_ParameterDefinitionStrongReferenceSet" : ( "05050900-0000-0000-060e-2b3401040101" , "kAAFTypeID_ParameterDefinitionStrongReference" ),
"kAAFTypeID_PluginDefinitionStrongReferenceSet" : ( "05050a00-0000-0000-060e-2b3401040101" , "kAAFTypeID_PluginDefinitionStrongReference" ),
"kAAFTypeID_PropertyDefinitionStrongReferenceSet" : ( "05050b00-0000-0000-060e-2b3401040101" , "kAAFTypeID_PropertyDefinitionStrongReference" ),
"kAAFTypeID_TypeDefinitionStrongReferenceSet" : ( "05050c00-0000-0000-060e-2b3401040101" , "kAAFTypeID_TypeDefinitionStrongReference" ),
"kAAFTypeID_KLVDataDefinitionStrongReferenceSet" : ( "05050d00-0000-0000-060e-2b3401040101" , "kAAFTypeID_KLVDataDefinitionStrongReference" ),
"kAAFTypeID_ParameterDefinitionWeakReferenceSet" : ( "05030e00-0000-0000-060e-2b3401040101" , "ParameterDefinitionWeakReference" ),
"kAAFTypeID_TaggedValueDefinitionStrongReferenceSet" : ( "05050e00-0000-0000-060e-2b3401040101" , "kAAFTypeID_TaggedValueDefinitionStrongReference" ),
}

strongrefs = {
"kAAFTypeID_ContentStorageStrongReference" : ( "05020100-0000-0000-060e-2b3401040101" , "ContentStorage" ),
"kAAFTypeID_DictionaryStrongReference" : ( "05020200-0000-0000-060e-2b3401040101" , "Dictionary" ),
"kAAFTypeID_EssenceDescriptorStrongReference" : ( "05020300-0000-0000-060e-2b3401040101" , "EssenceDescriptor" ),
"kAAFTypeID_NetworkLocatorStrongReference" : ( "05020400-0000-0000-060e-2b3401040101" , "NetworkLocator" ),
"kAAFTypeID_OperationGroupStrongReference" : ( "05020500-0000-0000-060e-2b3401040101" , "OperationGroup" ),
"kAAFTypeID_SegmentStrongReference" : ( "05020600-0000-0000-060e-2b3401040101" , "Segment" ),
"kAAFTypeID_SourceReferenceStrongReference" : ( "05020800-0000-0000-060e-2b3401040101" , "SourceReference" ),
"kAAFTypeID_ClassDefinitionStrongReference" : ( "05020900-0000-0000-060e-2b3401040101" , "ClassDefinition" ),
"kAAFTypeID_CodecDefinitionStrongReference" : ( "05020a00-0000-0000-060e-2b3401040101" , "CodecDefinition" ),
"kAAFTypeID_ComponentStrongReference" : ( "05020b00-0000-0000-060e-2b3401040101" , "Component" ),
"kAAFTypeID_ContainerDefinitionStrongReference" : ( "05020c00-0000-0000-060e-2b3401040101" , "ContainerDefinition" ),
"kAAFTypeID_ControlPointStrongReference" : ( "05020d00-0000-0000-060e-2b3401040101" , "ControlPoint" ),
"kAAFTypeID_DataDefinitionStrongReference" : ( "05020e00-0000-0000-060e-2b3401040101" , "DataDefinition" ),
"kAAFTypeID_EssenceDataStrongReference" : ( "05020f00-0000-0000-060e-2b3401040101" , "EssenceData" ),
"kAAFTypeID_IdentificationStrongReference" : ( "05021000-0000-0000-060e-2b3401040101" , "Identification" ),
"kAAFTypeID_InterpolationDefinitionStrongReference" : ( "05021100-0000-0000-060e-2b3401040101" , "InterpolationDefinition" ),
"kAAFTypeID_LocatorStrongReference" : ( "05021200-0000-0000-060e-2b3401040101" , "Locator" ),
"kAAFTypeID_MobStrongReference" : ( "05021300-0000-0000-060e-2b3401040101" , "Mob" ),
"kAAFTypeID_MobSlotStrongReference" : ( "05021400-0000-0000-060e-2b3401040101" , "MobSlot" ),
"kAAFTypeID_OperationDefinitionStrongReference" : ( "05021500-0000-0000-060e-2b3401040101" , "OperationDefinition" ),
"kAAFTypeID_ParameterStrongReference" : ( "05021600-0000-0000-060e-2b3401040101" , "Parameter" ),
"kAAFTypeID_ParameterDefinitionStrongReference" : ( "05021700-0000-0000-060e-2b3401040101" , "ParameterDefinition" ),
"kAAFTypeID_PluginDefinitionStrongReference" : ( "05021800-0000-0000-060e-2b3401040101" , "PluginDefinition" ),
"kAAFTypeID_PropertyDefinitionStrongReference" : ( "05021900-0000-0000-060e-2b3401040101" , "PropertyDefinition" ),
"kAAFTypeID_TaggedValueStrongReference" : ( "05021a00-0000-0000-060e-2b3401040101" , "TaggedValue" ),
"kAAFTypeID_TypeDefinitionStrongReference" : ( "05021b00-0000-0000-060e-2b3401040101" , "TypeDefinition" ),
"kAAFTypeID_KLVDataStrongReference" : ( "05021c00-0000-0000-060e-2b3401040101" , "KLVData" ),
"kAAFTypeID_FileDescriptorStrongReference" : ( "05021d00-0000-0000-060e-2b3401040101" , "FileDescriptor" ),
"kAAFTypeID_DescriptiveFrameworkStrongReference" : ( "05021f00-0000-0000-060e-2b3401040101" , "DescriptiveFramework" ),
"kAAFTypeID_KLVDataDefinitionStrongReference" : ( "05022000-0000-0000-060e-2b3401040101" , "KLVDataDefinition" ),
"kAAFTypeID_TaggedValueDefinitionStrongReference" : ( "05022100-0000-0000-060e-2b3401040101" , "TaggedValueDefinition" ),
"kAAFTypeID_SubDescriptorStrongReference" : ( "05022600-0000-0000-060e-2b3401040101" , "SubDescriptor" ),
"AvidStrongReference" : ( "f9a74d0a-7b30-11d3-a044-006094eb75cb" , "InterchangeObject" ),
}

weakrefs = {
"ClassDefinitionWeakReference" : ( "05010100-0000-0000-060e-2b3401040101" , "ClassDefinition" ,
     ( "MetaDictionary", "ClassDefinitions" )),
"ContainerDefinitionWeakReference" : ( "05010200-0000-0000-060e-2b3401040101" , "ContainerDefinition" ,
     ( "Header", "Dictionary", "ContainerDefinitions" )),
"DataDefinitionWeakReference" : ( "05010300-0000-0000-060e-2b3401040101" , "DataDefinition" ,
     ( "Header", "Dictionary", "DataDefinitions" )),
"InterpolationDefinitionWeakReference" : ( "05010500-0000-0000-060e-2b3401040101" , "InterpolationDefinition" ,
     ( "Header", "Dictionary", "InterpolationDefinitions" )),
"OperationDefinitionWeakReference" : ( "05010700-0000-0000-060e-2b3401040101" , "OperationDefinition" ,
     ( "Header", "Dictionary", "OperationDefinitions" )),
"ParameterDefinitionWeakReference" : ( "05010800-0000-0000-060e-2b3401040101" , "ParameterDefinition" ,
     ( "Header", "Dictionary", "ParameterDefinitions" )),
"TypeDefinitionWeakReference" : ( "05010900-0000-0000-060e-2b3401040101" , "TypeDefinition" ,
     ( "MetaDictionary", "TypeDefinitions" )),
"CodecDefinitionWeakReference" : ( "05010b00-0000-0000-060e-2b3401040101" , "CodecDefinition" ,
     ( "Header", "Dictionary", "CodecDefinitions" )),
}
