import time
import threading
import json
import math

class HearingTest:
    def __init__(self, **kwargs):
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.test_freqs = [250, 500, 1000, 2000, 4000, 8000]
        self.stop = threading.Event()

    def start_test_sequence(self=None, instance=None):
        self.buttonPressed = False
        self.resultsJSON = None
        self.leftThresholds = []
        self.leftBoneThresholds = []
        self.rightThresholds = []
        self.rightBoneThresholds = []

        for freq in self.test_freqs:
            if self.stop.is_set():
                self.stop_freq()
                self.print_thresholds()
                return
            self.leftThresholds.append(self.find_threshold(freq, True, False))
            
        for freq in self.test_freqs:
            if self.stop.is_set():
                self.stop_freq()
                self.print_thresholds()
                return
            self.rightThresholds.append(self.find_threshold(freq, False, False))
            
        #Bone conduction if needed
        for i, threshold in enumerate(self.leftThresholds):
            if self.stop.is_set():
                self.stop_freq()
                self.print_thresholds()
                return
            if threshold > 0.4:
                self.leftBoneThresholds.append(self.find_threshold(freq, True, True))
            else:
                self.leftBoneThresholds.append(None)

        for i, threshold in enumerate(self.rightThresholds):
            if self.stop.is_set():
                self.stop_freq()
                self.print_thresholds()
                return
            if threshold > 0.4:
                self.rightBoneThresholds.append(self.find_threshold(freq, False, True))
            else:
                self.rightBoneThresholds.append(None)

        self.print_thresholds()

    def find_threshold(self, freq, side, bone):
        amps = []
        #Start at 10db below lowest threshold indicated during familiarization
        lastResponse = 0
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
            
        # if side:
        #     #Left side
        #     if not bone:
        #         self.audio_controller.play_sound(frequencies=[(freq,0),(freq,0),(freq, amp),(freq,0)], duration=2)
        #     else:
        #         self.audio_controller.play_sound(frequencies=[(freq, amp),(freq,0)], duration=2)
        # else:
        #     #Right side
        #     if not bone:
        #         self.audio_controller.play_sound(frequencies=[(freq, 0),(freq, 0),(freq, 0),(freq, amp)], duration=2)
        #     else:
        #         self.audio_controller.play_sound(frequencies=[(freq, 0),(freq, amp)], duration=2)
            
    
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
        with open('test.json', 'w') as outfile:
            json.dump([{'left':[{'air':self.leftThresholds}, {'bone':self.leftBoneThresholds}]}, \
                       {'right' : [{'air':self.rightThresholds}, {'bone':self.rightBoneThresholds}]}], outfile)


    def getSoundcardAmp(self, freq, desiredAmp):
        ret = math.exp(.115*desiredAmp)*.0003
        if ret > 1:
            ret = 1
        return ret

    def getRelativeAmp(self, freq, desiredAmp):
        thresholdCurve = {250:17, 500:6, 1000:4.2, 2000:1, 4000:-3.9, 8000:15.3}
        return desiredAmp + thresholdCurve[freq]
