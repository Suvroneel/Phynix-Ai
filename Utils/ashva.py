import base64
import logging
import random
import streamlit as st
import streamlit.components.v1 as components
from Utils.auth_guard import get_supabase_service


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


image_base64 = get_base64_image("images/sigmund-ljJDx95-6gE-unsplash.png")

GAP = "<div style='margin-top: 14px;'></div>"

return_user_emotion_messages = {
    "sadness": [
        f"You weren’t feeling the best last time.{GAP}I’m really glad you’re here again.{GAP}What’s been on your mind lately?",
        f"Last time felt a little heavy for you.{GAP}I’ve been thinking about that.{GAP}How have things been going since then?",
        f"It’s comforting to see you again after a rough moment.{GAP}Let’s gently talk through whatever’s been on your mind.",
        f"You seemed weighed down before.{GAP}Let’s talk about what’s been feeling heavy for you lately.",
        f"I’ve been holding space for you since our last chat.{GAP}How have things been feeling since we last talked?"
    ],
    "fear": [
        f"You seemed a little unsure last time.{GAP}I’m really glad you returned.{GAP}What’s been going on since then?",
        f"I know you were feeling nervous last time.{GAP}It’s okay to take it slow.{GAP}What’s been on your mind these days?",
        f"You were holding a lot last time.{GAP}You don’t have to carry it alone.{GAP}What’s been on your mind lately?",
        f"It means a lot to see you back.{GAP}Let’s gently explore whatever you’ve been feeling inside lately.",
        f"Even when things feel uncertain, you still showed up.{GAP}I’m here with you,{GAP}let’s talk about what’s been going on."
    ],
    "anger": [
        f"You were feeling frustrated last time.{GAP}It’s okay,{GAP}you can let it out.{GAP}What’s still on your mind these days?",
        f"I remember how intense things felt before.{GAP}I’m still here,{GAP}no judgment.{GAP}What’s been sticking with you?",
        f"You came in strong last time, and that’s okay.{GAP}We all need space to express it.{GAP}What’s been bothering you lately?",
        f"I’m glad you’re back.{GAP}Let’s talk about whatever’s still feeling intense for you.",
        f"It takes courage to return with heavy emotions.{GAP}I’m here to hold space,{GAP}let’s talk through what’s still bothering you."
    ],
    "disgust": [
        f"You seemed really bothered before.{GAP}I’m grateful to see you again.{GAP}What’s been bugging you lately?",
        f"There was something that didn’t sit right with you last time.{GAP}I’ve held that in mind.{GAP}What’s been feeling off since then?",
        f"Some moments leave a bad vibe.{GAP}If you’re ready,{GAP}let’s talk about what’s stayed with you.",
        f"I felt how deeply something impacted you before.{GAP}I’m here with care,{GAP}let’s talk about what’s been on your mind.",
        f"It’s good to reconnect.{GAP}I’ve been holding space for your thoughts,{GAP}tell me what’s still been tough to deal with."
    ],
    "joy": [
        f"You were in a great mood last time.{GAP}I’ve been hoping your days stayed bright.{GAP}What’s been keeping you happy lately?",
        f"You were in a great mood last time.{GAP}What moments lately have kept you feeling good?",
        f"You carried joy into this space before.{GAP}I’d love to hear what’s made your heart feel full recently.",
        f"You’ve returned with that same warm energy.{GAP}Let’s share in what’s made life feel a little brighter lately."
    ],
    "surprise": [
        f"Last time caught you off guard.{GAP}I’ve been wondering how things unfolded since.{GAP}What’s happened since then?",
        f"That unexpected moment last time stuck with me.{GAP}What’s been going on since then?",
        f"I remember the surprise in your words before.{GAP}Let’s pick things up and see how things have been going.",
        f"There was wonder in our last talk.{GAP}Tell me what new things have come up since then.",
        f"You left me curious last time.{GAP}Let’s catch up,{GAP}what’s been going on in your world?"
    ]
}

# Ashva nsights ---------------------Home.py

