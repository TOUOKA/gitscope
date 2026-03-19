# 🔭 GitScope

> Understand any engineer's GitHub profile without a technical background.

GitScope fetches publicly available GitHub data and formats it into plain-language summaries that anyone can understand. Paste the output into Claude or ChatGPT to ask questions about a candidate's skills, experience, and fit — no engineering knowledge required.

---

## Features

- Analyze any GitHub profile by username or URL
- Automatically collects profile info, repositories, and language usage
- Generates LLM-ready text in Japanese, English, or both
- Privacy notice included in every export
- Download results as `.txt`

---

## Setup

**Requirements:** Python 3.9+

```bash
pip install streamlit requests
streamlit run github_analyzer_app.py
```

Your browser will open automatically.

---

## How to use

1. Enter a candidate's GitHub username (e.g. `torvalds`) or profile URL
2. Click **Analyze →**
3. Select output language: Japanese / English / Bilingual
4. Copy the generated text
5. Paste into Claude or ChatGPT and ask questions like:
   - *"What is this engineer's area of expertise?"*
   - *"Are they stronger in backend or frontend?"*
   - *"Would they suit a small startup team?"*

---

## GitHub API rate limits

| | Limit |
|---|---|
| Without token | 60 requests / hour |
| With token | 5,000 requests / hour |

For analyzing multiple candidates, add a GitHub Personal Access Token in the sidebar.

**How to get a token:** GitHub → Settings → Developer settings → Personal access tokens → Generate new token (no scopes needed)

---

## Privacy

GitScope retrieves **public information only**. All data is processed locally in your browser and is never stored on or transmitted to any external server. Please use candidate information solely for recruitment purposes.

---

## Tech stack

- [Streamlit](https://streamlit.io/) — UI framework
- [GitHub REST API](https://docs.github.com/en/rest) — Data source

---

## License

MIT
