# Problem Set 4C
# Name: sco1
# Collaborators:
# Time Spent: 1:00

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        # Initialize attributes per the docstring
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        # Iterate through our vowel permutation and map the shifted values
        shiftdict = {}
        for idx, vowel in enumerate(vowels_permutation):
            shiftdict[VOWELS_LOWER[idx]] = vowel.lower()
            shiftdict[VOWELS_UPPER[idx]] = vowel.upper()
        
        # Map upper and lowercase consonents to themselves
        for letter in CONSONANTS_LOWER:
            shiftdict[letter] = letter
        for letter in CONSONANTS_UPPER:
            shiftdict[letter] = letter
        
        return shiftdict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        # Short circuit on empty string
        if len(self.message_text) == 0:
            return ''

        outstr = ''  # Initialize output string
        
        # Iterate over the letters in our message text and replace where needed
        for letter in self.message_text:
            # Check to see if we have a letter that needs replacing
            if letter in transpose_dict.keys():
                outstr += transpose_dict[letter]
            else:
                # Pass through
                outstr += letter
        
        return outstr
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        # Call our superclass constructor, initializes message_text and valid_words
        super().__init__(text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        # Short circuit on empty string
        if len(self.get_message_text()) == 0:
            return self.get_message_text()
        
        vowelperms = get_permutations(VOWELS_LOWER)  # Get vowel permutations
        nvalidwords = []  # Initialize list to store number of valid words per perm
        for perm in vowelperms:
            # Generate list of words to iterate over
            testdict = self.build_transpose_dict(perm)
            teststr = self.apply_transpose(testdict)
            testwords = teststr.split()
            
            # Test each word in the list for validity
            validwords = 0
            for word in testwords:
                if is_word(self.get_valid_words(), word):
                    validwords += 1
            
            # Add number of valid words for permutation to top level list
            nvalidwords.append(validwords)

            if validwords == len(testwords):
                # If any permutation returns all valid words, break out of loop
                # and consider it the winner
                break
        
        # Find the maximum number of valid words we've found and find the
        # first corresponding index. This corresponds to the permutation to return
        maxvalid = max(nvalidwords)
        bestperm = nvalidwords.index(maxvalid)

        # Construct and return the best decryption attempt
        bestdict = self.build_transpose_dict(vowelperms[bestperm])
        return self.apply_transpose(bestdict)

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('=======')
     
    message = SubMessage('')
    permuation = ('iuoea')
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", '')
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('=======')

    message = SubMessage('This is a test string! Test, test-test')
    permutation = ('aeiou')
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", 'This is a test string! Test, test-test')
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('=======')

    message = SubMessage('This is a test string! Test, test-test')
    permutation = ('uoiea')
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", 'This is u tost string! Tost, tost-tost')
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('=======')