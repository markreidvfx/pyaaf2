ints = {
}

enums = {
"ColorSitingType"     : ("02010105-0000-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101",{
      5 : "LineAlternating",
      6 : "VerticalMidpoint",
   }
),
"AvidPannerKindType"  : ("3659b342-4f19-4316-9309-f139434a94e5", "01010300-0000-0000-060e-2b3401040101",{
      1 : "AvidPannerKind_Stereo",
      2 : "AvidPannerKind_LCR",
      3 : "AvidPannerKind_Quad",
      4 : "AvidPannerKind_LCRS",
      5 : "AvidPannerKind_5dot0",
      6 : "AvidPannerKind_5dot1",
      7 : "AvidPannerKind_6dot0",
      8 : "AvidPannerKind_6dot1",
      9 : "AvidPannerKind_7dot0",
     10 : "AvidPannerKind_7dot1",
   }
),
"AvidEssenceElementSizeKind" : ("0e040201-0101-0000-060e-2b3401040101", "01010100-0000-0000-060e-2b3401040101",{
      0 : "AvidEssenceElementSizeKind_Unknown",
      1 : "AvidEssenceElementSizeKind_CBE",
      2 : "AvidEssenceElementSizeKind_VBE",
   }
),
}

records = {
"BoundsBox"           : ("0e040301-0200-0000-060e-2b3401040101", (
   ("PositionX"          ,"03010100-0000-0000-060e-2b3401040101"),
   ("PositionY"          ,"03010100-0000-0000-060e-2b3401040101"),
   ("Width"              ,"03010100-0000-0000-060e-2b3401040101"),
   ("Height"             ,"03010100-0000-0000-060e-2b3401040101"),
   ),
),
"AvidManifestElement" : ("0e040301-0100-0000-060e-2b3401040101", (
   ("did"                ,"01010100-0000-0000-060e-2b3401040101"),
   ("sdid"               ,"01010100-0000-0000-060e-2b3401040101"),
   ),
),
"EqualizationBand"    : ("c4c670c9-bd44-11d3-80e9-006008143e6f", (
   ("type"               ,"01030100-0000-0000-060e-2b3401040101"),
   ("frequency"          ,"01010300-0000-0000-060e-2b3401040101"),
   ("gain"               ,"01010300-0000-0000-060e-2b3401040101"),
   ("q"                  ,"01010300-0000-0000-060e-2b3401040101"),
   ("enable"             ,"01040100-0000-0000-060e-2b3401040101"),
   ),
),
"RGBColor"            : ("e96e6d43-c383-11d3-a069-006094eb75cb", (
   ("red"                ,"01010200-0000-0000-060e-2b3401040101"),
   ("green"              ,"01010200-0000-0000-060e-2b3401040101"),
   ("blue"               ,"01010200-0000-0000-060e-2b3401040101"),
   ),
),
"AudioSuitePlugInChunk" : ("4e4d8f5f-eefd-11d3-9ff5-0004ac969f50", (
   ("Version"            ,"01010300-0000-0000-060e-2b3401040101"),
   ("ManufacturerID"     ,"0f96cb41-2aa8-11d4-a00f-0004ac969f50"),
   ("ProductID"          ,"0f96cb41-2aa8-11d4-a00f-0004ac969f50"),
   ("PlugInID"           ,"0f96cb41-2aa8-11d4-a00f-0004ac969f50"),
   ("ChunkID"            ,"0f96cb41-2aa8-11d4-a00f-0004ac969f50"),
   ("Name"               ,"3271a34f-f3a1-11d3-9ff5-0004ac969f50"),
   ("ChunkDataUID"       ,"01030100-0000-0000-060e-2b3401040101"),
   ),
),
}

fixed_arrays = {
"AvidBounds"          : ("8bc42732-6bab-11d3-80cf-006008143e6f", "01010100-0000-0000-060e-2b3401040101", 48),
"AvidColor"           : ("8bc42733-6bab-11d3-80cf-006008143e6f", "01010100-0000-0000-060e-2b3401040101", 68),
"AvidCrop"            : ("8bc4272f-6bab-11d3-80cf-006008143e6f", "01010100-0000-0000-060e-2b3401040101", 32),
"AvidGlobalKeyFrame"  : ("09997778-960e-11d3-a04e-006094eb75cb", "01010100-0000-0000-060e-2b3401040101", 16),
"AvidPosition"        : ("8bc4272e-6bab-11d3-80cf-006008143e6f", "01010100-0000-0000-060e-2b3401040101", 24),
"AvidScale"           : ("8bc42730-6bab-11d3-80cf-006008143e6f", "01010100-0000-0000-060e-2b3401040101", 16),
"AvidSpillSupress"    : ("8bc42731-6bab-11d3-80cf-006008143e6f", "01010100-0000-0000-060e-2b3401040101", 8),
"AvidString4"         : ("0f96cb41-2aa8-11d4-a00f-0004ac969f50", "01010100-0000-0000-060e-2b3401040101", 4),
"AvidWideString32"    : ("3271a34f-f3a1-11d3-9ff5-0004ac969f50", "01010200-0000-0000-060e-2b3401040101", 32),
}

