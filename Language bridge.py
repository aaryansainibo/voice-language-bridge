import streamlit as st
from streamlit_mic_recorder import mic_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import io

st.set_page_config(page_title="Voice Bridge", page_icon="🎤")
st.title("🎤 Auto-Language Bridge")

languages = {
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "de": "German",
    "zh-CN": "Chinese"
}

target_lang = st.selectbox(
    "Translate to:",
    list(languages.keys()),
    format_func=lambda x: languages[x]
)

st.write("Record your message:")

audio = mic_recorder(
    start_prompt="⏺️ Start Recording",
    stop_prompt="⏹️ Stop & Translate",
    key="recorder"
)

if audio and "bytes" in audio:

    try:
        # Convert WebM to WAV
        audio_bytes = io.BytesIO(audio["bytes"])
        audio_segment = AudioSegment.from_file(audio_bytes)
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)

        user_text = recognizer.recognize_google(audio_data)
        st.info(f"You said: **{user_text}**")

        translated = GoogleTranslator(source="auto", target=target_lang).translate(user_text)
        st.success(f"Translation: **{translated}**")

        tts = gTTS(text=translated, lang=target_lang)
        audio_out = io.BytesIO()
        tts.write_to_fp(audio_out)
        audio_out.seek(0)

        st.audio(audio_out.read(), format="audio/mp3", autoplay=True)

    except Exception as e:
        st.error(f"Error: {e}")
