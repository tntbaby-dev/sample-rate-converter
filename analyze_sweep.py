import numpy as np
import soundfile as sf
from scipy.signal import stft


V1_FILE = "output/src_sweep_test_48000Hz.wav"
V2_FILE = "output_v2/src_sweep_test_48000Hz.wav"


def analyze_sweep(file_path, label):

    audio, sample_rate = sf.read(
        file_path,
        dtype="float64"
    )

    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    print()
    print("========================================")
    print(label)
    print("========================================")

    print(f"Sample rate: {sample_rate} Hz")
    print(f"Samples: {len(audio)}")

    # STFT
    frequencies, times, Zxx = stft(
        audio,
        fs=sample_rate,
        window="hann",
        nperseg=4096,
        noverlap=3072
    )

    magnitude = np.abs(Zxx)

    # Convert to dB
    magnitude_db = 20 * np.log10(
        magnitude + 1e-12
    )

    # Analyze several frequency regions
    regions = [
        ("20 Hz - 1 kHz", 20, 1000),
        ("1 kHz - 10 kHz", 1000, 10000),
        ("10 kHz - 15 kHz", 10000, 15000),
        ("15 kHz - 18 kHz", 15000, 18000),
        ("18 kHz - 20 kHz", 18000, 20000),
        ("20 kHz - 22 kHz", 20000, 22000),
        ("22 kHz - 24 kHz", 22000, 24000),
    ]

    print()
    print("Frequency-region levels")
    print("----------------------------------------")

    for name, low, high in regions:

        mask = (
            (frequencies >= low) &
            (frequencies < high)
        )

        if not np.any(mask):
            continue

        region_values = magnitude_db[mask, :]

        maximum = np.max(region_values)
        average = np.mean(region_values)

        print(
            f"{name:18s} "
            f"Max: {maximum:8.2f} dB   "
            f"Avg: {average:8.2f} dB"
        )

    return {
        "frequencies": frequencies,
        "times": times,
        "magnitude_db": magnitude_db
    }


def compare(v1, v2):

    print()
    print("========================================")
    print("V1 vs V2 SWEEP COMPARISON")
    print("========================================")

    frequencies = v1["frequencies"]

    difference = (
        v2["magnitude_db"] -
        v1["magnitude_db"]
    )

    regions = [
        ("20 Hz - 1 kHz", 20, 1000),
        ("1 kHz - 10 kHz", 1000, 10000),
        ("10 kHz - 15 kHz", 10000, 15000),
        ("15 kHz - 18 kHz", 15000, 18000),
        ("18 kHz - 20 kHz", 18000, 20000),
        ("20 kHz - 22 kHz", 20000, 22000),
        ("22 kHz - 24 kHz", 22000, 24000),
    ]

    print()
    print("Maximum V1/V2 difference")
    print("----------------------------------------")

    for name, low, high in regions:

        mask = (
            (frequencies >= low) &
            (frequencies < high)
        )

        if not np.any(mask):
            continue

        region_difference = np.abs(
            difference[mask, :]
        )

        maximum = np.max(
            region_difference
        )

        average = np.mean(
            region_difference
        )

        print(
            f"{name:18s} "
            f"Max: {maximum:8.3f} dB   "
            f"Avg: {average:8.3f} dB"
        )

    print()
    print("Interpretation")
    print("----------------------------------------")

    print(
        "The most important regions are "
        "15-22 kHz and 22-24 kHz."
    )

    print(
        "The 22-24 kHz region is especially "
        "important because 48 kHz audio has "
        "a Nyquist frequency of 24 kHz."
    )


if __name__ == "__main__":

    v1 = analyze_sweep(
        V1_FILE,
        "V1 SWEEP"
    )

    v2 = analyze_sweep(
        V2_FILE,
        "V2 SWEEP"
    )

    compare(
        v1,
        v2
    )

    print()
    print("========================================")
    print("SWEEP ANALYSIS COMPLETE")
    print("========================================")
