# Phynix AI

<a href="https://www.producthunt.com/products/ashva?embed=true&utm_source=embed&utm_medium=post_embed" target="_blank">
  <img src="https://ph-files.imgix.net/dd7b14ef-438d-4b6a-93de-3cf1752a3231.png?auto=compress,format&codec=mozjpeg&cs=strip&fit=crop&h=120&w=120" align="left" width="88" />
</a>

### Ashva
An AI companion that remembers what you said

<img width="1920" height="1080" alt="Phynix AI" src="https://github.com/user-attachments/assets/b75f37d6-2b68-44a7-9d44-7e42010ce526" />

<a href="https://www.producthunt.com/products/ashva?embed=true&utm_source=embed&utm_medium=post_embed" target="_blank">
  <img src="https://img.shields.io/badge/Check%20it%20out%20on%20Product%20Hunt%20%E2%86%92-FF6154?style=for-the-badge&logo=producthunt&logoColor=white" alt="Check it out on Product Hunt" />
</a>

<br clear="left">

**Live Demo:** https://phynix.streamlit.app/

Phynix is a mood-aware GenAI platform. A fine-tuned emotion model reads how you feel, an LLM replies with empathy, and a RAG memory layer lets Ashva remember your past chats and diary entries.

---

## Recent Updates

### v2.4 - Native Google Login + Hardened Prompt
- Login now uses Streamlit native auth (`st.login("google")` and `st.user`). The old Supabase email/password flow is archived in `auth/google_login_migration/`.
- Every page is protected by one function, `require_google_auth()`, in `Utils/auth_guard.py`.
- Ashva's system prompt now has safety rules, prompt-injection resistance, and protected-internals rules.

### v2.3 - OpenRouter Backend Migration
Moved the LLM from the Hugging Face Inference API to OpenRouter. Uses free models (Baidu ERNIE 5.5 Flash, Google Gemma 4, inclusionAI Ling 3.2 Flash, dots Note) with an automatic fallback chain, so one rate-limited model does not break the chat.

### v2.2 - RAG Memory Engine (pgvector)
Chats and diary entries are embedded with `all-MiniLM-L6-v2` and stored in Supabase pgvector. On return, Ashva retrieves relevant memories and writes a personal welcome. Falls back to an emotion-based welcome, then a generic one.

### v2.1.1 - Ashva Diaries
Private daily journal with optional photo, stored in Supabase with a fresh view every day at midnight IST.

### v2.0 - GenAI Backend
Replaced hard-coded replies with live LLM responses.

---

## How It Works (Request Flow)

```
User sends a message (pages/1_Chat.py)
   │
   ├─ 1. Utils/model.py          predict_emotion()     -> "sadness", "joy", ...
   ├─ 2. Utils/emotion_responses get_risk_with_emoji() -> "High" / "Moderate" / "Low" / "Neutral"
   ├─ 3. Utils/gen_ai.py         PhynixAI.generate_response()  -> OpenRouter -> reply
   ├─ 4. Supabase `user_data`    insert (message, emotion, risk, reply)
   └─ 5. Utils/memory.py         upsert_memory()       -> embedding saved in `memory_embeddings`
```

Next time the user opens the chat, `Utils/ashva.py -> display_welcome_message()` calls `memory.retrieve_memories()` and `gen_ai.PhynixAI` to write a personal welcome.

---

## Project Structure

```
Phynix-Ai/
├── Logout.py                  Entry point + Google login screen
├── pages/
│   ├── 1_Chat.py              Chat with Ashva
│   ├── 2_Home.py              Dashboard, daily advice, insights
│   └── 3_Ashva Diaries.py     Journal, profile, settings, logout
├── Utils/                     All shared logic (see file map below)
├── auth/google_login_migration/   Old Supabase OAuth version (archived)
├── SQL/user_data_rows.sql     Sample rows for `user_data`
├── Phynix_FineTune.ipynb      Emotion model training notebook
├── images/  Lottie/  favicon_io/  Site Images/
├── Dockerfile                 Runs `streamlit run Logout.py`
└── requirements.txt
```

---

## File Map: Who Controls What

### Pages (what the user sees)

