from audiometer.audio.audiocontroller import AudioController
from time import sleep
import platform

def main():
    audio_controller = AudioController()

    if platform.system() == "Darwin":
        print "testing default arguments"
        audio_controller.play_sound()
        sleep(2)

        print "testing frequency arguments"
        audio_controller.play_sound(frequencies=[(400,.8),(0,.8)])
        sleep(2)

        print "testing different volumes"
        audio_controller.play_sound(frequencies=[(400,.2),(400,.5)])
        sleep(2)

        print "testing different frequencies"
        audio_controller.play_sound(frequencies=[(8000,.2),(400,.2)])
        sleep(2)
    else:
        print "testing default arguments"
        audio_controller.play_sound()
        sleep(2)

        print "testing frequency arguments"
        audio_controller.play_sound(frequencies=[(400,.8),(0,.8),(400,.8),(0,.8)])
        sleep(2)

        print "testing different volumes"
        audio_controller.play_sound(frequencies=[(400,.8),(400,.5),(400,.8),(400,.5)])
        sleep(2)

        print "testing different frequencies"
        audio_controller.play_sound(frequencies=[(400,.8),(8000,.8),(400,.8),(8000,.8)])


if __name__ == '__main__':
    main()

