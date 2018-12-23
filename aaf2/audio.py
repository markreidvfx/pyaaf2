from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import wave
import struct

pcm_profiles = {
'pcm_32000_s16le' : {'sample_format' : 's16le', 'sample_rate' : 32000},
'pcm_32000_s24le' : {'sample_format' : 's24le', 'sample_rate' : 32000},

'pcm_44100_s16le' : {'sample_format' : 's16le', 'sample_rate' : 44100},
'pcm_44100_s24le' : {'sample_format' : 's24le', 'sample_rate' : 44100},

'pcm_48000_s16le' : {'sample_format' : 's16le', 'sample_rate' : 48000},
'pcm_48000_s24le' : {'sample_format' : 's24le', 'sample_rate' : 48000},
}

audio_format_sizes = {
's16'   :  (16, 2),
's32'   :  (32, 4),
'flt'   :  (32, 4),
'dbl'   :  (64, 8),
'u8p'   :  (8,  1),
's16p'  :  (16, 2),
's32p'  :  (32, 4),
'fltp'  :  (32, 4),
'dblp'  :  (64, 8),
's64'   :  (64, 8),
's64p'  :  (64, 8),
}

WAVE_EXTENSIBLE_PCM=0xFFFE

def wave_infochunk(path):
    with open(path,'rb') as file:
        if file.read(4) != b"RIFF":
            return None
        data_size = file.read(4) # container size
        if file.read(4) != b"WAVE": 
            return None
        while True:
            chunkid = file.read(4)
            sizebuf = file.read(4)
            if len(sizebuf) < 4 or len(chunkid) < 4:
                return None
            size    = struct.unpack('<L', sizebuf )[0]
            if chunkid[0:3] != b"fmt":
                if size % 2 == 1:
                    seek = size + 1
                else:
                    seek = size
                file.seek(size,1)
            else:
                return bytearray(b"RIFF" + data_size + b"WAVE" + chunkid + sizebuf + file.read(size))

def create_network_locator(f, path):
    n = f.create.NetworkLocator()
    n['URLString'].value = "file://" + urllib.parse.quote(path)
    return n

def create_wav_descriptor(f, source_mob, path, stream_meta):
    d = f.create.WAVEDescriptor()
    rate = stream_meta['sample_rate']
    d['SampleRate'].value = rate
    d['Summary'].value = wave_infochunk(path)
    d['Length'].value = stream_meta['duration_ts']
    d['ContainerFormat'].value = source_mob.root.dictionary.lookup_containerdef("AAF")
    d['Locator'].append( create_network_locator(f,path) )
    return d

def create_wav_link(f, metadata):
    """
This will return three MOBs for the given `metadata`: master_mob, source_mob, 
tape_mob

The parameter `metadata` is presumed to be a dictionary from a run of ffprobe.

It's not clear for the purposes of Pro Tools that a tape_mob needs to be made, 
it'll open the AAF perfectly well without out one.

A lot of this recaps the AMA link code but it's subtly different enough, but it 
could all bear to be refactored.
    """
    path       = metadata['format']['filename']
    master_mob = f.create.MasterMob()
    source_mob = f.create.SourceMob()
    tape_mob   = f.create.SourceMob()
    
    source_url = "file://" + urllib.parse.quote(path)
    
    edit_rate  = metadata['streams'][0]['sample_rate']
    length     = metadata['streams'][0]['duration_ts']
    
    master_mob.name = os.path.basename(path)
    source_mob.name = os.path.basename(path) + " Source MOB"
    tape_mob.name   = os.path.basename(path) + " Tape MOB"
    container_guid  = UUID("3711d3cc-62d0-49d7-b0ae-c118101d1a16") # WAVE/AIFF
    
    f.content.mobs.append(master_mob)
    f.content.mobs.append(source_mob)
    f.content.mobs.append(tape_mob)
    
    tape_mob.descriptor = aaf.create.TapeDescriptor()
    tape_mob.descriptor["VideoSignal"].value = "VideoSignalNull"
    
    # Tape timecode
    
    t = tape_mob.create_empty_sequence_slot(edit_rate, media_kind='timecode')
    tc = f.create.Timecode(int(float(edit_rate)+0.5), drop=False)
    tc.length = int(length)
    if 'tags' not in metadata['format'].keys(): 
        tc.start = 0
    else:
        tc.start = int(metadata['format']['tags']['time_reference']) or 0
        
    t.segment.length = int(length)
    t.segment.components.append(tc)
    
    descriptor = create_wav_descriptor(aaf, source_mob, path, metadata['streams'][0]) 
    source_mob.descriptor = descriptor
        
    for channel_index in range(metadata['streams'][0]['channels']):
        tape_slot = tape_mob.create_empty_sequence_slot(edit_rate, media_kind='sound')
        tape_slot.segment.length = length
        nul_ref = f.create.SourceClip(media_kind='sound')
        nul_ref.length = length
        tape_slot.segment.components.append(nul_ref)
        
        tape_clip = tape_mob.create_source_clip(tape_slot.slot_id)
        tape_clip.length = length
        tape_clip.media_kind = 'sound'
        
        src_slot = source_mob.create_empty_sequence_slot(edit_rate, media_kind='sound')
        src_slot.segment.length = length
        src_slot.segment.components.append(tape_clip)
        src_slot['PhysicalTrackNumber'].value = channel_index + 1
        
        clip = source_mob.create_source_clip(src_slot.slot_id)
        clip.length = length
        clip.media_kind = 'sound'

        master_slot = master_mob.create_empty_sequence_slot(edit_rate, media_kind='sound')
        master_slot.segment.components.append(clip)
        master_slot.segment.length = length

        master_slot['PhysicalTrackNumber'].value = channel_index + 1
        
    return master_mob, source_mob, tape_mob


class WaveReader(wave.Wave_read):
    def __init__(self, f):
        self._blockalign = None
        # can't use super in OldStyle 2.7 class
        wave.Wave_read.__init__(self, f)

    def _read_fmt_chunk(self, chunk):

        # added support for wave extensible

        wFormatTag, self._nchannels, self._framerate, dwAvgBytesPerSec, wBlockAlign = struct.unpack_from(b'<HHLLH', chunk.read(14))
        if wFormatTag in  (wave.WAVE_FORMAT_PCM, WAVE_EXTENSIBLE_PCM):
            sampwidth = struct.unpack_from(b'<H', chunk.read(2))[0]
            self._sampwidth = (sampwidth + 7) // 8
        else:
            raise wave.Error('unknown format: %r' % (wFormatTag,))

        if not self._sampwidth in (2, 3):
            raise wave.Error('unsupported sample width: %r' % (self._sampwidth,))

        self._framesize = self._nchannels * self._sampwidth
        self._comptype = 'NONE'
        self._blockalign = wBlockAlign
        self._compname = 'not compressed'

    def getblockalign(self):
        return self._blockalign
