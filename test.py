from audiometer.audio.audiocontroller import AudioController
from time import sleep
import sys, getopt

def main(argv):
    channels = 2
    try:
        opts, args = getopt.getopt(argv, "c:")
    except: 
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-c":
            channels = int(arg)

    audio_controller = AudioController()

    if channels == 2:
        print "right muted"
        audio_controller.play_sound(frequencies=[(400,.1),(0,0)])
        sleep(2)
        audio_controller.stop_sound()

        print "testing different volumes"
        audio_controller.play_sound(frequencies=[(400,.05),(400,.1)])
        sleep(2)
        audio_controller.stop_sound()

        print "testing different frequencies"
        audio_controller.play_sound(frequencies=[(8000,.1),(400,.1)])
        sleep(2)
        audio_controller.stop_sound()

        print "testing white noise"
        audio_controller.play_sound(frequencies=[(-1,.1),(400,.1)])
        sleep(2)
        audio_controller.stop_sound()

        print "testing infinite tone"
        audio_controller.play_sound(frequencies=[(8000,.1),(400,.1)], duration=-1)
        sleep(2)
        audio_controller.update_tones(frequencies=[(800,.1),(400,.1)])
        sleep(2)
        audio_controller.stop_sound()

    elif channels == 4:
        print "right muted"
        audio_controller.play_sound(frequencies=[(400,.8),(0,.8),(400,.8),(0,.8)])
        sleep(2)
	audio_controller.stop_sound()

        print "testing different volumes"
        audio_controller.play_sound(frequencies=[(400,.8),(400,.5),(400,.8),(400,.5)])
        sleep(2)
	audio_controller.stop_sound()

        print "testing different frequencies"
        audio_controller.play_sound(frequencies=[(400,.8),(8000,.8),(400,.8),(8000,.8)])
        sleep(2)
	audio_controller.stop_sound()

    else:
        print "bad channels"


if __name__ == '__main__':
    main(sys.argv[1:])

