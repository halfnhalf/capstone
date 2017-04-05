import time

class HearingTest:
    def __init__(self, **kwargs):
		super(ClassName, self).__init__()
		self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
		self.test_freqs = [250, 500, 1000, 2000, 4000, 8000]
		self.leftThresholds = []
		self.rightThresholds = []
		self.buttonPressed = False

    def start_test_sequence(self):
    	for freq in test_freqs:
    		self.leftThresholds.append(find_threshold(freq, True))

    	for freq in test_freqs:
    		self.rightThresholds.append(find_threshold(freq, False))
    		

    def find_threshold(self, freq, side):
    	amps = []
		#Start at 10db below lowest threshold indicated during familiarization
		lastResponse = 10
		while len(amps) < 5:
			lastResponse = ascend(freq, lastResponse)
			if lastResponse in amps:
				#found our threshold for this freq
				return lastResponse

			amps.append(lastResponse)
			lastResponse = descend(freq, lastResponse)

		#If we made it out of loop, then could not get the same threshold twice out of 5 ascents
		#Present a test tone at a level 10 dB higher than the level of the last response.
		lastResponse = descend(freq, amps[4])
		return ascend(freq, lastResponse)


    def ascend(self, freq, amp):
    	#Go up by increments of 5 until button pressed
    	while not buttonPressed:
			self.play_freq(freq, amp, side)
			time.sleep(2)
			stop_freq()
			amp = amp + 5
			if amp == 120:
				break

		buttonPressed = False
		return amp

	def descend(self, freq, amp):
		#Go down in increments of 10 until no button press
		self.play_freq(freq, amp, side)
		while buttonPressed:
			buttonPressed = False
			amp = amp - 10
			self.play_freq(freq, amp, side)
			time.sleep(2)
			stop_freq()
			if amp < 10:
				break

		return amp

	def button_press(self):
		self.buttonPressed = True
    
    def play_freq(self, freq, amp, side):
    	if side:
    		#Left side
    		self.audio_controller.play_sound(frequencies=[(freq, amp),(freq,0)], duration=2)
    	else:
    		#Right side
    		self.audio_controller.play_sound(frequencies=[(freq, 0),(freq, amp)], duration=2)
	
	def stop_freq(self):
		self.audio_controller.stop_sound()
