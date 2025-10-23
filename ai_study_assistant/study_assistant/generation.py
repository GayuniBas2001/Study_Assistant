# study_assistant/generation.py

"""
Student 2: AI Content Generation (using Huggingface Model)

Functions:
- function_X_generate_answer(query, vector_store) - > Q&A Mode
- function_Y_synthesize_notes(query, vector_store) - > Note Maker
Notes:
- Primary Task: Engineer Prompts Tailored to Different Context Sizes
- Utilizes Local HuggingFace Model for Offline Generation
- Integrates with retrieval.py for context fetching
"""

import os
from dotenv import load_dotenv

# HuggingFace Transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Import retrieval utilities from retrieval.py file
from retrieval import (
    function_B_precise_retrieval,
    function_C_comprehensive_retrieval,
    load_vectorstore_from_dir,
)

load_dotenv()

# ------------------------
# Model Initialization
# ------------------------
MODEL_NAME = os.getenv("HF_MODEL", "openai-community/gpt2")
print(f"🔹 Loading model: {MODEL_NAME} (first time may take a while)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

# ------------------------
# Core LLM Wrapper
# ------------------------
def send_to_llm(prompt: str, temperature: float = 0.4, max_new_tokens: int = 512) -> str:
    """
    Sends a prompt to the local HuggingFace model and returns generated text.
    Works fully offline after downloading the model.
    """
    try:
        result = generator(
            prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )[0]["generated_text"]
        # Return only the part after the prompt
        return result[len(prompt):].strip()
    except Exception as e:
        return f"[Error: {str(e)}]"

# ------------------------
# Prompt Engineering Logic
# ------------------------
def function_X_generate_answer(query, vector_store):
    """
    Q&A Prompt: Designed for focused, concise answers using precise context related to the document.
    """
    precise_context = function_B_precise_retrieval(query, vector_store, k=4)
    context_text = "\n\n".join([chunk.page_content for chunk in precise_context])

    prompt = f"""
You are an expert teaching assistant helping a student answer questions clearly.

Context:
{context_text}

Question:
{query}

Answer directly and accurately in 3 to 5 sentences. If unsure, say the context do not include enough info.
    """

    return send_to_llm(prompt, temperature=0.4)


def function_Y_synthesize_notes(query, vector_store):
    """
    Synthesizer / Note-Maker Prompt: Structures large, unordered context into clean study notes.
    """
    retrieved_docs = function_C_comprehensive_retrieval(query, vector_store, threshold=0.75)
    comprehensive_context = "\n\n".join([doc.page_content for doc, score in retrieved_docs])

    prompt = f"""
You are an expert academic note-maker.

Task:
From the following context, create structured, easy-to-study notes about:
"{query}"

Context:
{comprehensive_context}

Guidelines:
- Use headings, bullet points, and concise paragraphs.
- Organize information logically.
- Avoid redundancy or irrelevant info.
- End with a short summary of the key ideas.
    """

    return send_to_llm(prompt, temperature=0.6, max_new_tokens=800)

# ------------------------
# Example Usage
# ------------------------
if __name__ == "__main__":
    query = "Explain the main differences between supervised and unsupervised learning."
    vector_store = load_vectorstore_from_dir("./vector_store/sample_index")

    print("\n=== Q&A MODE ===")
    answer = function_X_generate_answer(query, vector_store)
    print(answer)

    print("\n=== NOTE-MAKER MODE ===")
    notes = function_Y_synthesize_notes(query, vector_store)
    print(notes)