# Emotion → Insight suggestions
ashva_guidance = {
    "sadness": [
        "You’ve been feeling down, huh? I’m here. Let’s take it one step at a time.",
        "It’s okay to feel heavy. You don’t have to act like everything’s fine.",
        "Even a small moment of self-care today can help. Maybe try something simple?",
        "Maybe take a short walk or grab a cozy drink. It can help you feel a bit more grounded.",
        "Feeling sad doesn’t mean you’re broken. It just means you’re human, and I’m with you."
    ],

    "anger": [
        "You’re frustrated, and that’s totally okay. Let’s take a deep breath together.",
        "Anger’s loud because it’s protecting something you care about. Wanna talk about it?",
        "You don’t have to push it down, but you don’t have to let it take over either. Let’s find a balance.",
        "If things feel too intense, try taking a walk or writing what’s on your mind. You’ll be okay after.",
        "I’m not here to judge your anger—just to help you ease it when you’re ready."
    ],

    "fear": [
        "Feeling worried? That’s okay. Let’s slow things down for a bit.",
        "Fear gets big when things feel uncertain. Let’s focus on what you know right now—your breath, your space.",
        "Saying what’s scaring you out loud can make it feel less heavy. I’m here to listen.",
        "It’s okay to not be ready yet. You can pause until you feel more grounded.",
        "Being afraid doesn’t make you weak. You’re strong for dealing with it."
    ],

    "joy": [
        "You seem happy today! Hope you’re enjoying that feeling.",
        "Hold onto what’s making you smile. It’s a good thing to keep close.",
        "Happiness deserves space, just like any other feeling. Let it stick around.",
        "Even a small smile feels good. Hope it stays with you for a while.",
        "You’re in a great mood, and that’s awesome. Let’s keep it going."
    ],

    "tired": [
        "You’ve been pushing hard. It’s okay to take a break.",
        "Breathe, grab some water, and let your shoulders relax. You don’t have to keep going all the time.",
        "Rest isn’t something you earn—it’s something you deserve. Take it when you need it.",
        "Even five minutes of quiet can help you recharge. Wanna try it?",
        "Your body’s telling you it needs a break. It’s okay to listen."
    ],

    "disgust": [
        "Something really got to you, didn’t it? Let’s just take a moment to process.",
        "Disgust often means something crossed a line for you. What happened?",
        "Let’s step back from whatever’s bothering you. You don’t have to hold onto it.",
        "Try finding a calm space or taking a deep breath to reset. We can talk it through after.",
        "You don’t have to put up with what feels wrong. It’s okay to set boundaries."
    ],

    "surprise": [
        "Whoa, something caught you off guard, right? It’s okay to still be sorting it out.",
        "Surprises can shake things up. Let’s take a second to see what’s going on.",
        "No need to figure it all out right away. Let’s just breathe first.",
        "Even if it threw you off, you’re handling it. One step at a time.",
        "This could be a big moment. For now, let’s just stay calm."
    ],

    "neutral": [
        "Some days feel calm and quiet. That’s okay—it’s just space to breathe.",
        "You don’t need to feel big emotions all the time. Quiet moments count too.",
        "Let today be easy. No need to push for anything more.",
        "Feeling neutral isn’t a problem. It’s just a moment to rest.",
        "If things feel calm, that’s fine. Your mind might just need a little break."
    ]
}

ashva_diary = [
    "Write whatever feels right, even if it’s just one line.",
    "You can write anything that feels like you, even if it’s just a single thought.",
    "Still empty. Write what feels right, even if it’s small.",
    "No words yet. This space is yours when you feel like speaking.",
    "Nothing here yet. When you're ready, say something that feels true.",
]


def journal():
    st.markdown(f" {random.choice(ashva_diary)}")


