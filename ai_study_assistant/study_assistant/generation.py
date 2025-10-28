# study_assistant/generation.py
# --- NEW VERSION USING FAST OPENAI API ---

"""
Student 2: AI Content Generation (using OpenAI API)
This version is DECOUPLED from retrieval.py and uses a fast, cloud-based LLM from OpenAI.
"""
from google.cloud import translate_v2 as translate
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ------------------------
# Model Initialization (API)
# ------------------------
try:
    # The client automatically reads the OPENAI_API_KEY from the .env file
    client = OpenAI()
    # We recommend 'gpt-3.5-turbo' for a great balance of speed, cost, and quality.
    # 'gpt-4o' is more powerful but also more expensive.
    MODEL_NAME = "gpt-3.5-turbo"
    print("🔹 OpenAI API client configured successfully.")
    print(f"🔹 Using model: {MODEL_NAME}")

except Exception as e:
    print(f"❌ ERROR: Could not configure OpenAI API client. Please check your OPENAI_API_KEY. Details: {e}")
    client = None

# ------------------------
# Core LLM Wrapper (Now an OpenAI API call)
# ------------------------
def send_to_llm(prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
    """
    Sends a prompt to the OpenAI API and returns the generated text.
    """
    if not client:
        return "[Error: OpenAI client is not configured. Check API key.]"
    try:
        # OpenAI's new API structure uses a 'messages' list
        # The 'system' message sets the AI's role, and 'user' is the actual prompt
        messages = [
            {"role": "system", "content": "You are a helpful and expert academic assistant."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[API Error: {str(e)}]"

# ------------------------
# Prompt Engineering Logic (Prompts are now inside the user message)
# ------------------------
def function_X_generate_answer(query: str, precise_context: list):
    """
    Q&A Prompt: Takes a PRE-FETCHED context and generates an answer via OpenAI API.
    `precise_context` should be a list of LangChain Document objects.
    """
    context_text = "\n\n".join([chunk.page_content for chunk in precise_context])

    # The prompt is the "user" part of the conversation
    prompt = f"""
        Based ONLY on the context provided below, please answer the user's question. If the context is insufficient, state that the information is not available in the document.

        Context:
        ---
        {context_text}
        ---

        Question:
        {query}
            """
    return send_to_llm(prompt)


def function_Y_synthesize_notes(query: str, comprehensive_context: list):
    """
    Synthesizer Prompt: Takes a PRE-FETCHED context and makes notes via OpenAI API.
    `comprehensive_context` should be a list of (Document, score) tuples.
    """
    context_text = "\n\n".join([doc.page_content for doc, score in comprehensive_context])

    prompt = f"""
        Your task is to act as an expert academic note-maker. Create a structured set of study notes about the topic "{query}" using ONLY the context I provide below.

        Context:
        ---
        {context_text}
        ---

        Guidelines for the notes:
        - Create a main title for the notes.
        - Use headings for different sub-topics found in the context.
        - Use bullet points to list key information.
        - Organize the information logically for easy studying.
        - End with a short, one-paragraph summary of the key ideas.
            """
    return send_to_llm(prompt)


# --- Translation Function (No changes needed) ---
def translate_to_sinhala(text: str) -> str:
    """
    Translates a given text string into Sinhala using the Google Cloud Translation API.
    """
    try:
        translate_client = translate.Client()
        if not text or not isinstance(text, str):
            return ""
        target_language = 'si'
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"[Translation Error] {text}"