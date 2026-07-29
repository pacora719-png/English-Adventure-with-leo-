# voice.py - English Adventure with Leo by Juan Pablo Villegas
"""
Reconocimiento de voz real usando el micrófono del navegador
(streamlit-mic-recorder) + Google Speech Recognition.
"""
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder


def record_and_transcribe(key="voice_recorder"):
    """
    Muestra un botón de grabar/detener. Cuando el usuario termina de grabar,
    transcribe el audio a texto en inglés.
    Devuelve el texto reconocido (en minúsculas) o None si no se pudo entender.
    """
    audio = mic_recorder(
        start_prompt="🎤 Grabar",
        stop_prompt="⏹️ Detener",
        just_once=True,
        use_container_width=True,
        key=key,
    )

    if audio is None:
        return None

    recognizer = sr.Recognizer()
    try:
        audio_data = sr.AudioData(audio['bytes'], audio['sample_rate'], 2)
        text = recognizer.recognize_google(audio_data, language='en-US')
        return text.lower().strip()
    except sr.UnknownValueError:
        return ""  # se escuchó algo pero no se entendió
    except sr.RequestError:
        return None  # error de conexión con el servicio de Google


def check_pronunciation(heard_text, target_word):
    """Compara lo que se escuchó contra la palabra objetivo."""
    if not heard_text:
        return False
    target = target_word.lower().strip()
    heard = heard_text.lower().strip()
    return heard == target or target in heard.split()
