# ZentroMart Voice Support Agent - VoiceOps 2026 Capstone

This repository contains the end-to-end code for the VoiceOps 2026 Capstone Project: building a voice-enabled AI support agent for ZentroMart using Gemini, Qdrant, and Gnani STT/TTS.

**Public Repository URL:** \[https://github.com/Avinashpandey09/AvinashPandey_voiceops\]

## Architecture (The Four Steps)

1. **Brain (LLM):** `gemini-3.8-flash` handles conversational logic and strict policy adherence.

2. **Memory (RAG):** Qdrant local vector database retrieves relevant Markdown chunks using `text-embedding-004`.

3. **Actions (Tools):** Integrated with `lookup_order` and `create_ticket` with mandatory identity verification.

4. **Voice (Speech):** Gnani Python SDK for STT (audio to text) and TTS (text to audio using the 'Kaveri' voice).

## Setup Instructions

1. **Clone the repository:**

   ```
   git clone https://github.com/Avinashpandey09/AvinashPandey_voiceops/
   cd AvinashPandey_voiceops
   
   ```

2. **Install Dependencies:**
   Ensure you have Python installed, then run:

   ```
   pip install -r requirements.txt
   
   ```

3. **Environment Variables:**
   Do NOT commit real API keys. Copy the provided example file to a new `.env` file:

   ```
   cp .env.example .env
   
   ```

   Open the `.env` file and add your valid Google Gemini and Gnani API keys.

4. **Prepare the Dataset:**
   Ensure the Capstone dataset folders (`kb`, `data`, `tools`) are placed in the root directory.

## How to Run (Evaluation Command)

As per the Capstone evaluation requirements, the agent processes a batch of customer audio queries, retrieves source chunks, and synthesizes audio replies.

1. Create a folder named `test_audios` in the root directory and place your `.wav` test queries inside.

2. Run the automated evaluation script:

   ```
   python run.py
   
   ```

3. **Outputs:** The script will automatically create a `sample_outputs` folder containing:

   * The generated audio replies (`reply_filename.wav`).

   * A log file (`log_filename.txt`) containing the transcribed customer text, agent reply, and the **Document Section IDs** used for retrieval.

## Interactive Mode (Optional)

To test the agent via text without voice models:

```
python agent.py

```
# "Note: The original dataset (policies, customer data, and mock files) is not included in this repository to comply with the Capstone Project submission guidelines. To run this project, please use your own dataset in the kb/ and data/ folders."
