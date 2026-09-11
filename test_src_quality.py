import numpy as np
import soundfile as sf
from scipy.signal import periodogram


V1_FILE = "output/src_test_signal_48000Hz.wav"
V2_FILE = "output_v2/src_test_signal_48000Hz.wav"


def analyze_file(file_path, label):

    audio, sample_rate = sf.read(
        file_path,
        always_2d=True,
        dtype="float64"
    )

    # Convert stereo to mono for frequency analysis
    mono = np.mean(audio, axis=1)

    # FFT / frequency analysis
    frequencies, power = periodogram(
        mono,
        sample_rate
    )

    power_db = 10 * np.log10(
        power + 1e-20
    )

    print()
    print("========================================")
    print(label)
    print("========================================")

    print(f"Sample rate: {sample_rate} Hz")
    print(f"Channels: {audio.shape[1]}")
    print(f"Samples: {audio.shape[0]}")

    peak = np.max(np.abs(audio))

    peak_dbfs = (
        20 * np.log10(peak)
        if peak > 0
        else -np.inf
    )

    rms = np.sqrt(
        np.mean(audio ** 2)
    )

    rms_dbfs = (
        20 * np.log10(rms)
        if rms > 0
        else -np.inf
    )

    print(f"Peak: {peak_dbfs:.6f} dBFS")
    print(f"RMS: {rms_dbfs:.6f} dBFS")

    print()
    print("Strongest frequency components:")
    print("----------------------------------------")

    # Ignore frequencies below 100 Hz
    valid = frequencies > 100

    valid_indices = np.where(valid)[0]

    # Find strongest components
    strongest = valid_indices[
        np.argsort(power_db[valid_indices])[-10:]
    ]

    strongest = strongest[::-1]

    for index in strongest:

        print(
            f"{frequencies[index]:8.1f} Hz"
            f"   {power_db[index]:8.2f} dB"
        )

    return {
        "audio": audio,
        "sample_rate": sample_rate,
        "frequencies": frequencies,
        "power_db": power_db
    }


def compare_files(v1, v2):

    print()
    print("========================================")
    print("V1 vs V2 COMPARISON")
    print("========================================")

    # Make sure both files have the same number of samples
    samples = min(
        v1["audio"].shape[0],
        v2["audio"].shape[0]
    )

    v1_audio = v1["audio"][:samples]
    v2_audio = v2["audio"][:samples]

    # Difference between V1 and V2
    difference = v2_audio - v1_audio

    difference_rms = np.sqrt(
        np.mean(difference ** 2)
    )

    difference_peak = np.max(
        np.abs(difference)
    )

    print(
        f"Difference RMS: "
        f"{difference_rms:.12f}"
    )

    print(
        f"Difference peak: "
        f"{difference_peak:.12f}"
    )

    if difference_rms > 0:

        difference_db = (
            20 * np.log10(difference_rms)
        )

    else:

        difference_db = -np.inf

    print(
        f"Difference RMS level: "
        f"{difference_db:.2f} dBFS"
    )

    # Compare frequency responses
    v1_power = v1["power_db"]
    v2_power = v2["power_db"]

    frequency_difference = (
        v2_power - v1_power
    )

    # Only inspect audible range
    audible = (
        (v1["frequencies"] >= 20) &
        (v1["frequencies"] <= 22000)
    )

    max_difference = np.max(
        np.abs(
            frequency_difference[audible]
        )
    )

    print(
        f"Maximum frequency-response "
        f"difference: {max_difference:.6f} dB"
    )

    print()
    print("RESULT")
    print("----------------------------------------")

    if difference_db < -80:

        print(
            "V1 and V2 are extremely similar."
        )

    elif difference_db < -60:

        print(
            "V1 and V2 are very similar."
        )

    elif difference_db < -40:

        print(
            "V1 and V2 have a small "
            "but measurable difference."
        )

    else:

        print(
            "V1 and V2 have a significant "
            "measurable difference."
        )


if __name__ == "__main__":

    v1 = analyze_file(
        V1_FILE,
        "V1 RESULT"
    )

    v2 = analyze_file(
        V2_FILE,
        "V2 RESULT"
    )

    compare_files(
        v1,
        v2
    )

    print()
    print("========================================")
    print("QUALITY TEST COMPLETE")
    print("========================================")
