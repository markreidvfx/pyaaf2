import aaf2

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
from aaf2 import auid

from pprint import pprint

FFMPEG_EXEC = "ffmpeg"
FFPROBE_EXEC = "ffprobe"

Audio_Profiles = aaf2.audio.pcm_profiles
Video_Profiles = aaf2.video.dnx_profiles

# FFMPEG_EXEC = "/Users/mark/Dev/ffmpeg/ffmpeg_g"
# FFPROBE_EXEC = "/Users/mark/Dev/ffmpeg/ffprobe_g"

def probe(path, show_packets=False):

    cmd = [FFPROBE_EXEC, '-of','json','-show_format','-show_streams', path]

    if show_packets:
        cmd.extend(['-show_packets',])
    print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout,stderr = p.communicate()

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, subprocess.list2cmdline(cmd), stderr)

    return json.loads(stdout)

def timecode_to_seconds(time_string):
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

def seconds_to_timecode(seconds):
    format = "%S.%f"
    t = datetime.timedelta(seconds=float(seconds))


    return str(t)

def has_alpha(stream):
    if stream['pix_fmt'] in ('yuva444p10le','rgba'):
        return True
    return False

def conform_media(path,
                  output_dir,
                  start=None,
                  end=None,
                  duration=None,
                  width=None,
                  height=None,
                  frame_rate=None,
                  video_profile_name=None,
                  audio_profile_name=None,
                  ignore_alpha=False):

    if not video_profile_name:
        video_profile_name = 'dnx_1080p_36_23.97'
    if not audio_profile_name:
        audio_profile_name = 'pcm_48000_s16le'

    video_profile = Video_Profiles[video_profile_name]
    audio_profile = Audio_Profiles[audio_profile_name]

    format = probe(path)

    out_files = []

    cmd = [FFMPEG_EXEC,'-y', '-nostdin']

    # cmd.extend(['-loglevel', 'debug'])

    if end:
        duration = timecode_to_seconds(end) - timecode_to_seconds(start)
        duration = seconds_to_timecode(duration)
        end = None

    if start:
        start_seconds = timecode_to_seconds(start)

        fast_start = max(0,int(start_seconds-30))

        if fast_start:
            start = seconds_to_timecode(start_seconds - fast_start)
            cmd.extend(['-ss', seconds_to_timecode(fast_start)])

    frame_rate = video_profile['frame_rate']
    pix_fmt = video_profile['pix_fmt']
    bitrate = video_profile['bitrate']
    dnxhd_profile = video_profile.get("video_profile", None)

    if format['format']['format_name'] == "image2":
        frame_rate = frame_rate or "24000/1001"
        cmd.extend([ '-framerate', frame_rate])

    cmd.extend(['-i', path,])
    if video_profile['size']:
        width, height = video_profile['size']
    else:
        width = None
        height = None

    interlaced = video_profile['interlaced']

    #sample_rate =44100
    sample_rate = audio_profile['sample_rate']

    for stream in format['streams']:

        #pprint(stream)
        stream_index = stream['index']
        if stream['codec_type'] == 'video':
            out_meta = {}
            # pprint(stream)
            alpha = has_alpha(stream)
            passes = 1
            if alpha and not ignore_alpha:
                passes = 2
            for i in range(passes):
                if i == 1:
                    cmd.extend(['-an', '-f', 'rawvideo', '-pix_fmt', 'gray'])
                    if frame_rate:
                        cmd.extend(['-r', frame_rate])
                else:
                    cmd.extend(['-an','-vcodec', 'dnxhd', '-pix_fmt', pix_fmt])
                    if dnxhd_profile:
                        cmd.extend(['-profile:v', dnxhd_profile])

                    if bitrate:
                        cmd.extend(['-vb', '%dM' % bitrate])
                    if frame_rate:
                        cmd.extend(['-r', frame_rate])

                if not start is None:
                    cmd.extend(['-ss', str(start)])

                if not duration is None:
                    cmd.extend(['-t', str(duration)])

                vfilter = []
                if i == 1:
                    vfilter.append("alphaextract")

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

                    padding_ofs_x = (max_width  - scale_width)/2
                    padding_ofs_y = (max_height - scale_height)/2


                    vfilter.append("scale=%d:%d,pad=%d:%d:%d:%d" % (scale_width,scale_height,
                                                               max_width,max_height, padding_ofs_x,padding_ofs_y))
                else:
                    out_width = stream['width']
                    out_height = stream['height']

                if vfilter:
                    cmd.extend(['-vf', ','.join(vfilter)])
                    # cmd.extend(['-s', "%dx%d" % (width, height)])

                if i == 1:
                    out_file = os.path.join(output_dir, 'out_%d.alpha' % (stream_index))
                    out_meta['path_alpha'] = out_file
                else:
                    out_rate = frame_rate or str(stream['avg_frame_rate'])
                    out_file = os.path.join(output_dir, 'out_%d.dnxhd' % (stream_index))
                    out_meta = {'path':out_file, 'frame_rate':out_rate, 'type': 'video', 'profile':video_profile_name}
                    out_meta['width'] = out_width
                    out_meta['height'] = out_height

                cmd.extend([out_file])

                #pprint(stream)
                print("USING FRAMREATE",  out_rate, str(stream['avg_frame_rate']))

            out_files.append(out_meta)

        elif stream['codec_type'] == 'audio':

            input_sample_rate = int(stream['sample_rate'])
            channels = stream['channels']

            cmd.extend(['-vn', '-acodec', 'pcm_s16le', '-ar', str(sample_rate)])
            # afilter = ['-af', "aresample=async=1:first_pts=0"]
            # cmd.extend(afilter)
            if not start is None:
                cmd.extend(['-ss', str(start)])

            if not duration is None:
                cmd.extend(['-t', str(duration)])

            out_file = os.path.join(output_dir, 'out_%d_%d_%d.wav' % (stream_index, sample_rate, channels))

            cmd.extend([out_file])

            out_files.append({'path':out_file, 'sample_rate':sample_rate, 'channels':channels,'type': 'audio'})

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


