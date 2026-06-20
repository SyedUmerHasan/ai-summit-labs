"""
Voice Agent — ElevenLabs Conversational AI (full duplex, smooth audio).
Speak into mic, AI responds with premium human voice. No flickering.

Set: ELEVENLABS_API_KEY, AGENT_ID
Create agent at: https://elevenlabs.io/app/conversational-ai
"""
import os
import signal
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")

if not agent_id:
    print("❌ Set AGENT_ID env var. Create an agent at:")
    print("   https://elevenlabs.io/app/conversational-ai")
    exit(1)

elevenlabs = ElevenLabs(api_key=api_key)

conversation = Conversation(
    elevenlabs,
    agent_id,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda r: print(f"  🤖 Agent: {r}"),
    callback_user_transcript=lambda t: print(f"  🎤 You: {t}"),
)

print("🎙️  ElevenLabs Conversational AI — Full Duplex Voice")
print("   Speak naturally. AI responds in real-time.")
print("   Ctrl+C to stop\n")

signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
conversation.start_session()
conversation_id = conversation.wait_for_session_end()
print(f"\n✅ Conversation ID: {conversation_id}")
