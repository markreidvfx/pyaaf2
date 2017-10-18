from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import subprocess
from aaf2 import video, audio

FFMPEG_EXEC='ffmpeg'
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

def test_empty_file():
    return os.path.join(test_files_dir(), "empty.aaf")

def sample_dir():
    s = os.path.join(sandbox(), 'samples')
    if not os.path.exists(s):
        os.makedirs(s)

    return s

def generate_dnxhd(profile_name, name, frames,  size=None, pix_fmt=None, frame_rate=None, overwrite=True):

    profile = video.dnx_profiles.get(profile_name)
    bitrate = profile.get('bitrate')
    pix_fmt = profile.get('pix_fmt') or pix_fmt
    size = profile.get('size') or size
    interlaced = profile.get("interlaced")
    frame_rate = profile.get('frame_rate') or frame_rate
    dnxhd_profile = profile.get("video_profile", None)

    outfile = os.path.join(sample_dir(), "%s.dnxhd" % name )

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

    cmd.extend([outfile])

    # print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

    stdout,stderr = p.communicate()
    if p.returncode < 0:
        print(stderr)
        return Exception("error encoding footage")
    return outfile


def generate_pcm_audio_mono(name, sample_rate = 48000, duration = 2, sample_format='s16le', format='wav'):

    outfile = os.path.join(sample_dir(), '%s.%s' % (name, format))

    cmd = [FFMPEG_EXEC,'-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t)::s=%d:d=%f' % (sample_rate, duration)]
    cmd.extend([ '-acodec', 'pcm_%s' % sample_format])

    cmd.extend([outfile])
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()

    if p.returncode < 0:
        print(subprocess.list2cmdline(cmd))
        print(stderr)
        return Exception("error encoding footage")
    return outfile

def generate_pcm_audio_stereo(name, sample_rate = 48000, duration = 2):

    outfile = os.path.join(sample_dir(), '%s.pcm' % name)

    cmd = [FFMPEG_EXEC,'-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t):cos(430*2*PI*t)::s=%d:d=%f'% ( sample_rate, duration)]

    #mono
    #cmd = ['ffmpeg','-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t)::s=48000:d=10']

    cmd.extend([ '-f','s16le', '-acodec', 'pcm_s16le'])

    cmd.extend([outfile])

    print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    print(stderr)
    if p.returncode < 0:
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