| File | Controls | Imports from Utils |
|---|---|---|
| `Logout.py` | Login screen, first-time username dialog, redirect to chat | `auth_guard.get_supabase_service`, `footer.render_footer`, `sidebar.hide_sidebar`, `sidebar.add_sidebar_tooltip`, `title.render_main_title`, `title.render_tagline` |
| `pages/1_Chat.py` | Chat UI, message bubbles, model selector, saving chats | `auth_guard`, `ashva.display_welcome_message`, `model.predict_emotion`, `emotion_responses.get_risk_with_emoji`, `gen_ai.PhynixAI`, `memory.upsert_memory`, `sidebar.render_sidebar_logo`, `title` (main title, dynamic greeting, tagline) |
| `pages/2_Home.py` | Welcome text, New Chat button, daily quote, Ashva Insights, metrics and charts | `auth_guard`, `title`, `advice.free_advice`, `ashva.ashva_insights`, `Progression_Chart.show_last_chat_metrics`, `Progression_Chart.session_progress`, `sidebar.render_sidebar_logo` |
| `pages/3_Ashva Diaries.py` | Profile, bio, journal entry form, today's entries, settings, logout | `auth_guard`, `journal` (fetch, insert, upload), `profile` (avatar, bio), `memory.upsert_memory`, `ashva.ashva_diary`, `title` (headers), `sidebar.render_sidebar_logo` |

### Utils (the logic layer)

