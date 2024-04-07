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
        self.output = []

    def next_token(self):
        #keep track of the number of tokens we have
        print(self.current_token)
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        #else if there are no more tokens

    def match(self, expected_token):
        if self.current_token[0] == expected_token:
            self.next_token()
        elif self.current_token[1] == '$':
            self.next_token()
        elif self.current_token[1] == expected_token:
            self.next_token()
        else:
            raise SyntaxError(f"Expected '{expected_token}' but found '{self.current_token[0]}'.")

    def parse(self):
        self.Rat24S()
        return self.output

#R1 CHANGED
    def Rat24S(self):
        switch = False
        try:
            self.match('$')
            self.opt_func_def()
        except:
            self.empty()
        try:
            self.match('$')
            self.opt_declaration_list()
        except:
            self.empty()
        try:
            self.match('$')
            switch = True
        except:
            self.empty()

        self.statement_list()
        self.match('$')

#R2 CHANGED
    def opt_func_def(self):
        if self.current_token[0] == 'function':
            self.match('$')
            self.func_def()
        else:
            self.empty()

#R3 CHANGEDd
    def func_def(self):
        self.func()
        self.function_def_prime()

    def function_def_prime(self):
        if self.current_token[0]:
            self.func()
            print('hi')
            self.function_def_prime()
        else:
            self.empty()

#R4 CHANGED
    def func(self):
        if self.current_token[0] == 'function':
            self.identifier()
            self.match('(')
            self.opt_parameter_list()
            self.match(')')
            self.opt_declaration_list()
            self.body()
        else:
            self.empty()
        
#R5 CHANGED
    def opt_parameter_list(self):
        if self.current_token:
            self.match('$')
            self.parameter_list()
        else:
            self.empty()

#R6 CHANGED
    def parameter_list(self):
        self.parameter()
        self.parameter_list_prime()

    def parameter_list_prime(self):
        if self.current_token[1] == ',':
            self.match(',')
            self.parameter()
            self.parameter_list_prime()
        else:
            self.empty()

#R7 CHANGED
    def parameter(self):
        self.IDs()
        self.qualifier()

#R8
    def qualifier(self):
        if self.current_token[0] in ['integer', 'boolean', 'real']:
            # If the current token matches any of the valid qualifiers, consume it
            qualifier_value = self.current_token[1]
            self.next_token()  # Move to the next token
            return qualifier_value
        else:
            raise SyntaxError(f"Expected 'integer', 'boolean', or 'real' but found '{self.current_token}'.")

#R9 CHANGED
    def body(self):
        self.match('{')
        self.statement_list()
        self.match('}')


#R10 CHANGED
    def opt_declaration_list(self):
        if self.current_token:
            self.match('$')
            self.declaration_list()
        else:
            self.empty()

#R11 CHANGED
    def declaration_list(self):
        self.declaration()
        self.match(';')
        self.declaration_list_prime()

    def declaration_list_prime(self):
        if self.current_token:
            self.declaration()
            self.match(';')
            self.declaration_list_prime()
        else:
            self.empty()

#R12 CHANGED
    def declaration(self):
        self.qualifier()
        self.IDs()

#R13 CHANGED
    def IDs(self):
        self.identifier()
        self.IDs_prime()

    def IDs_prime(self):
        if self.current_token[1] == ',':
            self.match(',')
            self.identifier()
            self.IDs_prime()
        else:
            self.empty()

