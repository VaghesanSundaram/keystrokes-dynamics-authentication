from pynput import keyboard
import threading
import sys
import Stopwatch

text = []
timings = []
keyphrase = "the quick brown fox jumped over the lazy dog"
stopwatch =  Stopwatch.Stopwatch()

def on_key_press(key): 
    stopwatch.start()
    try:
        text.append(key.char)
        print(key)
    except AttributeError:
        if str(key) == 'Key.space':
            text.append(" ")
        elif str(key) == "Key.backspace":
            text.pop(len(text)-1)
        else:
            text.append(str(key))
    
    

def on_key_release(key):
    stopwatch.stop()
    timings.append(stopwatch.get_elapsed_time())
    stopwatch.reset()


def check():
    global text
    global timings
    while True:
        if len(text) == len(keyphrase):
            if text == list(keyphrase):
                print("Correct!")
                print(text)
                print(timings)
                text = []
                timings = []
            else:
                print("Nope")
                text = []



my_thread = threading.Thread(target=check, daemon=True)
my_thread.start()

with keyboard.Listener(daemon = True, on_press = on_key_press, on_release=on_key_release) as press_listener:
    print("starting")
    press_listener.join()
    
    my_thread.join()
    
    