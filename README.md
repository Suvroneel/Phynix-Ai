# Phynix Ai

<a href="https://www.producthunt.com/products/ashva?embed=true&utm_source=embed&utm_medium=post_embed" target="_blank">
  <img src="https://ph-files.imgix.net/dd7b14ef-438d-4b6a-93de-3cf1752a3231.png?auto=compress,format&codec=mozjpeg&cs=strip&fit=crop&h=120&w=120" align="left" width="88" />
</a>

### Ashva
An AI companion that remembers what you said

**🏆 Ranked #20 on Product Hunt's daily leaderboard with 85 upvotes**

<img width="1920" height="1080" alt="Phynix AI" src="https://github.com/user-attachments/assets/b75f37d6-2b68-44a7-9d44-7e42010ce526" />

<a href="https://www.producthunt.com/products/ashva?embed=true&utm_source=embed&utm_medium=post_embed" target="_blank">
  <img src="https://img.shields.io/badge/Check%20it%20out%20on%20Product%20Hunt%20%E2%86%92-FF6154?style=for-the-badge&logo=producthunt&logoColor=white" alt="Check it out on Product Hunt" />
</a>

<br clear="left">

Most AI talks at you. Phynix grows with you. It remembers how you felt last session, notices your patterns over time, and meets you where you actually are instead of starting from zero every single time.

**Live Demo:** https://phynix.streamlit.app/

Phynix is an end-to-end, mood-aware GenAI platform. The heart of it is **Ashva**, a companion that combines a fine-tuned emotion model, an LLM for empathetic replies, and a memory layer built from your chats and diary entries.

---

## Recent Updates

### v2.5 - Memory Management (Beta)
A new page where you can see how many memories Ashva holds and clean up old ones, so replies stay sharp.

### v2.4 - Google Sign-In
Login now uses Google sign-in, so there is no password to remember.

### v2.3 - LLM Backend Upgrade
Ashva's replies now run through OpenRouter for better availability and fewer rate-limit problems.

### v2.2 - Memory Engine
Ashva now remembers context from past conversations and diary entries, and uses it to welcome you back in a personal way.

### v2.1.1 - Ashva Diaries
A private daily journal with optional photos. Fresh view every day at midnight IST.

### v2.0 - GenAI Backend
Replaced fixed replies with live, context-aware responses.

---

## Pages

### Login

Sign in with Google and pick a display name to get started.

![Login](Site%20Images/Login.png)

---

### Chat

Talk to Ashva. Every message gets an emotion and risk analysis, and replies are shaped by how you are feeling.

![Chat](https://github.com/Suvroneel/Phynix-GenAI-Platform/blob/Suvroneel-patch-1/Site%20Images/Phynix_Genai_Chat.png?raw=true)

---

### Home

Your daily advice, Ashva Insights, and a mood dashboard showing confidence, risk, and emotion trends.

![Home1](Site%20Images/Home_1.png)
![Home2](Site%20Images/Home_2.png)

---

### My Journals

A private journal with optional photos, plus your profile picture and name.

![Mood Journal](https://github.com/Suvroneel/Phynix-GenAI-Platform/blob/Suvroneel-patch-1/Site%20Images/Ashva_diary.png)

---

### Memory Plans

See how many memories Ashva is holding, clean up old ones (Beta), and log out of all sessions.

---

## Features

- **Emotion detection:** a fine-tuned model classifies each message into 7 emotions (joy, sadness, anger, fear, surprise, disgust, neutral)
- **Empathetic replies:** responses shaped by how you are feeling
- **Memory:** Ashva recalls what you shared before, from both chats and diary entries
- **Memory management:** see your memory count and clean up old memories
- **Mood dashboard:** confidence, risk, and emotion trends over time
- **Private journal:** write freely, attach a photo, no mood tagging or judgment
- **Daily advice:** a short quote each day

---

## Project Structure

```
Phynix-Ai/
├── Logout.py        Entry point and login
├── pages/           Chat, Home, My Journals, Memory Plans
├── Utils/           Shared app logic
├── images/          Static assets
├── Dockerfile
└── requirements.txt
```

---

## Technologies Used

- **Frontend:** Streamlit, HTML/CSS
- **Backend:** Supabase (auth data, database, storage), Python
- **AI / ML:** Transformers and PyTorch (emotion model), sentence-transformers (memory), OpenRouter (LLM replies)
- **Data:** Pandas, Altair

---

## Getting Started

```bash
git clone https://github.com/Suvroneel/Phynix-Mental-Health-Chatbot.git
cd Phynix-Mental-Health-Chatbot
pip install -r requirements.txt
streamlit run Logout.py
```

You will need your own credentials for Supabase, OpenRouter, and Google sign-in, added in `.streamlit/secrets.toml`.

---

## Roadmap

- [ ] Voice interaction
- [ ] Crisis detection with emergency routing
- [ ] Multi-language support
- [ ] Mobile app
- [ ] You_AI, the next chapter, is in active development

---

## Disclaimer

Phynix is a reflection and wellbeing companion. It is not a substitute for professional mental health advice. Please consult a qualified professional if you need support.

---

## Contributing

Contributions are welcome. Fork the repo, create a feature branch, and open a pull request.

## License

MIT License

---

**Developed by Suvroneel** | [GitHub](https://github.com/Suvroneel) | [Live Demo](https://phynix.streamlit.app/)
