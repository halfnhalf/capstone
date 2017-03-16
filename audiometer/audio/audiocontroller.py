#import time

class AudioController:
	def __init__(self):
		# super(ClassName, self).__init__()
		# self.arg = arg
		# self.test_freqs = [250, 500, 1000, 2000, 4000, 8000]
		# self.leftThresholds = []
		# self.rightThresholds = []

    def mute_left_channel(self):
        pass

 #    def start_test_sequence(self):
 #    	for freq in test_freqs:
 #    		self.leftThresholds.append(find_threshold(freq))

 #    	for freq in test_freqs:
 #    		self.rightThresholds.append(find_threshold(freq))
    		

 #    def find_threshold(self, freq):
 #    	amps = []
	# 	#Start at 10db below lowest threshold indicated during familiarization
	# 	lastResponse = 10
	# 	while len(amps) < 5:
	# 		lastResponse = ascend(freq, lastResponse)
	# 		if lastResponse in amps:
	# 			#found our threshold for this freq
	# 			return lastResponse

	# 		amps.append(lastResponse)
	# 		lastResponse = descend(freq, lastResponse)

	# 	#If we made it out of loop, then could not get the same threshold twice out of 5 ascents
	# 	#Present a test tone at a level 10 dB higher than the level of the last response.
	# 	lastResponse = descend(freq, amps[4])
	# 	return ascend(freq, lastResponse)


 #    def ascend(self, freq, amp):
 #    	#Go up by increments of 5 until button pressed
 #    	while not button_pressed():
	# 		play_freq(freq, amp)
	# 		time.sleep(2)
	# 		stop_freq()
	# 		amp = amp + 5
	# 		if amp == 120:
	# 			break

	# 	return amp

	# def descend(self, freq, amp):
	# 	#Go down in increments of 10 until no button press
	# 	play_freq(freq, amp)
	# 	while button_pressed():
	# 		amp = amp - 10
	# 		play_freq(freq, amp)
	# 		time.sleep(2)
	# 		stop_freq()
	# 		if amp < 10:
	# 			break

	# 	return amp

 #    def play_freq(self, freq, amp):
 #    	pass
	
	# def stop_freq(self):
	# 	pass