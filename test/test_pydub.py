import os

from pydub import AudioSegment
from pydub.playback import play

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def play_sound():
    sound = AudioSegment.from_mp3(f'bgms/0.mp3')
    play(sound)


if __name__ == '__main__':
    play_sound()