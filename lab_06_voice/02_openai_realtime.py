"""
Voice Agent — OpenAI Realtime (paid, ~$0.30/min, smooth audio).
Set OPENAI_API_KEY. Type to talk, AI speaks back.
"""
import os, ctypes
# Suppress ALSA warnings
try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(ctypes.c_void_p(None))
except:
    pass
os.environ['JACK_NO_START_SERVER'] = '1'

import asyncio
from strands.experimental.bidi import BidiAgent, BidiAudioIO
from strands.experimental.bidi.io import BidiTextIO
from strands.experimental.bidi.models.openai_realtime import BidiOpenAIRealtimeModel
from strands.experimental.bidi.types.events import BidiTranscriptStreamEvent
from strands_tools import calculator, current_time


class CleanTextOutput:
    """Only prints final responses, no preview chunks."""
    async def __call__(self, event):
        if isinstance(event, BidiTranscriptStreamEvent) and event.is_final:
            print(event.text)


text_io = BidiTextIO()

model = BidiOpenAIRealtimeModel(
    provider_config={
        "audio": {
            "output_rate": 24000,
        }
    }
)
agent = BidiAgent(
    model=model,
    tools=[calculator, current_time],
    system_prompt="You are a helpful voice assistant. Keep responses short.",
)
audio_io = BidiAudioIO(input_buffer_size=50, output_buffer_size=100, input_frames_per_buffer=4096, output_frames_per_buffer=4096)
text_io = BidiTextIO()


async def main():
    print("🎙️  Voice Agent — OpenAI Realtime (paid, smooth audio)")
    print("   Type your message, AI speaks back")
    print("   Ctrl+C to stop\n")
    try:
        await agent.run(inputs=[text_io.input()], outputs=[audio_io.output(), CleanTextOutput()])
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\n👋 Done.")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