var_arrays = {
"AudioSuitePIChunkArray"                            : ("4e4d8f60-eefd-11d3-9ff5-0004ac969f50", "4e4d8f5f-eefd-11d3-9ff5-0004ac969f50"),
"AudioSuitePIChunkData"                             : ("5cf19caf-ef83-11d3-9ff5-0004ac969f50", "01010100-0000-0000-060e-2b3401040101"),
"AvidBagOfBits"                                     : ("ccaa73d1-f538-11d3-a081-006094eb75cb", "01010100-0000-0000-060e-2b3401040101"),
"AvidManifestArray"                                 : ("0e040402-0100-0000-060e-2b3401040101", "0e040301-0100-0000-060e-2b3401040101"),
"AvidTKMNTrackedParamArray"                         : ("b56a2ec2-fc3b-11d3-9ff7-0004ac969f50", "f9a74d0a-7b30-11d3-a044-006094eb75cb"),
"AvidTKMNTrackerDataArray"                          : ("b56a2ec3-fc3b-11d3-9ff7-0004ac969f50", "f9a74d0a-7b30-11d3-a044-006094eb75cb"),
"EqualizationBandArray"                             : ("c4c670ca-bd44-11d3-80e9-006008143e6f", "c4c670c9-bd44-11d3-80e9-006008143e6f"),
"kAAFTypeID_SubDescriptorStrongReferenceVector"     : ("05060e00-0000-0000-060e-2b3401040101", "05022600-0000-0000-060e-2b3401040101"),
}

renames = {
}

strings = {
}

streams = {
}

opaques = {
}

extenums = {
"CodingEquationsType" : ("02020106-0000-0000-060e-2b3401040101", {
   "0e040501-0201-0000-060e-2b3404010101" : "CodingEquations_ITU2020",
   },
),
"ColorPrimariesType"  : ("02020105-0000-0000-060e-2b3401040101", {
   "04010101-0304-0000-060e-2b340401010d" : "ColorPrimaries_ITU2020",
   "0e040501-0301-0000-060e-2b3404010101" : "ColorPrimaries_SMPTE_RP431",
   "0e040501-0302-0000-060e-2b3404010101" : "ColorPrimaries_Sony_SGamut3",
   "0e040501-0303-0000-060e-2b3404010101" : "ColorPrimaries_Sony_SGamut3_Cine",
   },
),
"TransferCharacteristicType" : ("02020102-0000-0000-060e-2b3401040101", {
   "0e040501-0101-0000-060e-2b3404010101" : "TransferCharacteristic_DPXPrintingDensity",
   "0e040501-0102-0000-060e-2b3404010101" : "TransferCharacteristic_DPXLogarithmic",
   "0e040501-0103-0000-060e-2b3404010101" : "TransferCharacteristic_SRGB",
   "0e040501-0105-0000-060e-2b3404010101" : "TransferCharacteristic_SMPTE_RP431",
   "0e040501-0106-0000-060e-2b3404010101" : "TransferCharacteristic_SMPTE_ST2084",
   "0e040501-0108-0000-060e-2b3404010101" : "TransferCharacteristic_ARIB_B67",
   "0e040501-010a-0000-060e-2b3404010101" : "TransferCharacteristic_ITU709_Extended2",
   "0e060401-0101-0605-060e-2b3404010106" : "TransferCharacteristic_Sony_SLog3",
   "0e170000-0001-0101-060e-2b340401010c" : "TransferCharacteristic_ARRI_LogC",
   },
),
}

chars = {
}

indirects = {
}

sets = {
}

strongrefs = {
"AvidStrongReference"                               : ("f9a74d0a-7b30-11d3-a044-006094eb75cb", "0d010101-0101-0100-060e-2b3402060101"),
"kAAFTypeID_SubDescriptorStrongReference"           : ("05022600-0000-0000-060e-2b3401040101", "0d010101-0101-5900-060e-2b3402060101"),
}

weakrefs = {
}
