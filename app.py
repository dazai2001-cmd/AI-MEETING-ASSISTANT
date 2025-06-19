import os
import streamlit as st
import whisper
import tempfile
import requests
import uuid

# === OLLAMA LLM CALL FUNCTION ===
def ollama_llm(prompt, model="llama3"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

# === WHISPER MODEL SETUP ===
@st.cache_resource
def get_whisper_model():
    return whisper.load_model("base")  # Use 'small' or 'large-v3' for higher accuracy

whisper_model = get_whisper_model()

# === SESSION STATE INIT ===
if "meetings" not in st.session_state:
    st.session_state["meetings"] = {}
if "summary" not in st.session_state:
    st.session_state["summary"] = ""
if "action_items" not in st.session_state:
    st.session_state["action_items"] = ""
if "submitted_transcript" not in st.session_state:
    st.session_state["submitted_transcript"] = ""
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = "uploader_0"
if "my_transcript_text" not in st.session_state:
    st.session_state["my_transcript_text"] = ""
if "reset_transcript" not in st.session_state:
    st.session_state["reset_transcript"] = False

# === RESET TRICK: Before widget creation ===
if st.session_state["reset_transcript"]:
    st.session_state["my_transcript_text"] = ""
    st.session_state["uploader_key"] = str(uuid.uuid4())
    st.session_state["reset_transcript"] = False

st.title("AI Meeting Assistant (Ollama Edition)")

# === UPLOAD SECTION ===
st.header("Upload Meeting Recording or Transcript")
audio_file = st.file_uploader(
    "Upload audio file (.mp3/.wav/.m4a) OR .txt transcript",
    type=["mp3", "wav", "m4a", "txt"],
    key=st.session_state["uploader_key"],
)
transcript_text = st.text_area(
    "Or paste your meeting transcript here:",
    value=st.session_state["my_transcript_text"],
    key="my_transcript_text",
)

if st.button("Submit Transcript / Audio"):
    transcript = ""
    if audio_file and audio_file.type != "text/plain":
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[-1]) as tmpfile:
            tmpfile.write(audio_file.read())
            tmpfile_path = tmpfile.name
        with st.spinner("Transcribing audio..."):
            result = whisper_model.transcribe(tmpfile_path)
            transcript = result["text"]
        os.remove(tmpfile_path)
        st.success("Transcription complete!")
        st.write("**Transcript:**")
        st.write(transcript)
    elif audio_file and audio_file.type == "text/plain":
        transcript = audio_file.read().decode("utf-8")
        st.success("Text transcript uploaded!")
        st.write("**Transcript:**")
        st.write(transcript)
    elif transcript_text.strip():
        transcript = transcript_text.strip()
        st.success("Text transcript submitted!")
        st.write("**Transcript:**")
        st.write(transcript)
    else:
        st.warning("Please upload or enter a transcript before submitting.")
    # Only update session state if transcript is nonempty
    if transcript.strip():
        st.session_state["submitted_transcript"] = transcript
        st.session_state["summary"] = ""
        st.session_state["action_items"] = ""
    else:
        st.session_state["submitted_transcript"] = ""

transcript = st.session_state.get("submitted_transcript", "")

# === SUMMARIZATION & ACTION ITEMS WORKFLOW ===
if transcript:
    st.header("Summarize and Save Meeting")
    if st.button("Summarize Meeting"):
        with st.spinner("Summarizing..."):
            prompt = (
                "Summarize the following meeting transcript, highlighting who said what, "
                "main decisions, and all action items:\n\n"
            )
            prompt += transcript
            summary = ollama_llm(prompt, model="llama3")
            st.session_state["summary"] = summary
            st.success("Summary generated!")
        st.session_state["action_items"] = ""  # Reset action items after summarizing

    if st.session_state["summary"]:
        st.write("### Meeting Summary")
        st.write(st.session_state["summary"])
        if st.button("Extract Action Items"):
            with st.spinner("Extracting action items..."):
                action_words = (
                    "prepare, send, coordinate, organize, complete, finish, launch, update, provide, "
                    "review, analyze, share, email, deliver, report, contact, schedule, finalize, "
                    "submit, assign, implement, present, install, start, arrange"
                )
                ai_prompt = (
                    f"Extract all action items from this meeting transcript. "
                    f"Action items usually start with words like: {action_words}.\n"
                    "For each action item, include: Task, Responsible Person, Deadline (if mentioned).\n"
                    "Transcript:\n"
                )
                ai_prompt += transcript
                action_items = ollama_llm(ai_prompt, model="llama3")
                st.session_state["action_items"] = action_items
                st.success("Action items extracted!")
    if st.session_state["action_items"]:
        st.write("### Action Items")
        st.write(st.session_state["action_items"])
    meeting_date = st.text_input("Meeting Date (e.g., 2024-06-17):")
    if st.session_state["summary"] and st.session_state["action_items"]:
        if st.button("Save Meeting Summary"):
            if meeting_date:
                st.session_state["meetings"][meeting_date] = {
                    "transcript": transcript,
                    "summary": st.session_state["summary"],
                    "action_items": st.session_state["action_items"],
                }
                st.success("Meeting summary saved!")
                st.session_state["summary"] = ""
                st.session_state["action_items"] = ""
                st.session_state["submitted_transcript"] = ""
                st.session_state["reset_transcript"] = True  # Set flag for next run
                st.rerun()  # Rerun immediately—no further assignments!
            else:
                st.warning("Please enter the meeting date above.")

