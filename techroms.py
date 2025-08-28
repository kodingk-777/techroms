import difflib

stories = [
    "You and T/N are competing leads on rival AI research teams. Your lab is focused on explainable AI, theirs on sheer computational power. Every conference panel turns into a duel of words. When your organizations are forced into a merger, you’re suddenly co-authors on the same paper, forced to share datasets, coffee, and grudging respect. The long nights debugging neural networks blur into something warmer.",

    "You and T/N met at a local hackathon years ago, cobbling together apps over pizza and bad Wi-Fi. Over time, you’ve been the go-to pair for late-night coding jams and debugging marathons. Now, you’re both finalists in a global XR competition. As you pull all-nighters polishing your demo, you realize the spark in T/N’s smile isn’t just the monitor glow—it’s been there all along.",

    "At a tiny startup trying to revolutionize quantum cloud computing, you and T/N are the only ones who stay past midnight. You handle code optimization, they handle system architecture. The office is dark, except for humming servers and the quiet beat of music from T/N’s headphones. When a crisis threatens to tank the company’s big demo, you two pull together—and discover the chemistry isn’t only professional.",

    "You and T/N meet inside a VR collaboration platform—both working remotely on a museum’s immersive exhibit. At first, T/N is just an avatar with a glitchy mic and a sharp wit. Weeks in, you realize you don’t even know what they look like. The first time you meet in person—at the exhibit’s grand opening—it feels like stepping into an augmented reality that was waiting all along.",

    "You and T/N dated in grad school but broke apart when your ambitions clashed. Years later, fate throws you together at a major corporation, where your teams are forced to collaborate on a patent for next-gen neural implants. The old tension crackles. But as the project nears completion, you both realize the future you’re building isn’t just technological—it could be personal too.",

    "You and T/N have been contributors on the same open source AI library for years, chatting only through comments and pull requests. Eventually, you become maintainers together. As you write documentation and troubleshoot user issues side by side, you realize the bond is deeper than shared code. The first time you video call to plan the next release, there’s an undeniable warmth in the way T/N says your name.",

    "You and T/N are two of the engineers sent on a mission to establish communication systems on Mars. A sudden solar storm damages the base, cutting you off from Earth. With only each other, your skills, and the failing hardware, you have to jury-rig a solution. In the claustrophobic habitat, the line between survival partnership and something more intimate begins to blur.",

    "Your company builds cutting-edge AR hardware. T/N’s company builds the software layer. Historically, you’ve been fierce competitors, mocking each other at tech expos. Now, after a billion-dollar merger, you’re co-heads of innovation. Neither of you is happy. But as prototypes fail and deadlines loom, the bickering turns into brainstorming, and the sparks turn into fire.",

    "You’re a senior researcher in AI ethics; T/N is your colleague’s brilliant intern. You promise yourself you’ll keep it professional. But as you coach T/N through drafting their first publication and hear their ideas reshaping your own, the boundaries weaken. The lab whispers about your late-night brainstorming sessions, but what they don’t know is how much you already struggle to keep your feelings in check.",

    "You and T/N both work at different corporations, but secretly you’re co-founders of a stealth startup tackling the holy grail of brain-computer interfaces. To the outside world, you’re competitors. To each other, you’re partners—sharing clandestine cafés, burner laptops, and late-night Slack calls. The thrill of invention mixes with the thrill of secrecy, and somewhere in the mess of prototypes, you realize you’ve built more than just tech together."
]

# Map each canonical trope to its story index
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

# Accepted aliases (all compared in lowercase via .casefold())
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
    # Exact/alias match
    for canon, names in aliases.items():
        if s in names:
            return canon, stories[tropes[canon]]
    # Fuzzy fallback on canonical keys (helps with minor typos)
    match = difflib.get_close_matches(s, tropes.keys(), n=1, cutoff=0.7)
    if match:
        canon = match[0]
        return canon, stories[tropes[canon]]
    return None, None

prompt = (
    "Pick a trope:\n"
    + ", ".join(title.title() for title in tropes.keys())
    + "\n> "
)

user_input = input(prompt)
canon, story = pick_story(user_input)

if story:
    print(f"\n[{canon.title()}]\n{story}")
else:
    print("Didn’t catch that. Try one of these exactly or an alias:\n- " +
          "\n- ".join(canon.title() + " → " + ", ".join(sorted(list(names))[:3]) + ("…" if len(names) > 3 else "")
                     for canon, names in aliases.items()))
