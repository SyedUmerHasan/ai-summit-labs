"""
Voice Clone — Record your voice, then clone it.
Set: ELEVENLABS_API_KEY
"""
import os
import wave
import pyaudio
from elevenlabs.client import ElevenLabs

api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=api_key)

SAMPLE_FILE = "voice_sample.wav"
RATE = 44100
CHUNK = 1024
DURATION = 30


def record_voice():
    print(f"🎤 Recording {DURATION} seconds... Speak clearly!")
    print("   Read aloud: 'The quick brown fox jumps over the lazy dog.'")
    print("   Repeat until time is up.\n")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)
        elapsed = int(i * CHUNK / RATE)
        if elapsed % 5 == 0 and i % int(RATE / CHUNK) == 0:
            print(f"   {DURATION - elapsed}s remaining...")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(SAMPLE_FILE, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"\n✅ Saved recording to {SAMPLE_FILE}")


def clone_voice():
    print(f"\n🧬 Cloning voice from {SAMPLE_FILE}...")

    voice = elevenlabs.voices.ivc.create(
        name="My Cloned Voice",
        files=[open(SAMPLE_FILE, "rb")],
        description="Cloned voice for AI Summit demo",
    )

    print(f"\n✅ Voice cloned!")
    print(f"   Voice ID: {voice.voice_id}")
    print(f"\n   Use in 03_elevenlabs.py:")
    print(f'   voice_id="{voice.voice_id}"')


if __name__ == "__main__":
    print("🧬 ElevenLabs Voice Clone\n")

    if not os.path.exists(SAMPLE_FILE):
        input("Press ENTER to start recording (30 seconds)...")
        record_voice()

    clone_voice()