| File | What it does | Key functions | Used by |
|---|---|---|---|
| `auth_guard.py` | Enforces Google login on every page and loads the username from `user_credentials`. Holds the cached Supabase service client. | `require_google_auth()`, `get_supabase_service()` | All pages, `Logout.py`, `journal.py` |
| `gen_ai.py` | LLM client (OpenRouter), Ashva's system prompt, model fallback chain | `PhynixAI.generate_response()`, `set_model()`, `_model_chain()`, `get_model_info()` | `1_Chat.py`, `ashva.py` |
| `model.py` | Loads the fine-tuned emotion model `Suvroneel/phynix-emotion-model` (cached) | `predict_emotion()` | `1_Chat.py` |
| `memory.py` | Embeddings (`all-MiniLM-L6-v2`) and vector search via the `match_memories` RPC | `upsert_memory()`, `retrieve_memories()` | `1_Chat.py`, `3_Ashva Diaries.py`, `ashva.py` |
| `ashva.py` | Ashva's personality: welcome engine (RAG, then emotion, then generic), insight text, diary placeholders | `display_welcome_message()`, `ashva_insights()`, `ashva_diary`, `ashva_guidance` | `1_Chat.py`, `2_Home.py`, `3_Ashva Diaries.py` |
| `emotion_responses.py` | Emotion to risk mapping. Old template replies are legacy. | `get_risk_with_emoji()` (active), `get_emotion_response()` (legacy) | `1_Chat.py` |
| `Progression_Chart.py` | Dashboard math and Altair charts (confidence, risk, mental health, today's emotion flow) | `show_last_chat_metrics()`, `session_progress()`, `session_progress2()` (unused) | `2_Home.py` |
| `journal.py` | Diary database and image storage (`mood_journal` table, `journal-images` bucket) | `fetch_today_entries()`, `insert_entry()`, `upload_image()`, `get_today_entry_count()` | `3_Ashva Diaries.py` |
| `profile.py` | Avatar picker dialog and bio (`user_bio` table) | `prof_change()`, `update_profile()`, `profile_name()`, `show_bio()` | `3_Ashva Diaries.py` |
| `title.py` | Titles, headers, greetings | `render_main_title()`, `render_tagline()`, `new_tagline()`, `render_dynamic_greeting()`, `render_welcome_message()`, `render_custom_header()`, `render_custom_header2()`, `render_custom_subheader()` | All pages |
| `sidebar.py` | Sidebar logo, hide sidebar, sidebar tooltip | `render_sidebar_logo()`, `hide_sidebar()`, `add_sidebar_tooltip()` | All pages |
| `footer.py` | Fixed bottom footer | `render_footer()` | `Logout.py` |
| `advice.py` | Daily Bhagavad Gita quotes | `free_advice` | `2_Home.py` |
| `feedback.py` | Star rating and review form (`user_feedbacks` table) | `handel_feedback()` | Not wired into a page yet |
| `config.py` | Page config and log suppression | `set_config()` | Not called yet |

### Legacy or unused files (safe to clean up later)
`reply.py` (old Google Sheets logger), `Otp_verification.py` (imports a file that no longer exists), `database.py`, `personality.py` (image upload stub), `Website_Title.py` (old banner), `location.py`, `matcher.py`, `Automated_Messages.py` (empty).

---

## Who Controls Which CSS

There is no single stylesheet in the Streamlit app. CSS is injected with `st.markdown(..., unsafe_allow_html=True)`, so each file owns its own part.

| File | CSS it controls |
|---|---|
| `pages/1_Chat.py` | Chat layout: `.bubble` (Ashva message), `.user-bubble`, `.user-reply`, `.ashva-reply`, `details/summary` (Analysis dropdown), orange gradient `.stButton > button` |
| `pages/2_Home.py` | `.fade-in-text` (welcome line animation), `.quote-box` and `.quote-text` (daily advice card), orange gradient `.stButton > button` |
| `pages/3_Ashva Diaries.py` | `.stImage > img` (profile and journal image style), orange gradient `.stButton > button`. Journal entry cards are styled inline. |
| `Logout.py` | `.login-card` and its button style |
| `Utils/ashva.py` | `.ashva-tagline`, `.ashva-highlight` (Insights text), `.bubble` for the welcome message (rendered in an iframe) |
| `Utils/title.py` | `.streamlit-like-header`, `.streamlit-like-subheader`, `.custom-welcome`, plus Inter, Montserrat and Poppins fonts |
| `Utils/Progression_Chart.py` | `.status` (the Stable, Caution, Vulnerable line) |
| `Utils/profile.py` | `.custom-welcome` (profile name size) |
| `Utils/sidebar.py` | Hides the sidebar and hamburger menu, adds the "Sidebar Disabled" tooltip |
| `Utils/footer.py` | `.footer` and all its link, separator and tagline styles |

The orange gradient button style (`#ff914d` to `#ff6e40`) is copied in 4 files. Moving it into one shared helper would be a good cleanup.

---

## Database (Supabase)

| Table or bucket | Purpose | Written by |
|---|---|---|
| `user_credentials` | Email to username mapping | `Logout.py`, `1_Chat.py` |
| `user_data` | Messages, predicted emotion, risk, AI reply | `1_Chat.py` |
| `memory_embeddings` | Vector memories (chat and diary) | `memory.upsert_memory()` |
| `mood_journal` | Diary entries | `journal.insert_entry()` |
| `user_bio` | Profile bio | `profile.update_profile()` |
| `user_feedbacks` | Ratings and reviews | `feedback.py` |
| `journal-images` (storage) | Diary photos | `journal.upload_image()` |

RPC: `match_memories(query_embedding, match_user_email, match_count)` does the vector search.

---

## AI Layer

### Emotion model
- Base: `j-hartmann/emotion-english-distilroberta-base`, fine-tuned on GoEmotions mapped to 7 classes (anger, disgust, fear, joy, neutral, sadness, surprise).
- Test accuracy 0.70, macro F1 0.63 (see `Phynix_FineTune.ipynb`).
- Published at `Suvroneel/phynix-emotion-model`.

### Risk mapping
Sadness, fear, anger map to High. Disgust maps to Moderate. Neutral stays Neutral. Joy and surprise map to Low.

### LLM replies
- OpenRouter with free models and automatic fallback (ERNIE, Ling, Gemma, dots, then `openrouter/free`).
- Emotion and risk are passed into the prompt as context.
- If every model fails, the user sees a friendly traffic message instead of an error.

### Memory (RAG)
Chat messages and diary entries are embedded and stored. The welcome message retrieves the 4 most relevant memories and has the LLM write one casual line from them.

---

## Setup

```bash
git clone https://github.com/Suvroneel/Phynix-Mental-Health-Chatbot.git
cd Phynix-Mental-Health-Chatbot
pip install -r requirements.txt
streamlit run Logout.py
```

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "..."
SUPABASE_KEY = "..."
SUPABASE_SERVICE_KEY = "..."
OPENROUTER_API_KEY = "..."

[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "..."
client_id = "..."
client_secret = "..."
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

Docker: `docker build -t phynix .` then `docker run -p 8501:8501 phynix`.

---

## Tech Stack
Streamlit, Supabase (Postgres, pgvector, Storage), PyTorch and Transformers, sentence-transformers, OpenRouter, Altair, Pandas.

---

## Roadmap
- [ ] Move shared CSS into one helper
- [ ] Remove legacy files listed above
- [ ] Voice input
- [ ] Crisis detection with emergency routing
- [ ] Mobile app
- [ ] You_AI, the next chapter, is in active development

---

## License
MIT

**Developed by Suvroneel** | [GitHub](https://github.com/Suvroneel) | [Live Demo](https://phynix.streamlit.app/)
