# 💼 Copy Studio AI — The Freelance Pitch Engine

> **Generate premium freelance copy that positions you as the elite choice — and moves clients to act.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-copystudioai.streamlit.app-gold?style=for-the-badge)](https://copystudioai.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-deployed-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Groq API](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=for-the-badge)](https://groq.com)

---

## 🎯 What It Does

Copy Studio AI is an AI-powered pitch engine built for freelancers. You enter your service and your target client — and the app generates ready-to-use professional copy in seconds, powered by **LLaMA 3.3 70B via Groq API**.

No more staring at a blank screen before sending a cold email or writing your bio.

---

## ✨ Features

- **7 Content Types** — Cold Email, Professional Bio, LinkedIn Post, Instagram Carousel Script, Client Proposal, Elevator Pitch, Testimonial Request
- **4 Tone Modes** — Luxury/Premium, Professional & Formal, Bold & Confident, Friendly & Casual
- **Pitch Archive** — All generated pitches saved in-session for easy reference
- **Copy-Ready Output** — Expandable code block for easy select-all copy
- **Session Rate Limiting** — 10 pitches per session with a visual progress bar
- **Google Analytics** — Built-in usage tracking
- **Luxury Dark UI** — Custom-styled with gold accents, Cormorant Garamond typography, and smooth animations

---

## 🖥️ Live Demo

👉 **[copystudioai.streamlit.app](https://copystudioai.streamlit.app/)**

![Copy Studio AI Screenshot](<img width="1178" height="730" alt="image" src="https://github.com/user-attachments/assets/9bdbc476-e30f-47e7-a2e5-f059e0366dbe" />
)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| AI Model | LLaMA 3.3 70B Versatile |
| AI API | Groq (free tier) |
| Styling | Custom CSS (dark luxury theme) |
| Analytics | Google Analytics (GA4) |
| Deployment | Streamlit Cloud |

---

## 🚀 Run It Locally

### 1. Clone the repo
```bash
git clone https://github.com/sushanttt-dev/agency-agent.git
cd agency-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
agency-agent/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignores .env and other sensitive files
└── README.md           # You're reading it!
```

---

## 💡 How to Use

1. Enter the **service you're offering** (e.g. "Brand Identity Design")
2. Enter your **target client** (e.g. "Luxury Real Estate Agencies in Mumbai")
3. Choose a **content type** (Cold Email, LinkedIn Post, etc.)
4. Choose your **tone** (Luxury, Bold, Friendly, etc.)
5. Click **Generate Pitch Copy**
6. Copy your result and send it 🚀

---

## ⚙️ Configuration

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (required) |
| `MAX_CHARS` | Max characters per input field (default: 300) |
| `SESSION_LIMIT` | Max pitches per session (default: 10) |

---

## 🔒 Security Notes

- API key is loaded via `.env` (never hardcoded)
- `.env` is listed in `.gitignore` — your key stays private
- Session limiting prevents API abuse

---

## 👨‍💻 Built By

**Sushant Thombare** — 15 y/o builder from India 🇮🇳  
Aspiring Software Engineer | Python & AI Enthusiast  

[![GitHub](https://img.shields.io/badge/GitHub-sushanttt--dev-black?style=flat&logo=github)](https://github.com/sushanttt-dev)

---

## 📄 License

This project is open source. Feel free to fork and build on it!