#R14 CHANGED
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
        print(self.output)
        if 'identifier' == self.current_token[0]:
            self.output.append(f"Token: Identifier Lexeme: {self.current_token[1]}")
            self.output.append("<Statement> -> <Assign>")
            print(f"Token: Identifier Lexeme: {self.current_token[1]}")
            print("<Statement> -> <Assign>")
            self.assign()
        elif self.current_token[1] == '{':
            if switch:
                self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
                self.output.append('<Statement> -> <Compound>')
                print('<Statement> -> <Compound>')
            self.compound()
        elif self.current_token[1] == '=':
            if switch:
                self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
                self.output.append('<Statement> -> <Assign>')
                print('<Statement> -> <Assign>')
            self.assign()
        elif self.current_token[1] == 'if':
            if switch:    
                self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
                self.output.append('<Statement> -> <If>')
                print('<Statement> -> <If>')
            self.if_()
        elif self.current_token[1] == 'return':
            if switch:
                self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
                self.output.append('<Statement> -> <Return>')
                print('<Statement> -> <Return>')
            self.return_()
        elif self.current_token[1] == 'print':
            if switch:
                self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
                self.output.append('<Statement> -> <Print>')
                print('<Statement> -> <Print>')
            self.print_()
        elif self.current_token[1] == 'scan':
            if switch:
                self.output.append("<Statement> -> <Assign>")
                print('<Statement> -> <Scan>')
            self.scan_()
        elif self.current_token[1] == 'while':
            if switch:
                self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
                self.output.append("<Statement> -> <Assign>")
                print('<Statement> -> <While>')
            self.while_()
        elif self.current_token[1] == ';':
            self.match(';')
        else:
            raise SyntaxError("Expected an identifier.")

#R16 CHANGED
    def compound(self):
        self.match('{')
        self.statement_list()
        self.match('}')

