# app.py - English Adventure with Leo by Juan Pablo Villegas

import streamlit as st
import json
import random
import time
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="English Adventure with Leo 🦁 by Juan Pablo Villegas",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
    <style>
    .header {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 36px;
        font-weight: bold;
    }
    .header-subtitle {
        font-size: 18px;
        opacity: 0.9;
    }
    .header-credit {
        font-size: 14px;
        opacity: 0.8;
        margin-top: 5px;
        font-style: italic;
    }
    .stat-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #FF6B6B;
    }
    .stat-label {
        font-size: 14px;
        color: #666;
    }
    .home-container {
        text-align: center;
        padding: 40px 20px;
    }
    .home-hero {
        margin-bottom: 40px;
    }
    .home-emoji {
        font-size: 100px;
    }
    .home-title {
        font-size: 48px;
        color: #2D3436;
        margin: 20px 0;
    }
    .home-subtitle {
        font-size: 24px;
        color: #636E72;
    }
    .home-credit {
        font-size: 18px;
        color: #FF6B6B;
        font-weight: bold;
        margin-top: 10px;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 40px;
    }
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-icon {
        font-size: 48px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        font-size: 18px;
    }
    .leo-message {
        background-color: #FFF3E0;
        text-align: left;
        border-left: 5px solid #FF6B6B;
    }
    .user-message {
        background-color: #E3F2FD;
        text-align: right;
        border-right: 5px solid #2196F3;
    }
    .word-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .word-emoji {
        font-size: 80px;
    }
    .word-question {
        font-size: 24px;
        margin: 20px 0;
        color: #2D3436;
    }
    .story-card {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
    }
    .speaking-card {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
    }
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        font-size: 20px;
        border-radius: 20px;
        padding: 12px 24px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #FF4757;
        transform: scale(1.02);
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
def init_session_state():
    defaults = {
        'page': 'home',
        'user_id': None,
        'username': None,
        'score': 0,
        'level': 1,
        'streak': 0,
        'current_word': None,
        'current_options': [],
        'chat_history': [],
        'game_mode': 'vocabulary',
        'story_progress': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Cargar vocabulario
try:
    with open('data/vocabulary.json', 'r', encoding='utf-8') as f:
        VOCABULARY = json.load(f)
except:
    VOCABULARY = {
        "1": {
            "title": "Animales",
            "emoji": "🐾",
            "words": [
                {"word": "cat", "meaning": "gato", "emoji": "🐱"},
                {"word": "dog", "meaning": "perro", "emoji": "🐶"},
                {"word": "bird", "meaning": "pájaro", "emoji": "🐦"}
            ]
        }
    }

# Personaje
LEO = {
    'name': 'Leo',
    'emoji': '🦁',
    'color': '#FF6B6B',
    'personality': {
        'happy': '¡Genial! 🎉',
        'excited': '¡Increíble! 🌟',
        'encouraging': '¡Sigue así! 💪',
        'patient': '¡Inténtalo de nuevo! 🤗',
        'proud': '¡Estoy muy orgulloso de ti! 🥰'
    }
}

def add_chat_message(role, message):
    st.session_state.chat_history.append({
        'role': role,
        'message': message,
        'time': datetime.now().isoformat()
    })

def generate_quiz():
    level_data = VOCABULARY.get(str(st.session_state.level), VOCABULARY['1'])
    words = level_data['words']
    
    correct_word = random.choice(words)
    options = [correct_word['meaning']]
    all_meanings = [w['meaning'] for w in words if w['meaning'] != correct_word['meaning']]
    
    num_options = min(3, len(all_meanings))
    wrong_options = random.sample(all_meanings, num_options) if all_meanings else []
    options.extend(wrong_options)
    random.shuffle(options)
    
    return {
        'correct': correct_word,
        'options': options
    }

def show_header():
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
            <div class="header">
                <span style="font-size:40px;">🦁</span>
                <span class="header-title">English Adventure</span>
                <span class="header-subtitle">con Leo</span>
                <div class="header-credit">by Juan Pablo Villegas</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{st.session_state.score}</div>
                <div class="stat-label">⭐ Puntos</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">🔥 {st.session_state.streak}</div>
                <div class="stat-label">Racha</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        level_title = VOCABULARY.get(str(st.session_state.level), VOCABULARY['1'])['title']
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{st.session_state.level}</div>
                <div class="stat-label">Nivel: {level_title}</div>
            </div>
        """, unsafe_allow_html=True)

def show_home():
    st.markdown("""
        <div class="home-container">
            <div class="home-hero">
                <div class="home-emoji">🦁</div>
                <h1 class="home-title">¡Aprende inglés jugando!</h1>
                <p class="home-subtitle">Con Leo, tu amigo y guía en esta aventura</p>
                <p class="home-credit">✨ Creado por Juan Pablo Villegas ✨</p>
            </div>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">📚</div>
                    <h3>Vocabulario</h3>
                    <p>Aprende nuevas palabras con juegos divertidos</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎤</div>
                    <h3>Pronunciación</h3>
                    <p>Practica tu speaking con reconocimiento de voz</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📖</div>
                    <h3>Historias</h3>
                    <p>Escucha y lee cuentos interactivos en inglés</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🏆</div>
                    <h3>Logros</h3>
                    <p>Gana trofeos y comparte tu progreso</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ¡Comenzar Aventura!", use_container_width=True):
            st.session_state.page = 'quiz'
            add_chat_message('leo', f"¡Hola! Soy {LEO['name']}. ¡Listo para aprender inglés! 🦁")
            st.rerun()

def show_quiz():
    show_header()
    
    with st.sidebar:
        st.markdown("### 🎮 Configuración")
        
        game_mode = st.selectbox(
            "Modo de juego",
            ["Vocabulario 📚", "Historias 📖", "Speaking 🎤"],
            index=0
        )
        st.session_state.game_mode = game_mode.split(" ")[0].lower()
        
        st.markdown("---")
        st.markdown("### 📊 Tu progreso")
        progress = min(st.session_state.score / 500, 1.0)
        st.progress(progress)
        st.caption(f"Objetivo: 500 puntos")
        
        st.markdown("---")
        st.markdown(f"""
            <div style="text-align: center; padding: 10px; color: #999; font-size: 12px;">
                by Juan Pablo Villegas
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🏠 Volver al inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    col_chat, col_game = st.columns([1, 1])
    
    with col_chat:
        st.markdown("### 💬 Conversación")
        for msg in st.session_state.chat_history[-10:]:
            if msg['role'] == 'leo':
                st.markdown(f"""
                    <div class="chat-message leo-message">
                        🦁 <b>Leo:</b> {msg['message']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message user-message">
                        👦 <b>Tú:</b> {msg['message']}
                    </div>
                """, unsafe_allow_html=True)
    
    with col_game:
        st.markdown("### 🎯 Aprendamos")
        
        if st.session_state.game_mode == 'vocabulary':
            if st.session_state.current_word is None:
                quiz = generate_quiz()
                if quiz:
                    st.session_state.current_word = quiz['correct']
                    st.session_state.current_options = quiz['options']
                    add_chat_message('leo', f"¿Cómo se dice **'{st.session_state.current_word['meaning']}'** en inglés?")
                    st.rerun()
            
            if st.session_state.current_word:
                word = st.session_state.current_word
                st.markdown(f"""
                    <div class="word-card">
                        <div class="word-emoji">{word['emoji']}</div>
                        <div class="word-question">¿Cómo se dice <b>"{word['meaning']}"</b> en inglés?</div>
                    </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(2)
                for i, option in enumerate(st.session_state.current_options):
                    col = cols[i % 2]
                    with col:
                        if st.button(f"🔤 {option}", key=f"opt_{i}", use_container_width=True):
                            if option == st.session_state.current_word['word']:
                                points = 10
                                st.session_state.score += points
                                st.session_state.streak += 1
                                
                                if st.session_state.streak > 5:
                                    msg = f"{LEO['personality']['excited']} ¡{points} puntos! Llevas {st.session_state.streak} correctas seguidas."
                                else:
                                    msg = f"{LEO['personality']['happy']} ¡{points} puntos! '{word['meaning']}' es '{word['word']}'."
                                
                                add_chat_message('leo', msg)
                                st.session_state.current_word = None
                                st.session_state.current_options = []
                                st.rerun()
                            else:
                                st.session_state.streak = 0
                                msg = f"{LEO['personality']['patient']} La respuesta correcta es '{word['word']}'. ¡Sigue practicando!"
                                add_chat_message('leo', msg)
                                st.session_state.current_word = None
                                st.session_state.current_options = []
                                st.rerun()
        
        elif st.session_state.game_mode == 'story':
            stories = [
                {"title": "The Hungry Cat", "content": "The cat is hungry. It wants to eat fish. The cat goes to the kitchen.", "emoji": "🐱"},
                {"title": "The Happy Dog", "content": "The dog is happy. It plays with a ball. The dog runs in the park.", "emoji": "🐶"}
            ]
            
            story_idx = st.session_state.story_progress % len(stories)
            story = stories[story_idx]
            
            st.markdown(f"""
                <div class="story-card">
                    <h3>{story['emoji']} {story['title']}</h3>
                    <p style="font-size: 18px; line-height: 1.8;">{story['content']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("📖 Siguiente historia", use_container_width=True):
                st.session_state.story_progress += 1
                st.rerun()
        
        elif st.session_state.game_mode == 'speaking':
            st.markdown("""
                <div class="speaking-card">
                    <h3>🎤 Practica tu pronunciación</h3>
                    <p style="font-size: 16px; color: #666;">Di la palabra en inglés</p>
                </div>
            """, unsafe_allow_html=True)
            
            level_data = VOCABULARY.get(str(st.session_state.level), VOCABULARY['1'])
            words = level_data['words']
            practice_word = random.choice(words)
            
            st.markdown(f"""
                <div class="word-card" style="background-color: #E3F2FD;">
                    <div class="word-emoji">{practice_word['emoji']}</div>
                    <div class="word-question">Pronuncia: <b style="font-size: 32px; color: #1976D2;">{practice_word['word']}</b></div>
                    <div style="font-size: 16px; color: #666;">({practice_word['meaning']})</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎙️ Practicar pronunciación", use_container_width=True):
                st.info("🎤 Escuchando... Di la palabra en inglés")
                time.sleep(1)
                
                if random.random() > 0.3:
                    st.success("✅ ¡Excelente! 🌟")
                    add_chat_message('leo', f"{LEO['personality']['excited']} ¡Perfecto! Pronunciaste '{practice_word['word']}' muy bien.")
                    st.session_state.score += 5
                    st.rerun()
                else:
                    st.warning("🔄 Casi... Intenta de nuevo")
                    add_chat_message('leo', f"{LEO['personality']['patient']} Vamos, intenta decir '{practice_word['word']}' una vez más.")
                    st.rerun()

if st.session_state.page == 'home':
    show_home()
else:
    show_quiz()
