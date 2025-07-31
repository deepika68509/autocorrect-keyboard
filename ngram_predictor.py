import re
import nltk
from nltk.corpus import brown, words
from nltk.util import ngrams
from collections import defaultdict, Counter
import string

# Download required NLTK data
try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown')
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

class SmartWordPredictor:
    def __init__(self, n=3):
        self.n = n
        self.ngrams = defaultdict(Counter)
        self.word_freq = Counter()
        self.common_words = set(words.words())
        
    def train(self, corpus_path=None):
        """Train on Brown corpus and custom corpus if provided"""
        # Train on Brown corpus
        brown_words = [word.lower() for word in brown.words() if word.isalpha()]
        self._build_ngrams(brown_words)
        
        # Train on custom corpus if provided
        if corpus_path:
            try:
                with open(corpus_path, 'r', encoding='utf-8') as f:
                    text = f.read().lower()
                custom_words = re.findall(r'\b\w+\b', text)
                self._build_ngrams(custom_words)
            except FileNotFoundError:
                pass
    
    def _build_ngrams(self, words):
        """Build n-gram model from word list"""
        # Build word frequency
        self.word_freq.update(words)
        
        # Build n-grams
        for ngram in ngrams(words, self.n):
            key = tuple(ngram[:-1])
            next_word = ngram[-1]
            self.ngrams[key][next_word] += 1
    
    def predict_next_words(self, context, max_predictions=5):
        """Predict next words based on context"""
        if not context:
            return self._get_most_common_words(max_predictions)
        
        # Clean and normalize context
        context_words = [word.lower().strip(string.punctuation) 
                        for word in context if word.strip(string.punctuation)]
        
        if len(context_words) < self.n - 1:
            # Not enough context, return most common words
            return self._get_most_common_words(max_predictions)
        
        # Get the last n-1 words for prediction
        key = tuple(context_words[-(self.n-1):])
        
        if key in self.ngrams:
            # Get predictions from n-gram model
            predictions = self.ngrams[key].most_common(max_predictions)
            return [word for word, count in predictions]
        else:
            # Fallback to most common words
            return self._get_most_common_words(max_predictions)
    
    def _get_most_common_words(self, max_predictions):
        """Get most common words as fallback"""
        return [word for word, count in self.word_freq.most_common(max_predictions)]
    
    def get_word_suggestions(self, partial_word, context=None, max_suggestions=5):
        """Get word suggestions for partial input"""
        if not partial_word:
            return self.predict_next_words(context, max_suggestions)
        
        partial_word = partial_word.lower()
        suggestions = []
        
        # Get context-based predictions
        if context:
            context_predictions = self.predict_next_words(context, max_suggestions * 2)
            for word in context_predictions:
                if word.startswith(partial_word) and word not in suggestions:
                    suggestions.append(word)
                    if len(suggestions) >= max_suggestions:
                        break
        
        # Add common words that start with the partial word
        for word, freq in self.word_freq.most_common():
            if word.startswith(partial_word) and word not in suggestions:
                suggestions.append(word)
                if len(suggestions) >= max_suggestions:
                    break
        
        return suggestions[:max_suggestions]