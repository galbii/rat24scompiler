switch = True

class Parser:
    def __init__(self, tokens):
        #token list is defined in a 3tuple zip object
        #token[i][0] will be the type of token
        #token[i][1] will be the lexeme
        #token[i][2] will be the line number

        self.tokens = list(tokens)
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]
        print(self.current_token)
        self.lookahead=None

    def next_token(self):
        #keep track of the number of tokens we have
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        #else if there are no more tokens

    def match(self, expected_token):
        if self.current_token[0] == expected_token:
            self.next_token()
        else:
            raise SyntaxError(f"Expected '{expected_token}' but found '{self.current_token[0]}'.")

    def parse(self):
        self.Rat24S()

#R1
    def Rat24S(self):
        self.opt_func()

#R2
    def opt_func(self):
        if self.current_token:
            self.func_def()
        else:
            self.empty()

#R3
    def func_def(self):
        self.func()
        self.function_def_prime()

    def function_def_prime(self):
        if self.current_token:
            self.func()
            self.function_def_prime()
        else:
            self.empty()

#R4
    def func(self):
        self.identifier()
        self.opt_parameter_list()
        self.opt_declaration_list()
        self.body()

#R5
    def opt_parameter_list(self):
        if self.current_token:
            self.parameter_list()
        else:
            self.empty()

#R6
    def parameter_list(self):
        self.parameter()
        self.parameter_list_prime()

    def parameter_list_prime(self):
        if self.current_token:
            self.parameter()
            self.parameter_list_prime()
        else:
            self.empty()

#R7
    def parameter(self):
        self.IDs()
        self.qualifier()
#R8
    def qualifier(self):
        if self.current_token in ['integer', 'boolean', 'real']:
            # If the current token matches any of the valid qualifiers, consume it
            qualifier_value = self.current_token
            self.next_token()  # Move to the next token
            return qualifier_value
        else:
            raise SyntaxError(f"Expected 'integer', 'boolean', or 'real' but found '{self.current_token}'.")

#R9
    def body(self):
        self.statement_list()

#R10
    def opt_declaration_list(self):
        if self.current_token:
            self.declaration_list()
        else:
            self.empty()

#R11
    def declaration_list(self):
        self.declaration()
        self.declaration_list_prime()

    def declaration_list_prime(self):
        if self.current_token:
            self.declaration()
            self.declaration_list_prime()
        else:
            self.empty()

#R12
    def declaration(self):
        self.qualifier()
        self.IDs()

#R13
    def IDs(self):
        self.identifier()
        self.IDs_prime()

    def IDs_prime(self):
        if self.current_token:
            self.identifier()
            self.IDs_prime()
        else:
            self.empty()

#R14
    def statement_list(self):
        self.statement()
        self.statement_list_prime()

    def statement_list_prime(self):
        if self.current_token:
            self.statement()
            self.statement_list_prime()
        else:
            self.empty()

#R15
    def statement(self):
        if self.current_token == '{':
            if switch:
                print('<Statement> -> <Compound>')
            self.compound()
        elif self.current_token == '=':
            if switch:
                print('<Statement> -> <Assign>')
            self.assign()
        elif self.current_token == 'if':
            if switch:    
                print('<Statement> -> <If>')
            self.if_()
        elif self.current_token == 'return':
            if switch:
                print('<Statement> -> <Return>')
            self.return_()
        elif self.current_token == 'print':
            if switch:
                print('<Statement> -> <Print>')
            self.print_()
        elif self.current_token == 'scan':
            if switch:
                print('<Statement> -> <Scan>')
            self.scan_()
        elif self.current_token == 'while':
            if switch:
                print('<Statement> -> <While>')
            self.while_()

#R16
    def compound(self):
        self.statement_list()

#R17
    def assign(self):
        if switch:
            print('<Assign> -> <Identifier> = <Expression>')

#R18
    def if_(self):
        if switch:
            print('<If>-> if(<Condition>) <Statement> endif | if <Condition>) <Statement>   else  <Statement>  endif')

#R19
    def return_(self):
        if switch:
            print('<Return> -> return ; | return <Expression> ;')

#R20
    def print_(self):
        if switch:
            print('<Print> -> print(<Expression>)')

#R21
    def scan_(self):
        if switch:
            print('<Scan>-> scan(<IDs>)')

#R22
    def while_(self):
        if switch:
            print('<While> -> while (<Condition>) <Statement> endwhile')

#R23
    def condition(self):
        if switch:
            print('<Condition> -> <Expression><Relop><Expression>')

#R24
    def relop(self):
        if switch:
            print('<Relop> -> == | != | > | < | <= | =>')

#R25
    def expression(self):
        if switch:
            print('<Expression> -> <Term> <Expression Prime>')
        self.term()
        self.expression_prime()

    def expression_prime(self):
        if switch:
            print('<Expression Prime> -> +<Term><Expression Prime> | -<Term><Expression Prime> | Empty')
        if self.current_token == '+' or '-':
            self.term()
            self.expression_prime()
#R26
    def term(self):
        if switch:
            print('<Term> -> <Factor><Term Prime>')
        self.factor()
        self.term_prime()

    def term_prime(self):
        if switch:
            print('<Term Prime> -> *<Factor><Term Prime> | /<Factor><Term Prime> | Empty')
        if self.current_token == '*' or "/":
            self.factor()
            self.term_prime()
        else:
            self.empty()

    def identifier(self):
        if self.current_token[0] == 'identifier':
            # If the current token is an identifier, consume it
            identifier_value = self.current_token[0]
            self.match(identifier_value)  # Match the identifier token
        else:
            raise SyntaxError(f"Expected an identifier but found '{self.current_token[0]}'.")
#R27
    def factor(self):
        self.primary()
        self.factor_prime()

    def factor_prime(self):
        if self.current_token:
            self.primary()
            self.factor_prime()
        else:
            self.empty()
#R28 Returns token types
    #def primary():

#R29
    def empty(self):
        if switch:
            print('<Empty>') 
