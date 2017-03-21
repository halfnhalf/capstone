from audiostream import get_output
from audiostream.sources.wave import SineSource

CHANNELS = 2
BUFSIZE = 2048
INCSIZE = 512

class AudioController:
    sound_is_playing = False

    def __init__(self, **kwargs):
        pass

    def mute_left_channel(self):
        pass

    def toggle_sound(self, instance):
        if not AudioController.sound_is_playing:
            stream = get_output(channels=CHANNELS, buffersize=BUFSIZE, rate=22050)
            self.source = SineSource(stream, 440)
            self.source.start()
        else:
            self.source.stop()

        AudioController.sound_is_playing = not AudioController.sound_is_playing

    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if AudioController.sound_is_playing:
            if value != self.source.frequency:
                self.source.frequency = value
