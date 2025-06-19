# AI Meeting Assistant

A private, local-first Streamlit app for transcribing, summarizing, extracting action items, and querying your meeting recordings—using open-source AI models (Whisper & Llama 3 via Ollama).

---

## Features

* Upload **meeting audio** (MP3, WAV, M4A) or **paste text transcripts**
* Accurate, fast **speech-to-text** (Whisper, runs locally)
* Automated **meeting summaries** and **action item extraction** (Llama 3 via Ollama, runs locally)
* Save, browse, and organize meetings with summaries, transcripts, and action lists
* **Ask questions** about any meeting, or search all meetings with AI
* **Conversational Q\&A**: Keep a running chat about any meeting
* **All data is private**: nothing sent to the cloud!

---

## Quick Start

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/ai-meeting-assistant.git
cd ai-meeting-assistant
```

### 2. Install Python Packages

Python 3.8+ recommended.

```sh
pip install -r requirements.txt
```

> **Note:** Whisper needs [ffmpeg](https://ffmpeg.org/) installed on your system.

### 3. Install and Start Ollama

* [Download Ollama](https://ollama.com/download) and install for your OS.

* Download the Llama 3 model:

  ```sh
  ollama pull llama3
  ```

* Start the Ollama server:

  ```sh
  ollama serve
  ```

### 4. Run the App

```sh
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Example Data

Example transcripts and sample audio files are included:

* `examples/transcripts/project_launch_2024-06-10.txt`
* `examples/transcripts/retrospective_2024-06-18.txt`
* `examples/audio/` (add your own .wav/.mp3 if needed)

---

## Directory Structure

```
ai-meeting-assistant/
├── app.py
├── requirements.txt
├── README.md
├── examples/
│   ├── transcripts/
│   └── audio/
├── assets/
│   └── screenshots/
└── LICENSE
```

---

## Requirements

* Python 3.8+
* Streamlit
* Whisper (from OpenAI, plus PyTorch and ffmpeg)
* Ollama (local LLM server for Llama 3)
* requests

Install all Python requirements with:

```sh
pip install -r requirements.txt
```

---

## Usage

1. **Upload** an audio file or paste a meeting transcript.
2. **Transcribe** (if audio), **summarize**, and **extract action items**.
3. **Save** meetings and browse past meetings.
4. **Ask questions**: about a single meeting, across all meetings, or with chat.

All processing is **local** and private.

---

## Troubleshooting

* **Ollama connection errors?**
  Make sure `ollama serve` is running and the Llama 3 model is downloaded.

* **Whisper/ffmpeg errors?**
  Ensure `ffmpeg` is installed and available in your system PATH.

* **Slow performance?**
  Both models can run on CPU, but will be faster if you have a GPU.

---

## License

MIT License (see LICENSE file).

---

**Questions or contributions? Open an issue or pull request!**
