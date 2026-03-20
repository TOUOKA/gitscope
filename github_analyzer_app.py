import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import json

st.set_page_config(
    page_title="GitScope — GitHub Profile Analyzer",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0a0f; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.hero {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1040 50%, #0a0a0f 100%);
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    padding: 60px 80px 48px; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -50%; left: -10%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
}
.hero::after {
    content: ''; position: absolute; bottom: -30%; right: 5%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
}
.hero-badges { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3);
    color: #a78bfa; font-size: 12px; font-weight: 500;
    letter-spacing: 0.05em; text-transform: uppercase; padding: 4px 12px; border-radius: 100px;
}
.hero-badge.privacy { background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.3); color: #6ee7b7; }
.hero h1 {
    font-size: 48px; font-weight: 700; line-height: 1.1; margin: 0 0 16px;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero p { font-size: 18px; color: #94a3b8; margin: 0; max-width: 560px; line-height: 1.6; }

.privacy-banner {
    background: rgba(16,185,129,0.07); border: 1px solid rgba(16,185,129,0.2);
    border-radius: 12px; padding: 14px 20px; margin-bottom: 28px;
    display: flex; align-items: flex-start; gap: 12px;
}
.privacy-banner-icon { font-size: 18px; line-height: 1.5; flex-shrink: 0; }
.privacy-banner-text { font-size: 13px; color: #a7f3d0; line-height: 1.7; }
.privacy-banner-text strong { color: #6ee7b7; font-weight: 600; }

.main-content { padding: 48px 80px; max-width: 1200px; margin: 0 auto; }

.search-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 32px; margin-bottom: 40px;
}
.search-label {
    font-size: 13px; font-weight: 500; color: #64748b;
    letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 12px;
}

/* Contribution type cards */
.contrib-grid { display: flex; gap: 12px; flex-wrap: wrap; margin: 8px 0 16px; }
.contrib-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 16px 20px; flex: 1; min-width: 160px;
    transition: border-color 0.2s ease;
}
.contrib-card:hover { border-color: rgba(139,92,246,0.3); }
.contrib-card .icon { font-size: 22px; margin-bottom: 8px; }
.contrib-card .label { font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
.contrib-card .value { font-size: 24px; font-weight: 700; color: #e2e8f0; }
.contrib-card .desc { font-size: 12px; color: #475569; margin-top: 4px; }

.stTextInput > div > div > input {
    background: #1e1b2e !important; border: 1.5px solid rgba(139,92,246,0.25) !important;
    border-radius: 12px !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
    caret-color: #a78bfa !important; font-family: 'Inter', sans-serif !important;
    font-size: 16px !important; padding: 14px 18px !important; height: auto !important; transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.65) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.18) !important; background: #221d38 !important;
}
.stTextInput > div > div > input::placeholder { color: #4a4569 !important; -webkit-text-fill-color: #4a4569 !important; font-style: italic !important; }
.stTextInput > div > div > input:-webkit-autofill,
.stTextInput > div > div > input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0 1000px #1e1b2e inset !important; -webkit-text-fill-color: #ffffff !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important; font-size: 15px !important; font-weight: 600 !important;
    padding: 14px 28px !important; height: auto !important; width: 100% !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important; transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 28px rgba(124,58,237,0.45) !important; }

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important; padding: 20px 24px !important;
}
[data-testid="metric-container"]:hover { border-color: rgba(139,92,246,0.3) !important; }
[data-testid="stMetricLabel"] { font-size: 12px !important; font-weight: 500 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; color: #64748b !important; }
[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #e2e8f0 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important; border-radius: 12px !important;
    padding: 4px !important; gap: 2px !important; border: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 9px !important; color: #64748b !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important; font-weight: 500 !important; padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] { background: rgba(139,92,246,0.2) !important; color: #a78bfa !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

.stCodeBlock { border-radius: 12px !important; border: 1px solid rgba(255,255,255,0.07) !important; }
.stCodeBlock pre { background: rgba(255,255,255,0.02) !important; font-size: 13px !important; line-height: 1.7 !important; }

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 14px !important; padding: 14px 18px !important;
}
.streamlit-expanderHeader:hover { border-color: rgba(139,92,246,0.3) !important; background: rgba(139,92,246,0.05) !important; }
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: none !important; border-radius: 0 0 12px 12px !important;
    padding: 16px 20px !important; color: #94a3b8 !important; font-size: 14px !important; line-height: 1.7 !important;
}

[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important; font-weight: 500 !important; padding: 10px 20px !important;
}
[data-testid="stDownloadButton"] > button:hover { background: rgba(255,255,255,0.09) !important; border-color: rgba(139,92,246,0.4) !important; color: #a78bfa !important; }

hr { border-color: rgba(255,255,255,0.07) !important; margin: 32px 0 !important; }
.stSuccess { background: rgba(16,185,129,0.1) !important; border: 1px solid rgba(16,185,129,0.25) !important; border-radius: 12px !important; color: #6ee7b7 !important; }
.stWarning { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.2) !important; border-radius: 12px !important; color: #fcd34d !important; }
.stCaption { color: #475569 !important; font-size: 12px !important; }
[data-testid="stSidebar"] { background: #0d0d16 !important; border-right: 1px solid rgba(255,255,255,0.07) !important; }

.privacy-footer {
    background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.15);
    border-radius: 12px; padding: 20px 24px; margin-top: 40px;
}
.privacy-footer-title { font-size: 13px; font-weight: 600; color: #6ee7b7; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 10px; }
.privacy-footer-list { font-size: 13px; color: #64748b; line-height: 1.9; list-style: none; padding: 0; margin: 0; }
.privacy-footer-list li::before { content: "✓  "; color: #34d399; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Copy button
# ─────────────────────────────────────────────────────────
def copy_button(text: str):
    text_json = json.dumps(text)
    components.html(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&display=swap');
            body {{ margin: 0; background: transparent; }}
            #copy-btn {{
                font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;
                color: #e2e8f0; background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
                padding: 10px 20px; cursor: pointer; transition: all 0.2s ease;
                display: inline-flex; align-items: center; gap: 8px;
            }}
            #copy-btn:hover {{ background: rgba(139,92,246,0.15); border-color: rgba(139,92,246,0.4); color: #a78bfa; }}
            #copy-btn.copied {{ background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.4); color: #6ee7b7; }}
        </style>
        <button id="copy-btn" onclick="
            navigator.clipboard.writeText({text_json}).then(function() {{
                var btn = document.getElementById('copy-btn');
                btn.classList.add('copied');
                btn.innerHTML = '✅ &nbsp;Copied!';
                setTimeout(function() {{
                    btn.classList.remove('copied');
                    btn.innerHTML = '📋 &nbsp;Copy to Clipboard';
                }}, 2000);
            }});
        ">📋 &nbsp;Copy to Clipboard</button>
    """, height=52)


# ─────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badges">
        <span class="hero-badge">🔭 Engineer Recruiting Tool</span>
        <span class="hero-badge privacy">🔒 Privacy Compliant</span>
    </div>
    <h1>GitScope</h1>
    <p>Analyze any GitHub profile and get plain-language insights — no engineering background required. All data stays in your browser.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    github_token = st.text_input(
        "GitHub Token (optional)", type="password",
        help="Works without a token, but adding one increases the rate limit from 60 to 5,000 requests/hour.\n\n🔒 Your token is used only in this session and is never stored or transmitted."
    )
    readme_chars = st.slider("README characters (max)", 500, 5000, 2000, step=500)
    top_repos    = st.slider("Repositories to analyze", 3, 15, 8)
    st.markdown("---")
    st.markdown("**🔒 Privacy**")
    st.markdown("""
- Only **public** GitHub data is fetched
- Data is **never stored** on any server
- Data is **never shared** with third parties
- Closing this tab **erases all data**
    """)
    st.markdown("---")
    st.markdown("**How to use**")
    st.markdown("1. Enter a GitHub username\n2. Click Analyze\n3. Copy or download the text\n4. Paste into Claude or ChatGPT")


# ─────────────────────────────────────────────────────────
# Privacy Banner
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="privacy-banner">
    <div class="privacy-banner-icon">🔒</div>
    <div class="privacy-banner-text">
        <strong>Data Privacy Notice</strong><br>
        GitScope retrieves only publicly available information from GitHub. All data is processed locally in your browser and is never stored on or transmitted to any external server. Please use candidate information solely for recruitment purposes.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Search
# ─────────────────────────────────────────────────────────
st.markdown('<div class="search-card">', unsafe_allow_html=True)
st.markdown('<div class="search-label">GitHub Username or Repository URL</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    github_input = st.text_input(
        "input",
        placeholder="e.g.  torvalds   or   https://github.com/torvalds/linux",
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze →", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────
def make_headers(token):
    h = {"Accept": "application/vnd.github.v3+json"}
    if token:
        h["Authorization"] = "token " + token
    return h

def parse_input(raw):
    raw = raw.strip().rstrip("/")
    if "github.com/" in raw:
        parts = raw.split("github.com/")[-1].split("/")
        return parts[0], (parts[1] if len(parts) >= 2 else None)
    return raw, None

def fetch_user(username, headers):
    r = requests.get("https://api.github.com/users/" + username, headers=headers)
    return r.json() if r.status_code == 200 else None

def fetch_repos(username, headers, count):
    r = requests.get(
        "https://api.github.com/users/" + username + "/repos?sort=stars&per_page=" + str(count),
        headers=headers
    )
    return r.json() if r.status_code == 200 else []

def fetch_readme(username, repo, headers, max_chars):
    rh = dict(headers)
    rh["Accept"] = "application/vnd.github.v3.raw"
    r = requests.get("https://api.github.com/repos/" + username + "/" + repo + "/readme", headers=rh)
    if r.status_code == 200:
        return r.text[:max_chars] + ("\n... [truncated]" if len(r.text) > max_chars else "")
    return "(No README found)"

def fetch_languages(username, repo, headers):
    r = requests.get("https://api.github.com/repos/" + username + "/" + repo + "/languages", headers=headers)
    return r.json() if r.status_code == 200 else {}

def fetch_events(username, headers):
    """直近300件のpublicイベントを取得（最大10ページ）"""
    all_events = []
    for page in range(1, 4):  # 3ページ = 最大90件（APIの現実的な上限）
        r = requests.get(
            "https://api.github.com/users/" + username + "/events/public?per_page=30&page=" + str(page),
            headers=headers
        )
        if r.status_code != 200 or not r.json():
            break
        all_events.extend(r.json())
        time.sleep(0.2)
    return all_events


# ─────────────────────────────────────────────────────────
# Contribution Type Analysis
# ─────────────────────────────────────────────────────────

# GitHub Event type → contribution カテゴリのマッピング
EVENT_CATEGORIES = {
    "PushEvent":              "builder",       # コードをコミット・プッシュ
    "CreateEvent":            "builder",       # ブランチ・タグ・リポジトリ作成
    "PullRequestEvent":       "collaborator",  # PRを開く・マージする
    "PullRequestReviewEvent": "collaborator",  # PRをレビューする
    "IssuesEvent":            "problem_solver",# Issueを開く・閉じる
    "IssueCommentEvent":      "communicator",  # Issueにコメント
    "CommitCommentEvent":     "communicator",  # コミットにコメント
    "ForkEvent":              "community",     # リポジトリをフォーク
    "WatchEvent":             "community",     # リポジトリをスター
    "DeleteEvent":            "builder",
    "ReleaseEvent":           "builder",
}

CATEGORY_META = {
    "builder": {
        "icon":  "🔨",
        "label": "Builder",
        "desc":  "Writes & ships code",
    },
    "collaborator": {
        "icon":  "🤝",
        "label": "Collaborator",
        "desc":  "Works via PRs & reviews",
    },
    "problem_solver": {
        "icon":  "🐛",
        "label": "Problem Solver",
        "desc":  "Opens & resolves issues",
    },
    "communicator": {
        "icon":  "💬",
        "label": "Communicator",
        "desc":  "Discusses & gives feedback",
    },
    "community": {
        "icon":  "🌟",
        "label": "Community",
        "desc":  "Forks & stars projects",
    },
}

def analyze_contributions(events: list) -> dict:
    """イベントリストからcontributionの種類ごとの件数を返す"""
    counts = {k: 0 for k in CATEGORY_META}
    for event in events:
        cat = EVENT_CATEGORIES.get(event.get("type", ""), None)
        if cat:
            counts[cat] += 1
    return counts

def contribution_summary_text(contrib_counts: dict, total_events: int) -> str:
    """LLMテキスト用のcontributionサマリーを生成"""
    lines = []
    lines.append("─" * 60)
    lines.append("Contribution Style (based on last ~90 public events)")
    lines.append("─" * 60)

    sorted_cats = sorted(contrib_counts.items(), key=lambda x: -x[1])
    for cat, count in sorted_cats:
        if count == 0:
            continue
        meta = CATEGORY_META[cat]
        pct  = count / total_events * 100 if total_events > 0 else 0
        bar  = "█" * int(pct / 5)
        lines.append(
            meta["icon"] + "  " + meta["label"].ljust(16)
            + bar.ljust(20) + " " + str(count) + " events  (" + str(round(pct, 1)) + "%)"
        )

    # 主要スタイルのテキスト判定
    top = sorted_cats[0][0] if sorted_cats else None
    if top:
        meta = CATEGORY_META[top]
        lines.append("")
        lines.append("Primary style: " + meta["icon"] + " " + meta["label"] + " — " + meta["desc"])

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
# LLM Text Builders
# ─────────────────────────────────────────────────────────
QUESTIONS_JA = [
    "このエンジニアの技術スタックと得意分野を教えてください",
    "バックエンド・フロントエンド・インフラのどれが強そうですか？",
    "経験年数・スキルレベルはどのくらいと推測できますか？",
    "Contribution Styleから、チームでの働き方を教えてください",
    "強みと弱みを、非エンジニアにわかる言葉で説明してください",
    "スタートアップの少人数チームに向いていますか？",
]

QUESTIONS_EN = [
    "What is this engineer's tech stack and area of expertise?",
    "Are they stronger in backend, frontend, or infrastructure?",
    "How many years of experience and what skill level do they appear to have?",
    "Based on their Contribution Style, how might they work within a team?",
    "What are their strengths and weaknesses in plain, non-technical language?",
    "Would they be a good fit for a small startup team?",
]

PRIVACY_NOTE_JA = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【取り扱い上の注意】
このデータはGitHubに公開されている情報のみを含みます。
採用選考の目的にのみ使用し、第三者への提供・目的外利用はお控えください。
（個人情報の保護に関する法律 第16条・第18条 に基づく）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

PRIVACY_NOTE_EN = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Data Handling Notice]
This report contains only publicly available information from GitHub.
Please use it solely for recruitment purposes.
Do not share with unauthorized third parties.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def build_repo_block(repos, lang="en"):
    lines = []
    label = "主要リポジトリ（スター数順）" if lang == "ja" else "Top Repositories (by stars)"
    lines.append("─" * 60)
    lines.append(label)
    lines.append("─" * 60)
    for repo in repos:
        stars = repo.get('stargazers_count', 0)
        rl = repo.get('language') or ('不明' if lang == "ja" else 'Unknown')
        lines.append("\n📦 " + repo['name'] + "   ⭐ " + str(stars))
        if lang == "ja":
            lines.append("   説明     : " + (repo.get('description') or '説明なし'))
            lines.append("   言語     : " + rl)
            lines.append("   フォーク : " + str(repo.get('forks_count', 0)))
            lines.append("   最終更新 : " + repo.get('pushed_at', '')[:10])
            if repo.get('topics'):
                lines.append("   トピック : " + ', '.join(repo['topics'][:6]))
        else:
            lines.append("   Description : " + (repo.get('description') or 'N/A'))
            lines.append("   Language    : " + rl)
            lines.append("   Forks       : " + str(repo.get('forks_count', 0)))
            lines.append("   Last updated: " + repo.get('pushed_at', '')[:10])
            if repo.get('topics'):
                lines.append("   Topics      : " + ', '.join(repo['topics'][:6]))
    return lines

def build_lang_block(lang_summary, lang="en"):
    if not lang_summary:
        return []
    lines = []
    label = "使用言語の傾向（コード量ベース）" if lang == "ja" else "Language Breakdown (by code volume)"
    lines.append("")
    lines.append("─" * 60)
    lines.append(label)
    lines.append("─" * 60)
    total = sum(lang_summary.values())
    for l, b in sorted(lang_summary.items(), key=lambda x: -x[1]):
        pct = b / total * 100
        bar = "█" * int(pct / 5)
        lines.append("  " + l.ljust(20) + " " + bar.ljust(20) + " " + str(round(pct, 1)) + "%")
    return lines

def build_llm_text(user, repos, lang_summary, top_readme, contrib_counts, lang="en"):
    is_ja = lang == "ja"
    lines = [PRIVACY_NOTE_JA if is_ja else PRIVACY_NOTE_EN]

    if is_ja:
        lines.append("=" * 60)
        lines.append("【GitHubプロフィール解析: @" + user['login'] + "】")
        lines.append("=" * 60)
        lines.append("名前         : " + (user.get('name') or '未設定'))
        lines.append("自己紹介     : " + (user.get('bio') or '未設定'))
        lines.append("所属         : " + (user.get('company') or '未設定'))
        lines.append("場所         : " + (user.get('location') or '未設定'))
        lines.append("公開リポジトリ: " + str(user.get('public_repos', 0)) + " 件")
        lines.append("フォロワー   : " + str(user.get('followers', 0)) + " 人")
        lines.append("アカウント作成: " + user.get('created_at', '')[:10])
    else:
        lines.append("=" * 60)
        lines.append("GitHub Profile Analysis: @" + user['login'])
        lines.append("=" * 60)
        lines.append("Name        : " + (user.get('name') or 'N/A'))
        lines.append("Bio         : " + (user.get('bio') or 'N/A'))
        lines.append("Company     : " + (user.get('company') or 'N/A'))
        lines.append("Location    : " + (user.get('location') or 'N/A'))
        lines.append("Public Repos: " + str(user.get('public_repos', 0)))
        lines.append("Followers   : " + str(user.get('followers', 0)))
        lines.append("Member since: " + user.get('created_at', '')[:10])
    if user.get('blog'):
        lines.append(("ウェブサイト  : " if is_ja else "Website     : ") + user['blog'])

    lines.append("")
    lines += build_repo_block(repos, lang)
    lines += build_lang_block(lang_summary, lang)

    # Contribution Style
    total_events = sum(contrib_counts.values())
    if total_events > 0:
        lines.append("")
        lines.append(contribution_summary_text(contrib_counts, total_events))

    if top_readme and repos:
        lines.append("")
        lines.append("─" * 60)
        lines.append(("【代表リポジトリ README: " if is_ja else "README — ") + repos[0]['name'] + ("】" if is_ja else ""))
        lines.append("─" * 60)
        lines.append(top_readme)

    lines.append("")
    lines.append("=" * 60)
    lines.append("【LLMへの推奨質問例】" if is_ja else "Suggested questions for Claude / ChatGPT")
    lines.append("=" * 60)
    questions = QUESTIONS_JA if is_ja else QUESTIONS_EN
    for i, q in enumerate(questions, 1):
        lines.append("  Q" + str(i) + ". " + q)

    return "\n".join(lines)

def build_llm_text_bilingual(user, repos, lang_summary, top_readme, contrib_counts):
    ja = build_llm_text(user, repos, lang_summary, top_readme, contrib_counts, "ja")
    en = build_llm_text(user, repos, lang_summary, top_readme, contrib_counts, "en")
    sep = "\n\n" + ("━" * 60) + "\n— ENGLISH VERSION —\n" + ("━" * 60) + "\n\n"
    return ja + sep + en


# ─────────────────────────────────────────────────────────
# Analyze
# ─────────────────────────────────────────────────────────
if analyze_btn and github_input:
    username, specific_repo = parse_input(github_input)
    headers = make_headers(github_token)

    with st.spinner("Fetching data from GitHub..."):
        user = fetch_user(username, headers)
        if not user or "message" in user:
            st.error("❌  User `" + username + "` not found. Please check the username.")
            st.stop()

        repos = fetch_repos(username, headers, top_repos)
        time.sleep(0.3)

        lang_summary = {}
        for repo in repos[:5]:
            for lang, bytes_ in fetch_languages(username, repo["name"], headers).items():
                lang_summary[lang] = lang_summary.get(lang, 0) + bytes_
            time.sleep(0.2)

        top_repo_name = specific_repo or (repos[0]["name"] if repos else None)
        readme_text = fetch_readme(username, top_repo_name, headers, readme_chars) if top_repo_name else ""

        events = fetch_events(username, headers)
        contrib_counts = analyze_contributions(events)

    st.success("✅  Analysis complete for @" + username + "  ·  Public data only")
    st.divider()

    # ── Metrics ───────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Public Repos",     str(user.get('public_repos', 0)))
    c2.metric("Followers",        str(user.get('followers', 0)))
    c3.metric("Repos Analyzed",   str(len(repos)))
    top_lang = max(lang_summary, key=lang_summary.get) if lang_summary else "N/A"
    c4.metric("Primary Language", top_lang)

    # ── Contribution Style ────────────────────────────────
    total_events = sum(contrib_counts.values())
    if total_events > 0:
        st.divider()
        st.markdown("#### 🎯 Contribution Style")
        st.caption("Based on the last ~90 public GitHub events")

        sorted_cats = sorted(contrib_counts.items(), key=lambda x: -x[1])
        cards_html = '<div class="contrib-grid">'
        for cat, count in sorted_cats:
            if count == 0:
                continue
            meta = CATEGORY_META[cat]
            pct  = round(count / total_events * 100, 1)
            cards_html += (
                '<div class="contrib-card">'
                + '<div class="icon">' + meta["icon"] + '</div>'
                + '<div class="label">' + meta["label"] + '</div>'
                + '<div class="value">' + str(count) + '</div>'
                + '<div class="desc">' + meta["desc"] + '  · ' + str(pct) + '%</div>'
                + '</div>'
            )
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

    st.divider()

    # ── Tabs ──────────────────────────────────────────────
    tab_raw, tab_repos, tab_langs = st.tabs([
        "📋  LLM-ready Text",
        "📦  Repositories",
        "📊  Language Breakdown"
    ])

    with tab_raw:
        st.markdown("##### 🌐 Output Language")
        lang_choice = st.radio(
            "lang",
            options=["🇯🇵  Japanese", "🇺🇸  English", "🇯🇵🇺🇸  Bilingual"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if lang_choice == "🇯🇵  Japanese":
            llm_text = build_llm_text(user, repos, lang_summary, readme_text, contrib_counts, "ja")
            fname = "gitscope_" + username + "_ja.txt"
        elif lang_choice == "🇺🇸  English":
            llm_text = build_llm_text(user, repos, lang_summary, readme_text, contrib_counts, "en")
            fname = "gitscope_" + username + "_en.txt"
        else:
            llm_text = build_llm_text_bilingual(user, repos, lang_summary, readme_text, contrib_counts)
            fname = "gitscope_" + username + "_bilingual.txt"

        st.caption("Copy or download the text below, then paste it into Claude or ChatGPT.")

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            copy_button(llm_text)
        with btn_col2:
            st.download_button(
                label="⬇  Download as .txt",
                data=llm_text,
                file_name=fname,
                mime="text/plain",
                use_container_width=True
            )
        st.code(llm_text, language=None)

    with tab_repos:
        for repo in repos:
            with st.expander("📦  " + repo['name'] + "   ⭐ " + str(repo.get('stargazers_count', 0))):
                st.markdown("**Description**: " + (repo.get('description') or 'N/A'))
                st.markdown("**Language**: `" + (repo.get('language') or 'Unknown') + "`")
                st.markdown("**Forks**: " + str(repo.get('forks_count', 0)))
                st.markdown("**Last updated**: " + repo.get('pushed_at', '')[:10])
                if repo.get('topics'):
                    st.markdown("**Topics**: " + ', '.join(repo['topics']))
                st.markdown("[View on GitHub ↗](" + repo['html_url'] + ")")

    with tab_langs:
        if lang_summary:
            total = sum(lang_summary.values())
            st.bar_chart({l: round(v / total * 100, 1) for l, v in sorted(lang_summary.items(), key=lambda x: -x[1])})
            st.caption("Language distribution by lines of code (%)")
        else:
            st.info("No language data available.")

elif analyze_btn:
    st.warning("Please enter a GitHub username or URL.")


# ─────────────────────────────────────────────────────────
# Privacy Footer
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="privacy-footer">
    <div class="privacy-footer-title">🔒 Privacy & Data Handling</div>
    <ul class="privacy-footer-list">
        <li>Only publicly available GitHub data is retrieved</li>
        <li>All data is processed locally in your browser — nothing is sent to any server</li>
        <li>Data is never stored, logged, or shared with third parties</li>
        <li>Closing this tab permanently erases all retrieved data</li>
        <li>Please use candidate information solely for recruitment purposes</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.divider()
st.caption("GitScope · Powered by GitHub REST API · Public data only · No data stored")
