import numpy as np
import soundfile as sf


V1_FILE = "output/alias_test_48k_44100Hz.wav"
V2_FILE = "output_v2/alias_test_48k_44100Hz.wav"

SOURCE_RATE = 48000
TARGET_RATE = 44100

TEST_FREQUENCIES = [
    22100,
    22500,
    23000,
    23500,
    23900
]


def measure_frequency(audio, sample_rate, frequency):

    # Use the middle 3 seconds
    start = sample_rate
    end = len(audio) - sample_rate

    audio = audio[start:end]

    # Hann window
    window = np.hanning(len(audio))

    # FFT
    spectrum = np.fft.rfft(
        audio * window
    )

    frequencies = np.fft.rfftfreq(
        len(audio),
        1 / sample_rate
    )

    magnitude = np.abs(spectrum)

    index = np.argmin(
        np.abs(
            frequencies - frequency
        )
    )

    return magnitude[index]


def analyze_file(label, file_path):

    audio, sample_rate = sf.read(
        file_path,
        dtype="float64"
    )

    if audio.ndim > 1:
        audio = np.mean(
            audio,
            axis=1
        )

    print()
    print("========================================")
    print(label)
    print("========================================")

    print()
    print("Source → Expected alias → Level")
    print("----------------------------------------")

    for source_frequency in TEST_FREQUENCIES:

        # Correct alias calculation:
        #
        # alias = target_rate - source_frequency
        #
        # Example:
        # 23900 Hz → 44100 - 23900
        #          → 20200 Hz

        alias_frequency = (
            TARGET_RATE - source_frequency
        )

        magnitude = measure_frequency(
            audio,
            sample_rate,
            alias_frequency
        )

        # Convert to relative dB
        #
        # We use the maximum source/test level
        # as the reference.

        reference = np.max(
            np.abs(audio)
        )

        level_db = (
            20 *
            np.log10(
                magnitude / (
                    len(audio) * reference / 2
                ) + 1e-15
            )
        )

        print(
            f"{source_frequency:5d} Hz"
            f" → "
            f"{alias_frequency:5d} Hz"
            f" → "
            f"{level_db:8.2f} dB"
        )


analyze_file(
    "V1",
    V1_FILE
)

analyze_file(
    "V2",
    V2_FILE
)

print()
print("========================================")
print("CORRECTED ALIASING TEST COMPLETE")
print("========================================")
