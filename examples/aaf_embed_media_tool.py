#!/usr/bin/env python
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import traceback
import subprocess
import json
import os
import datetime
import sys
import tempfile
import shutil
import time
import fractions
import random
import string
import re
import math
from pprint import pprint

import aaf2

FFMPEG_EXEC = "ffmpeg"
FFPROBE_EXEC = "ffprobe"

Audio_Profiles = aaf2.audio.pcm_profiles
Video_Profiles = aaf2.video.dnx_profiles

def probe(path, show_packets=False):

    cmd = [FFPROBE_EXEC, '-of','json','-show_format','-show_streams', '-i', path]

    if show_packets:
        cmd.extend(['-show_packets',])
    print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout,stderr = p.communicate()

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, subprocess.list2cmdline(cmd), stderr)

    return json.loads(stdout)

def ffmpeg_timecode_to_seconds(time_string):
    try:
        return float(time_string)
    except:
        pass

    for format in ("%H:%M:%S.%f", "%H:%M:%S", "%M:%S.%f","%M:%S"):
        try:
            t = datetime.datetime.strptime(time_string, format)

            seconds = 0

            if t.minute:
                seconds += 60*t.minute

            if t.hour:
                seconds += 60 * 60 * t.hour
            seconds += t.second
            seconds += float(t.strftime(".%f"))

            return seconds
        except:
            #print traceback.format_exc()
            pass

    raise ValueError("invalid time format: %s" % time_string)

