from typing import Optional

"""record Class:

    Description: The record class will hold the processed data after the source code is passed through
             the finite state machine to determine weather the token is a proper token.

    Private params:
            
            self.token|list = list of tokens; tokens will be appended to the end of the list after
                              being processed by the fsm

            self.lexeme|list = the uniqe string; also called by the rec.add_entry(token, lexeme)

            Note: self.[separators|operators|keywords] are just reserved words and are divided for 
                  modularity's sake

    Class functions:

        self.__init__(self) = whenever a record is created, space is allocated for all the data to be
                              stored in the record, as well as reserved string literals

        self.add_entry(token, lexeme) = add function to add an entry; token and lexeme are of form
                                        self.token and self.lexeme respectively

        self.list() = prints out list of tokens and lexemes
"""
class record:
    def __init__(self):
        self.token = []
        self.lexeme = []
        self.separators = [";", "(", ")", "{", "}", ",", "$"]
        self.operators = ["=", "+", "-", "*", "/", "==", "!=", ">", "<","<<", ">>", "<=", "=>", "!"]
        self.invalid = ["#", "_", "."]
        self.keywords = [
            "function",
            "integer",
            "if",
            "else",
            "endif",
            "while",
            "return",
            "scan",
            "print",
            "boolean",
            "real",
            "true",
            "false",
            "endwhile",
        ]

    # appends new entries to the token and lexeme lists
    def add_entry(self, t, l):
        self.token.append(t)
        self.lexeme.append(l)
        return True

    # initializes output string
    # iterates over token list and lexeme list
    # pairs each token type with corresponding lexeme
    # f-string appends formatted string to the output string for each pair of tokens and lexemes
    def list(self):
        # print headers for token and lexeme columns
        output = f"{'Token':<20}{'Lexeme'}\n"
        # dividing line below columns
        output += f"{'-'*30}\n"
        for t, l in zip(self.token, self.lexeme):
            output += f"{t:<20}{l}\n"
        return output.strip()

    def output(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(self.list())


# fsm will parse tokens by line
# fsm function will also handle adding entries to the record that's why we are passing the record through there


# notes from class
# concatination and union of sets

"""finitestate Class:

    Description: This class is used to handle the strings fed into the tokengen() function
                 as well as holds a record object within the class initialization

    self.tokenhandler() = the finite state machine is coded into this function. It handles
                          the source line by line to determine the tokens and lexemes of the code

"""
class finitestate:
    def __init__(self, rec: record):
        self.rec = rec
        self.state = "start"
        self.token = ""

    def tokenhandler(self, line, state:Optional[str] = "start"):
        self.state = state
        index = 0
        # loop iterates through each character in the line and sets current character to current index
        while index < len(line):
            char = line[index]
            # uncomment the following line to see how Rat24S .txt file is processed
            #print(char)
            # checks current state of lexer
            if self.state == "start":
                # checks for the start of a comment which begins with a left bracket and an asterisk
                if char == "[" and (index + 1 < len(line) and line[index + 1] == "*"):
                    # switches state of the lexer to "comment" and skips the bracket and asterisk
                    self.state = "comment"
                    index += 2
                    # ignore characters after the comment marker
                    continue
                # invalid comment if statement
                if char in self.rec.invalid:
                    self.state = "unknown"
                    self.token += char
                # checks if current character is an integer
                # if current character is an integer the character is appended to current token
                elif char.isdigit():
                    self.state = "int"
                    self.token += char
                # checks if current character is a real number
                # if current character is a real number the character is appended to current token
                elif char.isalpha():
                    self.state = "identifier"
                    self.token += char
                # checks if current character is a real number
                # if current character is a real number the character is appended to current token
                # prepends "0." to real numbers beginning in a decimal point
                elif char == ".":
                    if index + 1 < len(line) and line[index + 1].isdigit():
                        self.state = "real"
                        self.token += "0."
                    else:
                        raise ValueError(
                            f"Invalid character at index {index}: '.' is not followed by a digit"
                        )

                # checks if current character is a separator
                # if current character is a separator the character is appended to current token
                elif char in self.rec.separators:
                    self.state = "separator"
                    self.token += char
                    self.rec.add_entry(self.state, self.token)
                    # reset
                    self.state = "start"
                    self.token = ""
                # checks if current character is an operator
                # if current character is an operator the character is appended to current token
                elif char in self.rec.operators:
                    # check next character to see if operator has multiple characters
                    next_char = line[index + 1] if index + 1 < len(line) else ""
                    if char + next_char in self.rec.operators:
                        # adds multiple character operator to record as single token
                        self.rec.add_entry("operator", char + next_char)
                        index += 1
                    else:
                        # adds single character operator to record
                        self.rec.add_entry("operator", char)
                # ignore whitespace
                elif char.isspace():
                    pass
                # ignores invalid characters
                else:
                    print(state)
                    raise ValueError(f"Invalid character at index {index}: '{char}'")
            elif self.state == "unknown":
                self.token += char
                # executes if lexer is in the middle of the "comment" state
            elif self.state == "comment":
                # checks if current character is an asterisk and the next character is a right bracket which signifies the end of a comment
                if char == "*" and index + 1 < len(line) and line[index + 1] == "]":
                    self.state = "start"
                    # skips asterisk and bracket so they are not processed
                    index += 2
                    # ignore characters within comment
                    continue
                # ignores any possible invalid characters within comment
                else:
                    pass
            elif self.state == "int":
                # checks if the next digit is an int to continue, if not token is complete and we have identified the lexeme
                if char.isdigit():
                    self.token += char
                # if the character "." comes after an integer it signifies the start of a real number
                elif char == ".":
                    self.state = "real"
                    self.token += char
                    if not line[index + 1].isalnum() or index + 1 >= len(line):
                        self.state = "unknown"
                elif char.isalpha():
                    self.state = "unknown"
                    self.token += char
                else:
                    # if the next character is not a digit or a "." the current integer token is complete and the state is reset for the next lexeme
                    self.rec.add_entry(self.state, self.token)
                    # reset
                    self.state = "start"
                    self.token = ""
                    self.tokenhandler(char, self.state)
                # continues appending tokens until the digits following the decimal point in the real number are complete
            elif self.state == "real":
                if char.isdigit():
                    self.token += char
                elif char == ".":
                    raise ValueError(
                        f"Invalid character at index {index}: number cannot have multiple decimal points"
                    )
                else:
                    # add completed real number token
                    self.rec.add_entry(self.state, self.token)
                    # reset
                    self.state = "start"
                    self.token = ""
                    self.tokenhandler(char)
                    # appending alphanumeric characters and underscores to build identifiers
            elif self.state == "identifier":
                if char.isalnum() or char == "_":
                    self.token += char
                else:
                    # checks if the token is a keyword before adding entry
                    if self.token in self.rec.keywords:
                        # now labelled as keyword
                        self.rec.add_entry("keyword", self.token)
                    else:
                        # if token is not in the list of keywords then it is simply an identifier
                        self.rec.add_entry("identifier", self.token)
                    # reset
                    self.state = "start"
                    self.token = ""
                    self.tokenhandler(char)
                    # whitespace and separators are not valid parts within keywords or identifiers in Rat24S
                    # stops token accumulation when whitespace or separator is detected
                    if not char.isspace() and char not in self.rec.separators:
                        self.tokenhandler(char)
            index += 1

        # handles end of the line
        # checks if the lexer's current state is not in the "start" or "comment state"
        # only numbers, identifiers, operators, and separators are added as entries
        if self.state not in ["start", "comment"]:
            self.rec.add_entry(self.state, self.token)
            # after adding the token to the record the lexer state is reset to "start"
            # token string is reset to an empty string
            self.state = "start"
            self.token = ""
            # if lexer is in a comment state continue to ignore inputs until end of comment
#        elif self.state == "comment":
#            print(line)
#            raise ValueError(f"Unclosed comment at the end of line: {line}")
        return 1


"""line Function:

    Description: Simple function to keep track of which line the lexer is on while analyzing the code

"""
def lines(contents):
    # split the contents into tokens
    lines = contents.split("\n")
    return lines


"""lexer Function

    Description: Puts the classes and functions together to create our lexer. 

"""
def lexer(file):
    if(file[-6:] != "rat24s"):
        print("[error] please input a valid rat24s file")
        return "None"
    else:
        rec = record()
        fsm = finitestate(rec)

        contents = open(file, "r").read()
        line_arr = lines(contents)
        # keep track of line number in case fsm returns 0(false) so we can return the error message
        line_no = 0
        for line in line_arr:
            # val will be 0 or 1
            val = fsm.tokenhandler(line, fsm.state)
            if not val:
                errormsg = "error on line {}".format(line_no)
                return errormsg
            line_no = line_no + 1

        rec.output("tokenized_" + file[:-7] + ".txt")

        return rec.list()
