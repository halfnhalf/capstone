from audiometer.audio.audiocontroller import AudioController
from time import sleep

def main():
    audio_controller = AudioController()

    print "testing default arguments"
    audio_controller.play_sound()
    sleep(2)

    print "testing frequency arguments"
    audio_controller.play_sound(frequencies=[(400,.8),(400,.8)])
    sleep(2)

    print "testing different volumes"
    audio_controller.play_sound(frequencies=[(400,.2),(400,.5)])
    sleep(2)

    print "testing different frequencies"
    audio_controller.play_sound(frequencies=[(800,.2),(400,.2)])

if __name__ == '__main__':
    main()

