# Problem Set 2, hangman.py
# Name: sco1
# Collaborators: N/A
# Time spent: 1:15

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    else:
        return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_guessed = ['_ ']*len(secret_word)

    for idx, letter in enumerate(secret_word):
        if letter in letters_guessed:
          word_guessed[idx] = letter
    
    return(''.join(word_guessed))


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    for letter in letters_guessed:
        if letter in available_letters:
            available_letters = available_letters.replace(letter, '')
    
    return available_letters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Initial game prompts
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is %i letters long.' % len(secret_word))
    
    n_warnings = 3
    print('You have %i warnings left.' % n_warnings)
    print('­­­­­­­­­­­­­­­­­­­­­­­­­­--------------')

    # Begin main game loop
    n_guessesleft = 6
    word_guessed = False
    letters_guessed = []
    while not word_guessed and n_guessesleft > 0:
        print('You have %i guesses left.' % n_guessesleft)
        print('Available letters: %s' % get_available_letters(letters_guessed))
        guess = input('Please guess a letter: ').lower()  # Lowercase our input for easier comparison

        # Check to see if the guess is valid
        if guess in string.ascii_lowercase:
            # Valid letter entered
            if guess in letters_guessed:
                # Letter already guessed, subtract a warning if they're greater than zero, otherwise remove a guess
                if n_warnings > 0:
                    n_warnings -= 1
                    print('Oops! You\'ve already guessed that letter. You have %i warnings left.' % n_warnings)
                else:
                    print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose a guess')
                    n_guessesleft -= 1
            else:
                # Letter hasn't been guessed, add it to the list and see if it's in our word
                letters_guessed.append(guess)
                if guess in secret_word:
                    print('Good guess: %s' % get_guessed_word(secret_word, letters_guessed))
                else:
                    print('Oops! That letter is not in my word: %s' % get_guessed_word(secret_word, letters_guessed))

                word_guessed = is_word_guessed(secret_word, letters_guessed)
                if not word_guessed:
                    n_guessesleft -= 1
        else:
            if n_warnings > 0:
                n_warnings -= 1
                print('Oops! That is not a valid letter. You have %i warnings left.' % n_warnings)
            else:
                print('Oops! That is not a valid letter. You have no warnings left so you lose a guess')
                n_guessesleft -= 1

        print('­­­­­­­­­­­­­­­­­­­­­­­­­­--------------')
    
    if not word_guessed:
      # We lose :(
      print('Sorry, you ran out of guesses. The word was %s.' % secret_word)
    else:
      # We win!
      print('Congratulations, you won!')
      n_uniqueletters = len(''.join(set(secret_word)))  # Calculate number of unique letters in secret_word
      print('Your total score for this game is: %i' % (n_guessesleft * n_uniqueletters))


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(' ', '')  # Strip out whitespace

    # Do an easy length comparison first
    if len(my_word) != len(other_word):
        return False
    
    # Check remaining letters to see if they match
    for idx, letter in enumerate(my_word):
        # Check underscores to see if their corresponding letter in other_word is already in my_word
        # Because we reveal all matching letters on a guess, 'a_ ple' shouldn't match 'apple'
        if letter == '_':
            if other_word[idx] in my_word:
                return False
        else:
            # See if the letter in my_word matches that of other_word
            if my_word[idx] != other_word[idx]:
                return False
    else:
        # If we get here everything has matched
        return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    
    if len(possible_matches) == 0:
        print('No matches found')
    else:
        print(' '.join(possible_matches))


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Initial game prompts
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is %i letters long.' % len(secret_word))
    
    n_warnings = 3
    print('You have %i warnings left.' % n_warnings)
    print('­­­­­­­­­­­­­­­­­­­­­­­­­­--------------')

    # Begin main game loop
    n_guessesleft = 6
    word_guessed = False
    letters_guessed = []
    while not word_guessed and n_guessesleft > 0:
        print('You have %i guesses left.' % n_guessesleft)
        print('Available letters: %s' % get_available_letters(letters_guessed))
        guess = input('Please guess a letter: ').lower()  # Lowercase our input for easier comparison

        # Check to see if the guess is valid
        if guess in string.ascii_lowercase:
            # Valid letter entered
            if guess in letters_guessed:
                # Letter already guessed, subtract a warning if they're greater than zero, otherwise remove a guess
                if n_warnings > 0:
                    n_warnings -= 1
                    print('Oops! You\'ve already guessed that letter. You have %i warnings left.' % n_warnings)
                else:
                    print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose a guess')
                    n_guessesleft -= 1
            else:
                # Letter hasn't been guessed, add it to the list and see if it's in our word
                letters_guessed.append(guess)
                if guess in secret_word:
                    print('Good guess: %s' % get_guessed_word(secret_word, letters_guessed))
                else:
                    print('Oops! That letter is not in my word: %s' % get_guessed_word(secret_word, letters_guessed))

                word_guessed = is_word_guessed(secret_word, letters_guessed)
                if not word_guessed:
                    n_guessesleft -= 1
        else:
            if guess == '*':
                # Show our word matches
                print('Possible matches are:')
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            else:
                if n_warnings > 0:
                    n_warnings -= 1
                    print('Oops! That is not a valid letter. You have %i warnings left.' % n_warnings)
                else:
                    print('Oops! That is not a valid letter. You have no warnings left so you lose a guess')
                    n_guessesleft -= 1

        print('­­­­­­­­­­­­­­­­­­­­­­­­­­--------------')
    
    if not word_guessed:
      # We lose :(
      print('Sorry, you ran out of guesses. The word was %s.' % secret_word)
    else:
      # We win!
      print('Congratulations, you won!')
      n_uniqueletters = len(''.join(set(secret_word)))  # Calculate number of unique letters in secret_word
      print('Your total score for this game is: %i' % (n_guessesleft * n_uniqueletters))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
