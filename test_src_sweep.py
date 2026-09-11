import numpy as np
import soundfile as sf
from scipy.signal import chirp


SOURCE_RATE = 44100
DURATION = 10.0
TEST_FILE = "src_sweep_test.wav"


def create_sweep():
    print("Creating logarithmic frequency sweep...")

    samples = int(SOURCE_RATE * DURATION)
    t = np.arange(samples) / SOURCE_RATE

    # Sweep from 20 Hz to 22 kHz
    signal = chirp(
        t,
        f0=20,
        f1=22000,
        t1=DURATION,
        method="logarithmic"
    )

    # Apply short fade-in and fade-out
    fade_samples = int(SOURCE_RATE * 0.01)

    fade_in = np.linspace(
        0,
        1,
        fade_samples
    )

    fade_out = np.linspace(
        1,
        0,
        fade_samples
    )

    signal[:fade_samples] *= fade_in
    signal[-fade_samples:] *= fade_out

    # Set peak to -6 dBFS
    peak = np.max(np.abs(signal))

    signal /= peak
    signal *= 10 ** (-6 / 20)

    sf.write(
        TEST_FILE,
        signal.astype(np.float32),
        SOURCE_RATE,
        subtype="FLOAT"
    )

    print()
    print("✓ Sweep created")
    print(f"File: {TEST_FILE}")
    print(f"Sample rate: {SOURCE_RATE} Hz")
    print(f"Duration: {DURATION} seconds")
    print("Start frequency: 20 Hz")
    print("End frequency: 22000 Hz")
    print("Peak level: -6 dBFS")


if __name__ == "__main__":
    create_sweep()

    print()
    print("Next:")
    print("Run converter.py")
    print()
    print("Then analyze the output.")