def import_video_essence(f, mastermob, stream, compmob=None, tapemob=None):
    tape = None
    edit_rate = stream['frame_rate']

    if tapemob:
        timecode_fps=  int(round(float(fractions.Fraction(edit_rate))))
        start_time = timecode_fps * 60 * 60
        tape = tapemob.create_source_clip(1, start=start_time)

    alpha_path = stream.get("path_alpha", None)

    color_slot = mastermob.import_dnxhd_essence(stream['path'], edit_rate, tape=tape)
    if alpha_path:
        pixel_layout = [{u'Code': u'CompAlpha', u'Size': 8}]
        width = stream['width']
        height = stream['height']

        source_mob = f.create.SourceMob()
        f.content.mobs.append(source_mob)
        if tapemob:
            tape = tapemob.create_source_clip(1, start=start_time)

        source_slot = source_mob.import_rawvideo_essence(alpha_path, edit_rate, width, height, pixel_layout, tape=tape)
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

def create_aaf(path, media_streams, mobname, tape_name=None, start_timecode=None):

    with aaf2.open(path, 'w') as f:

        mastermob = f.create.MasterMob(mobname)
        f.content.mobs.append(mastermob)

        edit_rate = None
        for stream in media_streams:
            if stream['type'] == 'video':
                edit_rate =fractions.Fraction(stream['frame_rate'])
                break

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
        timecode_fps=  int(round(float(edit_rate)))

        if tape_name:
            tapemob = f.create.SourceMob()
            tapemob.create_tape_slots(tape_name, edit_rate, timecode_fps)
            f.content.mobs.append(tapemob)

        for stream in media_streams:
            if stream['type'] == 'video':
                print("importing video...")
                start = time.time()
                import_video_essence(f, mastermob, stream, compmob, tapemob)
                print("imported video in %f secs" % (time.time()- start))

        for stream in media_streams:
            if stream['type'] == 'audio':
                print("importing audio...")
                start = time.time()
                sample_rate = stream['sample_rate']
                slot = mastermob.import_audio_essence(stream['path'], edit_rate)
                if compmob:
                    sound_slot = compmob.create_sound_slot(edit_rate)
                    sound_slot.segment = mastermob.create_source_clip(slot.slot_id, length = slot.segment.length)

                print("imported audio in %f secs" % (time.time()- start))




