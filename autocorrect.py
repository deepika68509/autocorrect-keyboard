from spellchecker import SpellChecker

spell = SpellChecker()

def correct_word(word):
    if word in spell:
        return word, []
    suggestions = list(spell.candidates(word))
    return spell.correction(word), suggestions