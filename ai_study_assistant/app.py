# This file is owned by Student 3 (UI & Application Integrator)
# This script simulates the backend workflow without a UI.

# Renaming to 'main.py' or 'test_backend.py' might be clearer,
# since 'app.py' usually implies a Streamlit UI. But for now, this works!

from study_assistant.retrieval import (
    create_vector_store,
    precise_retrieval,
    comprehensive_retrieval,
)
from study_assistant.generation import (
    generate_answer,
    synthesize_notes,
    translate_to_sinhala,
)

def run_app_logic():
    """
    Executes the main application logic, simulating a user session.
    """
    print("--- STEP 1: INITIALIZING THE APPLICATION (User uploads a PDF) ---")
    # Make sure this path is correct relative to where you run the script
    sample_pdf_path = "data/Basic-Biology-an-introduction.pdf"
    
    # Student 1's function to process the PDF and create the knowledge base
    vector_store = create_vector_store(sample_pdf_path)
    print("Application is ready.\n" + "="*50 + "\n")


    print("--- USE CASE 1: User asks a specific question ---")
    user_question = "What is the primary function of a mitochondria?"

    # 1. Retrieve context using Student 1's "precise" retriever
    precise_context = precise_retrieval(user_question, vector_store)
    print(f"Retrieved {len(precise_context)} chunks for the question.")

    # 2. Generate an answer using Student 2's Q&A generator
    english_answer = generate_answer(user_question, precise_context)
    
    print("\n[Generated English Answer]")
    print(english_answer)

    # 3. Translate the answer using Student 2's translation function
    sinhala_answer = translate_to_sinhala(english_answer)
    print("\n[Translated Sinhala Answer]")
    print(sinhala_answer)
    print("\n" + "="*50 + "\n")


    print("--- USE CASE 2: User wants to create study notes on a broad topic ---")
    user_topic = "The Industrial Revolution"

    # 1. Retrieve context using Student 1's "comprehensive" retriever
    comprehensive_context = comprehensive_retrieval(user_topic, vector_store)
    print(f"Retrieved {len(comprehensive_context)} chunks for the topic.")

    # 2. Synthesize notes using Student 2's note generator
    english_notes = synthesize_notes(user_topic, comprehensive_context)
    print("\n[Generated English Study Notes]")
    print(english_notes)

    # 3. Translate the notes using Student 2's translation function
    sinhala_notes = translate_to_sinhala(english_notes)
    print("\n[Translated Sinhala Study Notes]")
    print(sinhala_notes)
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    # This ensures the script runs when you execute it from the command line
    run_app_logic()