if __name__ == "__main__":
    from optparse import OptionParser

    usage = "usage: %prog [options] output_aaf_file media_file"
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--start', type="string", dest="start",default=None,
                      help = "start recording at, in timecode or seconds")
    parser.add_option('-e', '--end', type="string", dest='end',default=None,
                      help = "end recording at in timecode or seconds")
    parser.add_option('-d', '--duration', type="string", dest='duration',default=None,
                      help = "record duration in timecode or seconds")

    parser.add_option('--tape',  type="string", dest="tape_name",default=None,
                      help = "tape name")

    parser.add_option('--start_timecode',  type="string", dest="start_timecode", default=None,
                      help = "start timecode [default 01:00:00:00]")

    parser.add_option('--ignore_alpha', action='store_true', dest="ignore_alpha", default=False,
                      help = "ignore alpha channel if present")

    parser.add_option("-v", '--video-profile', type='string', dest = 'video_profile', default="dnx_1080p_36_23.97",
                      help = "encoding profile for video [default: 1080p_36_23.97]")
    parser.add_option("-a", '--audio-profile', type='string', dest = 'audio_profile',default='pcm_48000_s16le',
                      help = 'encoding profile for audio [default: pcm_48000]')

    parser.add_option("--size", type='string', dest='size', default=None,
                      help = "video resolution for dnxhr [default: src size]")
    parser.add_option("--framerate", type='string', dest='framerate',
                      help = "video framerate for dnxhr [default: use src rate]")

    parser.add_option('--list-profiles', dest='list_profiles',
                      action="store_true",default=False,
                      help = "lists profiles")

    (options, args) = parser.parse_args()


    if options.list_profiles:

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
            print(row_format.format(key, value['size'],
                                    value['frame_rate'], value['bitrate'], value['pix_fmt'], codec))

        sys.exit()

    if len(args) < 2:
        parser.error("not enough args")

    details = probe(args[1])


    #if not os.path.exists(args[1]):
        #parser.error("No such file or directory: %s" % args[1])

    if options.end and options.duration:
        parser.error("Can only use --duration or --end not both")

    print(options.audio_profile)
    if not options.audio_profile in Audio_Profiles:
        parser.error("No such audio profile: %s" % options.audio_profile)

    if not options.video_profile.lower() in Video_Profiles:
        parser.error("No such video profile: %s" % options.video_profile)

    aaf_file = args[0]

    # tempdir = os.path.join(os.getcwd(), 'samples', 'convert')
    # if not os.path.exists(tempdir):
    #     os.makedirs(tempdir)
    tempdir = tempfile.mkdtemp("-aaf_import")
    print(tempdir)

    media_streams = []

    width = None
    height = None
    if options.size and options.video_profile.lower().startswith("dnxhr"):
        width,height = options.size.split("x")
        width = int(width)
        height = int(height)

    try:
        for src in args[1:]:
            media_streams.extend(conform_media(src,
                                 output_dir=tempdir,
                                 start=options.start,
                                 end=options.end,
                                 duration=options.duration,
                                 width=width,
                                 height=height,
                                 frame_rate=options.framerate,
                                 video_profile_name = options.video_profile.lower(),
                                 audio_profile_name = options.audio_profile.lower(),
                                 ignore_alpha = options.ignore_alpha)
                                 )
    except:
        print(traceback.format_exc())
        shutil.rmtree(tempdir)
        parser.error("error conforming media")

    try:
        basename = os.path.basename(args[1])
        name,ext = os.path.splitext(basename)
        if details['format']['format_name'] == 'image2':
            name, padding = os.path.splitext(name)
        create_aaf(aaf_file, media_streams, name, options.tape_name, options.start_timecode)
    finally:
        pass
        shutil.rmtree(tempdir)
