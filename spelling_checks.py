import argparse
import os
import fitz  # PyMuPDF
import language_tool_python
from spellchecker import SpellChecker

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            # Extract text from each page
            text += page.get_text()
        return text

def check_grammar_and_spelling(text, log_file):
    # Initialize the language tool for grammar check with British English
    language_tool = language_tool_python.LanguageTool('en-GB', config={'disabledRuleIds': 'EN_SPLIT_WORDS_HYPHEN,OXFORD_SPELLING_Z_NOT_S'})

    # Initialize the spell checker
    spell = SpellChecker(language='en')

    # Open log file for writing
    with open(log_file, 'w') as log:
        # Check grammar
        grammar_matches = language_tool.check(text)
        for match in grammar_matches:
            log.write(f"Grammar issue: {match}\n")

        # Tokenize the text into words for spell checking
        words = text.split()
        # Find those words that may be misspelled
        misspelled = spell.unknown(words)
        for word in misspelled:
            # Get the one `most likely` answer
            correct_word = spell.correction(word)
            log.write(f"Mispelled word: {word}, Suggestion: {correct_word}\n")

def main(pdf_path):
    # Extract the base name of the PDF file to create a corresponding log file
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    log_file = f"{base_name}.log"

    pdf_text = extract_text_from_pdf(pdf_path)
    check_grammar_and_spelling(pdf_text, log_file)
    print(f"Grammar and spelling check completed. Results have been saved to {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Grammar and Spelling Checker")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file to be checked")
    args = parser.parse_args()

    main(args.pdf_path)
