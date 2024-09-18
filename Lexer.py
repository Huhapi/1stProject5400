"""
Project01 - CS5400
Group Members: Daniel Hayes and Sarah Crane
Semptember 18, 2024
"""
class Lexer:
    """
    Class Lexer
    Processes input strings and produces tokens
    """
    def __init__(self, text):
        """
        Initializes the lexer with the input text.
        Sets the initial position and current character.
        """
        self.text = text
        self.charlist = list(text)  # Creates list of chars out of String input
        self.current_char = self.charlist[0]    # Stores current char
        self.position = 0       # Stores int position in char list
        self.current_token = "" # Stores String of current token
        self.period_counter = 0 # Counts periods in numbers (cannot have more than 1)
        self.is_alpha = False   # Currently reading variable boolean - is True if going through variable
        self.is_number = False  # Currently reading numerical boolean - is True is going through number
        self.last_token_type = None # Stores previous token type for potential error handling
        self.past_assign_op = False # Stores whether or not past = sign

    def error(self,a):
        """
        Raises an exception for invalid characters encountered
        during tokenization.
        """
        if(a == 0):
            raise Exception("General error code.")
        if(a == 1):
            raise Exception("There must be a number before a '.'.")
        if(a == 2):
            raise Exception("There can only be one '.' in a number.")
        if(a == 3):
            raise Exception("Cannot have a number value prior to assignment operator.")

    def advance(self):
        """
        Advances to the next character in the input text.
        Updates the current character to the new position.
        """
        self.position = self.position+1
        if self.position >= len(self.charlist):
            self.current_char = None
        else: 
            self.current_char = self.charlist[self.position]

    def get_next_token(self):
        """
        Returns the next token in the input text. Tokens can be:
        - 'ASSIGN' for the '=' character
        - 'EOF' when the end of the text is reached
        """
        while self.current_char is not None: #starts loop to tokenize each component
            #token 'variable'
            if self.current_char.isalpha():
                if self.is_number:
                    self.error(0)
                if self.is_alpha:   # determines if continuing variable or new variable
                    self.current_token += self.current_char
                else:
                    self.is_alpha = True
                    self.current_token = self.current_char
            else:
                if (self.is_alpha):
                    self.is_alpha = False
                    return ('VARIABLE', self.current_token)
            
            #token 'int or decimal'
            if (self.current_char.isdigit() or self.current_char == '.'):
                if not self.past_assign_op:
                    self.error(3)
                if self.is_number: # Determines if continueing number or new number.
                    self.current_token += self.current_char
                    if(self.current_char == '.'):
                        self.period_counter +=1
                else:
                    self.current_token = self.current_char
                    self.is_number = True
                    if(self.current_char == '.'):
                        self.error(1)  
            else:
                if(self.is_number):
                    if(self.period_counter < 2):
                        self.period_counter = 0
                        self.is_number = False
                        return ('VALUE', self.current_token)
                    else:
                        self.error(2)
                    self.is_number = False
                    
            #whitespace to be ignored
            if self.current_char.isspace():
                self.advance()
                return ('SPACE', ' ')
                #continue
            
            #token '+'
            if self.current_char == '+':
                self.advance()
                return ('ADD', '+')
            
            #token '-'
            if self.current_char == '-':
                self.advance()
                return ('SUBTRACT', '-')
            
            #token '*'
            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')
            
            #token '/'
            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')
            
            #token '='
            if self.current_char == '=':
                self.advance()
                self.past_assign_op = True
                return ('ASSIGN', '=')
            
            #check invalid character
            if not (self.is_alpha or self.is_number):
                print(self.is_alpha)
                self.error(0)

            self.advance() # advancing for number and variables (done after alternate checks)

        # If end of file is reached and number or variable has not been returned
        # Return them before ending file.
        if(self.is_alpha):
            self.is_alpha = False
            return ('VARIABLE', self.current_token)
        if(self.is_number):
            self.is_number = False
            return ('VALUE', self.current_token)
        return ('EOF', None)

def runlexer(file_in):
    lexer = Lexer(file_in)              # 1. Initialize the lexer with the input string
    token = lexer.get_next_token()      # 2. Get the first token from the lexer
    tokens = ""                         # For testing get output in string instead of print line
    while token[0] != 'EOF':            # 3. Loop until the end of the input is reached
        tokens += "["+token[0]+"]"+"["+token[1]+"]"                    # 4. save the current tokens
        token = lexer.get_next_token()  # 5. Get the next token
    return tokens                       # return results

"""
Test Cases
Includes various arithmetic expressions to test lexer and correctly identify and tokenize each component
"""
def testalpha():
    testfile1 = runlexer("betrius = 2 + 3 / 4 * 5") # multiple letters and multiple math signs
    successes = 0
    if(testfile1 == "[VARIABLE][betrius][SPACE][ ][ASSIGN][=][SPACE][ ][VALUE][2][SPACE][ ][ADD][+][SPACE][ ][VALUE][3][SPACE][ ][DIVIDE][/][SPACE][ ][VALUE][4][SPACE][ ][MULTIPLY][*][SPACE][ ][VALUE][5]"):
        successes +=1

    #testfile2 = runlexer(" 2letrius = 2 + 3 / 4 * 5") # Starting with a number prior to =
    #successes = 0
    #if(testfile2 == ""):
    #    successes +=1
    #This test should: raise Exception("Cannot have a number value prior to assignment operator.")

    testfile3 = runlexer(" celcius = 257 + 2 ") # starting and ending with spaces
    print(testfile3)
    if(testfile3 == "[SPACE][ ][VARIABLE][celcius][SPACE][ ][ASSIGN][=][SPACE][ ][VALUE][257][SPACE][ ][ADD][+][SPACE][ ][VALUE][2][SPACE][ ]"):
        successes +=1
        
    """
        testfile4 = runlexer("c = 2 + betrius")
    successes = 0
    if(testfile4 == ""):
        successes +=1
    """
    
    testfile5 = runlexer("a=1+1") #testing add, no spaces
    print(testfile5)
    if(testfile5 == "[VARIABLE][a][ASSIGN][=][VALUE][1][ADD][+][VALUE][1]"):
        successes +=1

    testfile6 = runlexer("b=2-1") #testing subtract, no spaces
    print(testfile6)
    if(testfile6 == "[VARIABLE][b][ASSIGN][=][VALUE][2][SUBTRACT][-][VALUE][1]"):
        successes +=1

    testfile7 = runlexer("c=1*1") #testing multiply, no spaces
    print(testfile7)
    if(testfile7 == "[VARIABLE][c][ASSIGN][=][VALUE][1][MULTIPLY][*][VALUE][1]"):
        successes +=1

    testfile8 = runlexer("d=4/2") #testing divide, no spaces
    print(testfile8)
    if(testfile8 == "[VARIABLE][d][ASSIGN][=][VALUE][4][DIVIDE][/][VALUE][2]"):
        successes +=1

    testfile9 = runlexer("e=10000000000/1000") #testing large values, no spaces
    print(testfile9)
    if(testfile9 == "[VARIABLE][e][ASSIGN][=][VALUE][10000000000][DIVIDE][/][VALUE][1000]"):
        successes +=1

    testfile10 = runlexer("e=100000 00000/1000") #testing large values, with space in value
    print(testfile10)
    if(testfile10 == "[VARIABLE][e][ASSIGN][=][VALUE][100000][SPACE][ ][VALUE][00000][DIVIDE][/][VALUE][1000]"):
        successes +=1  

    return successes #returns total number of successfully run tests
    
def main():
    # Example usage
    x = testalpha()
    print(x)
    
main()
