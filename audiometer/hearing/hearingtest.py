import time

class HearingTest:
    def __init__(self, **kwargs):
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.test_freqs = [250, 500, 1000, 2000, 4000, 8000]
        self.leftThresholds = []
        self.rightThresholds = []
        self.buttonPressed = False

    def start_test_sequence(self=None, instance=None):
        for freq in self.test_freqs:
            self.leftThresholds.append(self.find_threshold(freq, True))
            if self.audiometer.stop.is_set():
                return

        for freq in self.test_freqs:
            self.rightThresholds.append(self.find_threshold(freq, False))
            if self.audiometer.stop.is_set():
                return
            

    def find_threshold(self, freq, side):
        amps = []
        #Start at 10db below lowest threshold indicated during familiarization
        lastResponse = .1
        while len(amps) < 5:
            if self.audiometer.stop.is_set():
                return

            lastResponse = self.ascend(freq, lastResponse, side)
            if lastResponse in amps:
                #found our threshold for this freq
                return lastResponse

            amps.append(lastResponse)
            lastResponse = self.descend(freq, lastResponse, side)

        if self.audiometer.stop.is_set():
            return
            
        #If we made it out of loop, then could not get the same threshold twice out of 5 ascents
        #Present a test tone at a level 10 dB higher than the level of the last response.
        lastResponse = self.descend(freq, amps[4], side)
        return self.ascend(freq, lastResponse, side)


    def ascend(self, freq, amp, side):
        #Go up by increments of 5db until button pressed
        while True:
            if self.audiometer.stop.is_set():
                return

            self.play_freq(freq, amp, side)
            time.sleep(2)
            # self.stop_freq()
            if self.buttonPressed:
                break

            amp = amp + .1
            if amp > 1:
                break

        self.buttonPressed = False
        return amp

    def descend(self, freq, amp, side):
        #Go down in increments of 10 until no button press
        self.play_freq(freq, amp, side)
        while True:
            if self.audiometer.stop.is_set():
                return

            self.buttonPressed = False
            amp = amp - .2
            self.play_freq(freq, amp, side)
            time.sleep(2)
            #self.stop_freq()
            if (not self.buttonPressed) or amp < .1:
                break

        return amp

    def button_press(self=None, instance=None):
        self.buttonPressed = True
    
    def play_freq(self, freq, amp, side):
        if side:
            #Left side
            if self.audio_controller.sound_is_playing:
                self.audio_controller.stop_sound()

            self.audio_controller.play_sound(frequencies=[(freq, amp),(freq,0)], duration=2)
        else:
            #Right side
            if self.audio_controller.sound_is_playing:
                self.audio_controller.stop_sound()

            self.audio_controller.play_sound(frequencies=[(freq, 0),(freq, amp)], duration=2)
    
    def stop_freq(self):
        self.audio_controller.stop_sound()
