"""
Arguments:
    - wav_file: str


"""

import argparse
import threading
import time
import wave

import keyboard
import pyaudio

START_SECS = 7.6
END_SECS = 50.0
LENGTH_SECS = 0.2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("wav_file", type=str)
    return parser.parse_args()


def skip_to_start(wf: wave.Wave_read, start_secs: float = 0.0):
    wf.setpos(int(wf.getframerate() * start_secs))


def play_audio(wf: wave.Wave_read, start_secs: float = 0.0):
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )
    skip_to_start(wf, start_secs)
    data = wf.readframes(int(wf.getframerate() * LENGTH_SECS))
    if len(data) == 0:
        return
    stream.write(data)
    stream.stop_stream()


if __name__ == "__main__":
    args = parse_args()

    # 音源ファイルの読み込み
    wf = wave.open(args.wav_file, "rb")
    p = pyaudio.PyAudio()

    # 開始位置までスキップ
    print("Start listening...")
    cursor = START_SECS
    while True:
        # Esc キーが押されたら終了
        if keyboard.is_pressed("esc"):
            break
        # event が発生したらwavファイルを再生
        if keyboard.read_event():
            threading.Thread(target=play_audio, args=(wf, cursor)).start()
            cursor += LENGTH_SECS
            if cursor >= END_SECS:
                cursor = START_SECS
            time.sleep(0.03)
