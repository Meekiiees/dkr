# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

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
    secret_word_set = set(secret_word)
    letters_guessed_set = set(letters_guessed)

    if secret_word_set <= letters_guessed_set:
        return True
    else:
        return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    res = []
    for i in range(len(secret_word)):
        if list(secret_word)[i] not in letters_guessed:
            res += '_ '
        else:
            res += secret_word[i]
    res = ''.join(res)
    
    return res



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    res = string.ascii_lowercase
    for let in letters_guessed:
        res = res.replace(let, '')
    
    return res



def is_available_symbol(symbol, letters_guessed):
  '''
    symbol: string, the letter the user is inputing
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: True if symbol length is 1 , symbol is a letter from latin alphabet and is not in letters_guessed;
      0 if symbol is *
      False otherwise
    '''
  symbol = symbol.lower()
  if len(symbol) != 1:
    print('Oops! That is not a valid letter.')
    return False

  elif symbol not in string.ascii_lowercase:
    print('Oops! That is not a valid letter.')
    if symbol == '*':
      return 0
    return False
    
  elif symbol in letters_guessed:
    print("Oops! You've already guessed this letter.")
    return False

  return True



def print_remaining_opportunities(guesses, letters_guessed):
  '''print value guesses and available letters for letters_guessed with comments'''
  print('-'*25)
  print(f'You have {guesses} guesses left')
  print(f'Available letters: {get_available_letters(letters_guessed)}')    

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
    warnings = 3
    guesses = 6
    letters_guessed = []

    print(f'Welcome to the game Hangman!', f'I am thinking of a word that is {len(secret_word)} letters long.', f'You have {warnings} warnings left', sep='\n')
    
    while True:
        print_remaining_opportunities(guesses, letters_guessed)
        entered = input('Please guess a letter: ').lower()
        
        if is_available_symbol(entered, letters_guessed) == True:
            letters_guessed.append(entered)
            if entered in secret_word:
                print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                print(f'Oops! This letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
                if entered in 'euioa':
                    guesses -=2
                else:
                    guesses -=1
                if guesses <= 0:
                    print(f'Sorry, you rang out of guesses. The word was {secret_word}.')
                    break
            if is_word_guessed(secret_word, letters_guessed):
                print(f"Congratulations, you won!\nYour total score for this game is: {guesses * len(set(secret_word))}")
                break             
        else:
            if warnings != 0:
                warnings -=1
                print(f'{warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                guesses -=1
                warnings = 3
                print(f"You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
                if guesses <= 0:
                        print(f'Sorry, you rang out of guesses. The word was {secret_word}.')
                        break



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
    my_word = my_word.replace(" ", "")
    my_word_l = list(my_word)
    other_word_l = list(other_word)
    marker = 0
    if len(other_word_l) != len(my_word_l):
        return False
    for i in range(len(my_word_l)):
        if my_word_l[i] != '_':
            if my_word_l[i] != other_word_l[i]:
                marker = 1
        else:
            if other_word_l[i] in set(my_word.replace('_ ', '')):
                return False
    if marker == 1:
        return False
    else:
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
    res = []
    for word in wordlist:
        if match_with_gaps(my_word, word) == True:
            res.append(word)
    if res == []:
        res += 'No matches found'
    return ' '.join(res)



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
    warnings = 3
    guesses = 6
    letters_guessed = []

    print(f'Welcome to the game Hangman!', f'I am thinking of a word that is {len(secret_word)} letters long.', f'You have {warnings} warnings left', sep='\n')
    while True:
        print_remaining_opportunities(guesses, letters_guessed)
        entered = input('Please guess a letter: ').lower()
        is_available = is_available_symbol(entered, letters_guessed)
        if is_available == True:
            if entered != '*': letters_guessed.append(entered); 
            if entered in secret_word:
                print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                print(f'Oops! This letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
                if entered in 'euioa':
                    guesses -=2
                else:
                    guesses -=1
                if guesses <= 0:
                    print(f'Sorry, you rang out of guesses. The word was {secret_word}.')
                    break
            if is_word_guessed(secret_word, letters_guessed):
                print(f"Congratulations, you won!\nYour total score for this game is: {guesses * len(set(secret_word))}")
                break             
        elif is_available == 0:
          print(f'Possible word matches are: {show_possible_matches(get_guessed_word(secret_word, letters_guessed))}')
        else:
            if warnings != 0:
                warnings -=1
                print(f'{warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                guesses -=1
                warnings = 3
                print(f"You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
                if guesses <= 0:
                        print(f'Sorry, you rang out of guesses. The word was {secret_word}.')
                        break


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