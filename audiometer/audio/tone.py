import pyaudio
from itertools import *
import math
import struct
import time

#sampling rate, Hz, must be integer
RATE = 44100*1
#how large we want our pcm chunks to be
BUFSIZE = 512*4
SAMPWIDTH = 2
MAX_AMP= float(int((2 ** (SAMPWIDTH* 8)) / 2) - 1)
p = pyaudio.PyAudio()

#based on https://zach.se/generate-audio-with-python/

samples = None

class Tone():
    def __init__(self, frequencies):
        self.num_channels = len(frequencies)
        self.frequencies = frequencies
        self.periods = []
        self.table = []
        self.position = 0

        for channel in range(self.num_channels):
            self.periods.append(int(RATE / frequencies[channel][0]))
            period = self.periods[channel]
            self.table.append([float(frequencies[channel][1]) * math.sin(2.0 * 3.14159 * float(self.frequencies[channel][0]) * (float(i%period) / float(RATE))) for i in xrange(period)])

    def callback(self, in_data, frame_count, time_info, status):

        return (self._get_chunk(frame_count), pyaudio.paContinue)
    
    def _get_chunk(self, frame_count):
        data = []
        for i in xrange(self.position, self.position+frame_count):
            for channel in range(self.num_channels):
                datum = int(MAX_AMP * self.table[channel][int(i%self.periods[channel])])
                data.append(datum)

        self.position = self.position+frame_count
        return ''.join(struct.pack('h', item) for item in data)

def generate_tone(frequencies, duration):
    '''
    generate a tone for each frequency passed in a list called frequencies
    each tone is played on a single channel
    '''
    tone = Tone(frequencies)
    num_channels = len(frequencies)

    stream = p.open(format=pyaudio.get_format_from_width(2),
            channels=num_channels,
            rate=RATE,
            frames_per_buffer=BUFSIZE,
            output=True,
            stream_callback=tone.callback)

    stream.start_stream()
    time.sleep(duration)
    stream.stop_stream()
    stream.close()


    #_write_pcm(stream, samples)

def _sine_wave(frequency=440.0, framerate=RATE, amplitude=0.5,
        skip_frame=0):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    for i in count(skip_frame):
        sine = math.sin(2.0 * 3.14159 * float(frequency) * (float(i) / float(framerate)))
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

def _write_pcm(f, samples, sampwidth=1, framerate=RATE, bufsize=BUFSIZE):
    "Write samples as raw PCM data."
    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    #for chunk in _grouper(bufsize, samples):
    frames = b''.join(b''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in samples if channels is not None)
    f.write(frames)

    f.close()
