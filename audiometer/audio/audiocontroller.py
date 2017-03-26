from tone import generate_tone

class AudioController:
    sound_is_playing = False

    def __init__(self, **kwargs):
        pass

    def mute_left_channel(self):
        pass

    def play_sound(self, instance):
        if not AudioController.sound_is_playing:
            AudioController.sound_is_playing = True

            #[(channel 1, volume 1), (channel 2, volume 2) ... (channel n, volume n)]
            frequencies = [(400,.1), (80,.5)]
            generate_tone(frequencies, 2)

        AudioController.sound_is_playing = False 


    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if AudioController.sound_is_playing:
            if value != self.source.frequency:
                self.source.frequency = value

