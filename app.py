import streamlit as st
import os
import html
from groq import Groq
from dotenv import load_dotenv

# ── Config (must be first Streamlit call) ────────────────────────────────────
st.set_page_config(
    page_title="Pitch Engine — AI Copy Studio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# ── Session state ─────────────────────────────────────────────────────────────
if "pitch_history" not in st.session_state:
    st.session_state.pitch_history = []
if "last_output" not in st.session_state:
    st.session_state.last_output = None

# ── Luxury CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
  --gold:        #c9a84c;
  --gold-bright: #e8c96a;
  --gold-dim:    #7a621e;
  --gold-glow:   rgba(201,168,76,0.18);
  --bg:          #080810;
  --surface:     rgba(255,255,255,0.028);
  --surface-h:   rgba(255,255,255,0.045);
  --border:      rgba(201,168,76,0.22);
  --border-h:    rgba(201,168,76,0.5);
  --text:        #e2ddd4;
  --text-dim:    #6e6a62;
  --text-mid:    #a09a90;
}

/* ── Global reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
  background: var(--bg) !important;
  font-family: 'DM Sans', sans-serif;
  color: var(--text);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
  padding: 0 2.5rem 4rem !important;
  max-width: 1280px !important;
}

/* ── Subtle star/grain overlay ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(1px 1px at 20% 30%, rgba(201,168,76,0.25) 0%, transparent 100%),
    radial-gradient(1px 1px at 75% 15%, rgba(255,255,255,0.12) 0%, transparent 100%),
    radial-gradient(1px 1px at 50% 70%, rgba(201,168,76,0.15) 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 55%, rgba(255,255,255,0.08) 0%, transparent 100%),
    radial-gradient(1px 1px at 10% 85%, rgba(201,168,76,0.12) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
}

/* ── Gold ambient glow top ── */
.stApp::after {
  content: '';
  position: fixed;
  top: -200px; left: 50%;
  transform: translateX(-50%);
  width: 900px; height: 400px;
  background: radial-gradient(ellipse, rgba(201,168,76,0.08) 0%, transparent 65%);
  pointer-events: none;
  z-index: 0;
}

/* ── Hero header ── */
.hero {
  text-align: center;
  padding: 3.5rem 1rem 2.5rem;
  position: relative;
  z-index: 1;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg,rgba(201,168,76,0.12),rgba(201,168,76,0.04));
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 0.35rem 1.1rem;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 1.4rem;
}
.hero-eyebrow::before, .hero-eyebrow::after {
  content: '✦';
  font-size: 0.55rem;
  opacity: 0.7;
}
.hero h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3rem, 6vw, 5.5rem);
  font-weight: 700;
  line-height: 1.05;
  margin: 0 0 1.2rem;
  background: linear-gradient(
    130deg,
    #e8c96a 0%,
    #c9a84c 25%,
    #f5e6b0 50%,
    #c9a84c 75%,
    #e8c96a 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: goldShimmer 5s linear infinite;
}
@keyframes goldShimmer {
  0%   { background-position: 0% center; }
  100% { background-position: 200% center; }
}
.hero p {
  color: var(--text-mid);
  font-size: 1.05rem;
  font-weight: 300;
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.75;
  letter-spacing: 0.01em;
}

/* ── Decorative rule ── */
.gold-rule {
  position: relative;
  height: 1px;
  margin: 0.5rem 0 2.5rem;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--gold-dim) 20%,
    var(--gold) 50%,
    var(--gold-dim) 80%,
    transparent 100%
  );
  opacity: 0.45;
}
.gold-rule::before {
  content: '◆';
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg);
  color: var(--gold);
  font-size: 0.6rem;
  padding: 0 0.5rem;
  opacity: 0.8;
}

