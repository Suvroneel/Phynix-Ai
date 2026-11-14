"""
GenAI Backend for Phynix Mental Health Chatbot
Integrates with BERT emotion detection for empathetic responses
Uses OpenRouter with verified November 2026 free models
"""

from openai import OpenAI
import streamlit as st


class PhynixAI:
    def __init__(self, api_key=None):
        """
        Initialize the GenAI client with OpenRouter.
        The key comes from the parameter or from Streamlit secrets.
        """
        if api_key:
            self.api_key = api_key
        else:
            try:
                self.api_key = st.secrets.get("OPENROUTER_API_KEY")
            except Exception:
                self.api_key = None
                print("Warning: No OPENROUTER_API_KEY found.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            timeout=30,
            default_headers={
                "HTTP-Referer": "https://phynix.streamlit.app",
                "X-Title": "Phynix",
            },
        )

        # Verified active free models on OpenRouter (Nov 2026, zero NVIDIA)
        self.available_models = {
            "ernie": "baidu/ernie-5.5-flash-preview:free",
            "ling": "inclusionai/ling-3.2-flash:free",
            "gemma": "google/gemma-4-31b-it:free",
            "dots": "dots-studio/dots-3-note-preview:free",
            "auto": "openrouter/free",
        }

        # Default model: ERNIE 5.5 Flash (fast, newly added, low 429 congestion)
        self.current_model = self.available_models["ernie"]

        # System prompt for mental health context
        self.system_prompt = """You are Ashva, a compassionate AI companion within the Phynix mental health platform. Your role is to:
- Listen empathetically and validate emotions
- Provide supportive, non-judgmental responses
- Ask gentle follow-up questions when appropriate
- Never diagnose or provide medical advice
- Encourage professional help for serious concerns
- Keep responses conversational and warm (2-4 sentences typically)
- Use a caring, understanding tone"""

    def set_model(self, model_name):
        """Change the active GenAI model"""
        if model_name in self.available_models:
            self.current_model = self.available_models[model_name]
            return True
        return False

    def _model_chain(self):
        """Selected model first, then remaining free models, ending with openrouter/free."""
        others = [
            m for m in self.available_models.values()
            if m != self.current_model and m != "openrouter/free"
        ]
        chain = [self.current_model] + others
        if self.current_model != "openrouter/free":
            chain.append("openrouter/free")
        return chain

    def _call(self, model, messages, max_tokens, temperature):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            extra_body={
                # Prevents hybrid reasoning models from burning hidden thinking tokens
                "reasoning": {"effort": "none"}
            },
        )
        return (response.choices[0].message.content or "").strip()

    @staticmethod
    def _merge_system_into_user(messages):
        """For models that reject the system role: fold it into the first user message."""
        system_text = messages[0]["content"]
        rest = [dict(m) for m in messages[1:]]
        for m in rest:
            if m["role"] == "user":
                m["content"] = f"{system_text}\n\n{m['content']}"
                break
        return rest

    def generate_response(
        self,
        user_message,
        detected_emotion=None,
        risk_level=None,
        chat_history=None,
        max_tokens=300,
        temperature=0.7,
    ):
        """
        Generate empathetic AI response based on user input and emotion context.
        Tries the user's selected model first, then falls back cleanly across active free tiers.
        """
        emotion_context = ""
        if detected_emotion and risk_level:
            emotion_context = (
                f"\n[Context: User's detected emotion is '{detected_emotion}' "
                f"with {risk_level} risk level. Respond with appropriate empathy and care.]"
            )

        messages = [
            {"role": "system", "content": self.system_prompt + emotion_context}
        ]
        if chat_history:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": user_message})

        last_error = ""
        for model in self._model_chain():
            try:
                reply = self._call(model, messages, max_tokens, temperature)
                if reply:
                    return reply
            except Exception as e:
                last_error = str(e)
                print(f"[OpenRouter] {model} failed: {last_error[:200]}")

                # Only retry the SAME model if it's a 400 (system prompt unsupported).
                # For 404/429/403, immediately move to the next model in the chain.
                if "400" in last_error:
                    try:
                        merged = self._merge_system_into_user(messages)
                        reply = self._call(model, merged, max_tokens, temperature)
                        if reply:
                            return reply
                    except Exception as e2:
                        last_error = str(e2)
                        print(f"[OpenRouter] {model} retry failed: {last_error[:200]}")

        return f"DEBUG ERROR: {last_error[:300] or 'all models returned an empty reply'}"

    def get_model_info(self):
        """Return current model information"""
        return {
            "current": self.current_model,
            "available": list(self.available_models.keys()),
        }

    def is_token_configured(self):
        """Check if the OpenRouter key is configured"""
        return self.api_key is not None
