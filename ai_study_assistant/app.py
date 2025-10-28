import os
import streamlit as st
from dotenv import load_dotenv

# Custom CSS to control font sizes, especially for Sinhala headers
custom_css = """
<style>
    /* Target all headers (h1, h2, h3) within the main Streamlit block */
    .stApp h1, .stApp h2, .stApp h3 {
        font-size: 1.5em !important; /* Reduce header size. Adjust '1.5em' as needed. */
    }
    
    /* You can be more specific if needed */
    .stApp h3 {
        font-size: 1.25em !important; /* Specifically target level 3 headers */
    }
</style>
"""

# Load environment variables
load_dotenv()

# Import the functions from the other team members' modules
from study_assistant.retrieval import (
    function_A as build_vector_store,
    function_B_precise_retrieval as get_precise_context,
    function_C_comprehensive_retrieval as get_comprehensive_context,
)
from study_assistant.generation import (
    function_X_generate_answer as generate_answer,
    function_Y_synthesize_notes as synthesize_notes,
    translate_to_sinhala,
)

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# --- ADD THE CSS INJECTION HERE ---
st.markdown(custom_css, unsafe_allow_html=True)
# --- END OF ADDITION ---

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "qa_messages" not in st.session_state:
    st.session_state.qa_messages = []
if "notes_messages" not in st.session_state:
    st.session_state.notes_messages = []
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "language" not in st.session_state:
    st.session_state.language = "English"

# Main title
st.title("📚 AI Study Assistant")
st.markdown("---")

