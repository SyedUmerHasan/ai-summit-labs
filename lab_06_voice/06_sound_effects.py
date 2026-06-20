"""
Sound Effects — Generate sound effects from text descriptions.
Set: ELEVENLABS_API_KEY
"""
import os
from elevenlabs.client import ElevenLabs

api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=api_key)


def generate_sfx(description: str, output_file: str = "sound_effect.mp3"):
    print(f"🎵 Generating: {description}")

    result = elevenlabs.text_to_sound_effects.convert(
        text=description,
        duration_seconds=5.0,
    )

    audio_bytes = b"".join(result)
    with open(output_file, "wb") as f:
        f.write(audio_bytes)

    print(f"✅ Saved to: {output_file}")
    print(f"   Play with: mpv {output_file}")


if __name__ == "__main__":
    print("🎵 ElevenLabs Sound Effects Generator\n")
    while True:
        try:
            desc = input("Describe a sound (or 'q' to quit): ")
            if desc.lower() == 'q':
                break
            generate_sfx(desc)
            print()
        except (KeyboardInterrupt, EOFError):
            break
