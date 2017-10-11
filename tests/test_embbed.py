from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import subprocess
import unittest
import hashlib

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

    # print(subprocess.list2cmdline(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

    stdout,stderr = p.communicate()
    if p.returncode < 0:
        print(stderr)
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

def md5(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_files(a, b):
    return md5(a) == md5(b)

class EmbbedTests(unittest.TestCase):

    def test_dnx_iter(self):
        profile_name = 'dnx_1080p_36_23.97'
        sample = generate_dnxhd(profile_name, "dnx_iter01.dnxhd", 10)
        for i, packet in enumerate(video.iter_dnx_stream(open(sample, 'rb'))):
            cid, width, height, bitdepth, interlaced = video.read_dnx_frame_header(packet)
            assert not interlaced
            assert bitdepth == 8

            assert (width, height) == (1920, 1080)

        assert i+1 == 10

        profile_name = 'dnx_1080i_120_25'
        sample = generate_dnxhd(profile_name, "dnx_iter02.dnxhd", 10)
        for i, packet in enumerate(video.iter_dnx_stream(open(sample, 'rb'))):
            cid, width, height, bitdepth, interlaced = video.read_dnx_frame_header(packet)
            assert interlaced
            assert bitdepth == 8
            assert (width, height) == (1920, 540)

        assert i+1 == 10

        frame_rate = '23.97'
        profile_name = 'dnxhr_lb'
        uhd2160 = (3840, 2160)
        sample = generate_dnxhd(profile_name, "dnx_iter03.dnxhd", 10, size=uhd2160, frame_rate=frame_rate)
        for i, packet in enumerate(video.iter_dnx_stream(open(sample, 'rb'))):
            cid, width, height, bitdepth, interlaced = video.read_dnx_frame_header(packet)
            assert not interlaced
            assert (width, height) == uhd2160
            assert bitdepth == 8

        assert i+1 == 10

    def test_dnxhd(self):

        for profile_name in ['dnx_1080p_36_23.97', 'dnx_720p_90x_25', 'dnx_1080i_120_25', 'dnx_1080p_175x_23.97']:
            new_file = os.path.join(common.sandbox(), '%s_embbed_essence.aaf' % profile_name)
            sample = generate_dnxhd(profile_name, '%s-embbed.dnxhd' % profile_name, 3)

            with aaf2.open(new_file, 'w') as f:
                profile = video.dnx_profiles.get(profile_name)

                mob = f.create.MasterMob(profile_name)
                f.content.mobs.append(mob)
                mob.embbed_dnxhd_essence(sample, profile['frame_rate'])

            with aaf2.open(new_file, 'r') as f:
                mob = next(f.content.sourcemobs())
                stream = mob.essence.open('r')
                dump_path = os.path.join(common.sandbox(),'%s-embbed-dump.dnxhd' % profile_name)
                with open(dump_path, 'w') as out:
                    out.write(stream.read())

                assert compare_files(dump_path, sample)

    def test_dnxhr(self):

        frame_rate = '23.97'
        uhd2160 = (3840, 2160)

        for profile_name in ['dnxhr_lb', 'dnxhr_sq', 'dnxhr_hq']:
            new_file = os.path.join(common.sandbox(), '%s_embbed_essence.aaf' % profile_name)
            with aaf2.open(new_file, 'w') as f:
                profile = video.dnx_profiles.get(profile_name)
                sample = generate_dnxhd(profile_name, "%s-embbed.dnxhd" % profile_name, 3, size=uhd2160, frame_rate=frame_rate)

                mob = f.create.MasterMob(profile_name)
                f.content.mobs.append(mob)
                mob.embbed_dnxhd_essence(sample, frame_rate)

            with aaf2.open(new_file, 'r') as f:
                mob = next(f.content.sourcemobs())
                stream = mob.essence.open('r')
                dump_path = os.path.join(common.sandbox(),'%s-embbed-dump.dnxhd' % profile_name)
                with open(dump_path, 'w') as out:
                    out.write(stream.read())

                assert compare_files(dump_path, sample)



if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
