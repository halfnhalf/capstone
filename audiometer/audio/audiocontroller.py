from audiostream import get_output
from audiostream.sources.wave import SineSource
import pyaudio
import numpy as np
from itertools import *
import math
import struct

CHANNELS = 4
BUFSIZE = 2048
INCSIZE = 512

volume = 0.1     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0  
p = pyaudio.PyAudio()

class AudioController:
    sound_is_playing = False

    def __init__(self, **kwargs):
        pass

    def mute_left_channel(self):
        pass

    def toggle_sound(self, instance):
        stream = p.open(format=pyaudio.get_format_from_width(2),
                channels=2,
                rate=fs,
                output=True)

        AudioController.sound_is_playing = not AudioController.sound_is_playing

        channels = ((sine_wave(400.0, amplitude=0.1),),
            (sine_wave(100.0, amplitude=0.1),))

        samples = compute_samples(channels, 44100 * 2)

        write_pcm(stream, samples)

    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if AudioController.sound_is_playing:
            if value != self.source.frequency:
                self.source.frequency = value

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5,
        skip_frame=0):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    for i in count(skip_frame):
        sine = np.sin(2.0 * np.pi * float(frequency) * (float(i) / float(framerate))).astype(np.float32)
        yield float(amplitude) * sine

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def compute_samples(channels, nsamples=None):
    '''
    create a generator which computes the samples.
    essentially it creates a sequence of the sum of each function in the channel
    at each sample in the file for each channel.
    '''
    return islice(izip(*(imap(sum, izip(*channel)) for channel in channels)), nsamples)

def write_pcm(f, samples, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples as raw PCM data."
    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = b''.join(b''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        f.write(frames)

    f.close()
