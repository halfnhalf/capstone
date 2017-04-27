import time
import threading
import json
import math
import os
import datetime as dt

class HearingTest:
    def __init__(self, **kwargs):
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.test_freqs = [250, 500, 1000, 2000, 4000, 8000]
        self.stop = threading.Event()

    def start_test_sequence(self=None, instance=None):
        self.buttonPressed = False
        self.resultsJSON = None
        self.leftThresholds = [-20]*len(self.test_freqs)
        self.leftBoneThresholds = [-20]*len(self.test_freqs)
        self.rightThresholds = [-20]*len(self.test_freqs)
        self.rightBoneThresholds = [-20]*len(self.test_freqs)

        print str(self.leftThresholds)
        print str(self.rightThresholds)
        print str(self.rightBoneThresholds)
        print str(self.leftBoneThresholds)
        
        for i, freq in enumerate(self.test_freqs):
           if self.stop.is_set():
               self.stop_freq()
               self.print_thresholds()
               return
           self.leftThresholds[i] = self.find_threshold(freq, True, False)
           
        for i, freq in enumerate(self.test_freqs):
           if self.stop.is_set():
               self.stop_freq()
               self.print_thresholds()
               return
           self.rightThresholds[i] = self.find_threshold(freq, False, False)
           
        #Bone conduction if needed
        for i, threshold in enumerate(self.leftThresholds):
            print "LENGTH OF LEFT THRESHOLDS: " + str(len(self.leftThresholds))
            if self.stop.is_set():
               self.stop_freq()
               self.print_thresholds()
               return
            if threshold > 40:
                self.leftBoneThresholds[i] = self.find_threshold(self.test_freqs[i], True, True)
            else:
                self.leftBoneThresholds[i] = -20

        for i, threshold in enumerate(self.rightThresholds):
            if self.stop.is_set():
               self.stop_freq()
               self.print_thresholds()
               return
            if threshold > 40:
                self.rightBoneThresholds[i] = self.find_threshold(self.test_freqs[i], False, True)
            else:
                self.rightBoneThresholds[i] = -20

        self.print_thresholds()

    def find_threshold(self, freq, side, bone):
        amps = []
        #Start at 10db below lowest threshold indicated during familiarization
        lastResponse = 30 if bone else 0
        while len(amps) < 5:
            if self.stop.is_set():
                self.stop_freq()
                return

            lastResponse = self.ascend(freq, lastResponse, side, bone)
            if lastResponse in amps:
                #found our threshold for this freq
                return lastResponse

            amps.append(lastResponse)
            lastResponse = self.descend(freq, lastResponse, side, bone)

        if self.audiometer.stop.is_set():
            return
            
        #If we made it out of loop, then could not get the same threshold twice out of 5 ascents
        #Present a test tone at a level 10 dB higher than the level of the last response.
        lastResponse = self.descend(freq, amps[4], side, bone)
        return self.ascend(freq, lastResponse, side, bone)


    def ascend(self, freq, amp, side, bone):
        print "starting ascent"
        print "current freq: " + str(freq)
        print "current amp: " + str(amp)
        #Go up by increments of 5db until button pressed
        while True:
            if self.stop.is_set():
                self.stop_freq()
                return
            print "playing tone. amp: " + str(amp)
            self.play_freq(freq, amp, side, bone)
            time.sleep(2)
            if self.buttonPressed:
                print "Found button press!"
                time.sleep(1)
                break

            amp = amp + 5
            if amp > 120:
                amp = 120
                time.sleep(1)
                break
            time.sleep(1)

        self.buttonPressed = False
        return amp

    def descend(self, freq, amp, side, bone):
        print "starting descent"
        print "current freq: " + str(freq)
        print "current amp: " + str(amp)
        #Go down in increments of 10 until no button press
        while True:
            if self.stop.is_set():
                self.stop_freq()
                return

            self.buttonPressed = False
            print "playing tone. amp: " + str(amp)
            self.play_freq(freq, amp, side, bone)
            time.sleep(2)
            if (not self.buttonPressed):
                time.sleep(1)
                break
            print "Found button press!"
            amp = amp - 10
            if amp < 0:
                amp = 0
                break
                
            time.sleep(1)

        self.buttonPressed = False
        return amp

    def button_press(self=None, instance=None):
        self.buttonPressed = True
    
    def play_freq(self, freq, amp, side, bone):
        if self.audio_controller.sound_is_playing:
            self.audio_controller.stop_sound()

        #Calibrate relative to MAF Threshold
        amp = self.getRelativeAmp(freq, amp)
        amp = 0 if amp < 0 else amp
        #Get soundcard amplitude percentage based on desired decibel level
        amp = self.getSoundcardAmp(freq, amp)
        
        if bone:
            whiteNoiseAmp = amp
        else:
            whiteNoiseAmp = amp-40 if amp > 40 else 0    
        
        #Calibrate relative to MAF Threshold (white noise)
        whiteNoiseAmp = self.getRelativeAmp(freq, whiteNoiseAmp)
        whiteNoiseAmp = 0 if whiteNoiseAmp < 0 else whiteNoiseAmp
        #Get soundcard amplitude percentage based on desired decibel level
        whiteNoiseAmp = self.getSoundcardAmp(freq, whiteNoiseAmp)

        # if not bone:
        #     if side:
        #         self.audio_controller.play_sound(frequencies=[(freq,0),(freq,0),(freq, amp),(-1,whiteNoiseAmp)], duration=2)
        #     else:
        #         self.audio_controller.play_sound(frequencies=[(freq, 0),(freq, 0),(-1, whiteNoiseAmp),(freq, amp)], duration=2)
        # else:
        #     if side:
        #         self.audio_controller.play_sound(frequencies=[(freq, amp),(freq,0),(freq, 0),(-1,whiteNoiseAmp)], duration=2)
        #     else:
        #         self.audio_controller.play_sound(frequencies=[(freq, 0),(freq, amp),(-1,whiteNoiseAmp),(freq,0)], duration=2)
            
    
    def stop_freq(self):
        if self.audio_controller.sound_is_playing:
            self.audio_controller.stop_sound()

    def stop_thread(self):
        self.stop.set()

    def print_thresholds(self):
        print "Left Air Conduction: " + str(self.leftThresholds)
        print "Right Air Conduction: " + str(self.rightThresholds)
        print "Left Bone Conduction: " + str(self.leftBoneThresholds)
        print "Right Bone Conduction: " + str(self.rightBoneThresholds)
        jsonObj = {"frequencies":self.test_freqs, "air":{"Left Ear": {"decibels": self.leftThresholds},"Right Ear": {"decibels": self.rightThresholds}}, \
           "bone":{"Left Ear":{"decibels": self.leftBoneThresholds},"Right Ear": {"decibels": self.rightBoneThresholds}}}
        with open(os.path.join(os.path.dirname(__file__),'../../data/current_audiogram.json'), 'w') as outfile:
           json.dump(jsonObj, outfile)

        with open(os.path.join(os.path.dirname(__file__),'../../data/' + str(dt.datetime.now()) + '.json'), 'w') as outfile:
           json.dump(jsonObj, outfile)
    
    def getSoundcardAmp(self, freq, desiredAmp):
        ret = math.exp(.115*desiredAmp)*.0003
        if ret > 1:
            ret = 1
        return ret

    def getRelativeAmp(self, freq, desiredAmp):
        thresholdCurve = {250:17, 500:6, 1000:4.2, 2000:1, 4000:-3.9, 8000:15.3}
        return desiredAmp + thresholdCurve[freq]
