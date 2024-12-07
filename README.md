import re

# Load an English dictionary
def load_dictionary():
    try:
        with open("/usr/share/dict/words", "r") as f:
            return set(word.strip().upper() for word in f)
    except FileNotFoundError:
        print("Dictionary file not found! Using a basic hardcoded dictionary.")
        return {"THIS", "IS", "A", "TEST", "EXAMPLE", "CRYPTOGRAM", "HAS", "NO", "SOLUTION", "AREN'T", "ISN'T"}

ENGLISH_WORDS = load_dictionary()

def is_english_word(word):
    """Check if a word is valid English."""
    clean_word = re.sub(r"[^A-Z]", "", word)  # Remove punctuation for validation
    return clean_word in ENGLISH_WORDS

def decrypt_cryptogram(cryptogram):
    """Attempt to solve the cryptogram."""
    words = re.findall(r"[A-Z']+", cryptogram)  # Extract words, keeping contractions
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
        possible_words = sorted(
            [word for word in ENGLISH_WORDS
             if len(re.sub(r"[^A-Z]", "", word)) == len(re.sub(r"[^A-Z]", "", current_word))]
        )

        # If no possible words remain, backtrack
        if not possible_words:
            return

        for pw in possible_words:
            temp_mapping = mapping.copy()
            valid = True

            for c, p in zip(current_word, pw):
                if c.isalpha():
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
        return "NO SOLUTION FOUND", words

    # Generate decrypted text from the best solution
    best_solution = solutions[0]
    decrypted_words = []
    for word in words:
        decrypted_word = "".join(best_solution.get(c, c) if c.isalpha() else c for c in word)
        decrypted_words.append(decrypted_word)

    # Identify original cryptogram words that are non-English
    non_english_words = []
    for original_word, decrypted_word in zip(words, decrypted_words):
        if not is_english_word(decrypted_word):  # Check if the decrypted word is valid English
            non_english_words.append(original_word)  # Flag the original cryptogram word

    # If all words are flagged as non-English, return failure
    if len(non_english_words) == len(words):
        return "NO SOLUTION FOUND", words

    return " ".join(decrypted_words), non_english_words


# Main Program
def main():
    print("Enter your cryptogram (uppercase, punctuation preserved):")
    cryptogram = input().strip().upper()

    # Retain punctuation for better usability
    try:
        solution, non_english = decrypt_cryptogram(cryptogram)

        if solution == "NO SOLUTION FOUND":
            print("Answer:\nTHIS CRYPTOGRAM HAS NO SOLUTION.")
        else:
            print(f"Decrypted Text: {solution}")

        if non_english:
            print(f"Non-English words: {', '.join(non_english)}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
