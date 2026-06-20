"""
Voice Agent — Strands Agent + ElevenLabs TTS (high-quality voice output).
Agent thinks with Claude, speaks with ElevenLabs.
Set ELEVENLABS_API_KEY and ANTHROPIC_API_KEY.

Free tier: 10,000 characters/month.
Get key: https://elevenlabs.io/app/settings/api-keys
"""
import io
import pyaudio
from strands import Agent
from strands_tools import calculator, current_time
from elevenlabs.client import ElevenLabs
from shared.model_config import get_model
from shared.terminal import callback_handler

# ElevenLabs TTS
import os
eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Strands Agent (text-based)
agent = Agent(
    model=get_model(),
    tools=[calculator, current_time],
    system_prompt="You are a helpful voice assistant. Keep responses under 2 sentences. Plain text only, no markdown.",
    callback_handler=callback_handler,
)


def speak(text: str):
    """Convert text to speech and play via speakers."""
    audio_gen = eleven.text_to_speech.convert(
        text=text,
        voice_id="EXAVITQu4vr4xnSDxMaL",  # "Sarah" soft female
        model_id="eleven_turbo_v2_5",
        output_format="pcm_24000",
    )
    # Collect audio bytes
    audio_bytes = b"".join(audio_gen)

    # Play with PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True, frames_per_buffer=4096)
    stream.write(audio_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
    print("🎙️  Voice Agent — Strands + ElevenLabs")
    print("   Type your message, AI responds with premium voice")
    print("   Ctrl+C to stop\n")

    while True:
        try:
            user_input = input("\033[32m> \033[0m")
            if not user_input.strip():
                continue
            result = agent(user_input)
            text = result.message['content'][0]['text'] if isinstance(result.message, dict) else str(result)
            print(f"\n🔊 Speaking...\n")
            speak(text)
            print()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Done.")
            break


if __name__ == "__main__":
    main()
