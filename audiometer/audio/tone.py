import math
import time
import pyaudio
from array import array

#sampling rate, Hz, must be integer
RATE = 48000*2
#how large we want our pcm chunks to be
BUFSIZE = 512*4
SAMPWIDTH = 2
MAX_AMP= float(int((2 ** (SAMPWIDTH* 8)) / 2) - 1)

#based on https://zach.se/generate-audio-with-python/

class Tone():
    def __init__(self, frequencies, duration):
        self.num_channels = len(frequencies)
        self.frequencies = frequencies
        self.periods = []
        self.table = []
        self.position = 0
        self.duration = duration
        self.play_sound = True

        for channel in range(self.num_channels):
            if frequencies[channel][0] > 0:
                self.periods.append(int(RATE / frequencies[channel][0]))
                period = self.periods[channel]
                self.table.append([float(frequencies[channel][1]) * math.sin(2.0 * 3.14159 * float(self.frequencies[channel][0]) * (float(i%period) / float(RATE))) for i in range(period)])

    def callback(self, in_data, frame_count, time_info, status):
        if not self.duration < 0 and self.position >= int((RATE * self.duration)/2):
            self.play_sound = False

        if not self.play_sound:
            callback_flag = pyaudio.paComplete
        else:
            callback_flag = pyaudio.paContinue
            

        return (self._get_chunk(frame_count), callback_flag)
    
    def _get_chunk(self, frame_count):
        data = array('h')
        for i in range(self.position, self.position+frame_count):
            for channel in range(self.num_channels):
                if self.frequencies[channel][0] > 0:
                    datum = int(MAX_AMP * self.table[channel][int(i%self.periods[channel])])
                else:
                    datum = 0
                data.append(datum)

        self.position = self.position+frame_count
        return data.tostring()
