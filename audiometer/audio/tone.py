import pyaudio
import numpy as np
from itertools import *
import math
import struct

#sampling rate, Hz, must be integer
RATE = 48000*1
#how large we want our pcm chunks to be
BUFSIZE = 512*2
p = pyaudio.PyAudio()

#based on https://zach.se/generate-audio-with-python/

def generate_tone(frequencies, duration):
    '''
    generate a tone for each frequency passed in a list called frequencies
    each tone is played on a single channel
    '''
    num_channels = len(frequencies)
    channels = ((_sine_wave(frequencies[0][0], amplitude=frequencies[0][1]),),)

    for freq in frequencies[1:]:
        channels = channels + ((_sine_wave(freq[0], amplitude=freq[1]),),)

    stream = p.open(format=pyaudio.get_format_from_width(2),
            channels=num_channels,
            rate=RATE,
            output=True,
            output_device_index=4)

    samples = _compute_samples(channels, RATE * duration)
    _write_pcm(stream, samples)

def _sine_wave(frequency=440.0, framerate=RATE, amplitude=0.5,
        skip_frame=0):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    for i in count(skip_frame):
        sine = math.sin(2.0 * np.pi * float(frequency) * (float(i) / float(framerate)))
        yield float(amplitude) * sine

def _grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def _compute_samples(channels, nsamples=None):
    '''
    create a generator which computes the samples.
    essentially it creates a sequence of the sum of each function in the channel
    at each sample in the file for each channel.
    '''
    return islice(izip(*(imap(sum, izip(*channel)) for channel in channels)), nsamples)

def _write_pcm(f, samples, sampwidth=2, framerate=RATE, bufsize=BUFSIZE):
    "Write samples as raw PCM data."
    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in _grouper(bufsize, samples):
        frames = b''.join(b''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        f.write(frames)

    f.close()
