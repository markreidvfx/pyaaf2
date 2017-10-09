from struct import unpack

dnx_profiles = {
'dnx_1080p_175x_23.97' : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 175,  "pix_fmt" : "yuv422p10", "frame_rate" : "24000/1001", },
'dnx_1080p_365x_50'    : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 185,  "pix_fmt" : "yuv422p10", "frame_rate" : "25/1",       },
'dnx_1080p_365x_60'    : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 365,  "pix_fmt" : "yuv422p10", "frame_rate" : "50/1",       },
'dnx_1080p_440x_23.97' : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 440,  "pix_fmt" : "yuv422p10", "frame_rate" : "60000/1001", },
'dnx_1080p_115_23.97'  : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 115,  "pix_fmt" : "yuv422p",   "frame_rate" : "24000/1001", },
'dnx_1080p_120_25'     : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 120,  "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_1080p_145_29.97'  : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 145,  "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_1080p_240_50'     : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 240,  "pix_fmt" : "yuv422p",   "frame_rate" : "50/1",       },
'dnx_1080p_290_59.94'  : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 290,  "pix_fmt" : "yuv422p",   "frame_rate" : "60000/1001", },
'dnx_1080p_175_23.97'  : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 175,  "pix_fmt" : "yuv422p",   "frame_rate" : "24000/1001", },
'dnx_1080p_185_25'     : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 185,  "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_1080p_220_29.97'  : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 220,  "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_1080p_365_50'     : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 365,  "pix_fmt" : "yuv422p",   "frame_rate" : "50/1",       },
'dnx_1080p_440_59.94'  : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 440,  "pix_fmt" : "yuv422p",   "frame_rate" : "60000/1001", },
'dnx_1080i_185x_25'    : { "size" : (1920, 1080), 'interlaced' : True,  "bitrate" : 185,  "pix_fmt" : "yuv422p10", "frame_rate" : "25/1",       },
'dnx_1080i_220x_29.97' : { "size" : (1920, 1080), 'interlaced' : True,  "bitrate" : 220,  "pix_fmt" : "yuv422p10", "frame_rate" : "30000/1001", },
'dnx_1080i_120_25'     : { "size" : (1920, 1080), 'interlaced' : True,  "bitrate" : 120,  "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_1080i_145_29.97'  : { "size" : (1920, 1080), 'interlaced' : True,  "bitrate" : 145,  "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_1080i_185_25'     : { "size" : (1920, 1080), 'interlaced' : True,  "bitrate" : 185,  "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_1080i_220_29.97'  : { "size" : (1920, 1080), 'interlaced' : True,  "bitrate" : 220,  "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_720p_90x_23.97'   : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 90,   "pix_fmt" : "yuv422p10", "frame_rate" : "24000/1001", },
'dnx_720p_90x_25'      : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 90,   "pix_fmt" : "yuv422p10", "frame_rate" : "25/1",       },
'dnx_720p_180x_50'     : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 180,  "pix_fmt" : "yuv422p10", "frame_rate" : "50/1",       },
'dnx_720p_220x_59.94'  : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 220,  "pix_fmt" : "yuv422p10", "frame_rate" : "60000/1001", },
'dnx_720p_90_23.97'    : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 90,   "pix_fmt" : "yuv422p",   "frame_rate" : "24000/1001", },
'dnx_720p_90_25'       : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 90,   "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_720p_110_29.97'   : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 110,  "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_720p_180_50'      : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 180,  "pix_fmt" : "yuv422p",   "frame_rate" : "50/1",       },
'dnx_720p_220_59.94'   : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 220,  "pix_fmt" : "yuv422p",   "frame_rate" : "60000/1001", },
'dnx_720p_60_23.97'    : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 60,   "pix_fmt" : "yuv422p",   "frame_rate" : "24000/1001", },
'dnx_720p_60_25'       : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 60,   "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_720p_75_29.97'    : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 75,   "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_720p_120_50'      : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 120,  "pix_fmt" : "yuv422p",   "frame_rate" : "50/1",       },
'dnx_720p_145_59.94'   : { "size" : (1280, 720),  'interlaced' : False, "bitrate" : 145,  "pix_fmt" : "yuv422p",   "frame_rate" : "60000/1001", },
'dnx_1080p_36_23.97'   : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 36,   "pix_fmt" : "yuv422p",   "frame_rate" : "24000/1001", },
'dnx_1080p_36_25'      : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 36,   "pix_fmt" : "yuv422p",   "frame_rate" : "25/1",       },
'dnx_1080p_45_29.97'   : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 45,   "pix_fmt" : "yuv422p",   "frame_rate" : "30000/1001", },
'dnx_1080p_75_50'      : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 75,   "pix_fmt" : "yuv422p",   "frame_rate" : "50/1",       },
'dnx_1080p_90_59.94'   : { "size" : (1920, 1080), 'interlaced' : False, "bitrate" : 90,   "pix_fmt" : "yuv422p",   "frame_rate" : "60000/1001", },
'dnxhr_lb'             : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_lb"},
'dnxhr_sq'             : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_sq"},
'dnxhr_hq'             : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_hq"},
'dnxhr_hqx'            : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_hqx"},
}

def read_dnx_header(path):
    f = open(path, 'rb')
    dnx_header = f.read(640)
    f.close()

    if len(dnx_header) != 640:
        raise ValueError("Invalid DNxHD file: header to Short")

    header_prefix = (0x00, 0x00, 0x02, 0x80, 0x01)

    if header_prefix != unpack(">BBBBB", dnx_header[:5]):
        raise ValueError("Invalid DNxHD file: header magick number wrong")

    width, height = unpack(">24xhh", dnx_header[:28])
    cid = unpack(">40xi", dnx_header[:44])[0]

    return width, height, cid
