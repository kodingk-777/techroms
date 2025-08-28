import streamlit as st
import difflib
import random
from io import StringIO

# ---------- Page + Styling ----------
st.set_page_config(page_title="Tech Trope Romance Generator", page_icon="💘", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=JetBrains+Mono:wght@400;600&family=Share+Tech+Mono&display=swap');

:root {
    --pink: #ffd9ea;          /* light pink */
    --pink-strong: #ffb8d5;   /* accent pink */
    --ink: #1a1a1a;
}

.stApp {
    background: linear-gradient(180deg, #fffafd 0%, #fff5fb 100%);
    color: var(--ink);
    font-family: 'IBM Plex Mono','JetBrains Mono','Share Tech Mono', monospace;
}

h1, h2, h3 {
    font-family: 'Share Tech Mono','IBM Plex Mono', monospace;
    letter-spacing: 0.4px;
}

.sidebar .sidebar-content {
    background: #fff7fb !important;
}

.pink-accent {
    border-left: 4px solid var(--pink-strong);
    background: #fff7fb;
    border-radius: 12px;
    padding: 14px 16px;
}

.stButton>button, .stDownloadButton>button {
    border-radius: 14px;
    border: 1px solid var(--pink-strong);
    background: var(--pink);
    color: #3a2a35;
    box-shadow: 0 4px 18px rgba(255, 184, 213, 0.45);
    transition: all 0.15s ease;
    font-weight: 600;
}

.stButton>button:hover, .stDownloadButton>button:hover {
    border-color: #ff8ab8;
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(255, 138, 184, 0.55);
}

textarea, .stTextInput>div>div>input, .stSelectbox [data-baseweb="select"] > div {
    font-family: 'JetBrains Mono', monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
stories = [
    """You and T/N are competing leads on rival AI research teams. Your lab is focused on explainable AI, theirs on sheer computational power. Every conference panel turns into a duel of words. When your organizations are forced into a merger, you’re suddenly co-authors on the same paper, forced to share datasets, coffee, and grudging respect. The long nights debugging neural networks blur into something warmer.""",

    """You and T/N met at a local hackathon years ago, cobbling together apps over pizza and bad Wi-Fi. Over time, you’ve been the go-to pair for late-night coding jams and debugging marathons. Now, you’re both finalists in a global XR competition. As you pull all-nighters polishing your demo, you realize the spark in T/N’s smile isn’t just the monitor glow—it’s been there all along.""",

    """At a tiny startup trying to revolutionize quantum cloud computing, you and T/N are the only ones who stay past midnight. You handle code optimization, they handle system architecture. The office is dark, except for humming servers and the quiet beat of music from T/N’s headphones. When a crisis threatens to tank the company’s big demo, you two pull together—and discover the chemistry isn’t only professional.""",

    """You and T/N meet inside a VR collaboration platform—both working remotely on a museum’s immersive exhibit. At first, T/N is just an avatar with a glitchy mic and a sharp wit. Weeks in, you realize you don’t even know what they look like. The first time you meet in person—at the exhibit’s grand opening—it feels like stepping into an augmented reality that was waiting all along.""",

    """You and T/N dated in grad school but broke apart when your ambitions clashed. Years later, fate throws you together at a major corporation, where your teams are forced to collaborate on a patent for next-gen neural implants. The old tension crackles. But as the project nears completion, you both realize the future you’re building isn’t just technological—it could be personal too.""",

    """You and T/N have been contributors on the same open source AI library for years, chatting only through comments and pull requests. Eventually, you become maintainers together. As you write documentation and troubleshoot user issues side by side, you realize the bond is deeper than shared code. The first time you video call to plan the next release, there’s an undeniable warmth in the way T/N says your name.""",

    """You and T/N are two of the engineers sent on a mission to establish communication systems on Mars. A sudden solar storm damages the base, cutting you off from Earth. With only each other, your skills, and the failing hardware, you have to jury-rig a solution. In the claustrophobic habitat, the line between survival partnership and something more intimate begins to blur.""",

    """Your company builds cutting-edge AR hardware. T/N’s company builds the software layer. Historically, you’ve been fierce competitors, mocking each other at tech expos. Now, after a billion-dollar merger, you’re co-heads of innovation. Neither of you is happy. But as prototypes fail and deadlines loom, the bickering turns into brainstorming, and the sparks turn into fire.""",

    """You’re a senior researcher in AI ethics; T/N is your colleague’s brilliant intern. You promise yourself you’ll keep it professional. But as you coach T/N through drafting their first publication and hear their ideas reshaping your own, the boundaries weaken. The lab whispers about your late-night brainstorming sessions, but what they don’t know is how much you already struggle to keep your feelings in check.""",

    """You and T/N both work at different corporations, but secretly you’re co-founders of a stealth startup tackling the holy grail of brain-computer interfaces. To the outside world, you’re competitors. To each other, you’re partners—sharing clandestine cafés, burner laptops, and late-night Slack calls. The thrill of invention mixes with the thrill of secrecy, and somewhere in the mess of prototypes, you realize you’ve built more than just tech together."""
]

tropes = {
    "enemies to lovers": 0,
    "friends to lovers": 1,
    "colleagues to lovers": 2,
    "strangers to lovers": 3,
    "second chances": 4,
    "slow burn": 5,
    "forced proximity": 6,
    "enemies to lovers (corporate edition)": 7,
    "forbidden romance": 8,
    "secret romance": 9,
}

aliases = {
    "enemies to lovers": {
        "enemies to lovers", "enemies 2 lovers", "enemies→lovers",
        "enemies -> lovers", "e2l", "enemies"
    },
    "friends to lovers": {"friends to lovers", "friends 2 lovers", "f2l", "friends"},
    "colleagues to lovers": {"colleagues to lovers", "coworkers to lovers", "office romance", "colleagues"},
    "strangers to lovers": {"strangers to lovers", "blind meet", "meet-cute", "strangers"},
    "second chances": {"second chances", "second chance", "exes", "rekindle"},
    "slow burn": {"slow burn", "long burn", "slowburn"},
    "forced proximity": {"forced proximity", "stuck together", "one room"},
    "enemies to lovers (corporate edition)": {
        "enemies to lovers (corporate edition)", "corporate enemies to lovers",
        "corporate rivals", "xr merger", "corporate edition"
    },
    "forbidden romance": {"forbidden romance", "off-limits", "taboo"},
    "secret romance": {"secret romance", "secret", "hidden", "covert"},
}

def pick_story(user_text: str):
    s = user_text.strip().casefold()
    for canon, names in aliases.items():
        if s in names:
            return canon, stories[tropes[canon]]
    match = difflib.get_close_matches(s, list(tropes.keys()), n=1, cutoff=0.7)
    if match:
        canon = match[0]
        return canon, stories[tropes[canon]]
    return None, None

def personalize(text: str, y_name: str, t_name: str):
    s = text
    if t_name:
        s = s.replace("T/N", t_name)
    # Light-touch Y/N replacement: only leading "You " or "You and "
    if y_name:
        if s.startswith("You and "):
            s = s.replace("You and ", f"{y_name} and ", 1)
        elif s.startswith("You "):
            s = s.replace("You ", f"{y_name} ", 1)
    return s

# ---------- UI ----------
st.title("Tech Trope Romance Generator 💘")
st.caption("Case-insensitive, alias-friendly.")

col1, col2 = st.columns([2,1])
with col1:
    choice = st.selectbox(
        "Choose a trope",
        list(tropes.keys()) + ["surprise me", "type my own"],
        index=0
    )
with col2:
    st.write("")  # spacing
    st.write("")

user_free = ""
if choice == "type my own":
    user_free = st.text_input("Type any trope/alias (e.g., 'e2l', 'office romance')", "")
elif choice == "surprise me":
    pass

with st.expander("Personalize (optional)"):
    y_name = st.text_input("Y/N (your name) – optional", "")
    t_name = st.text_input("T/N (their name) – optional", "")

gen = st.button("Generate 💾")

# ---------- Logic ----------
if gen:
    if choice == "surprise me":
        canon = random.choice(list(tropes.keys()))
        story = stories[tropes[canon]]
    else:
        text_in = user_free if choice == "type my own" else choice
        canon, story = pick_story(text_in)
        if not story:
            st.error("Didn’t catch that trope. Try a canonical name or a known alias (e.g., 'e2l', 'office romance').")
            st.stop()

    story_out = personalize(story, y_name.strip(), t_name.strip())
    st.subheader(canon.title())
    st.markdown(f"<div class='pink-accent'>{story_out}</div>", unsafe_allow_html=True)

    # Download
       # Download as PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, canon.title())

    # Story body (wrap to lines)
    from textwrap import wrap
    c.setFont("Helvetica", 11)
    y = height - 100
    for line in wrap(story_out, 90):  # 90 chars wide
        c.drawString(72, y, line)
        y -= 14
        if y < 72:  # new page if we hit bottom
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 72

    c.save()
    pdf_buffer.seek(0)

    st.download_button(
        "Download Story (.pdf)",
        data=pdf_buffer,
        file_name=f"{canon.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

    )
