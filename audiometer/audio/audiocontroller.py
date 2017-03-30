import tone
import pyaudio

class AudioController:
    sound_is_playing = False
    sound_object = None

    def __init__(self, **kwargs):
        self.p = pyaudio.PyAudio()

    def play_sound(self=None, instance=None, frequencies=[(0,0)], duration=2):
        '''
        generate a tone for each frequency passed in a list called frequencies
        each tone is played on a single channel
        '''

        if not AudioController.sound_is_playing:
            AudioController.sound_is_playing = True
            sound = tone.Tone(frequencies, duration)
            stream = self.p.open(format=pyaudio.get_format_from_width(2),
                    channels=sound.num_channels,
                    rate=tone.RATE,
                    frames_per_buffer=tone.BUFSIZE,
                    output=True,
                    stream_callback=sound.callback)

            stream.start_stream()
            AudioController.sound_object = sound

        AudioController.sound_is_playing = False 

    def stop_sound(self=None):
        AudioController.sound_object.play_sound = False



    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if AudioController.sound_is_playing:
            if value != self.source.frequency:
                self.source.frequency = value

