class Lexer:
    def __init__(self, text):
        """
        Initializes the lexer with the input text.
        Sets the initial position and current character.
        """
        self.text = text
        #pass

    def error(self):
        """
        Raises an exception for invalid characters encountered
        during tokenization.
        """
        pass

    def advance(self):
        """
        Advances to the next character in the input text.
        Updates the current character to the new position.
        """
        pass

    def get_next_token(self):
        """
        Returns the next token in the input text. Tokens can be:
        - 'ASSIGN' for the '=' character
        - 'EOF' when the end of the text is reached
        """
        while self.current_char is not None:
            #whitespace to be ignored
            if self.current_char.isspace():
                self.advance()
                continue
            #token 'int'
            if self.current_char.isdigit():
                self.advance()
                return ('VALUE', self)
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
            if self.current_char == '=':
                self.advance()
                return ('ASSIGN', '=')
            self.error()
        return ('EOF', None)

# Example usage
lexer = Lexer('a = 3')              # 1. Initialize the lexer with the input string
token = lexer.get_next_token()      # 2. Get the first token from the lexer
while token[0] != 'EOF':            # 3. Loop until the end of the input is reached
    print(token)                    # 4. Print the current token
    token = lexer.get_next_token()  # 5. Get the next token
