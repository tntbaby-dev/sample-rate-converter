import numpy as np
import soundfile as sf


SOURCE_RATE = 48000
DURATION = 5.0

TEST_FILE = "alias_test_48k.wav"

FREQUENCIES = [
    22000,
    22100,
    22500,
    23000,
    23500,
    23900
]


def create_test_signal():

    samples = int(
        SOURCE_RATE * DURATION
    )

    t = np.arange(samples) / SOURCE_RATE

    signal = np.zeros(samples)

    for frequency in FREQUENCIES:

        signal += (
            0.1 *
            np.sin(
                2 * np.pi * frequency * t
            )
        )

    # Prevent clipping
    peak = np.max(
        np.abs(signal)
    )

    signal /= peak

    signal *= 0.5

    sf.write(
        TEST_FILE,
        signal.astype(np.float32),
        SOURCE_RATE,
        subtype="FLOAT"
    )

    print()
    print("========================================")
    print("ALIASING TEST SIGNAL CREATED")
    print("========================================")

    print(
        f"Source sample rate: "
        f"{SOURCE_RATE} Hz"
    )

    print(
        f"Duration: {DURATION} seconds"
    )

    print()
    print("Test frequencies:")

    for frequency in FREQUENCIES:

        print(
            f"  {frequency} Hz"
        )

    print()
    print(
        f"File: {TEST_FILE}"
    )


if __name__ == "__main__":

    create_test_signal()
