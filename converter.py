import os
import soundfile as sf
from scipy.signal import resample_poly


INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

TARGET_SAMPLE_RATES = [44100, 48000]


def convert_audio(input_path, output_path, target_rate):
    audio, original_rate = sf.read(input_path)

    print(
        f"Converting {os.path.basename(input_path)}: "
        f"{original_rate} Hz → {target_rate} Hz"
    )

    if original_rate == target_rate:
        sf.write(output_path, audio, target_rate)
        print(f"✓ Created: {output_path}\n")
        return

    # Calculate the conversion ratio
    import math

    gcd = math.gcd(original_rate, target_rate)

    up = target_rate // gcd
    down = original_rate // gcd

    converted_audio = resample_poly(
        audio,
        up,
        down,
        axis=0
    )

    sf.write(
        output_path,
        converted_audio,
        target_rate
    )

    print(f"✓ Created: {output_path}\n")


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    wav_files = [
        file_name
        for file_name in os.listdir(INPUT_FOLDER)
        if file_name.lower().endswith(".wav")
    ]

    if not wav_files:
        print("No WAV files found in the input folder.")
        return

    print(f"Found {len(wav_files)} WAV file(s).\n")

    for file_name in wav_files:

        input_path = os.path.join(
            INPUT_FOLDER,
            file_name
        )

        base_name = os.path.splitext(file_name)[0]

        for target_rate in TARGET_SAMPLE_RATES:

            output_name = (
                f"{base_name}_{target_rate}Hz.wav"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                output_name
            )

            convert_audio(
                input_path,
                output_path,
                target_rate
            )


if __name__ == "__main__":
    main()