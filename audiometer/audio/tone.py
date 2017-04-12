import math
import time
import pyaudio
import random
import numpy as np
from array import array

#sampling rate, Hz, must be integer
RATE = 22050*1
#how large we want our pcm chunks to be
BUFSIZE = 256*2
SAMPWIDTH = 2
MAX_AMP = float((2 ** (SAMPWIDTH* 8)) / 2) - 1

class SineWave():
    def __init__(self, frequency, volume):
        self.frequency = np.float(frequency)
        self.volume = np.float(volume)
        self.samples_per_period = int(RATE / frequency) if self.frequency > 0 else 1

        if self.volume < 0:
            self.volume = 0
        elif self.volume > 1:
            self.volume = 1

        self.generate_period()

    def generate_period(self):
        seconds_per_period = np.reciprocal(self.frequency) if self.frequency > 0 else 1
        self.period = self.volume*np.sin(2*np.pi*self.frequency*np.linspace(0, seconds_per_period, num=self.samples_per_period))
        #print self.period
        #self.period = np.tile(self.period, int(BUFSIZE*2/self.samples_per_period))

class Noise():
    def __init__(self, volume):
        self.volume = volume
        self.samples_per_period = 50000

        self.generate_period()

    def generate_period(self):
        self.period = [float(self.volume) * random.uniform(-1, 1) for i in range(self.samples_per_period)]

class Silence():
    def __init__(self):

        self.generate_period()

    def generate_period(self):
        self.period = np.arange(BUFSIZE)*0

class Tones():
    '''
    used to generate multichannel tones
    '''
    def __init__(self, frequencies, duration):
        self.num_channels = len(frequencies)
        self.frequencies = frequencies
        self.position = 0
        self.duration = duration
        self.play_sound = True

        # This will store our sound objects
        self.sounds = []

        # This will store our buffer which we will pull chunks from
        
        self._generate_periods()

    def _generate_periods(self):
        for channel in range(self.num_channels):
            this_freq = self.frequencies[channel]
            if this_freq[0] > 0:
                self.sounds.append(SineWave(this_freq[0], this_freq[1]))
            elif this_freq[1] == 0 or this_freq[0] == 0:
                self.sounds.append(Silence())
            else:
                self.sounds.append(Noise(this_freq[1]))

    def callback(self, in_data, frame_count, time_info, status):
        if not self.duration < 0 and self.position >= int((RATE * self.duration)/2):
            self.stop_sound()

        if not self.play_sound:
            callback_flag = pyaudio.paComplete
        else:
            callback_flag = pyaudio.paContinue

        return (self._get_chunk(frame_count), callback_flag)

    def stop_sound(self):
        '''
        stop currently playing sounds. This should be called before starting a new sound
        if you already played a sound
        '''
        self.play_sound = False
        self.position = 0

    def change_freqs_to(self, frequencies):
        '''
        change the currently playing frequencies to new ones.
        This can also change volumes. frequency syntax is the same
        as AudioController.play_sound()
        '''
        self.frequencies = frequencies
        self.position = 0
        del self.sounds[:]

        self._generate_periods()
        time.sleep(.2) #allow time to generate the periods before we're allowed to update again
    
    def _get_chunk(self, frame_count):

        channel_chunks = []
        for channel_sound in self.sounds:
            if isinstance(channel_sound, Silence):
                channel_chunks.append(MAX_AMP * np.arange(frame_count)*0)
            else:
                #print (MAX_AMP * channel_sound.period[np.remainder(np.arange(self.position, self.position+frame_count), channel_sound.samples_per_period)]).astype(int)
                channel_chunks.append((MAX_AMP * channel_sound.period[np.remainder(np.arange(self.position, self.position+frame_count), channel_sound.samples_per_period)]).astype(np.int))

        self.position =  self.position + frame_count
        #print np.vstack((channel_chunks)).reshape((-1,),order='F').astype(np.int16).tostring()
        return (np.vstack((channel_chunks)).reshape((-1,),order='F')).astype(np.int16).tostring()



    def _get_chunk_quad(self, frame_count):
        data = array('h')
        for i in range(self.position, self.position+frame_count):
                data.append(int(MAX_AMP * self.table[0][int(i%self.periods[0])]))
                data.append(int(MAX_AMP * self.table[1][int(i%self.periods[1])]))
                data.append(int(MAX_AMP * self.table[2][int(i%self.periods[2])]))
                data.append(int(MAX_AMP * self.table[3][int(i%self.periods[3])]))

        self.position = self.position+frame_count
        return data.tostring()
