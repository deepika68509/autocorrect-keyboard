import streamlit as st
from autocorrect import correct_word
from ngram_predictor import SmartWordPredictor
import os

# Custom CSS for better styling
st.set_page_config(page_title="Smart Keyboard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .suggestion-box {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .suggestion-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .suggestion-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .autocorrect-suggestion {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
    }
    
    .prediction-suggestion {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
    }
    
    .completion-suggestion {
        background: linear-gradient(45deg, #a8edea, #fed6e3);
        color: #333;
    }
    
    .input-container {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the smart word predictor
@st.cache_resource
def load_predictor():
    predictor = SmartWordPredictor(n=3)
    predictor.train()  # Train on Brown corpus
    return predictor

predictor = load_predictor()

# Initialize session state
if 'main_input' not in st.session_state:
    st.session_state.main_input = ""
if 'suggestion_clicked' not in st.session_state:
    st.session_state.suggestion_clicked = False
if 'new_text' not in st.session_state:
    st.session_state.new_text = ""

# Callback function for suggestions
def apply_suggestion(suggestion_type, suggestion, current_words, current_input):
    if suggestion_type == "autocorrect":
        # Replace the current word
        new_words = current_words[:-1] + [suggestion]
        st.session_state.new_text = " ".join(new_words)
    elif suggestion_type == "prediction":
        # Add the predicted word
        st.session_state.new_text = current_input + " " + suggestion
    elif suggestion_type == "completion":
        # Replace current word with completion
        new_words = current_words[:-1] + [suggestion]
        st.session_state.new_text = " ".join(new_words)
    
    st.session_state.suggestion_clicked = True

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 Smart Autocorrect & Word Prediction Keyboard</h1>
    <p>Type below and get real-time suggestions like Google Keyboard!</p>
</div>
""", unsafe_allow_html=True)

# Handle suggestion clicks
if st.session_state.suggestion_clicked:
    st.session_state.main_input = st.session_state.new_text
    st.session_state.suggestion_clicked = False
    st.session_state.new_text = ""

# Input container
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Text input with real-time suggestions
    user_input = st.text_input(
        "Start typing here...",
        value=st.session_state.main_input,
        key="main_input",
        placeholder="Type your message and see real-time suggestions below..."
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Real-time suggestions container
if user_input:
    words = user_input.strip().split()
    
    if words:
        current_word = words[-1]
        context_words = words[:-1] if len(words) > 1 else []
        
        # Check if current word is complete (ends with space or punctuation)
        is_complete_word = current_word.endswith((' ', '.', ',', '!', '?'))
        
        # Get suggestions based on current state
        suggestions = []
        
        # Autocorrect suggestions
        if current_word and not is_complete_word:
            corrected, autocorrect_suggestions = correct_word(current_word)
            if corrected != current_word:
                suggestions.append(("🔧 Autocorrect", corrected, "autocorrect"))
            for suggestion in autocorrect_suggestions[:2]:
                suggestions.append(("✨ Suggestion", suggestion, "autocorrect"))
        
        # Word predictions and completions
        if is_complete_word or not current_word:
            # Predict next words based on context
            predictions = predictor.predict_next_words(context_words, max_predictions=5)
            for prediction in predictions:
                suggestions.append(("🔮 Next Word", prediction, "prediction"))
        else:
            # Suggest completions for current partial word
            completions = predictor.get_word_suggestions(current_word, context_words, max_suggestions=5)
            for completion in completions:
                suggestions.append(("✏️ Complete", completion, "completion"))
        
        # Display suggestions in a cool box
        if suggestions:
            st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
            st.markdown("### 💡 Smart Suggestions")
            
            # Create columns for suggestions
            cols = st.columns(min(3, len(suggestions)))
            
            for idx, (label, suggestion, suggestion_type) in enumerate(suggestions):
                col_idx = idx % len(cols)
                with cols[col_idx]:
                    if st.button(
                        f"{label}: **{suggestion}**",
                        key=f"suggestion_{idx}",
                        help=f"Click to use '{suggestion}'"
                    ):
                        apply_suggestion(suggestion_type, suggestion, words, user_input)
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics
        with st.container():
            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words Typed", len(words))
            with col2:
                st.metric("Characters", len(user_input))
            with col3:
                st.metric("Suggestions Available", len(suggestions))
            st.markdown('</div>', unsafe_allow_html=True)

# Tips and controls
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    ### 🎯 Features:
    - **🔧 Autocorrect**: Automatically fixes misspelled words
    - **🔮 Word Predictions**: Suggests the next word based on context
    - **✏️ Word Completions**: Completes partial words as you type
    - **💡 Smart Suggestions**: Real-time suggestions appear below as you type
    - **🚀 One-Click Apply**: Click any suggestion to instantly apply it
    """)

with col2:
    if st.button("🗑️ Clear All", type="primary"):
        st.session_state.main_input = ""
        st.rerun()
    
    if st.button("📋 Copy Text"):
        st.write("📋 Text copied to clipboard!")
        st.code(user_input)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 Powered by NLTK & Streamlit | Smart Keyboard v2.0</p>
</div>
""", unsafe_allow_html=True)