def timecode_to_frames(timecode_string, frame_rate=24):
    # 01:00:00:00
    TC_FORMAT = r"(?P<hours>[0-9]{2})[:](?P<minutes>[0-9]{2})[:](?P<seconds>[0-9]{2})[:;](?P<frames>[0-9]{2})"
    m = re.fullmatch(TC_FORMAT, timecode_string)

    if not m:
        raise ValueError("invalid timecode format: %s" % str(timecode_string))

    dropframes = 0
    if timecode_string.count(';'):
        if frame_rate == 30:
            dropframes = 2
        elif frame_rate == 60:
            dropframes = 4
        else:
            raise ValueError("drop frame tc only supported for 30 or 60 fps")

    d = m.groupdict()
    hours = int(d['hours'])
    minutes = int(d['minutes'])
    seconds = int(d['seconds'])
    frames  = int(d['frames'])

    total_minutes = hours * 60 + minutes

    frames += (((total_minutes * 60) + seconds) * frame_rate)
    frames -= dropframes * (total_minutes - (total_minutes // 10))

    return frames

def get_nearest_rate(frame_rate, rates):
    nearest = None
    min_diff = float('inf')
    frame_rate = float(frame_rate)

    for (num, den) in rates:
        valid_rate = float(num)/float(den)
        if frame_rate == valid_rate:
            return [num, den]

        diff = abs(frame_rate - valid_rate)
        if (diff >= min_diff):
            continue
        min_diff = diff
        nearest = [num, den]

    return nearest

def get_nearest_edit_rate(frame_rate):
    rates = ((12,       1),
             (15,       1),
             (24000, 1001),
             (24,       1),
             (25,       1),
             (30000, 1001),
             (30,       1),
             (48,       1),
             (60000, 1001),
             (50,       1),
             (60,       1),
             (100,      1),
             (120,      1),
             (240,      1))

    return get_nearest_rate(frame_rate, rates)

def get_nearest_timecode_rate(frame_rate):
    rates = ((24, 1),
             (25, 1),
             (30, 1),
             (48, 1),
             (50, 1),
             (60, 1))

    return get_nearest_rate(frame_rate, rates)[0]

def has_alpha(stream):
    if stream['pix_fmt'] in ('yuva444p10le','rgba'):
        return True
    return False

def random_str(size=12, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_embedded_timecode(format):
    for stream in format['streams']:
        timecode_rate = stream.get("avg_frame_rate", None)
        timecode = stream.get("tags", {}).get("timecode", None)
        if timecode:
            return timecode, timecode_rate

    timecode = format.get("format",{}).get("tags", {}).get("timecode", None)

    for stream in format['streams']:
        timecode_rate = stream.get("avg_frame_rate", None)
        if timecode_rate:
            break


    return timecode, timecode_rate


def ffmpeg_convert(path,
                   output_dir,
                   width=None,
                   height=None,
                   frame_rate=None,
                   video_profile_name=None,
                   audio_profile_name=None,
                   ignore_alpha=False,
                   copy_dnxhd_streams=True,
                   use_embedded_timecode=True,
                   lut3d_path=None):

    if not video_profile_name:
        video_profile_name = 'dnx_1080p_36_23.97'
    if not audio_profile_name:
        audio_profile_name = 'pcm_48000_s16le'

    video_profile = Video_Profiles[video_profile_name]
    audio_profile = Audio_Profiles[audio_profile_name]

    format = probe(path)
    out_files = []

    cmd = [FFMPEG_EXEC,'-y', '-nostdin']
    cmd.extend(['-loglevel', 'error'])
    # cmd.extend(['-loglevel', 'debug'])

    if frame_rate and video_profile['frame_rate']:
        # older versions of pyaaf are missing some 24/60 variants of dnxhd codecs
        # check the the frame rate would be valid
        if video_profile['frame_rate'] in ('24000/1001', '60000/1001'):
            rounded_rate = round(float(fractions.Fraction(video_profile['frame_rate'])))
            assert round(frame_rate) == rounded_rate
    else:
        frame_rate = video_profile['frame_rate'] or frame_rate

    pix_fmt = video_profile['pix_fmt']
    bitrate = video_profile['bitrate']
    dnxhd_profile = video_profile.get("video_profile", None)

    if format['format']['format_name'] == "image2":
        frame_rate = frame_rate or 24
        cmd.extend([ '-framerate', str(frame_rate)])

    cmd.extend(['-i', path,])
    if video_profile['size']:
        width, height = video_profile['size']
    else:
        width = None
        height = None

    interlaced = video_profile['interlaced']
    if interlaced:
        raise ValueError("interlaced support not implemented")

    #sample_rate =44100
    sample_rate = audio_profile['sample_rate']

    prefix = random_str()

    if use_embedded_timecode:
        embedded_timecode, timecode_rate = get_embedded_timecode(format)
        if timecode_rate:
            try:
                timecode_rate = float(fractions.Fraction(timecode_rate))
            except:
                timecode_rate = None

        if embedded_timecode and timecode_rate:
            out_files.append({'start':embedded_timecode, 'rate':timecode_rate, 'type': 'timecode'})

    for stream in format['streams']:

        #pprint(stream)
        stream_index = stream['index']
        if stream['codec_type'] == 'video':
            out_meta = {}

            alpha = has_alpha(stream)
            is_dnxhd_codec = stream['codec_name'] == 'dnxhd'
            out_rate = frame_rate or str(stream['avg_frame_rate'])

            # disable resize on stream copy
            if copy_dnxhd_streams and is_dnxhd_codec:
                width = None
                height = None

            passes = 1
            if alpha and not ignore_alpha:
                passes = 2
            for i in range(passes):
                if i == 1:
                    cmd.extend(['-an', '-f', 'rawvideo', '-pix_fmt', 'gray'])
                    if frame_rate:
                        cmd.extend(['-r', str(frame_rate)])
                else:
                    if copy_dnxhd_streams and is_dnxhd_codec:
                        cmd.extend(['-an','-vcodec', 'copy'])
                    else:
                        cmd.extend(['-an','-vcodec', 'dnxhd', '-pix_fmt', pix_fmt])
                        if dnxhd_profile:
                            cmd.extend(['-profile:v', dnxhd_profile])

                        if bitrate:
                            cmd.extend(['-vb', '%dM' % bitrate])

                        if frame_rate:
                            cmd.extend(['-r', str(frame_rate)])


                cmd.extend(['-map', '0:%d' % stream_index])

                vfilter = []
                if i == 1:
                    vfilter.append("alphaextract")

                if i != 1 and lut3d_path:
                    # fix issues with windows paths, need to escape ':" for filter syntax
                    clean_path = lut3d_path.replace("\\", '/').replace(':', '\\:')
                    vfilter.append(f"lut3d=file='{clean_path}'")

                if width and height:
                    out_width = width
                    out_height = height

                    input_width = stream['width']
                    input_height = stream['height']

                    max_width = width
                    max_height = height

                    scale = min(max_width/ float(input_width), max_height/float(input_height) )

                    scale_width = int(input_width*scale)
                    scale_height = int(input_height*scale)

                    padding_ofs_x = (max_width  - scale_width)//2
                    padding_ofs_y = (max_height - scale_height)//2


                    vfilter.append("scale=%d:%d,pad=%d:%d:%d:%d" % (scale_width,scale_height,
                                                               max_width,max_height, padding_ofs_x,padding_ofs_y))
                else:
                    out_width = stream['width']
                    out_height = stream['height']

                if vfilter:
                    cmd.extend(['-vf', ','.join(vfilter)])

                if i == 1:
                    out_file = os.path.join(output_dir, 'out_%s_%d.alpha' % (prefix, stream_index))
                    out_meta['path_alpha'] = out_file
                else:
                    out_file = os.path.join(output_dir, 'out_%s_%d.dnxhd' % (prefix, stream_index))
                    out_meta = {'path':out_file, 'frame_rate':out_rate, 'type': 'video', 'profile':video_profile_name}
                    out_meta['width'] = out_width
                    out_meta['height'] = out_height

                cmd.extend([out_file])

                #pprint(stream)
                print("using frame rate",  out_rate, str(stream['avg_frame_rate']))

            out_files.append(out_meta)

        elif stream['codec_type'] == 'audio':

            channels = stream['channels']
            # NOTE: each channel of each stream gets extracted
            for channel in range(channels):
                cmd.extend(['-vn', '-acodec', 'pcm_s16le', '-ar', str(sample_rate)])
                cmd.extend(['-map', '0:%d' % stream_index, '-af', "pan=1c|c0=c%d" % (channel)])

                out_file = os.path.join(output_dir, 'out_%s_%d_%d_%d.wav' % (prefix, stream_index, channel, sample_rate))
                cmd.extend([out_file])
                out_files.append({'path':out_file, 'sample_rate':sample_rate, 'channels':1,'type': 'audio'})

    print(subprocess.list2cmdline(cmd))

    subprocess.check_call(cmd)

    return out_files

def create_matte_key_definition(f):
    opdef = f.create.OperationDef(auid.AUID("0c864774-e428-3b2d-8115-1c736806191a"), 'MatteKey_2')
    opdef['IsTimeWarp'].value = False
    opdef['OperationCategory'].value = 'OperationCategory_Effect'
    opdef['NumberInputs'].value = 3
    opdef['Bypass'].value = 2
    opdef.media_kind = "picture"
    f.dictionary.register_def(opdef)
    return opdef

def import_video_essence(f, mastermob, stream, compmob=None, tapemob=None, timecode_start_time=None):
    tape_clip = None
    edit_rate = stream['frame_rate']

    if tapemob:
        tape_clip = tapemob.create_source_clip(1, start=timecode_start_time)

    alpha_path = stream.get("path_alpha", None)
    color_slot = mastermob.import_dnxhd_essence(stream['path'], edit_rate, tape=tape_clip)

    if alpha_path:
        pixel_layout = [{u'Code': u'CompAlpha', u'Size': 8}]
        width = stream['width']
        height = stream['height']

        source_mob = f.create.SourceMob()
        f.content.mobs.append(source_mob)
        if tapemob:
            tape_clip = tapemob.create_source_clip(1, start=timecode_start_time)

        source_slot = source_mob.import_rawvideo_essence(alpha_path, edit_rate, width, height, pixel_layout, tape=tape_clip)
        length = source_slot.segment.length
        essence_group = f.create.EssenceGroup()
        alpha_slot = mastermob.create_picture_slot(edit_rate)
        alpha_slot.segment = essence_group

        source_clip = source_mob.create_source_clip(source_slot.slot_id)
        source_clip.length = length
        essence_group['Choices'].append(source_clip)
        essence_group.length = length

        opdef = create_matte_key_definition(f)

        slot = compmob.create_picture_slot(edit_rate)
        op_group = f.create.OperationGroup(opdef)
        slot.segment = op_group

        scope = f.create.ScopeReference()
        scope['RelativeScope'].value = 1
        scope['RelativeSlot'].value = 1
        scope.length = length

        sequence = f.create.Sequence(length=length)
        sequence.components.append(scope)

        op_group.segments.append(sequence)
        op_group.segments.append(mastermob.create_source_clip(color_slot.slot_id, length=length))
        op_group.segments.append(mastermob.create_source_clip(alpha_slot.slot_id, length=length))

    return color_slot

def create_mastermob_from_streams(f, media_streams, mob_name, tape_name=None, edit_rate = None):
    mastermob = f.create.MasterMob(mob_name)
    f.content.mobs.append(mastermob)
    if not edit_rate:
        for stream in media_streams:
            if stream['type'] == 'video':
                edit_rate = fractions.Fraction(stream['frame_rate'])
                break

    # get the start timecode
    timecode_rate = None
    start_timecode = None
    for stream in media_streams:
        if stream['type'] == 'timecode':
            start_timecode = stream['start']
            timecode_rate = stream['rate']
            if start_timecode:
                break

    timecode_rate = get_nearest_timecode_rate(timecode_rate or (float(edit_rate)))
    timecode_start_time = timecode_to_frames(start_timecode, timecode_rate)

    print("start timecode:", start_timecode, timecode_start_time, timecode_rate)

    alpha = False
    compmob = None
    for stream in media_streams:
        if stream.get('path_alpha', False):
            alpha = True
            compmob = f.create.CompositionMob(mastermob.name)
            compmob.usage = 'Usage_Template'
            f.content.mobs.append(compmob)

            # this hides the mastermob in avid bin
            mastermob['AppCode'].value = 1
            mastermob.usage = "Usage_LowerLevel"

            break

    tapemob = None
    timecode_slot = None
    if tape_name:
        tapemob = f.create.SourceMob()
        _, timecode_slot = tapemob.create_tape_slots(tape_name, edit_rate, timecode_rate)
        f.content.mobs.append(tapemob)

    for stream in media_streams:
        if stream['type'] == 'video':
            print("importing video...")
            start = time.time()
            slot = import_video_essence(f, mastermob, stream, compmob, tapemob, timecode_start_time)
            # otio currently uses the length of the timecodes slot length for available ranges
            # in a media reference ensure it matches video length
            timecode_slot.segment.length = slot.segment.length
            print("imported video in %f secs" % (time.time()- start))

    for stream in media_streams:

        if stream['type'] == 'audio':
            print("importing audio...")
            start = time.time()
            slot = mastermob.import_audio_essence(stream['path'], edit_rate)
            if compmob:
                sound_slot = compmob.create_sound_slot(edit_rate)
                sound_slot.segment = mastermob.create_source_clip(slot.slot_id, length = slot.segment.length)
            print("imported audio in %f secs" % (time.time()- start))

    return mastermob.mob_id

def create_aaf_file(source_paths,
                    output_aaf_path,
                    aaf_mob_name = None,
                    aaf_tape_name=None,
                    aaf_start_timecode=None,
                    aaf_start_timecode_rate=None,
                    working_dir=None,
                    width=None,
                    height=None,
                    frame_rate=None,
                    video_profile_name = None,
                    audio_profile_name = None,
                    ignore_alpha = False,
                    copy_dnxhd_streams = True,
                    use_embedded_timecode = True,
                    lut3d_path = None):

    temp_dir = None
    if not working_dir:
        temp_dir = tempfile.mkdtemp("-aaf_import")
        working_dir = temp_dir

    try:
        media_streams = []
        for src in source_paths:
            streams = ffmpeg_convert(src,
                                     output_dir=working_dir,
                                     width=width, height=height,
                                     frame_rate=frame_rate,
                                     video_profile_name = video_profile_name,
                                     audio_profile_name = audio_profile_name,
                                     ignore_alpha = ignore_alpha,
                                     copy_dnxhd_streams = copy_dnxhd_streams,
                                     use_embedded_timecode = use_embedded_timecode,
                                     lut3d_path = lut3d_path
                                     )
            media_streams.extend(streams)

        if not aaf_mob_name:
            basename = os.path.basename(source_paths[0])
            aaf_mob_name, _ = os.path.splitext(basename)
            details = probe(source_paths[0])
            if details['format']['format_name'] == 'image2':
                aaf_mob_name, _ = os.path.splitext(aaf_mob_name)

        if not aaf_tape_name:
            aaf_tape_name = aaf_mob_name

        # add default timecode
        aaf_start_timecode = aaf_start_timecode or '00:00:00:00'
        aaf_start_timecode_rate = aaf_start_timecode_rate or 24
        media_streams.append({'type': 'timecode', 'start': aaf_start_timecode, 'rate': aaf_start_timecode_rate})

        edit_rate = frame_rate
        with aaf2.open(output_aaf_path, 'w') as f:
            return create_mastermob_from_streams(f,
                                                 media_streams,
                                                 aaf_mob_name,
                                                 aaf_tape_name,
                                                 edit_rate)
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='import_media',
                                     description='tool for creating aaf files with embedded media')

    parser.add_argument('--name', dest="mob_name",default=None,
                        help = "master mob name")

    parser.add_argument('--tape', dest="tape_name",default=None,
                        help = "tape mob name")

    parser.add_argument('--start_timecode', dest="start_timecode", default='00:00:00:00',
                        help = "start timecode [default 00:00:00:00] used as failback timecode if --ignore_embedded_timecode not used")
    parser.add_argument('--start_timecode_rate', type=int, dest="start_timecode_rate", default=24,
                        help = "start timecode framerate")
    parser.add_argument("--ignore_embedded_timecode", action='store_false', dest="use_embedded_timecode", default=True,
                        help="don't use embedded timecode detected from ffprobe")

    parser.add_argument('--ignore_alpha', action='store_true', dest="ignore_alpha", default=False,
                         help = "ignore alpha channel if present")

    parser.add_argument('--lut3d', dest="lut3d", metavar="FILE",
                        help = "apply 3d lut to video tracks")

    parser.add_argument('--disable_dnxhd_copy', action='store_false', dest="copy_dnxhd_streams", default=True,
                        help = "force re-encoding of streams if they are already encoded in dnxhd")

    parser.add_argument("-v", '--video-profile', dest = 'video_profile', default="dnx_1080p_36_23.97",
                         help = "encoding profile for video [default: 1080p_36_23.97]")
    parser.add_argument("-a", '--audio-profile', dest = 'audio_profile',default='pcm_48000_s16le',
                        help = 'encoding profile for audio [default: pcm_48000]')

    parser.add_argument("--size", dest='size', default=None,
                        help = "video resolution for dnxhr [default: src size]")
    parser.add_argument("--framerate",  dest='framerate', type=float, default=None,
                        help = "video framerate for dnxhr [default: use src rate]")

    parser.add_argument('--list-profiles', dest='list_profiles',
                        action="store_true",default=False,
                        help = "lists profiles")

    parser.add_argument('-i', '--input', action='append', dest='inputs', default=[],
                        help="media files supported by ffmpeg, can be multiple")
    parser.add_argument('-o', '--output', help='output aaf')

    args = parser.parse_args()

    if args.list_profiles:
        titles = ['Audio Profile', 'Sample Rate', 'Sample Fmt']
        row_format ="{:<25}{:<15}{:<15}"

        print("")
        print(row_format.format( *titles))
        print("")

        for key,value in sorted(Audio_Profiles.items()):
            print(row_format.format(key, value['sample_rate'], value['sample_format']))

        titles = ['Video Profile', "Size", 'Frame Rate', "Bitrate", "Pix Fmt", "Codec"]
        row_format ="{:<25}{:<15}{:<15}{:<10}{:<12}{:<10}"
        print("")
        print(row_format.format( *titles))
        print("")
        for key, value in sorted(Video_Profiles.items()):
            codec = 'dnxhd'
            if key.startswith("dnxhr"):
                codec = 'dnxhr'

            size = "%dx%d" % value['size'] if value['size'] else 'variable'
            frame_rate = str(value['frame_rate']) if value['frame_rate'] else 'variable'
            bitrate = str(value['bitrate']) if value['bitrate'] else 'auto'

            print(row_format.format(key, size,
                                    frame_rate, bitrate, value['pix_fmt'], codec))

        sys.exit()

    if not args.inputs:
        parser.error("no input media specified")

    if not args.output:
        parser.error("no output aaf specified")

    print(args.audio_profile)
    if not args.audio_profile in Audio_Profiles:
        parser.error("No such audio profile: %s" % args.audio_profile)

    if not args.video_profile.lower() in Video_Profiles:
        parser.error("No such video profile: %s" % args.video_profile)

    try:
        timecode_to_frames(args.start_timecode, args.start_timecode_rate)
    except:
        parser.error("invalid timecode string: %s at %d fps" % (args.start_timecode, args.start_timecode_fps))

    width = None
    height = None

    if args.size and args.video_profile.lower().startswith("dnxhr"):
        try:
            width,height = args.size.split("x")
            width = int(width)
            height = int(height)
        except:
            parser.error("unable to parse size: %s" % args.size)

    try:
        create_aaf_file(source_paths=args.inputs,
                        output_aaf_path=args.output,
                        aaf_mob_name=args.mob_name,
                        aaf_tape_name=args.tape_name,
                        aaf_start_timecode=args.start_timecode,
                        aaf_start_timecode_rate=args.start_timecode_rate,
                        working_dir=None,
                        width=width, height=height,
                        frame_rate=args.framerate,
                        video_profile_name = args.video_profile.lower(),
                        audio_profile_name = args.audio_profile.lower(),
                        ignore_alpha = args.ignore_alpha,
                        copy_dnxhd_streams = args.copy_dnxhd_streams,
                        use_embedded_timecode = args.use_embedded_timecode,
                        lut3d_path = args.lut3d
                        )
    except:
        print(traceback.format_exc())
        sys.exit(-1)

if __name__ == "__main__":
    main()