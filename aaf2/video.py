from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from struct import unpack
from . utils import int_from_bytes
from io import BytesIO

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
'dnxhr_lb'             : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_lb", },
'dnxhr_sq'             : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_sq", },
'dnxhr_hq'             : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_hq", },
'dnxhr_hqx'            : { "size" : None,         'interlaced' : False, "bitrate" : None, "pix_fmt" : "yuv422p",   "frame_rate" : None, "video_profile": "dnxhr_hqx",},
}

dnxhd_frame_sizes = {
1235 : 917504,
1237 : 606208,
1238 : 917504,
1241 : 917504,
1242 : 606208,
1243 : 917504,
1244 : 606208,
1250 : 458752,
1251 : 458752,
1252 : 303104,
1253 : 188416,
1256 : 1835008,
1258 : 212992,
1259 : 417792,
1260 : 835584,
}

dnxhr_compression_ratio = {
1270 : (57344, 255),
1271 : (28672, 255),
1272 : (28672, 255),
1273 : (18944, 255),
1274 : (5888, 255),
}

def dnx_frame_size(cid, width=None, height=None):
    size = dnxhd_frame_sizes.get(cid, None)
    if size:
        return size

    # DNxHR frame size caclulation
    ratio = dnxhr_compression_ratio[cid]
    size = ((height + 15) // 16) * ((width + 15) // 16) * ratio[0] // ratio[1]
    size = (size + 2048) // 4096 * 4096;

    return max(size, 8192);


def valid_dnx_prefix(prefix):

    # DNxHD prefix
    dnxhd_header_prefix = 0x000002800100
    if prefix == dnxhd_header_prefix:
        return True

    # DNxHR prefix
    data_offset = prefix >> 16
    if ((prefix & 0xFFFF0000FFFF) == 0x0300 and
         data_offset >= 0x0280 and data_offset <= 0x2170 and
         (data_offset & 3) == 0):
        return True

    return False

def read_dnx_frame_header(dnx_header):
    if len(dnx_header) < 640:
        raise ValueError("Invalid DNxHD frame: header to Short")

    prefix = int_from_bytes(bytearray(dnx_header[:6])) & 0xffffffffff00
    if not valid_dnx_prefix(prefix):
        raise ValueError("Invalid DNxHD frame: unknown prefix: 0x%012X" % prefix)

    #NOTE Stored height then width...
    height, width = unpack(">24xhh", dnx_header[:28])
    cid = unpack(">40xi", dnx_header[:44])[0]

    interlaced =  unpack('B', dnx_header[5:6])[0] & 2 != 0
    bitdepth = unpack('B', dnx_header[33:34])[0] >> 5
    if bitdepth == 1:
        bitdepth = 8
    elif bitdepth == 2:
        bitdepth = 10
    elif bitdepth == 3:
        bitdepth = 12
    else:
        raise ValueError("Invalid DNxHD frame: unknown bitdepth: %d" % bitdepth)

    horizontal_subsampling = 2
    # 444 HorizontalSubsampling
    if (unpack('B', dnx_header[44:45])[0] >> 6) & 1 != 0:
        raise NotImplementedError("444 not tested")
        horizontal_subsampling = 4

    return cid, width, height, bitdepth, interlaced

def iter_dnx_stream(f):
    while True:
        dnx_header = f.read(640)
        if not dnx_header or len(dnx_header) != 640:
            break
        cid, width, height, bitdepth, interlaced = read_dnx_frame_header(dnx_header)
        frame_size = dnx_frame_size(cid, width, height)

        data = BytesIO()
        data.write(dnx_header)
        data.write(f.read(frame_size - 640))
        yield data.getvalue()
