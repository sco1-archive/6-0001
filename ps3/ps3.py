# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : sco1
# Collaborators : N/A
# Time spent    : 1:15

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    word = word.lower()  # Force lowercase to simplify handling
    wordlength = len(word)

    wordscore = 0
    # Iterate over our letters to sum their points
    for letter in word:
        if letter != '*':  # Don't give points for wildcard
            wordscore = wordscore + SCRABBLE_LETTER_VALUES[letter]

    wordscore = wordscore * max((7*wordlength - 3*(n-wordlength)), 1)  # Multiply by second component
    
    return wordscore

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):  # Subtract 1 here to make room for the wildcard without messing up the consonants
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    hand['*'] = 1  # Add wildcard in place of one of the vowels
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    updated_hand = hand.copy()  # Create a copy of our dict so we don't overwrite it
    for letter in word.lower():  # Lowercase our word for simpler comparison
        if updated_hand.get(letter) is not None:  # Make sure our letter is still here
            # If our letter count is > 0, subtract one. Otherwise leave it alone
            if updated_hand[letter] > 0:
                updated_hand[letter] -= 1
    
    return updated_hand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()  # Lowercase our word for easier comparison
    hand_copy = hand.copy()  # Copy our hand so we don't mutate it
    if word in word_list:
        # Word is in our list, see if it's a valid play
        for letter in word:
            if hand_copy.get(letter) is not None:   # See if our letter is in the hand
                # If our letter count is > 0, subtract one. If we're zero then we've used up all the letters
                if hand_copy[letter] > 0:
                    hand_copy[letter] -= 1
                else: 
                    return False
            else:
                # Letter not in hand, invalid word
                return False
        else:
            # If we get here then our word is valid
            return True
    else:
        # Check for a wildcard, '*'
        if '*' in word:
            for vowel in VOWELS:
                # Iterate over our vowels, replace the wildcard, and see if it makes a valid word
                voweled_word = word.replace('*', vowel)
                voweled_hand = hand.copy()  # Make a copy to mess with wildcard key
                voweled_hand[vowel] = voweled_hand.pop('*')  # Replace the wildcard key with our vowel
                if is_valid_word(voweled_word, voweled_hand, word_list):
                    return True
            else:
                # If we get here, we never matched a voweled word
                return False

        else:
            # Word isn't in our list, and there's no wildcard, so it's invalid
            return False

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    handlen = 0
    for key in hand:
        handlen = handlen + hand[key]
    
    return handlen

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # Initialize our constants
    totalscore = 0

    # Prompt our user for guesses as long as we have letters in our hand
    while calculate_handlen(hand) > 0:
        print('Current Hand: ', end='')  # End the line without a newline so we can use display_hand
        display_hand(hand)
        word = input('Enter word, or "!!" to indicate that you are finished: ')  # Prompt for word
        if word == '!!':
            # User wants to end turn
            break
        else:
            # Check to see if the word is valid
            if is_valid_word(word, hand, word_list):
                # Valid word, update our score
                points_earned = get_word_score(word, HAND_SIZE)
                totalscore += points_earned
                print('"%s" earned %i points. Total: %i points' % (word, points_earned, totalscore))
            else:
                print('That is not a valid word. Please choose another word.')
            # Remove the letters regardless of whether or not the word is valid
            hand = update_hand(hand, word)
    return totalscore
#
# Problem #6: Playing a game
# 
#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    newhand = hand.copy()  # Make a copy of our hand to keep original untouched
    if letter in hand:  # See if our substitute letter is in our hand, do nothing if it's not
        newletter = random.choice(VOWELS + CONSONANTS)  # Make a random selection from all the letters
        newhand[newletter] = newhand.pop(letter) # Swap our old letter for the new one

    return newhand
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    totalscore = 0 # Initialize our score
    nreplays = 1  # Number of replays
    oldhandscore = 0  # Temporary hand score storage for replays
    subflagbool = True  # Set whether or not we ask for a substitution

    # Prompt user to input total number of hands
    nhandsleft = int(input('Enter total number of hands: '))  # Force integer input
    hand = deal_hand(HAND_SIZE)  # Deal the first hand here to make hand replay logic easier
    while nhandsleft > 0:  # Iterate until we run out of hands
        # Deal and display our hand for the round
        print('Current Hand: ', end='')  # End the line without a newline so we can use display_hand
        display_hand(hand)

        if subflagbool:
            subletter = input('Would you like to substitute a letter (Y/N)? ')
            if subletter.lower() == 'y':  # Use lower for easier comparison
                # Substitute our letter
                lettertoreplace = input('Which letter would you like to replace? ')
                handtoplay = substitute_hand(hand, lettertoreplace)
            elif subletter.lower() == 'n':
                # Don't substitute letter'
                handtoplay = hand.copy()
            else:
                # Catch invalid inputs
                print('Unrecognized input "%s", skipping letter substitution' % subletter)
                handtoplay = hand.copy()
        else:
            handtoplay = hand.copy
        
        handscore = play_hand(handtoplay, word_list)
        print('Ran out of letters')
        print('Total score for this hand: %i' % handscore)
        print('='*7)

        if nreplays > 0:
            toreplay = input('Would you like to replay the hand (Y/N)? ')
            if toreplay.lower() == 'y':  # Use lower for easier comparison
                # Replay the hand
                nreplays -= 1  # Remove a replay from our pool
                oldhandscore = handscore
                subflagbool = False  # Switch off our substitution prompt
                continue  # Skip round finishing
            elif toreplay.lower() == 'n':
                # Don't replay, continue to end of round
                pass
            else:
                # Catch invalid inputs
                print('Unrecognized input "%s", ending round' % toreplay)

        # Finish the round
        totalscore += max(handscore, oldhandscore)  # Update the score, if we've replayed use the higher of the two
        oldhandscore = 0  # Reset old score
        nhandsleft -= 1  # Update the number of hands left
        hand = deal_hand(HAND_SIZE)  # Deal new hand
        subflagbool = True  # Turn substitution prompt on
    
    # Print our final score
    print('')  # Print blank line
    print('Total score for all hands: %i' % totalscore)

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