/* ── Section labels ── */
.section-label {
  font-size: 0.67rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

/* ── Inputs ── */
.stTextInput label,
.stSelectbox label {
  color: var(--text-dim) !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input {
  background: rgba(201,168,76,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.92rem !important;
  padding: 0.65rem 1rem !important;
  transition: border-color 0.25s, box-shadow 0.25s;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important;
  outline: none !important;
}
.stTextInput > div > div > input::placeholder {
  color: var(--text-dim) !important;
  font-style: italic;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: rgba(201,168,76,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox > div > div:hover {
  border-color: var(--border-h) !important;
}
[data-baseweb="popover"] {
  background: #0f0f1a !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-baseweb="menu"] {
  background: #0f0f1a !important;
}
[role="option"] {
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
  background: transparent !important;
}
[role="option"]:hover,
[aria-selected="true"] {
  background: var(--gold-glow) !important;
  color: var(--gold-bright) !important;
}

/* ── Generate button ── */
.stButton > button[kind="primary"],
.stButton > button {
  width: 100% !important;
  background: linear-gradient(135deg, #c9a84c, #e8c96a, #a8892e) !important;
  background-size: 200% auto !important;
  color: #08080e !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.8rem 2rem !important;
  cursor: pointer !important;
  transition: background-position 0.4s ease, box-shadow 0.3s, transform 0.2s !important;
  box-shadow: 0 4px 20px rgba(201,168,76,0.28), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.stButton > button:hover {
  background-position: right center !important;
  box-shadow: 0 6px 30px rgba(201,168,76,0.45), inset 0 1px 0 rgba(255,255,255,0.25) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
}

/* ── Output result area ── */
.result-wrap {
  position: relative;
  margin-top: 1.5rem;
  border-radius: 16px;
  border: 1px solid rgba(201,168,76,0.35);
  background: linear-gradient(160deg, rgba(201,168,76,0.05) 0%, rgba(0,0,0,0) 60%);
  overflow: hidden;
  animation: fadeSlideUp 0.45s ease;
}
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.result-wrap::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.75rem 0;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.result-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--gold-bright);
  letter-spacing: 0.03em;
}
.result-pills {
  display: flex;
  gap: 0.6rem;
}
.result-pill {
  background: rgba(201,168,76,0.1);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 100px;
  padding: 0.2rem 0.75rem;
  font-size: 0.72rem;
  color: var(--gold);
  font-weight: 500;
  letter-spacing: 0.04em;
}
.result-body {
  padding: 1.25rem 1.75rem 1.75rem;
  color: #ccc9c0;
  font-size: 0.92rem;
  line-height: 1.9;
  font-weight: 300;
  white-space: pre-wrap;
}

/* ── History panel ── */
.hist-empty {
  border: 1px dashed rgba(201,168,76,0.18);
  border-radius: 14px;
  padding: 2.5rem 1.5rem;
  text-align: center;
  color: var(--text-dim);
  font-size: 0.85rem;
  line-height: 1.7;
}
.hist-empty-icon {
  font-size: 1.8rem;
  margin-bottom: 0.75rem;
  opacity: 0.35;
}

/* ── Streamlit expanders ── */
.streamlit-expanderHeader {
  background: rgba(201,168,76,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.85rem !important;
  padding: 0.75rem 1rem !important;
  transition: background 0.2s, border-color 0.2s !important;
}
.streamlit-expanderHeader:hover {
  background: var(--gold-glow) !important;
  border-color: var(--border-h) !important;
}
.streamlit-expanderContent {
  border: 1px solid var(--border) !important;
  border-top: none !important;
  border-radius: 0 0 10px 10px !important;
  background: rgba(0,0,0,0.2) !important;
  padding: 1rem !important;
}

/* ── Alerts ── */
.stAlert {
  border-radius: 10px !important;
  border: none !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }

/* ── Code block (copy area) ── */
.stCodeBlock {
  background: rgba(201,168,76,0.03) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

/* ── Columns gap fix ── */
[data-testid="stHorizontalBlock"] {
  align-items: flex-start;
  gap: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Tone instruction map ──────────────────────────────────────────────────────
TONES = {
    "Luxury / Premium": (
        "Write in an ultra-sophisticated, exclusive tone. Use elevated, precise language "
        "that radiates prestige and signals high-end expertise. Make the reader feel they "
        "are accessing something rare, and that working with this person is an investment "
        "in excellence, not an expense."
    ),
    "Professional & Formal": (
        "Write in a polished, formal business tone. Be authoritative, precise, and credible. "
        "Maintain gravity and professionalism throughout."
    ),
    "Bold & Confident": (
        "Write with raw confidence and direct energy. Be punchy, assertive, and make "
        "powerful claims grounded in value. No hedging, no fluff."
    ),
    "Friendly & Casual": (
        "Write in a warm, approachable, conversational tone. Sound like a knowledgeable "
        "friend who genuinely wants to help, not a corporate pitch machine."
    ),
}

# ── Content types ─────────────────────────────────────────────────────────────
CONTENT_TYPES = [
    "Cold Email",
    "Professional Bio",
    "Instagram Carousel Script",
    "LinkedIn Post",
    "Client Proposal / Quote Letter",
    "Elevator Pitch Script",
    "Testimonial Request Email",
]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI Copy Studio</div>
    <h1>The Freelance<br>Pitch Engine</h1>
    <p>Generate premium copy that positions you as the elite choice — and moves clients to act.</p>
</div>
<div class="gold-rule"></div>
""", unsafe_allow_html=True)


# ── Two-column layout ─────────────────────────────────────────────────────────
col_form, col_hist = st.columns([1.65, 1], gap="large")


# ════════════════════════════════ LEFT: FORM ══════════════════════════════════
with col_form:
    st.markdown('<div class="section-label">✦ &nbsp; Craft Your Pitch</div>', unsafe_allow_html=True)

    service_offered = st.text_input(
        "Service You're Offering",
        placeholder="e.g., Brand Identity Design, 4K Drone Videography, SEO Copywriting",
    )

    target_client = st.text_input(
        "Your Target Client",
        placeholder="e.g., Luxury Real Estate Agencies in Mumbai",
    )

    col_type, col_tone = st.columns(2)
    with col_type:
        task_type = st.selectbox("Content Type", CONTENT_TYPES)
    with col_tone:
        tone = st.selectbox("Tone", list(TONES.keys()))

    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("✦  Generate Pitch Copy")

    # ── Generate logic ────────────────────────────────────────────────────────
    if generate_clicked:
        if not service_offered.strip() or not target_client.strip():
            st.warning("Please fill in your service and target client before generating.")
        else:
            with st.spinner("Crafting premium copy…"):
                system_prompt = (
                    "You are an elite freelance copywriter specialising in premium personal branding "
                    "and business development for creative and digital service professionals.\n"
                    f"Tone directive: {TONES[tone]}\n"
                    "Your copy must be specific, persuasive, and ready to use — never generic filler. "
                    "Obsess over the concrete value the client receives, not just the features of the service. "
                    "Every sentence must earn its place."
                )

                content_type_extras = {
                    "Cold Email": "Include: compelling subject line, strong opening hook, concise body, clear CTA, professional sign-off.",
                    "Professional Bio": "Include: third-person voice, opening headline, expertise, credibility markers, unique value prop, closing statement.",
                    "Instagram Carousel Script": "Include: slide 1 hook, 5–7 body slides with punchy single insights, CTA slide. Format: 'Slide N: [text]'.",
                    "LinkedIn Post": "Include: scroll-stopping first line, value-packed body (no walls of text), strategic line breaks, CTA and 3–5 hashtags.",
                    "Client Proposal / Quote Letter": "Include: project understanding, proposed approach, deliverables list, timeline, pricing section placeholder, next steps.",
                    "Elevator Pitch Script": "Include: 60-second spoken script, hook, who you help, what you do, the result you deliver, memorable close.",
                    "Testimonial Request Email": "Include: warm personal opening, specific project reference, clear ask, two guiding questions to make it easy, grateful close.",
                }

                user_prompt = (
                    f"Write a {task_type} for a freelancer offering \"{service_offered}\" "
                    f"to \"{target_client}\".\n\n"
                    f"Requirements: {content_type_extras.get(task_type, '')}\n"
                    "Make it compelling and completely ready to send, post, or deliver."
                )

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": user_prompt},
                    ],
                    temperature=0.75,
                )

                generated = completion.choices[0].message.content
                word_count = len(generated.split())
                read_time  = max(1, round(word_count / 200))

                # Save to history
                st.session_state.pitch_history.append({
                    "type":    task_type,
                    "service": service_offered,
                    "client":  target_client,
                    "tone":    tone,
                    "content": generated,
                    "words":   word_count,
                })
                st.session_state.last_output = {
                    "type":    task_type,
                    "words":   word_count,
                    "read":    read_time,
                    "content": generated,
                }

    # ── Display last output ───────────────────────────────────────────────────
    if st.session_state.last_output:
        out = st.session_state.last_output
        safe_text = html.escape(out["content"])

        st.markdown(f"""
        <div class="result-wrap">
          <div class="result-header">
            <div class="result-title">✦ {out['type']}</div>
            <div class="result-pills">
              <span class="result-pill">📝 {out['words']} words</span>
              <span class="result-pill">⏱ {out['read']} min read</span>
            </div>
          </div>
          <div class="result-body">{safe_text}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 &nbsp; Copy-Ready Text (click to expand → select all → copy)"):
            st.code(out["content"], language=None)


# ═══════════════════════════════ RIGHT: HISTORY ═══════════════════════════════
with col_hist:
    st.markdown('<div class="section-label">✦ &nbsp; Pitch Archive</div>', unsafe_allow_html=True)

    if not st.session_state.pitch_history:
        st.markdown("""
        <div class="hist-empty">
          <div class="hist-empty-icon">🗂</div>
          Your generated pitches will be archived here.<br>
          Start generating to build your collection.
        </div>
        """, unsafe_allow_html=True)
    else:
        # newest first
        for i, item in enumerate(reversed(st.session_state.pitch_history)):
            label = f"{'📧' if 'Email' in item['type'] else '📄'} {item['type']}  ·  {item['service'][:22]}{'…' if len(item['service'])>22 else ''}"
            with st.expander(label, expanded=(i == 0)):
                st.markdown(f"""
                <div style="margin-bottom:0.9rem; display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center;">
                  <span style="font-size:0.72rem;color:var(--text-dim);">🎯</span>
                  <span style="font-size:0.82rem;color:#ccc;">{html.escape(item['client'])}</span>
                  <span style="font-size:0.7rem;background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.2);
                        border-radius:100px;padding:0.15rem 0.6rem;color:var(--gold);">
                    {item['tone']}
                  </span>
                  <span style="font-size:0.72rem;color:var(--text-dim);">{item['words']} words</span>
                </div>
                <div style="font-size:0.83rem;color:#aaa;line-height:1.75;white-space:pre-wrap;">
                {html.escape(item['content'][:380])}{'…' if len(item['content'])>380 else ''}
                </div>
                """, unsafe_allow_html=True)

                real_idx = len(st.session_state.pitch_history) - 1 - i
                with st.expander("   Show full text"):
                    st.code(item["content"], language=None)
                    # ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 2rem 0 1rem;
    color: #6e6a62;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
">
    <span style="color: rgba(201,168,76,0.4);">✦</span>
    &nbsp; Crafted & Powered by
    <span style="color: #c9a84c; font-weight: 600;">Sushant Thombare</span>
    &nbsp; <span style="color: rgba(201,168,76,0.4);">✦</span>
</div>
""", unsafe_allow_html=True)