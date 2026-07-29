# 🦁 English Adventure with Leo

### by Juan Pablo Villegas

Una app educativa interactiva para que niños de 5 a 11 años aprendan inglés jugando.

---

## 🎯 Características

- 🎮 Aprendizaje basado en juegos
- 🦁 Personaje guía amigable (Leo)
- 🏆 Sistema de puntos y rachas
- 📚 5 niveles de vocabulario
- 💬 Interacción conversacional
- 🎤 Práctica de pronunciación con reconocimiento de voz real
- 📖 Historias interactivas por nivel
- 💾 Progreso guardado por jugador (SQLite)

---

## 🚀 Cómo ejecutar

1. Instala las dependencias: `pip install -r requirements.txt`
2. Ejecuta la app: `streamlit run app.py`

---

## 📁 Estructura

```
app.py               # App principal (Streamlit)
database.py          # Persistencia de progreso (SQLite)
voice.py             # Reconocimiento de voz (micrófono + Google Speech)
data/vocabulary.json # Vocabulario por nivel (1-5)
data/stories.json    # Historias por nivel (1-5)
```

---

## 👨‍💻 Autor

**Juan Pablo Villegas**

Proyecto creado en Colombia 🇨🇴
