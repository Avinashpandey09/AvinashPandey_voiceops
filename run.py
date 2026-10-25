import os
import glob
from agent import ZentroMartAgent
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient

stt = GnaniSTTClient()
tts = GnaniTTSClient()

def run_batch(input_folder="test_audios", output_folder="sample_outputs"):
    os.makedirs(output_folder, exist_ok=True)
    agent = ZentroMartAgent()
    
    audio_files = glob.glob(os.path.join(input_folder, "*.wav"))
    if not audio_files:
        print(f"Error: '{input_folder}' folder mein koi audio file nahi mili.")
        return

    for audio_path in audio_files:
        filename = os.path.basename(audio_path)
        print(f"\nProcessing: {filename}...")
        
        heard = stt.transcribe(audio_path, language_code="en-IN")["transcript"]
        reply, sources = agent.respond(heard)
        
        # Audio save karna
        audio_out = os.path.join(output_folder, f"reply_{filename}")
        tts.synthesize(reply, voice="Kaveri", model="timbre-v2.5", language="en-IN", output_file=audio_out)
        
        # Text aur Source Chunks save karna
        text_out = os.path.join(output_folder, f"transcript_{filename}.txt")
        with open(text_out, "w", encoding="utf-8") as f:
            f.write(f"Customer: {heard}\nAgent: {reply}\nSources Used: {', '.join(sources)}\n")
            
        print(f"✅ Saved output for {filename}")

if __name__ == "__main__":
    run_batch()