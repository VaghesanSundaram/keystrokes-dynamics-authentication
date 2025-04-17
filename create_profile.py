from pynput import keyboard
from pynput.keyboard import Controller
import numpy
import threading
import os
import time
from scipy.stats import pearsonr

# State variables
text = []             # Characters typed so far
timings = []          # Timings between keypresses
timingsColl = []      # Collection of timings for profile creation
meanTimings = []      # Averaged profile timings

keyphrase = "the quick brown fox jumped over the lazy dog"
count = 0             # Current character index
attempts = 0          # Number of successful typing attempts
shutdown_event = threading.Event()
last_press_time = None
controller = Controller()  # Used to simulate key press if needed


def on_key_press(key):
    """Handles key press events: validates input and records timing."""
    global text, timings, count, last_press_time, attempts

    if shutdown_event.is_set():
        return False  # Stop listener if program is done

    if key == keyboard.Key.esc:
        print("Escape pressed. Exiting...")
        shutdown_event.set()
        return False

    if count >= len(keyphrase):
        return  # Ignore input once phrase is completed

    expected_char = keyphrase[count]
    actual_char = None

    # Convert key to character
    try:
        actual_char = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            actual_char = " "
        else:
            return  # Ignore non-character keys

    # Check if character is correct
    if actual_char != expected_char:
        print(f"Mistake made, expecting '{expected_char}', got '{actual_char}'")
        text.clear()
        timings.clear()
        count = 0
        last_press_time = None
        return

    # Record time between key presses
    current_time = time.perf_counter()
    if last_press_time is not None:
        interval = current_time - last_press_time
        timings.append(interval)

    last_press_time = current_time

    text.append(actual_char)
    count += 1
    print(f"Got '{actual_char}'")


def check():
    """Background thread that monitors when full phrase is typed, 
    then either compares against profile or builds it."""
    global text, timings, count, timingsColl, meanTimings, attempts, last_press_time

    while not shutdown_event.is_set():
        time.sleep(0.1)

        if len(text) == len(keyphrase):
            if text == list(keyphrase):
                print("\nCorrect phrase typed.")
                print("Typed:", ''.join(text))
                print("Timings:", timings)

                if os.path.exists("profile.npy"):
                    # Compare against saved profile
                    print("Profile found. Comparing...")
                    profile = numpy.load("profile.npy")

                    if len(timings) != len(profile):
                        print("Timing length mismatch. Try again.\n")
                    else:
                        corr, _ = pearsonr(profile, timings)
                        mse = numpy.mean((numpy.array(profile) - numpy.array(timings)) ** 2)

                        print(f"Pearson Correlation: {corr:.4f}")
                        print(f"Mean Squared Error: {mse:.6f}")

                        # Check if input matches profile
                        if corr > 0.8 and mse < 0.01:
                            print("Authentication successful!")
                            shutdown_event.set()
                        else:
                            print("Authentication failed. Try again.\n")
                else:
                    # Profile creation mode
                    print(f"Profile not found. Collecting attempt {attempts + 1}/3")
                    timingsColl.append(timings.copy())
                    attempts += 1

                    if attempts == 3:
                        # Save average timings as profile
                        meanTimings = numpy.mean(timingsColl, axis=0)
                        numpy.save('profile.npy', meanTimings)
                        print("Profile saved as 'profile.npy'.")
                        print("You can now authenticate.\n")
                        attempts = 0
                        timingsColl.clear()
            else:
                print("Text mismatch. Try again.\n")

            # Reset state for next attempt
            text.clear()
            timings.clear()
            count = 0
            last_press_time = None

            # Wake up listener if it's blocked
            controller.press(' ')
            controller.release(' ')


# Start timing validation thread
my_thread = threading.Thread(target=check, daemon=True)
my_thread.start()

print(f"Starting... expecting '{keyphrase[count]}' at index {count}")
print("Press ESC at any time to quit.\n")

# Start keyboard listener
with keyboard.Listener(daemon=True, on_press=on_key_press) as press_listener:
    try:
        press_listener.join()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")

# Wait for background thread to finish
my_thread.join()
