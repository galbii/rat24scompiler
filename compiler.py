#A lexer for the rat24s language

#This file is a collection of functions that will analyze the tokens in
#rat24s. The lexer will use finite state machine to ensure

#state information container
from sys import *
from lexer import *
from syntaxer import Parser

if __name__ == '__main__':

    #lexer returns list of tokens and lexems respectively
    tokens = lexer(argv[1])

    r24parser = Parser(tokens)
    output = r24parser.parse()



        


