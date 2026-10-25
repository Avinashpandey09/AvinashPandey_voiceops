import os
import warnings
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient
from agent import ZentroMartAgent

warnings.filterwarnings("ignore")
load_dotenv()

# Gnani ke Speech-to-Text aur Text-to-Speech clients setup karna
print("🎙️ Gnani Voice System load ho raha hai...")
stt = GnaniSTTClient()
tts = GnaniTTSClient()

def voice_turn(audio_path, ai_agent):
    print(f"\n🎧 Audio file '{audio_path}' sun raha hu...")
    
    # 1. Kaan (Ears): Audio sun kar text mein badalna
    heard = stt.transcribe(audio_path, language_code="en-IN")["transcript"]
    
    if not heard.strip():
        reply = "Sorry, main sun nahi paaya. Kya aap wapas bolenge?"
    else:
        print(f"🗣️ Customer ne bola: {heard}")
        # 2. Dimag (Brain): AI se answer sochna
        reply = ai_agent.respond(heard)
    
    print(f"🤖 AI ne likha: {reply}")
    
    # 3. Awaaz (Voice): AI ke text ko awaaz mein convert karna
    output_audio = "reply.wav"
    tts.synthesize(
        reply, 
        voice="Kaveri", 
        model="timbre-v2.5", 
        language="en-IN", 
        output_file=output_audio
    )
    print(f"✅ AI ki awaaz '{output_audio}' file mein save ho gayi hai! Aap ise sun sakte hain.")

if __name__ == "__main__":
    agent = ZentroMartAgent()
    
    # Ek test audio file ka naam (jo aapko record karke folder mein rakhni hogi)
    test_audio = "test.wav"
    
    if os.path.exists(test_audio):
        voice_turn(test_audio, agent)
    else:
        print(f"\n⚠️ ERROR: '{test_audio}' file nahi mili!")
        print("Please apne phone ya computer se ek choti si voice recording banayein (Jaise: 'Where is my order?'), usko 'test.wav' naam dekar isi folder mein save karein, aur fir ye code chalayein.")