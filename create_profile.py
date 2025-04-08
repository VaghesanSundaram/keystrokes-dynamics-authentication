from pynput import keyboard
import threading
import time
import sys
import Stopwatch

text = []
timings = []
keyphrase = "the quick brown fox jumped over the lazy dog"
count = 0
stopwatch = Stopwatch.Stopwatch()


def on_key_press(key):
    global text, timings, count

    if count >= len(keyphrase):
        return  

    expected_char = keyphrase[count]
    actual_char = None

    try:
        actual_char = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            actual_char = " "
        else:
           
            return

    if actual_char != expected_char:
        print(f"Mistake made, expecting '{expected_char}', got '{actual_char}'")
        text = []
        timings = []
        count = 0
        return
    else:
        stopwatch.start()
        text.append(actual_char)
        print(f"Got '{actual_char}'")
        count += 1


def on_key_release(key):
    if stopwatch.running:
        stopwatch.stop()
        timings.append(stopwatch.get_elapsed_time())
        stopwatch.reset()


def check():
    global text, timings, count
    while True:
        time.sleep(0.1)
        if len(text) == len(keyphrase):
            if text == list(keyphrase):
                print("Correct!")
                print("Typed:", ''.join(text))
                print("Timings:", timings)
            else:
                print("Text mismatch")
            text = []
            timings = []
            count = 0


my_thread = threading.Thread(target=check, daemon=True)
my_thread.start()

print(f"Starting... expecting '{keyphrase[count]}' at index {count}")

with keyboard.Listener(daemon=True, on_press=on_key_press, on_release=on_key_release) as press_listener:
    press_listener.join()
    my_thread.join()
