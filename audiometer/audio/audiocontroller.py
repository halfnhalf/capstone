from tone import generate_tone

class AudioController:
    sound_is_playing = False

    def __init__(self, **kwargs):
        pass

    def mute_left_channel(self):
        pass

    def play_sound(self=None, instance=None, frequencies=[(400,.1), (80,.1)], duration=2):
        if not AudioController.sound_is_playing:
            AudioController.sound_is_playing = True

            #[(channel 1, volume 1), (channel 2, volume 2) ... (channel n, volume n)]
            generate_tone(frequencies, duration)

        AudioController.sound_is_playing = False 


    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if AudioController.sound_is_playing:
            if value != self.source.frequency:
                self.source.frequency = value

