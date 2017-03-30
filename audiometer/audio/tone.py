import math
import time
import pyaudio
from array import array

#sampling rate, Hz, must be integer
RATE = 22050*2
#how large we want our pcm chunks to be
BUFSIZE = 512*200
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
        
        self._generate_period()

    def _generate_period(self):
        for channel in range(self.num_channels):
            if self.frequencies[channel][0] > 0:
                self.periods.append(int(RATE / self.frequencies[channel][0]))
                period = self.periods[channel]
                self.table.append([float(self.frequencies[channel][1]) * math.sin(2.0 * 3.14159 * float(self.frequencies[channel][0]) * (float(i%period) / float(RATE))) for i in range(period)])
            else:
                self.periods.append(0)
                self.table.append([])
        

    def callback(self, in_data, frame_count, time_info, status):
        if not self.duration < 0 and self.position >= int((RATE * self.duration)/2):
            self.play_sound = False

        if not self.play_sound:
            callback_flag = pyaudio.paComplete
        else:
            callback_flag = pyaudio.paContinue
            

        return (self._get_chunk(frame_count), callback_flag)

    def change_freqs_to(self, frequencies):
        print self.frequencies
        self.frequencies = frequencies
        print self.frequencies
        self.position = 0
        self.periods = []
        self.table = []

        self._generate_period()
    
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

    def _get_chunk_quad(self, frame_count):
        data = array('h')
        for i in range(self.position, self.position+frame_count):
                data.append(int(MAX_AMP * self.table[0][int(i%self.periods[0])]))
                data.append(int(MAX_AMP * self.table[1][int(i%self.periods[1])]))
                data.append(int(MAX_AMP * self.table[2][int(i%self.periods[2])]))
                data.append(int(MAX_AMP * self.table[3][int(i%self.periods[3])]))

        self.position = self.position+frame_count
        return data.tostring()
