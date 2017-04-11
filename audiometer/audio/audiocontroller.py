import tone
import pyaudio

class AudioController:
    '''
    use this controller to play and control sounds.
    you can only use one AudioController object at a time.
    when playing a sound you must call stop_sound before
    playing another. 
    '''

    sound_is_playing = False
    sound_object = None
    stream = None

    def __init__(self, **kwargs):
        self.p = pyaudio.PyAudio()
        pass

    def play_sound(self=None, instance=None, frequencies=[(400,.2), (400,.2)], duration=-1):
        '''
        generate a tone for each frequency passed in a list called frequencies
        each tone is played on a single channel
        '''

        if AudioController.sound_is_playing:
            return
        AudioController.sound_is_playing = True
        sounds = tone.Tones(frequencies, duration)
        AudioController.stream = self.p.open(format=pyaudio.get_format_from_width(2),
                channels=sounds.num_channels,
                rate=tone.RATE,
                frames_per_buffer=tone.BUFSIZE,
                output=True,
                stream_callback=sounds.callback)

        AudioController.stream.start_stream()
        AudioController.sound_object = sounds


    def stop_sound(self, instance=None):
        '''
        stop currently playing sound and close the stream
        this should be called before starting a new sound
        '''
        if not AudioController.sound_is_playing:
           return 
        AudioController.sound_object.stop_sound()
	self._stop_stream()

    def update_tones(self, slider=None, value=None, frequencies=None):
        '''
        update the currently playing tones with a new 
        frequency list
        '''
        if not AudioController.sound_is_playing:
           return 
        current_freqs = self.sound_object.frequencies
        if slider:
            AudioController.sound_object.change_freqs_to([(int(value), current_freqs[0][1])] + current_freqs[1:])
        else:
            AudioController.sound_object.change_freqs_to(frequencies)

    def _stop_stream(self):
        if AudioController.sound_is_playing == True:
            AudioController.stream.stop_stream()
            AudioController.stream.close()
        AudioController.sound_is_playing = False 
