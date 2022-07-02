from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import wave
import struct

pcm_profiles = {
'pcm_32000_s16le' : {'sample_format' : 'pcm_s16le', 'sample_rate' : 32000},
'pcm_32000_s24le' : {'sample_format' : 'pcm_s24le', 'sample_rate' : 32000},

'pcm_44100_s16le' : {'sample_format' : 'pcm_s16le', 'sample_rate' : 44100},
'pcm_44100_s24le' : {'sample_format' : 'pcm_s24le', 'sample_rate' : 44100},

'pcm_48000_s16le' : {'sample_format' : 'pcm_s16le', 'sample_rate' : 48000},
'pcm_48000_s24le' : {'sample_format' : 'pcm_s24le', 'sample_rate' : 48000},
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
