from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import subprocess
import unittest

FFMPEG_EXEC='ffmpeg'

import common
import aaf2
from aaf2 import video

sample_dir = os.path.join(common.sandbox(), 'samples')
if not os.path.exists(sample_dir):
    os.makedirs(sample_dir)

def generate_dnxhd(profile_name, name, frames,  size=None, pix_fmt=None, frame_rate=None):

    profile = video.dnx_profiles.get(profile_name)
    bitrate = profile.get('bitrate')
    pix_fmt = profile.get('pix_fmt') or pix_fmt
    size = profile.get('size') or size
    interlaced = profile.get("interlaced")
    frame_rate = profile.get('frame_rate') or frame_rate
    dnxhd_profile = profile.get("video_profile", None)

    outfile = os.path.join(sample_dir, "%s.dnxhd" % name )
    cmd = [FFMPEG_EXEC, '-y', '-f', 'lavfi', '-i', 'testsrc=size=%dx%d:rate=%s' % (size[0],size[1], frame_rate), '-frames:v', str(frames)]
    cmd.extend(['-vcodec', 'dnxhd','-pix_fmt', pix_fmt])
    if bitrate:
        cmd.extend(['-vb', '%dM' % bitrate])

    if dnxhd_profile:
        cmd.extend(['-profile:v', dnxhd_profile])

    if interlaced:
        cmd.extend(['-flags', '+ildct+ilme' ])

    cmd.extend([outfile])

    print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

    stdout,stderr = p.communicate()
    print(stderr)
    if p.returncode < 0:

        return Exception("error encoding footage")
    return outfile


def generate_pcm_audio_mono(name, sample_rate = 48000, duration = 2, format='pcm'):

    outfile = os.path.join(sample_dir, '%s.%s' % (name, format))
    cmd = [FFMPEG_EXEC,'-y', '-f', 'lavfi', '-i', 'aevalsrc=sin(420*2*PI*t)::s=%d:d=%f' % (sample_rate, duration)]

    if format == 'pcm':

        cmd.extend([ '-f','s16le', '-acodec', 'pcm_s16le'])

    cmd.extend([outfile])

    print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    print(stderr)
    if p.returncode < 0:
        return Exception("error encoding footage")
    return outfile

def generate_pcm_audio_stereo(name, sample_rate = 48000, duration = 2):

    outfile = os.path.join(sample_dir, '%s.pcm' % name)

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

class EmbbedTests(unittest.TestCase):

    def test_dnx_iter(self):
        profile_name = 'dnx_1080p_36_23.97'
        sample = generate_dnxhd(profile_name, "dnx_iter01.dnxhd", 10)
        for i, packet in enumerate(video.iter_dnx_stream(open(sample, 'rb'))):
            pass
        assert i+1 == 10

        frame_rate = '23.97'
        profile_name = 'dnxhr_lb'
        uhd2160 = (3840, 2160)
        sample = generate_dnxhd(profile_name, "dnx_iter02.dnxhd", 10, size=uhd2160, frame_rate=frame_rate)
        for i, packet in enumerate(video.iter_dnx_stream(open(sample, 'rb'))):
            pass
        assert i+1 == 10

    def test_dnxhd(self):
        new_file = os.path.join(common.sandbox(), 'dnxhd36_embbed_essence.aaf')
        profile_name = 'dnx_1080p_36_23.97'
        with aaf2.open(new_file, 'w') as f:
            profile = video.dnx_profiles.get(profile_name)
            sample = generate_dnxhd(profile_name, profile_name, 3)

            mob = f.create.MasterMob(profile_name)
            f.content.mobs.append(mob)
            mob.embbed_dnxhd_essence(sample, profile['frame_rate'])






if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