# Sidebar for PDF upload and settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language selection
    language = st.selectbox(
        "🌐 Select Language",
        ["English", "සිංහල (Sinhala)"],
        index=0 if st.session_state.language == "English" else 1,
        help="Choose the language for displaying answers"
    )
    st.session_state.language = language
    
    st.markdown("---")
    st.header("📄 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Upload a PDF file to start asking questions or generating notes"
    )
    
    if uploaded_file is not None and not st.session_state.pdf_processed:
        with st.spinner("Processing document... This may take a moment."):
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Build vector store
                st.session_state.vector_store = build_vector_store(temp_path)
                st.session_state.pdf_processed = True
                st.success("✅ Document processed successfully!")
                
                # Clean up temp file
                os.remove(temp_path)
            except Exception as e:
                st.error(f"❌ Error processing document: {e}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    if st.session_state.pdf_processed:
        st.success("📄 Document ready for queries")
        if st.button("🔄 Upload New Document"):
            st.session_state.vector_store = None
            st.session_state.pdf_processed = False
            st.session_state.qa_messages = []
            st.session_state.notes_messages = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("### About")
    st.info(
        "This AI Study Assistant helps you:\n"
        "- **Q&A**: Get precise answers to specific questions\n"
        "- **Notes**: Generate comprehensive study notes on topics"
    )

# Helper function to display messages with translation toggle
def display_message_with_translation(content_dict, message_key):
    """Display message with primary content and optional translation dropdown"""
    is_sinhala = st.session_state.language == "සිංහල (Sinhala)"
    
    # Display primary content based on selected language
    primary_content = content_dict["sinhala"] if is_sinhala else content_dict["english"]
    secondary_content = content_dict["english"] if is_sinhala else content_dict["sinhala"]
    
    primary_label = "සිංහල පිළිතුර:" if is_sinhala else "English Answer:"
    secondary_label = "English Translation" if is_sinhala else "සිංහල Translation"
    
    st.markdown(primary_content)
    
    # Show translation in expander
    with st.expander(f"🔄 View {secondary_label}"):
        st.markdown(secondary_content)

# Main content area with tabs
tab1, tab2 = st.tabs(["💬 Question Answering", "📝 Note Generation"])

# Tab 1: Question Answering
with tab1:
    st.header("Ask Questions About Your Document")
    
    if not st.session_state.pdf_processed:
        st.info("👈 Please upload a PDF document from the sidebar to start asking questions.")
    else:
        # Display chat messages
        for i, message in enumerate(st.session_state.qa_messages):
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    # Assistant message with translation
                    display_message_with_translation(message["content"], f"qa_{i}")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your document..."):
            # Add user message to chat history
            st.session_state.qa_messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Retrieve precise context
                        context_docs = get_precise_context(
                            prompt, 
                            st.session_state.vector_store, 
                            k=4
                        )
                        
                        # Generate answer
                        english_answer = generate_answer(prompt, context_docs)
                        
                        # Translate to Sinhala
                        sinhala_answer = translate_to_sinhala(english_answer)
                        
                        # Store both versions
                        content_dict = {
                            "english": english_answer,
                            "sinhala": sinhala_answer
                        }
                        
                        # Display based on selected language
                        display_message_with_translation(
                            content_dict, 
                            f"qa_{len(st.session_state.qa_messages)}"
                        )
                        
                        # Store assistant response with both versions
                        st.session_state.qa_messages.append({
                            "role": "assistant", 
                            "content": content_dict
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating answer: {e}")

# Tab 2: Note Generation
with tab2:
    st.header("Generate Study Notes on Topics")
    
    if not st.session_state.pdf_processed:
        st.info("👈 Please upload a PDF document from the sidebar to start generating notes.")
    else:
        # Display chat messages
        for i, message in enumerate(st.session_state.notes_messages):
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    # Assistant message with translation
                    display_message_with_translation(message["content"], f"notes_{i}")
        
        # Chat input
        if topic := st.chat_input("Enter a topic to generate study notes..."):
            # Add user message to chat history
            st.session_state.notes_messages.append({"role": "user", "content": topic})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(topic)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Generating comprehensive notes... This may take longer."):
                    try:
                        # Retrieve comprehensive context
                        context_docs = get_comprehensive_context(
                            topic, 
                            st.session_state.vector_store, 
                            threshold=0.65
                        )
                        
                        # Synthesize notes
                        english_notes = synthesize_notes(topic, context_docs)
                        
                        # Translate to Sinhala (translate line by line to preserve structure)
                        # Split by lines, translate non-empty lines, preserve structure
                        lines = english_notes.split('\n')
                        translated_lines = []
                        
                        for line in lines:
                            stripped_line = line.strip()
                            if stripped_line:
                                # Detect and preserve different markdown elements
                                
                                # Check for headers (###, ##, #)
                                if stripped_line.startswith('#'):
                                    # Count the number of # symbols
                                    hash_count = 0
                                    for char in stripped_line:
                                        if char == '#':
                                            hash_count += 1
                                        else:
                                            break
                                    
                                    prefix = '#' * hash_count + ' '
                                    content = stripped_line[hash_count:].strip()
                                    translated_content = translate_to_sinhala(content)
                                    translated_lines.append(prefix + translated_content)
                                
                                # Check for bullet points (* or -)
                                elif stripped_line.startswith('* ') or stripped_line.startswith('- '):
                                    prefix = stripped_line[0:2]  # '* ' or '- '
                                    content = stripped_line[2:].strip()
                                    translated_content = translate_to_sinhala(content)
                                    translated_lines.append(prefix + translated_content)
                                
                                # Check for bold text markers
                                elif stripped_line.startswith('**') and stripped_line.endswith('**'):
                                    content = stripped_line[2:-2]
                                    translated_content = translate_to_sinhala(content)
                                    translated_lines.append('**' + translated_content + '**')
                                
                                else:
                                    # Regular line - translate as is
                                    translated_lines.append(translate_to_sinhala(stripped_line))
                            else:
                                # Preserve empty lines
                                translated_lines.append('')
                        
                        sinhala_notes = '\n'.join(translated_lines)
                        
                        # Store both versions
                        content_dict = {
                            "english": english_notes,
                            "sinhala": sinhala_notes
                        }
                        
                        # Display based on selected language
                        display_message_with_translation(
                            content_dict,
                            f"notes_{len(st.session_state.notes_messages)}"
                        )
                        
                        # Store assistant response with both versions
                        st.session_state.notes_messages.append({
                            "role": "assistant", 
                            "content": content_dict
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating notes: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "AI Study Assistant | Powered by Local Transformer Models"
    "</div>",
    unsafe_allow_html=True
)