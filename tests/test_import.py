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
from aaf2 import video, audio

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


def generate_pcm_audio_mono(name, sample_rate = 48000, duration = 2, sample_format='s16le', format='wav'):

    outfile = os.path.join(sample_dir, '%s.%s' % (name, format))

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
    return ffmpeg_frame_md5(a) == ffmpeg_frame_md5(b)

def ffmpeg_frame_md5(path):
    cmd = [FFMPEG_EXEC, '-i', path,  '-f', 'framemd5' , '-']
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    if p.returncode < 0:
        return Exception("error framemd5 footage")

    return stdout


class ImportTests(unittest.TestCase):

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
        frames = 3
        for profile_name in ['dnx_1080p_36_23.97', 'dnx_720p_90x_25', 'dnx_1080i_120_25', 'dnx_1080p_175x_23.97']:
            new_file = os.path.join(common.sandbox(), '%s_import_essence.aaf' % profile_name)
            sample = generate_dnxhd(profile_name, '%s-import.dnxhd' % profile_name, frames=frames)

            with aaf2.open(new_file, 'w') as f:
                profile = video.dnx_profiles.get(profile_name)

                mob = f.create.MasterMob(profile_name)
                f.content.mobs.append(mob)
                mob.import_dnxhd_essence(sample, profile['frame_rate'])

            with aaf2.open(new_file, 'r') as f:
                mob = next(f.content.sourcemobs())
                stream = mob.essence.open('r')
                dump_path = os.path.join(sample_dir,'%s-import-dump.dnxhd' % profile_name)
                with open(dump_path, 'wb') as out:
                    out.write(stream.read())

                assert compare_files(dump_path, sample)
                assert mob.slots[0].segment.length == frames
                assert mob.descriptor.length == frames

    def test_dnxhr(self):

        frame_rate = '23.97'
        uhd2160 = (960, 540)

        frames = 3

        timecode_fps = 30
        start_time = int(timecode_fps * 60 * 60) # 1 hour

        for profile_name in ['dnxhr_lb', 'dnxhr_sq', 'dnxhr_hq']:
            new_file = os.path.join(common.sandbox(), '%s_import_essence.aaf' % profile_name)
            with aaf2.open(new_file, 'w') as f:


                profile = video.dnx_profiles.get(profile_name)
                sample = generate_dnxhd(profile_name, "%s-import.dnxhd" % profile_name, frames=frames, size=uhd2160, frame_rate=frame_rate)

                # create a tape
                tape_mob = f.create.SourceMob()
                tape_mob.create_tape_slots(profile_name, frame_rate, timecode_fps)
                f.content.mobs.append(tape_mob)
                tape = tape_mob.create_source_clip(1, start=start_time)

                mob = f.create.MasterMob(profile_name)
                f.content.mobs.append(mob)
                timecode = f.create.Timecode(timecode_fps)
                mob.import_dnxhd_essence(sample, frame_rate, tape=tape)

            with aaf2.open(new_file, 'r') as f:
                source_mobs = []
                tape_mobs = []
                for mob in f.content.sourcemobs():
                    if isinstance(mob.descriptor, aaf2.essence.TapeDescriptor):
                        tape_mobs.append(mob)
                    else:
                        source_mobs.append(mob)

                mob = source_mobs[0]
                stream = mob.essence.open('r')
                dump_path = os.path.join(sample_dir,'%s-import-dump.dnxhd' % profile_name)
                with open(dump_path, 'wb') as out:
                    out.write(stream.read())

                assert compare_files(dump_path, sample)
                assert mob.slots[0].segment.length == frames
                assert mob.slots[0].segment.start  == start_time
                assert mob.descriptor.length == frames


    def test_wav(self):
        # name, sample_rate = 48000, duration = 2, sample_fmt='s16le', format='wav'):
        # profile_name = 'pcm_48000_s24le'
        frame_rate = 30
        timecode_fps = 30
        start_time = int(timecode_fps * 60 * 60) * 2

        duration = 1.5
        for profile_name in sorted(audio.pcm_profiles):
            sample_format = audio.pcm_profiles[profile_name]['sample_format']
            sample_rate = audio.pcm_profiles[profile_name]['sample_rate']

            sample = generate_pcm_audio_mono(profile_name, sample_format=sample_format, sample_rate=sample_rate, duration=duration)
            new_file = os.path.join(common.sandbox(), '%s_import_essence.aaf' % profile_name)
            with aaf2.open(new_file, 'w') as f:

                tape_mob = f.create.SourceMob()
                f.content.mobs.append(tape_mob)
                tape_mob.create_tape_slots(profile_name, frame_rate, timecode_fps, media_kind='sound')

                tape = tape_mob.create_source_clip(1, start_time)

                mob = f.create.MasterMob(profile_name)
                f.content.mobs.append(mob)
                mob.import_audio_essence(sample, frame_rate, tape)

            with aaf2.open(new_file, 'r') as f:
                source_mobs = []
                tape_mobs = []
                for mob in f.content.sourcemobs():
                    if isinstance(mob.descriptor, aaf2.essence.TapeDescriptor):
                        tape_mobs.append(mob)
                    else:
                        source_mobs.append(mob)
                mob = source_mobs[0]
                tape_mob = tape_mobs[0]
                stream = mob.essence.open('r')
                dump_path = os.path.join(sample_dir,'%s-import-dump.wav' % profile_name)
                mob.export_audio(dump_path)
                assert compare_files(dump_path, sample)
                audio_samples = mob.descriptor['Length'].value
                assert audio_samples == sample_rate * duration
                edit_length = duration * frame_rate
                assert mob.slots[0].segment.length == edit_length
                assert mob.slots[0].segment.start == start_time
                assert mob.slots[0].segment.mob_id == tape_mob.id

    def test_multi(self):
        frame_rate = 30.0
        frames = 3
        audio_duration = frames/frame_rate
        uhd2160 = (960, 540)
        new_file = os.path.join(common.sandbox(), 'multi_import_essence.aaf')
        audio_profile_name = 'pcm_48000_s24le'

        sample_format = audio.pcm_profiles[audio_profile_name]['sample_format']
        sample_rate = audio.pcm_profiles[audio_profile_name]['sample_rate']
        audio_sample = generate_pcm_audio_mono(audio_profile_name, sample_format=sample_format, sample_rate=sample_rate, duration=audio_duration)
        samples = {}
        mastermobs = {}

        timecode_fps = 30
        start_time = int(timecode_fps * 60 * 60)
        tape_id = None
        with aaf2.open(new_file, 'w') as f:
            # create a tape
            tape_mob = f.create.SourceMob()
            tape_mob.create_tape_slots("mulit-import", frame_rate, timecode_fps)
            tape_id = tape_mob.id
            f.content.mobs.append(tape_mob)

            for i, profile_name in enumerate(['dnxhr_lb', 'dnxhr_sq', 'dnxhr_hq'], 1):
                profile = video.dnx_profiles.get(profile_name)
                sample = generate_dnxhd(profile_name, "%s-mulit-import.dnxhd" % profile_name, frames=frames, size=uhd2160, frame_rate=frame_rate)

                mob = f.create.MasterMob(profile_name)
                f.content.mobs.append(mob)

                tape = tape_mob.create_source_clip(1, start=start_time)

                vs_mob = mob.import_dnxhd_essence(sample, frame_rate, tape=tape)
                as_mob = mob.import_audio_essence(audio_sample, frame_rate)

                mob.comments['profile'] = profile_name
                mob.comments['integer'] = 100
                mob.comments['integer'] = i
                mastermobs[mob.id] = (profile_name, i)

                v_dump_path = os.path.join(sample_dir,'%s-multi-import-dump.wav' % profile_name)
                a_dump_path = os.path.join(sample_dir,'%s-multi-import-dump.dnxhd' % profile_name)

                samples[vs_mob.id] = (sample, v_dump_path, start_time)
                samples[as_mob.id] = (audio_sample, a_dump_path, start_time)

                start_time += 100

        with aaf2.open(new_file, 'r') as f:
            tape_mob = f.content.mobs.get(tape_id)
            for mob_id, (profile_name, v) in mastermobs.items():
                mob = f.content.mobs.get(mob_id)
                assert mob.comments['profile'] == profile_name
                assert mob.comments['integer'] == v

            for mob_id, (original_path, dump_path, start_time) in samples.items():
                mob = f.content.mobs.get(mob_id)

                if isinstance(mob.descriptor, aaf2.essence.PCMDescriptor):
                    mob.export_audio(dump_path)
                    assert compare_files(dump_path, original_path)
                    assert mob.slots[0].segment.length == frames

                if isinstance(mob.descriptor, aaf2.essence.CDCIDescriptor):
                    stream = mob.essence.open('r')
                    with open(dump_path, 'wb') as out:
                        out.write(stream.read())
                    assert compare_files(dump_path, original_path)
                    assert mob.slots[0].segment.length == frames
                    assert mob.slots[0].segment.start == start_time
                    assert mob.slots[0].segment.mob_id == tape_id




if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
