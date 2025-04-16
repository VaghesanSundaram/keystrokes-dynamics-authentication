from pynput import keyboard
import numpy
import threading
import time

text = []
timings = []
timingsColl = []
meanTimings = []

keyphrase = "the quick brown fox jumped over the lazy dog"
count = 0
attempts = 0
shutdown_event = threading.Event()

last_press_time = None


def on_key_press(key):
    global text, timings, count, last_press_time, attempts

    if key == keyboard.Key.esc:
        print("Escape pressed. Exiting...")
        shutdown_event.set()
        return False  # Stop the listener

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
            return  # Ignore other special keys

    if actual_char != expected_char:
        print(f"Mistake made, expecting '{expected_char}', got '{actual_char}'")
        text = []
        timings = []
        count = 0
        last_press_time = None
        return

    current_time = time.perf_counter()
    if last_press_time is not None:
        interval = current_time - last_press_time
        timings.append(interval)

    last_press_time = current_time

    text.append(actual_char)
    print(f"Got '{actual_char}'")
    count += 1


def check():
    global text, timings, count, timingsColl, meanTimings, attempts, last_press_time

    while not shutdown_event.is_set():
        time.sleep(0.1)
        if len(text) == len(keyphrase):
            if text == list(keyphrase):
                print("Correct!")
                print("Typed:", ''.join(text))
                print("Timings:", timings)
                timingsColl.append(timings.copy())
                attempts += 1
                if attempts == 3:
                    meanTimings = numpy.mean(timingsColl, axis=0)
                    print("Mean timings:", meanTimings)
                    shutdown_event.set()
            else:
                print("Text mismatch")
            text = []
            timings = []
            count = 0
            last_press_time = None


my_thread = threading.Thread(target=check, daemon=True)
my_thread.start()

print(f"Starting... expecting '{keyphrase[count]}' at index {count}")

with keyboard.Listener(daemon=True, on_press=on_key_press) as press_listener:
    press_listener.join()
    my_thread.join()
