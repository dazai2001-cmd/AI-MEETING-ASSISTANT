# AI Meeting Assistant

A Streamlit app for transcribing, summarizing, extracting action items, and querying meetings—all on your machine using open-source AI (Whisper and Llama 3 via Ollama).

---

## Features

- Upload meeting **audio files** (MP3, WAV, M4A) or **paste transcripts**
- **Transcribes** speech to text (OpenAI Whisper, local)
- **Summarizes meetings** and **extracts action items** (Llama 3 via Ollama, local)
- **Saves meetings** for later reference
- **Ask questions** about a meeting, all meetings, or have a running chat (AI-powered Q&A)
- **No data leaves your PC**—runs completely locally

---

## Setup & Installation

### 1. Clone the repository

```sh
git clone https://github.com/dazai2001-cmd/AI-MEETING-ASSISTANT
cd ai-meeting-assistant
2. Install Python dependencies
Python 3.8+ required.
(Optional but recommended: Create a virtual environment.)

sh
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
3. Install Whisper and dependencies
If not installed by the requirements:

sh
Copy
Edit
pip install git+https://github.com/openai/whisper.git
Note: Whisper requires ffmpeg to be installed system-wide.

4. Install and set up Ollama (Llama 3)
Download and install Ollama for your OS

Pull the Llama 3 model:

sh
Copy
Edit
ollama pull llama3
Start the Ollama server:

sh
Copy
Edit
ollama serve
Ollama should run by default at http://localhost:11434

5. Run the app
sh
Copy
Edit
streamlit run app.py
Visit http://localhost:8501 in your browser.

Directory Structure
arduino
Copy
Edit
ai-meeting-assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── examples/
│   ├── transcripts/
│   │   ├── project_launch_2024-06-10.txt
│   │   └── retrospective_2024-06-18.txt
│   └── audio/
│       ├── project_launch_2024-06-10.wav
│       └── retrospective_2024-06-18.wav
│
├── assets/
│   └── screenshots/    # (optional)
│
└── LICENSE
Example Data
Example transcripts in examples/transcripts/

Example audio files in examples/audio/

You can create your own or use the provided samples to test the app.

Requirements
Python 3.8+

Streamlit

Whisper

PyTorch

Ollama (for local Llama 3 model)

ffmpeg (system-level, for audio support)

requests

Install Python libraries:

sh
Copy
Edit
pip install -r requirements.txt
Usage
Upload an audio file or paste a meeting transcript.

Transcribe (if audio), summarize, and extract action items.

Save meetings and browse past meetings.

Ask questions:

About a single meeting

Search across all meetings

Use the conversational chat for a Q&A history

All processing is local and private.

Troubleshooting
Ollama not connecting?
Ensure ollama serve is running and the Llama 3 model is downloaded.

Whisper/ffmpeg errors?
Make sure ffmpeg is installed and in your system PATH.

CPU vs GPU:
Whisper and Llama 3 run faster on a GPU, but work on CPU as well.