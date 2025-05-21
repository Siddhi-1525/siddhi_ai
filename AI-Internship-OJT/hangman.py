import random

def play_hangman():
    word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    secret_word = random.choice(word_list)
    word_length = len(secret_word)
    guessed_letters = set()
    attempts_left = 6  # You can adjust the number of attempts
    display = ['_'] * word_length

    print("Welcome to Hangman!")
    print(f"The secret word has {word_length} letters.")
    print("You have {attempts_left} attempts remaining.")
    print(" ".join(display))
    print("-" * 20)

    while attempts_left > 0 and "_" in display:
        guess = input("Guess a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You've already guessed that letter. Try again.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
            for i in range(word_length):
                if secret_word[i] == guess:
                    display[i] = guess
        else:elif
            attempts_left -= 1
            print(f"Incorrect guess. You have {attempts_left} attempts remaining.")

        print(" ".join(display))
        print(f"Guessed letters: {', '.join(sorted(list(guessed_letters)))}")
        print("-" * 20)

    if "_" not in display:
        print("Congratulations! You guessed the word:", secret_word)
    else:
        print("You ran out of attempts. The secret word was:", secret_word)

if __name__ == "__main__":
    play_hangman()