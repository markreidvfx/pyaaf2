from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import json

import subprocess
import aaf2
from aaf2 import video, audio

FFMPEG_EXEC='ffmpeg'
FFPROBE_EXEC='ffprobe'
base = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def sandbox():
    dirname = os.path.join(base, 'results')
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    return dirname

def get_test_file(name):
    return os.path.join(sandbox(), name)

def test_files_dir():
    return os.path.join(base, 'test_files')

def test_file_01():
    return os.path.join(test_files_dir(), "test_file_01.aaf")

def test_file_512():
    return os.path.join(test_files_dir(), "sector_size_512.aaf")

def test_empty_file():
    return os.path.join(test_files_dir(), "empty.aaf")

def sample_dir():
    s = os.path.join(sandbox(), 'samples')
    if not os.path.exists(s):
        os.makedirs(s)

    return s

def dummy_print(*args):
    line = " ".join([str(item) for item in args])

def walk_aaf(root, space="", func=dummy_print):
    indent = "  "

    for p in root.properties():
        if isinstance(p, aaf2.properties.StrongRefProperty):
            func(space, p.name, p.typedef)
            walk_aaf(p.value, space + indent, func)

        if isinstance(p, aaf2.properties.StrongRefVectorProperty):
            func(space, p.name, p.typedef)
            for obj in p.value:
                func(space + indent, obj)
                walk_aaf(obj, space + indent*2, func)
            continue

        if isinstance(p, aaf2.properties.StrongRefSetProperty):
            func(space, p.name, p.typedef)
            for key, obj in p.items():
                func(space + indent, obj)
                walk_aaf(obj, space + indent*2, func)

            continue

        func(space, p.name, p.typedef, p.value)


def probe(path, show_packets=False):

    cmd = [FFPROBE_EXEC, '-of','json','-show_format','-show_streams', path]

    if show_packets:
        cmd.extend(['-show_packets',])

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout,stderr = p.communicate()

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, subprocess.list2cmdline(cmd), stderr)

    return json.loads(stdout.decode('utf8'))

def generate_mov(name, duration=2.0, frame_rate=23.97, audio_channels=2, overwrite=True, vcodec=None):
    frames = int(duration * float(frame_rate))
    audio_samples = []
    for i in range(audio_channels):
        sample = generate_pcm_audio_mono("%s_audio_%d.wav" % (name, i ), duration=duration)
        audio_samples.append(sample)


    size = (1920,1080)
    cmd = [FFMPEG_EXEC, '-y',]

    cmd.extend(['-f', 'lavfi', '-i', 'testsrc=size=%dx%d:rate=%s' % (size[0],size[1], frame_rate)])

    cmd.extend(['-frames:v', str(frames)])

    if vcodec:
        cmd.extend(vcodec)
    else:
        cmd.extend(['-pix_fmt', 'yuv420p'])
        cmd.extend(['-c:v', 'h264'])
        # cmd.extend(['-profile:v', 'high'])

    video_file = os.path.join(sample_dir(), name + "_video.mov")
    cmd.extend([video_file])
    # print(subprocess.list2cmdline(cmd))


    if overwrite or not os.path.exists(video_file):
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

        stdout,stderr = p.communicate()
        # print(stderr)
        if p.returncode != 0:
            print(stderr)
            return Exception("error video encoding footage")

    sample_rate= 48000
    cmd = [FFMPEG_EXEC, '-y',]
    cmd.extend(['-i', video_file])
    cmd.extend(['-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t)|cos(430*2*PI*t):s=%d' % (sample_rate, )])

    cmd.extend(['-c:a', 'aac'])
    cmd.extend(['-c:v', 'copy'])
    cmd.extend(['-frames:v', str(frames)])

    outfile = os.path.join(sample_dir(), name )
    cmd.extend([outfile])

    # print(subprocess.list2cmdline(cmd))

    if overwrite or not os.path.exists(outfile):
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

        stdout,stderr = p.communicate()
        # print(stderr)
        if p.returncode != 0:
            print(stderr)
            return Exception("error encoding footage")
    return outfile

def generate_dnxhd(profile_name, name, frames,  size=None, pix_fmt=None, frame_rate=None, overwrite=True, fmt=None):

    profile = video.dnx_profiles.get(profile_name)
    bitrate = profile.get('bitrate')
    pix_fmt = profile.get('pix_fmt') or pix_fmt
    size = profile.get('size') or size
    interlaced = profile.get("interlaced")
    frame_rate = profile.get('frame_rate') or frame_rate
    dnxhd_profile = profile.get("video_profile", None)

    outfile = os.path.join(sample_dir(), name )

    if not overwrite and os.path.exists(outfile):
        return outfile

    cmd = [FFMPEG_EXEC, '-y', '-f', 'lavfi', '-i', 'testsrc=size=%dx%d:rate=%s' % (size[0],size[1], frame_rate), '-frames:v', str(frames)]
    cmd.extend(['-vcodec', 'dnxhd','-pix_fmt', pix_fmt])
    if bitrate:
        cmd.extend(['-vb', '%dM' % bitrate])

    if dnxhd_profile:
        cmd.extend(['-profile:v', dnxhd_profile])

    if interlaced:
        cmd.extend(['-flags', '+ildct+ilme' ])

    if fmt:
        cmd.extend(['-f', fmt])

    cmd.extend([outfile])

    # print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

    stdout,stderr = p.communicate()
    if p.returncode < 0:
        print(stderr)
        return Exception("error encoding footage")
    return outfile


def generate_pcm_audio_mono(name, sample_rate = 48000, duration = 2, sample_format='pcm_s16le', fmt='wav'):

    cmd = [FFMPEG_EXEC,'-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t):s=%d:d=%f' % (sample_rate, duration)]
    cmd.extend([ '-acodec', '%s' % sample_format])

    cmd.extend(['-f', fmt])
    if fmt == 'mxf_opatom':
        fmt = 'mxf'
    outfile = os.path.join(sample_dir(), '%s.%s' % (name, fmt))

    cmd.extend([outfile])
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()

    if p.returncode != 0:
        print(subprocess.list2cmdline(cmd))
        print(stderr)
        return Exception("error encoding footage")
    return outfile

def generate_pcm_audio_stereo(name, sample_rate = 48000, duration = 2,  sample_format='pcm_s16le', fmt='wav'):
    # this default value for `fmt` looks like a mistake but we preserve it here

    outfile = os.path.join(sample_dir(), '%s.%s' % (name,fmt) )

    cmd = [FFMPEG_EXEC,'-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t)|cos(430*2*PI*t):s=%d:d=%f'% ( sample_rate, duration)]

    #mono
    #cmd = ['ffmpeg','-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t)::s=48000:d=10']

    cmd.extend([ '-f',fmt, '-acodec', sample_format])

    cmd.extend([outfile])

    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()

    if p.returncode != 0:
        print(subprocess.list2cmdline(cmd))
        print(stderr)
        return Exception("error encoding footage")
    return outfile

def md5(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_files(a, b):
    return ffmpeg_frame_md5(a) == ffmpeg_frame_md5(b)

def ffmpeg_frame_md5(path):
    cmd = [FFMPEG_EXEC, '-i', path,  '-f', 'framemd5' , '-']
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    if p.returncode < 0:
        return Exception("error framemd5 footage")

    return stdout
