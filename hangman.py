# Problem Set 2, hangman.py
# Name: MacGuffin_
# Collaborators: None, I run solo baby
# Time spent: like 3 hours? match_with_gaps() took at least a 3rd of that for that tasty 1-liner

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

# ----------------------------------

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
    return set(secret_word) <= set(letters_guessed)
        # all symbols in secret_word are in letters_guessed too.

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess = ''
    for char in secret_word:
        if char in letters_guessed:
            guess += char
        else:
            guess += '_'
    
    return guess



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            available_letters += char
        # I know I can make this into 1 line somehow, /shrug
        
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
    # Initialize Variables
    guesses_left = 6
    warns_left = 3
    letters_guessed = []
    
    # Welcome Message
    print('Lets hang someone!')
    print('There are',len(secret_word),'letters in the word')
    print('--------------------')
    
    # Game Loop
    while is_word_guessed(secret_word,letters_guessed) == False:
        print('You have',guesses_left,'guesses left')
        print('and',warns_left,'warnings left')
        print('Available letters:',get_available_letters(letters_guessed))
        
        # user input
        guess = str.lower(input('Input your guess: ',))
        letters_guessed += guess
        
        
        if not str.isalpha(guess):
            print('You absolute buffoon, "',guess,'" is not a letter...')
            warns_left -= 1
            if warns_left == 0:
                print("You clearly don't understand this game, you lose")
                break
        
        elif guess not in secret_word:
            print('The letter "',guess,'" is not in the word...')
            guesses_left -= 1
            if guesses_left == 0:
                print('and, you killed him')
                print('The word was:',secret_word)
                break
            
        else:
            print('The letter "',guess,'" is in the word!')
            if is_word_guessed(secret_word,letters_guessed):
                print('You won! The secret word was indeed:',secret_word)
                print('Your score: ',guesses_left*len(secret_word))
                break
            
        print(get_guessed_word(secret_word,letters_guessed))
        print('--------------------')
    
    
        

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
    my_word.strip()
    other_word.strip()
    return (all([char1 == char2 or char1 == '_' and char2 not in my_word for char1, char2 in zip(my_word, other_word)]) and len(my_word) == len(other_word))



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_) cannot be one of the letters in the word
             that has already been revealed.
    '''
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    
    if possible_matches == []:
        print('No possible matches, how did this happen?')
    else:
        print('Possible matches:', ", ".join(possible_matches))


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
    # Initialize Variables
    guesses_left = 6
    hints_left = 5
    warns_left = 3
    letters_guessed = []
    
    # Welcome Message
    print('Lets hang someone!')
    print('There are',len(secret_word),'letters in the word')
    print('--------------------')
    
    # Game Loop
    while is_word_guessed(secret_word,letters_guessed) == False:
        print('You have',guesses_left,'guesses left')
        print('and',warns_left,'warnings left')
        print('and',hints_left,'hints left')
        print('Available letters:',get_available_letters(letters_guessed))
        
        # user input
        guess = str.lower(input('Input your guess: ',))
        letters_guessed += guess
        my_word = get_guessed_word(secret_word,letters_guessed)
        
        if guess == '*':
            if hints_left > 0:
                print(show_possible_matches(my_word))
                hints_left -= 1
            else:
                print("Oops, you're out of hints")
            
        elif not str.isalpha(guess):
            print('You absolute buffoon, "',guess,'" is not a letter...')
            warns_left -= 1
            if warns_left == 0:
                print("You clearly don't understand this game, you lose")
                break
                    
        elif guess not in secret_word:
            print('The letter "',guess,'" is not in the word...')
            guesses_left -= 1
            if guesses_left == 0:
                print('and, you killed him')
                print('The word was:',secret_word)
                break
            
        else:
            print('The letter "',guess,'" is in the word!')
            if is_word_guessed(secret_word,letters_guessed):
                print('You won! The secret word was indeed:',secret_word)
                print('Your score: ',guesses_left*len(secret_word)*hints_left)
                break
            
        print(my_word)
        print('--------------------')


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
