#regular expressions for ints d+
#regular expressions for real d+.d+
#regular expressions for ints l(l|d|_)+


#eclosures are where the state can end up



#food for thought have a separate system to manage tokens
#so if you have a line, pass it through a tokenizer and then analyze each individual token????? but then there are inefficiencies??
#another thing to keep in mind, just have the finite state machine output 0 or 1 to evaluate if the token is valid and to identify which state it is in?
#process will go
#raw source code->split code by lines->splite lines by token->
class record:
    def __init__(self):
        self.token = []
        self.lexeme = []
        self.seperators = [';', '(', ')']
        self.operators = ['<', '=']
    
    def add_entry(self, t, l):
        self.token.append(t)
        self.lexeme.append(l)
        return True

    def list(self):
        return list(zip(self.token, self.lexeme))

#fsm will parse tokens by line
#fsm function will also handle adding entries to the record that's why we are passing the record through there


#notes from class
# concatination and union of sets
class finitestate:
    def __init__(self, rec: record):
        self.rec = rec
        self.state = "start"
        self.token = ""

    def tokengen(self, line):
        index = 0
        while index < len(line):
            char = line[index]
            print(char)
            if self.state == "start":
                if char.isdigit():
                    self.state = "int"
                    self.token += char
                elif char.isalpha():
                    self.state = 'identifier'
                    self.token += char
                elif char == '.':
                    self.state = 'real'
                    self.token += '0.'
                elif char in self.rec.seperators:
                    self.state = 'seperator'
                    self.token += char
                    self.rec.add_entry(self.state, self.token)
                    #reset
                    self.state = "start"
                    self.token = ''
                elif char in self.rec.operators:
                    self.state = 'operator'
                    self.token += char
                    self.rec.add_entry(self.state, self.token)
                    #reset
                    self.state = "start"
                    self.token = ''
                elif char.isspace():
                    pass
            elif self.state == "int":
                #checks if the next digit is an int to continue, if not token is complete and we have identified the lexeme
                if char.isdigit():
                    self.token += char
                elif char == ".":
                    self.state = "real"
                    self.token += char
                else:
                    self.rec.add_entry(self.state, self.token)
                    #reset
                    self.state = "start"
                    self.token = ''
                    self.tokengen(char)
            elif self.state == 'real':
                if char.isdigit():
                    self.token += char
                elif char == ".":
                    #invalid real
                    return 0
                else:
                    self.rec.add_entry(self.state, self.token)
                    #reset
                    self.state = "start"
                    self.token = ''
                    self.tokengen(char)
            elif self.state == 'identifier':
                if char.isalnum() or char == "_":
                    self.token += char
                else:
                    self.rec.add_entry(self.state, self.token)
                    #reset
                    self.state = "start"
                    self.token = ''
                    self.tokengen(char)
            index += 1

        #handles end of the line
        if self.state != "start":
            self.rec.add_entry(self.state, self.token)
            self.state = "start"
            self.token = ''
        return 1
                    

def lines(contents):
    #split the contents into tokens
    lines = contents.split('\n')
    return lines
    
##why are we passing thru the record through so many functions might be redundant see if you can make it simpler
def lexer(file):
    rec = record()
    fsm = finitestate(rec)

    contents = open(file, "r").read()
    line_arr = lines(contents)
    #keep track of line number in case fsm returns 0(false) so we can return the error message
    line_no = 0
    for line in line_arr:
        #val will be 0 or 1
        val = fsm.tokengen(line)
        if not val:
            errormsg = "error on line {}".format(line_no)
            return errormsg
        line_no = line_no + 1

    return rec.list()
