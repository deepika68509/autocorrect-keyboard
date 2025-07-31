# Smart Autocorrect & Word Prediction Keyboard

A modern, intelligent keyboard system built with Python and Streamlit that provides:
- **Autocorrect** for misspelled words
- **Next-word prediction** using NLTK n-grams
- **Word completion** suggestions
- **Real-time, interactive UI** inspired by Google Keyboard

## Features

- 🔧 **Autocorrect**: Instantly fixes misspelled words as you type
- 🔮 **Next-word prediction**: Suggests the next word based on context
- ✏️ **Word completion**: Completes partial words in real-time
- 💡 **Smart suggestions**: All suggestions appear below the input box
- 🚀 **One-click apply**: Click any suggestion to instantly update your text
- 🎨 **Cool UI**: Gradient backgrounds, animated buttons, and live stats

## Demo

![Demo Screenshot](demo_screenshot.png)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

## How It Works
- **Autocorrect** uses `pyspellchecker` to detect and suggest corrections for misspelled words.
- **Next-word prediction** uses an NLTK n-gram model trained on the Brown corpus and your custom corpus.
- **Word completion** uses context and partial input to suggest completions.
- **UI** is built with Streamlit and custom CSS for a modern, interactive experience.

## Project Structure
```
├── app.py                # Main Streamlit app
├── autocorrect.py        # SpellChecker logic
├── ngram_predictor.py    # NLTK n-gram predictor
├── requirements.txt      # Dependencies
├── data/
│   └── corpus.txt        # Custom corpus for n-gram training
└── README.md             # This file
```

## Customization
- To improve predictions, add more text to `data/corpus.txt`.
- You can further enhance the UI or add more advanced ML models as needed.

## License
MIT

---

> Built with ❤️ using Python, NLTK, and Streamlit.