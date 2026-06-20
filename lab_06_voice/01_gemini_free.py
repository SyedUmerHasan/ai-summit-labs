"""
Voice Agent — Gemini Live (FREE tier). Type to talk, AI speaks back.
Set GOOGLE_API_KEY. 
"""
import os, ctypes
try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(ctypes.c_void_p(None))
except:
    pass
os.environ['JACK_NO_START_SERVER'] = '1'

import warnings
warnings.filterwarnings('ignore', message='.*non-data parts.*')

import asyncio
from strands.experimental.bidi import BidiAgent, BidiAudioIO
from strands.experimental.bidi.io import BidiTextIO
from strands.experimental.bidi.models.gemini_live import BidiGeminiLiveModel
from strands.experimental.bidi.types.events import BidiTranscriptStreamEvent
from strands_tools import calculator, current_time


class CleanTextOutput:
    async def __call__(self, event):
        if isinstance(event, BidiTranscriptStreamEvent) and event.is_final:
            print(event.text)


model = BidiGeminiLiveModel()
agent = BidiAgent(
    model=model,
    tools=[calculator, current_time],
    system_prompt="You are a helpful voice assistant. Keep responses short.",
)
audio_io = BidiAudioIO(input_buffer_size=50, output_buffer_size=100, input_frames_per_buffer=4096, output_frames_per_buffer=4096)
text_io = BidiTextIO()


async def main():
    print("🎙️  Voice Agent — Gemini Live (FREE)")
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
