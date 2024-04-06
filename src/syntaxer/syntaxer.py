switch = True

class Parser:
    def __init__(self, tokens):
        #token list is defined in a 3tuple zip object
        #token[i][0] will be the type of token
        #token[i][1] will be the lexeme
        #token[i][2] will be the line number

        self.tokens = tokens
        self.token_index = 0
        self.current_token = tokens[self.token_index][0]
        self.lookahead=None

    def next_token(self):
        #keep track of the number of tokens we have
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index][0]
        #else if there are no more tokens

    def parse(self):
        #self.Rat24S()
        print(self.current_token)
##R1
#    def Rat24S(self):
#        self.opt_func()
#        self.opt_declaration_list()
#        self.statement_list()
#
##R2
#    def opt_func(self):
#        if self.token:
#            self.func_def()
#        else:
#            self.empty()
#
##R3
#    def func_def(self):
#        self.func()
#        self.function_def_prime()
#
#    def function_def_prime(self):
#        if self.token:
#            self.func()
#            self.function_def_prime()
#        else:
#            self.empty()
#
##R4
#    def func(self):
#        self.identifier()
#        self.opt_parameter_list()
#        self.opt_declaration_list()
#        self.body()
#
##R5
#    def opt_parameter_list(self):
#        if self.token:
#            self.parameter_list()
#        else:
#            self.empty()
#
##R6
#    def parameter_list(self):
#        self.parameter()
#        self.parameter_list_prime()
#
#    def parameter_list_prime(self):
#        if self.token:
#            self.parameter()
#            self.parameter_list_prime()
#        else:
#            self.empty()
#
##R7
#    def parameter(self):
#        self.IDs()
#        self.qualifier()
##R8
#    def qualifier(self):
#        
#
##R9
#    def body(self):
#        self.statement_list()
#
##R10
#    def opt_declaration_list(self):
#        if self.token:
#            self.declaration_list()
#        else:
#            self.empty()
#
##R11
#    def declaration_list(self):
#        self.declaration()
#        self.declaration_list_prime()
#
#    def declaration_list_prime(self):
#        if self.token:
#            self.declaration()
#            self.declaration_list_prime()
#        else:
#            self.empty()
#
##R12
#    def declaration(self):
#        self.qualifier()
#        self.IDs()
#
##R13
#    def IDs(self):
#        self.identifier()
#        self.IDs_prime()
#
#    def IDs_prime(self):
#        if self.token:
#            self.identifier()
#            self.IDs_prime()
#        else():
#            self.empty()
#
##R14
#    def statement_list(self):
#        self.statement()
#        self.statement_list_prime()
#
#    def statement_list_prime(self):
#        if self.token:
#            self.statement()
#            self.statement_list_prime()
#        else:
#            self.empty()
#
##R15
#    def statement(self):
#        if self.token == '{':
#            if switch:
#                print('<Statement> -> <Compound>')
#            self.compound()
#        elif self.token == '=':
#            if switch:
#                print('<Statement> -> <Assign>')
#            self.assign()
#        elif self.token == 'if':
#            if switch:    
#                print('<Statement> -> <If>')
#            self.if_()
#        elif self.token == 'return':
#            if switch:
#                print('<Statement> -> <Return>')
#            self.return_()
#        elif self.token == 'print':
#            if switch:
#                print('<Statement> -> <Print>')
#            self.print_()
#        elif self.token == 'scan':
#            if switch:
#                print('<Statement> -> <Scan>')
#            self.scan_()
#        elif token == 'while':
#            if switch:
#                print('<Statement> -> <While>')
#            self.while_()
#
##R16
#    def compound(self):
#        self.statement_list()
#
##R17
#    def assign(self):
#        if switch:
#            print('<Assign> -> <Identifier> = <Expression>')
#
##R18
#    def if_(self):
#        if switch:
#            print('<If>-> if(<Condition>) <Statement> endif | if <Condition>) <Statement>   else  <Statement>  endif')
#
##R19
#    def return_(self):
#        if switch:
#            print('<Return> -> return ; | return <Expression> ;')
#
##R20
#    def print_(self):
#        if switch:
#            print('<Print> -> print(<Expression>)')
#
##R21
#    def scan_(self):
#        if switch:
#            print('<Scan>-> scan(<IDs>)')
#
##R22
#    def while_(self):
#        if switch:
#            print('<While> -> while (<Condition>) <Statement> endwhile')
#
##R23
#    def condition(self):
#        if switch:
#            print('<Condition> -> <Expression><Relop><Expression>')
#
##R24
#    def relop(self):
#        if switch:
#            print('<Relop> -> == | != | > | < | <= | =>')
#
##R25
#    def expression(self):
#        if switch:
#            print('<Expression> -> <Term> <Expression Prime>')
#        self.term()
#        self.expression_prime()
#
#    def expression_prime(self):
#        if switch:
#            print('<Expression Prime> -> +<Term><Expression Prime> | -<Term><Expression Prime> | Empty')
#        if self.token == '+' or '-':
#            self.term()
#            self.expression_prime()
##R26
#    def term(self):
#        if switch:
#            print('<Term> -> <Factor><Term Prime>')
#        self.factor()
#        self.term_prime()
#
#    def term_prime(self):
#        if switch:
#            print('<Term Prime> -> *<Factor><Term Prime> | /<Factor><Term Prime> | Empty')
#        if self.token == '*' or "/":
#            self.factor()
#            self.term_prime()
#        else:
#            self.empty()
#            
##R27
#    def factor(self):
#        self.primary()
#        self.factor_prime()
#
#    def factor_prime(self):
#        if self.token:
#            self.primary()
#            self.factor_prime()
#        else:
#            self.empty()
##R28 Returns token types
#    def primary():
#
##R29
#    def empty():
#        if switch:
#            print('<Empty>') 