def ashva_insights(username: str, email: str):
    supabase = get_supabase_service()

    st.markdown("""
        <style>
            .ashva-tagline {
                font-size: 15px;
                color: #d35400;
                font-weight: 400;
                margin-top: 8px;
                margin-bottom: 6px;
                font-family: 'Inter', sans-serif;
                text-align: left;
            }

            .ashva-highlight {
                font-size: 21px;
                font-weight: 500;
                font-family: 'Inter', sans-serif;
                color: ;
                line-height: 1.7;
                margin-top: 6px;
                margin-bottom: 16px;
            }
        </style>

        <div class="ashva-tagline">Context-aware insights from your recent activity.</div>
    """, unsafe_allow_html=True)

    default_msg = "Take a moment for yourself today. Your emotional well-being matters."

    try:
        response = supabase.table("user_data") \
            .select("predicted_emotion") \
            .eq("user_name", username) \
            .eq("user_email", email) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        if response.data and len(response.data) > 0:
            last_emotion = response.data[0]["predicted_emotion"].lower()
            insight = random.choice(ashva_guidance.get(last_emotion, [default_msg]))
        else:
            insight = "We couldn't detect a recent emotional check-in."

    except Exception as e:
        insight = default_msg
        print("Ashva Insight Error:", e)

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="ashva-highlight">{insight}</div>
    """, unsafe_allow_html=True)


# -------------------------For Chat Section----------------------------------- Mainpart

def display_welcome_message(username: str, email: str):
    from Utils.memory import retrieve_memories
    from Utils.gen_ai import PhynixAI

    supabase = get_supabase_service()

    with st.spinner("Processing your request..."):
        try:
            clean_email = email.strip().lower()
            clean_username = username.strip().lower()

            # Try RAG first
            last_msg_response = supabase.table("user_data") \
                .select("messages") \
                .eq("user_email", clean_email) \
                .order("created_at", desc=True) \
                .limit(1) \
                .execute()

            query_text = last_msg_response.data[0]["messages"] if last_msg_response.data else None

            memories = retrieve_memories(query=query_text, user_email=clean_email, top_k=4) if query_text else []

            if memories:
                # Condition 1: RAG working, LLM generates natural welcome
                context = "\n".join([f"[{m['source']}]: {m['text']}" for m in memories])
                ai = PhynixAI()
                message = ai.generate_response(
                    user_message="You are Ashva, a close friend who genuinely remembers what the user shared before. Write ONE casual sentence welcoming them back, referencing something specific from their past context in past tense, like you actually remember it. Sound like a real friend texting, not an AI. No quotation marks, no em dashes, no emoji, no formal language, no lists.",
                    chat_history=[{
                        "role": "user",
                        "content": f"Here is what the user has shared before:\n{context}"
                    }],
                    max_tokens=100,
                    temperature=0.85
                )

            else:
                # Condition 2: No embeddings yet, fall back to emotion based message
                emotion_response = supabase.table("user_data") \
                    .select("predicted_emotion") \
                    .eq("user_name", clean_username) \
                    .eq("user_email", clean_email) \
                    .order("created_at", desc=True) \
                    .limit(1) \
                    .execute()

                if emotion_response.data:
                    emotion = emotion_response.data[0]["predicted_emotion"].lower()
                    message = random.choice(return_user_emotion_messages.get(emotion, ["What's going on your mind?"]))
                else:
                    # Condition 3: Brand new user, generic
                    message = "Hey, welcome back! What's been going on with you lately? 😊"

        except Exception as e:
            logging.error(f"RAG welcome error: {str(e)}")
            message = "Hey, welcome back! What's on your mind today? 😊"

    try:
        html_code = f"""
        <style>
        .bubble {{
            position: relative;
            background-color: #f9f9f9;
            padding: 14px 18px;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            color: #444;
            max-width: 600px;
            display: inline-block;
            line-height: 1.5;
        }}
        .bubble::before {{
            content: "";
            position: absolute;
            top: 18px;
            left: -10px;
            width: 0;
            height: 0;
            border-top: 10px solid transparent;
            border-bottom: 10px solid transparent;
            border-right: 10px solid #f9f9f9;
        }}
        </style>
        <div style="display: flex; align-items: flex-start; margin-top: 40px;">
            <img src="data:image/png;base64,{image_base64}" 
                 style="width: 40px; height: 40px; margin-right: 12px; border-radius: 50%;" 
                 alt="Ashva">
            <div class="bubble">
                <strong>Ashva:</strong> {message}
            </div>
        </div>
        """
        components.html(html_code, height=160)
    except Exception as e:
        logging.error(f"Welcome render error: {str(e)}")
