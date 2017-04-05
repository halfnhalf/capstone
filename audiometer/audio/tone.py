import math
import time
import pyaudio
from array import array

#sampling rate, Hz, must be integer
RATE = 22050*1
#how large we want our pcm chunks to be
BUFSIZE = 256*1
SAMPWIDTH = 2
MAX_AMP = float(int((2 ** (SAMPWIDTH* 8)) / 2) - 1)

#based on https://zach.se/generate-audio-with-python/

class SineWave():
    def __init__(self, frequency, volume):
        self.frequency = frequency
        self.volume = volume
        self.samples_per_period = int(RATE / frequency)

        self.generate_period()

    def generate_period(self):
        self.period = [float(self.volume) * math.sin(2.0 * 3.14159 * float(self.frequency) * (float(i%self.samples_per_period) / float(RATE))) for i in range(self.samples_per_period)]

class Noise():
    def __init__(self, frequency, volume):
        self.volume = volume

        def generate_period(self):
            self.period = [float(self.volume) * random.uniform(-1, 1) for i in range()]

class Tones():
    def __init__(self, frequencies, duration):
        self.num_channels = len(frequencies)
        self.frequencies = frequencies
        self.position = 0
        self.duration = duration
        self.play_sound = True
        self.sounds = []
        
        self._generate_periods()

    def _generate_periods(self):
        for channel in range(self.num_channels):
            if self.frequencies[channel][0] > 0:
                self.sounds.append(SineWave(self.frequencies[channel][0], self.frequencies[channel][1]))
            else:
                self.sounds.append(None)
        

    def callback(self, in_data, frame_count, time_info, status):
        if not self.duration < 0 and self.position >= int((RATE * self.duration)/2):
            self.stop_sound()

        if not self.play_sound:
            callback_flag = pyaudio.paComplete
        else:
            callback_flag = pyaudio.paContinue

        return (self._get_chunk(frame_count), callback_flag)

    def stop_sound(self):
        self.play_sound = False
        self.position = 0

    def change_freqs_to(self, frequencies):
        self.frequencies = frequencies
        self.position = 0
        del self.sounds[:]

        self._generate_periods()
        time.sleep(.2)
    
    def _get_chunk(self, frame_count):
        data = array('h')

        for i in range(self.position, self.position+frame_count):
            for channel_sound in self.sounds:
                if channel_sound:
                    datum = int(MAX_AMP * channel_sound.period[int(i%channel_sound.samples_per_period)])
                else:
                    datum = 0

                data.append(datum)

        self.position = self.position+frame_count
        return data.tostring()

    def _get_chunk_quad(self, frame_count):
        data = array('h')
        for i in range(self.position, self.position+frame_count):
                data.append(int(MAX_AMP * self.table[0][int(i%self.periods[0])]))
                data.append(int(MAX_AMP * self.table[1][int(i%self.periods[1])]))
                data.append(int(MAX_AMP * self.table[2][int(i%self.periods[2])]))
                data.append(int(MAX_AMP * self.table[3][int(i%self.periods[3])]))

        self.position = self.position+frame_count
        return data.tostring()
