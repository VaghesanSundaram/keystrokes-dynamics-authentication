# Keystroke Dynamics Authentication

This Python project implements a keystroke dynamics system that authenticates users based on their typing patterns. By analyzing the timing between key presses of a fixed keyphrase, the program can either build a typing profile or compare new attempts against an existing one for authentication.

## Features

- Monitors user keystrokes in real-time using `pynput`
- Records timing intervals between consecutive keystrokes
- Supports profile creation (3 successful samples averaged)
- Authenticates users via:
  - **Pearson correlation** of timing sequences
  - **Mean Squared Error** comparison
- Stores and loads profile using `.npy` (NumPy binary format)
- Graceful shutdown with ESC key

## Keyphrase

```
the quick brown fox jumped over the lazy dog
```

## Authentication Criteria

- **Pearson Correlation > 0.8**
- **Mean Squared Error < 0.01**

## Usage

1. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the script:**

    ```bash
    python keystroke_auth.py
    ```

3. **First run:**
   - Type the keyphrase correctly 3 times to create a profile.

4. **Subsequent runs:**
   - Type the phrase to authenticate.
   - If timing pattern matches the saved profile, access is granted.

5. **Press `ESC` at any time to quit.**

## File Outputs

- `profile.npy`: Saved mean timing profile after successful enrollment.

## Future Updates

- Timing profile visualizer with matplotlib
- Login GUI that can handle multiple users
  - Setting custom keyphrases with minimum length
  - Saving multiple profiles with different keyphrases
  
## Notes

- Only alphanumeric keys and spaces are processed.
- Mistyped phrases reset the current attempt.
- The system is intentionally simple and not intended for production security applications.
