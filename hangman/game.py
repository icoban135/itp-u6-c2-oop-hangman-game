from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self,letter,hit = None,miss = None):
        if miss and hit:
            raise InvalidGuessAttempt("Can't be both true")
            
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_miss(self):
        if self.miss:
            return True
        return False
    
    
    def is_hit(self):
        if self.hit:
            return True
        return False

class GuessWord(object):
    def __init__(self,word):
        if not word:
            raise InvalidWordException('please provide a word!')
        
        self.answer = word
        self.masked = '*' * len(word)
    
    def perform_attempt(self, letter):
        if len(letter) > 1 or len(letter) == 0:
            raise InvalidGuessedLetterException('Provide a valid guess')
        
        if letter.lower() in self.answer.lower():
            accuracy = GuessAttempt(letter, hit = True)
            
            index = 0
            
            for char in self.answer.lower():  
                if char == letter.lower():
                    the_list = list(self.masked)
                    the_list[index] = letter.lower()
                    self.masked = ''.join(the_list)
                    
                index += 1
        else:
            accuracy = GuessAttempt(letter, miss = True)
        
        return accuracy

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self,list_of_words = WORD_LIST, number_of_guesses = 5):
        self.list_of_words = list_of_words
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(list_of_words))
        self.previous_guesses = []
        self.is_over = False

    
    @classmethod    
    def select_random_word(cls,list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException('please provide a list')        
        return random.choice(list_of_words)
    
    def guess(self, letter):
        status = self.word.perform_attempt(letter)
        if letter not in self.previous_guesses:
            self.previous_guesses.append(letter.lower())
            
        if status.is_miss() and not status.is_hit():
            self.remaining_misses -= 1
        if self.is_finished():
            raise GameFinishedException('Game Over!')            
        if self.is_won():
            raise GameWonException("Good Job!!")
        if self.is_lost():
            raise GameLostException('You Lost!')


            
        return status
    
    def is_finished(self):
        if self.is_over:
            return True
        return False
    def is_won(self):
        if '*' not in self.word.masked:
            self.is_over = True
            return True
        return False
            
    def is_lost(self):
        if self.remaining_misses == 0:
            self.is_over = True
            return True
        return False
            