# === DISPLAY SAVED MEETINGS & TABS FOR CHAT/SEARCH ===
if st.session_state["meetings"]:
    st.header("Saved Meeting Summaries")
    for date, info in st.session_state["meetings"].items():
        with st.expander(f"Meeting on {date}"):
            st.write("**Summary:**")
            st.write(info["summary"])
            if info.get("action_items"):
                st.write("**Action Items:**")
                st.write(info["action_items"])
            st.write("**Transcript:**")
            st.write(info["transcript"])

    tab1, tab2, tab3 = st.tabs(["🔍 Ask About a Meeting", "🧠 Ask ALL Meetings", "💬 Conversational Chat"])

    # ---- CHAT WITH A MEETING ----
    with tab1:
        meeting_dates = list(st.session_state["meetings"].keys())
        selected_date = st.selectbox("Select a meeting date to chat with:", meeting_dates, key="select_meeting_chat")
        user_query = st.text_input("Ask a question about this meeting (e.g., What are the deadlines?)", key="single_meeting_query")
        if st.button("Ask Meeting AI", key="ask_single_meeting"):
            if selected_date and user_query.strip():
                with st.spinner("Thinking..."):
                    meeting = st.session_state["meetings"][selected_date]
                    context = (
                        f"MEETING SUMMARY:\n{meeting['summary']}\n\n"
                        f"ACTION ITEMS:\n{meeting.get('action_items', '')}\n\n"
                        f"FULL TRANSCRIPT:\n{meeting['transcript']}\n\n"
                    )
                    prompt = (
                        f"Based on the following meeting context, answer the user's question as helpfully as possible.\n\n"
                        f"User question: {user_query}\n\n"
                        f"Meeting context:\n{context}"
                    )
                    response = ollama_llm(prompt, model="llama3")
                    st.markdown(f"**AI Answer:** {response}")
            else:
                st.warning("Please select a meeting and enter a question.")

    # --- CHAT/SEARCH ACROSS ALL MEETINGS ---
    with tab2:
        user_query_all = st.text_input("Ask anything across all meetings (e.g., Which meetings mentioned supply chain delays?)", key="all_meetings_query")
        if st.button("Ask ALL Meetings AI", key="ask_all_meetings"):
            if user_query_all.strip():
                with st.spinner("Searching all meetings..."):
                    # Gather all contexts
                    context_all = ""
                    for date, info in st.session_state["meetings"].items():
                        context_all += (
                            f"\n=== MEETING: {date} ===\n"
                            f"SUMMARY: {info['summary']}\n"
                            f"ACTION ITEMS: {info.get('action_items','')}\n"
                            f"TRANSCRIPT: {info['transcript']}\n"
                        )
                    prompt = (
                        "Given the following set of meetings (with summaries, action items, and transcripts), "
                        "answer the user's question as helpfully as possible. "
                        "If a date or person is relevant, include that info in your answer. "
                        f"User question: {user_query_all}\n\n"
                        f"Meetings:\n{context_all}"
                    )
                    response = ollama_llm(prompt, model="llama3")
                    st.markdown(f"**AI Answer (all meetings):** {response}")
            else:
                st.warning("Enter a question to search all meetings.")

    # --- CONVERSATIONAL Q&A FOR SINGLE MEETING ---
    with tab3:
        chat_dates = list(st.session_state["meetings"].keys())
        selected_chat_date = st.selectbox("Choose a meeting to chat with (conversational):", chat_dates, key="chat_date_box")

        # Initialize chat history if not present
        if f"chat_history_{selected_chat_date}" not in st.session_state:
            st.session_state[f"chat_history_{selected_chat_date}"] = []

        chat_input = st.text_input("Ask anything about this meeting (running chat):", key="chat_input_box")

        if st.button("Send to Meeting Chatbot", key="chat_history_btn"):
            if chat_input.strip():
                history = st.session_state[f"chat_history_{selected_chat_date}"]
                meeting = st.session_state["meetings"][selected_chat_date]
                # Build chat history string
                history_str = ""
                for i, (q, a) in enumerate(history):
                    history_str += f"Q{i+1}: {q}\nA{i+1}: {a}\n"
                context = (
                    f"MEETING SUMMARY:\n{meeting['summary']}\n\n"
                    f"ACTION ITEMS:\n{meeting.get('action_items', '')}\n\n"
                    f"FULL TRANSCRIPT:\n{meeting['transcript']}\n\n"
                )
                prompt = (
                    "You are a helpful meeting assistant. Here is the meeting context and chat so far:\n\n"
                    f"{context}\n"
                    f"CHAT HISTORY SO FAR:\n{history_str}\n"
                    f"User: {chat_input}\nAI:"
                )
                response = ollama_llm(prompt, model="llama3")
                # Save Q&A to history
                history.append((chat_input, response))
                st.session_state[f"chat_history_{selected_chat_date}"] = history
                st.success("Response added to chat history!")

        # Display chat history for the selected meeting
        history = st.session_state.get(f"chat_history_{selected_chat_date}", [])
        if history:
            st.markdown("#### Chat History for this Meeting")
            for i, (q, a) in enumerate(history):
                st.markdown(f"**You:** {q}\n\n**AI:** {a}")