#R17 CHANGED
    def assign(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Assign> -> <Identifier> = <Expression>')
            print('<Assign> -> <Identifier> = <Expression>')
        self.identifier()
        self.match('operator')
        self.expression()
        self.match('separator')
#        if switch:
#            print('<Assign> -> <Identifier> = <Expression>')
#        self.match('operator')
#        try:
#            self.identifier()
#        except:
#            pass
#        try:
#            self.expression()
#        except:
#            pass
#        self.match(';')

#R18 CHANGED
    def if_(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<If>-> if(<Condition>) <Statement> endif | if <Condition>) <Statement else <Statement> endif')
            print('<If>-> if(<Condition>) <Statement> endif | if <Condition>) <Statement>   else  <Statement>  endif')
        self.match('if')
        self.match('(')
        self.condition()
        self.match(')')
        self.statement()
        self.if_prime()
        self.match("endif")

    def if_prime(self):
        if self.current_token[1] == 'else' or self.current_token[0] == 'else':
            self.match('else')
            self.statement()
        else:
            self.empty()
#R19 CHANGED
    def return_(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Return> -> return ; | return <Expression> ;')
            print('<Return> -> return ; | return <Expression> ;')
        self.match('return')
        self.return_prime()

    def return_prime(self):
        if self.current_token[1] == ';':
            self.match(';')
        else:
            self.expression()
            self.match(';')
    

#R20 CHANGED
    def print_(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Print> -> print(<Expression>)')
            print('<Print> -> print(<Expression>)')
        self.match('print')
        self.match('(')
        self.expression()
        self.match(')')
        self.match(';')


#R21 CHANGED
    def scan_(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Scan>-> scan(<IDs>)')
            print('<Scan>-> scan(<IDs>)')
        self.match('scan')
        self.match('(')
        self.IDs()
        self.match(')')
        self.match(';')

#R22 CHANGED
    def while_(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<While> -> while (<Condition>) <Statement> endwhile')
            print('<While> -> while (<Condition>) <Statement> endwhile')
        self.match('while')
        self.match('(')
        self.condition()
        self.match(')')
        self.statement()
        self.match('endwhile')

#R23 CHANGED
    def condition(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Condition> -> <Expression><Relop><Expression>')
            print('<Condition> -> <Expression><Relop><Expression>')
        self.expression()
        self.relop()
        self.expression()

#R24 CHANGED
    def relop(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Relop> -> == | != | > | < | <= | =>')
            print('<Relop> -> == | != | > | < | <= | =>')
        if self.current_token[1] in ['==', '!=', '>', '<', '<=', '=>']:
            self.match(self.current_token[1])
        else:
            raise SyntaxError('Invalid Relop Operator')

#R25 CHANGED
    def expression(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Expression> -> <Term> <Expression Prime>')
            print('<Expression> -> <Term> <Expression Prime>')
        self.term()
        self.expression_prime()

    def expression_prime(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Expression Prime> -> +<Term><Expression Prime> | -<Term><Expression Prime> | Empty')
            print('<Expression Prime> -> +<Term><Expression Prime> | -<Term><Expression Prime> | Empty')
        if self.current_token[0] in ['operator']:
            if self.current_token[1] == '+':
                self.match('operator')
            elif self.current_token[1] == '-':
                self.match('-')
            self.term()
            self.expression_prime()
        else:
            self.empty()
#R26 CHANGED
    def term(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Term> -> <Factor><Term Prime>')
            print('<Term> -> <Factor><Term Prime>')
        self.factor()
        self.term_prime()

    def term_prime(self):
        if switch:
            self.output.append(f"Token: {self.current_token[0]} Lexeme: {self.current_token[1]}")
            self.output.append('<Term Prime> -> *<Factor><Term Prime> | /<Factor><Term Prime> | Empty')
            print('<Term Prime> -> *<Factor><Term Prime> | /<Factor><Term Prime> | Empty')
        if self.current_token[1] in ['*', '/']:
            if self.current_token[1] == '*':
                self.match('*')
            elif self.current_token[1] == '/':
                self.match('/')
            self.factor()
            self.term_prime()
        else:
            self.empty()

    def identifier(self):
        if self.current_token[0] == 'identifier':
            # If the current token is an identifier, consume it
            identifier_value = self.current_token[1]
            self.match(identifier_value)  # Match the identifier token
        else:
            raise SyntaxError(f"Expected an identifier but found '{self.current_token[0]}'.")

#R27 CHANGED
    def factor(self):
        if self.current_token[1] == '-':
            self.match('-')
            self.primary()
        else:
            self.primary()
        


#R28 Returns token types
    def primary(self):
        if self.current_token[0] == 'identifier':
            # If the current token is an identifier, parse it as an identifier
            self.identifier()
        elif self.current_token[0] == 'integer':
            # If the current token is an integer, parse it as an integer
            self.integer()
        elif self.current_token[0] == 'real':
            # If the current token is a real number, parse it as a real number
            self.real()
        elif self.current_token[1] in ['true', 'false']:
            # If the current token is 'true' or 'false', parse it as a boolean value
            self.boolean()
        elif self.current_token[1] == '(':
            # If the current token is '(', parse it as a sub-expression enclosed in parentheses
            self.match('(')
            self.expression()
            self.match(')')
        else:
            self.empty()
            print(f"Unexpected token: '{self.current_token[1]}'.")
            #raise SyntaxError(f"Unexpected token: '{self.current_token[1]}'.")

    def integer(self):
        # Parse an integer
        if self.current_token[0] == 'integer':
            # If the current token is an integer, consume it
            integer_value = int(self.current_token[1])
            self.match('integer')  # Match the integer token
            return integer_value  # Return the integer value
        else:
            raise SyntaxError("Expected an integer.")

    def real(self):
        # Parse a real number
        if self.current_token[0] == 'real':
            # If the current token is a real number, consume it
            real_value = float(self.current_token[1])
            self.match('real')  # Match the real token
            return real_value  # Return the real number value
        else:
            raise SyntaxError("Expected a real number.")

    def boolean(self):
        # Parse a boolean value
        if self.current_token[1] in ['true', 'false']:
            # If the current token is 'true' or 'false', consume it
            boolean_value = self.current_token[1]
            self.match(boolean_value)  # Match the boolean token
            return boolean_value  # Return the boolean value
        else:
            raise SyntaxError("Expected 'true' or 'false'.")

#R29
    def empty(self):
        if switch:
            print(self.current_token)
            print('<Empty>')
