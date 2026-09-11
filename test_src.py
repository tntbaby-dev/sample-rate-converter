import numpy as np
import soundfile as sf


V1_FILE = "output/grapevine_baseline_48000Hz.wav"
V2_FILE = "output_v2/grapevine_baseline_48000Hz.wav"


def analyze_file(file_path):

    audio, sample_rate = sf.read(
        file_path,
        always_2d=True,
        dtype="float64"
    )

    peak = np.max(
        np.abs(audio)
    )

    rms = np.sqrt(
        np.mean(audio ** 2)
    )

    duration = (
        audio.shape[0] / sample_rate
    )

    peak_dbfs = (
        20 * np.log10(peak)
        if peak > 0
        else -np.inf
    )

    rms_dbfs = (
        20 * np.log10(rms)
        if rms > 0
        else -np.inf
    )

    return {
        "sample_rate": sample_rate,
        "channels": audio.shape[1],
        "duration": duration,
        "peak_dbfs": peak_dbfs,
        "rms_dbfs": rms_dbfs,
        "samples": audio.shape[0]
    }


print("\n========================================")
print("SAMPLE-RATE CONVERTER TEST")
print("========================================")


# ------------------------------------------------------------
# Analyze V1
# ------------------------------------------------------------

v1 = analyze_file(V1_FILE)

print("\nV1")
print("----------------------------------------")

for key, value in v1.items():
    print(f"{key}: {value}")


# ------------------------------------------------------------
# Analyze V2
# ------------------------------------------------------------

v2 = analyze_file(V2_FILE)

print("\nV2")
print("----------------------------------------")

for key, value in v2.items():
    print(f"{key}: {value}")


# ------------------------------------------------------------
# Compare
# ------------------------------------------------------------

print("\nCOMPARISON")
print("----------------------------------------")

print(
    f"Peak difference: "
    f"{v2['peak_dbfs'] - v1['peak_dbfs']:.6f} dB"
)

print(
    f"RMS difference: "
    f"{v2['rms_dbfs'] - v1['rms_dbfs']:.6f} dB"
)

print(
    f"Duration difference: "
    f"{v2['duration'] - v1['duration']:.9f} seconds"
)

print(
    f"Sample count difference: "
    f"{v2['samples'] - v1['samples']}"
)

print("\n========================================")
print("TEST COMPLETE")
print("========================================")
