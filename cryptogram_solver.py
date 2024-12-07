import re

# Load an English dictionary
def load_dictionary():
    try:
        with open("/usr/share/dict/words", "r") as f:
            return set(word.strip().upper() for word in f)
    except FileNotFoundError:
        print("Dictionary file not found! Using a basic hardcoded dictionary.")
        return {"THIS", "IS", "A", "TEST", "EXAMPLE", "CRYPTOGRAM", "HAS", "NO", "SOLUTION"}

ENGLISH_WORDS = load_dictionary()

def is_english_word(word):
    """Check if a word is valid English."""
    clean_word = re.sub(r"[^A-Z]", "", word)  # Remove punctuation for validation
    return clean_word in ENGLISH_WORDS

def generate_best_guess(word):
    """
    Generate a "best guess" for a non-English word by:
    - Suggesting dictionary words with similar lengths or letter overlaps.
    """
    word_length = len(word)
    guesses = [w for w in ENGLISH_WORDS if len(w) == word_length]
    if not guesses:
        return ["No suggestion"]
    return guesses[:3]  # Return up to three best guesses

def decrypt_cryptogram(cryptogram):
    """Attempt to solve the cryptogram."""
    words = cryptogram.split()
    solutions = []
    MAX_RECURSION_DEPTH = 1000
    recursion_depth = 0

    # Recursive function to solve the cryptogram
    def solve(mapping, index):
        nonlocal recursion_depth
        recursion_depth += 1
        if recursion_depth > MAX_RECURSION_DEPTH:
            return  # Stop if recursion depth exceeds limit

        if index == len(words):  # All words processed
            solutions.append(mapping)
            return

        current_word = words[index]
        possible_words = [word for word in ENGLISH_WORDS if len(word) == len(current_word)]

        # If no possible words remain, backtrack
        if not possible_words:
            return

        for pw in possible_words:
            temp_mapping = mapping.copy()
            valid = True

            for c, p in zip(current_word, pw):
                if c in temp_mapping:
                    if temp_mapping[c] != p:
                        valid = False
                        break
                elif p in temp_mapping.values():
                    valid = False
                    break
                else:
                    temp_mapping[c] = p

            if valid:
                solve(temp_mapping, index + 1)

    solve({}, 0)

    # If no solutions were found, return no solution
    if not solutions:
        non_english_words = [word for word in words if not is_english_word(word)]
        best_guesses = {word: generate_best_guess(word) for word in non_english_words[:3]}
        return "NO SOLUTION FOUND", best_guesses

    # Generate decrypted text
    best_solution = solutions[0]
    decrypted_words = ["".join(best_solution.get(c, c) for c in word) for word in words]

    # Identify non-English words
    non_english_words = [word for word, decrypted_word in zip(words, decrypted_words) if not is_english_word(decrypted_word)]
    best_guesses = {word: generate_best_guess(word) for word in non_english_words[:3]}
    return " ".join(decrypted_words), best_guesses

# Main Program
def main():
    print("Enter your cryptogram (uppercase, punctuation preserved):")
    cryptogram = input().strip().upper()

    # Extract only letters and preserve punctuation
    pattern = r"[A-Z]+|[^A-Z\s]"
    matches = re.findall(pattern, cryptogram)
    clean_cryptogram = " ".join([m if m.isalpha() else "" for m in matches])

    try:
        solution, non_english = decrypt_cryptogram(clean_cryptogram)

        if solution == "NO SOLUTION FOUND":
            print("Answer:\nTHIS CRYPTOGRAM HAS NO SOLUTION.")
            if non_english:
                for word, guesses in non_english.items():
                    print(f"Non-English word: '{word}', Best guesses: {', '.join(guesses)}")
        else:
            print(f"Decrypted Text: {solution}")
            if non_english:
                print("Non-English words detected:")
                for word, guesses in non_english.items():
                    print(f"'{word}': Best guesses: {', '.join(guesses)}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
