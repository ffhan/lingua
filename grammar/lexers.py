"""
Defines all Lexer implementations.
"""
import abc
import grammar.regular_expressions as rgx

class Token: #todo: some tokens do not have a value. Implement an abstract Token class and then valueless token.
    """
    Defines a Token, a result of a Lexer scan.
    """
    def __init__(self, token_type: str, token_value: str):
        """
        Initialises a Token. A token contains a token type (for example a variable, an integer..)
        and a value or an alias, what it's changing (token type: variable, token value: example_of_a_variable)

        :param str token_type: token type
        :param str token_value: token value
        """
        self.token_type = token_type
        self.token_value = token_value

    def __repr__(self):
        return '<' + self.token_type + ', ' + self.token_value + '>'

class Lexer:
    """
    Bare bones Lexer implementation.
    """
    def __init__(self, *regexes):
        """
        Creates a Lexer defined with regular expressions.

        :param regexes: regex class
        """
        self._regexes: list = regexes

    def scan(self, text: str)->list:
        """
        Scans the text and returns a list of found tokens.

        :param str text: string of text
        :return list: a list containing tokens
        """
        start_index = -1
        # end_index = -1

        current_regex = None
        tokens = []
        # print("entered", text)
        for i, char in enumerate(text): #todo: introdu
            # print(i, char, "'{}'".format(text[start_index:i + 1]), current_regex, tokens)
            if start_index == -1:
                for regex in self._regexes:
                    result = regex.check(char)
                    # print("'{}' '{}' {}".format(char, char.strip(), result))
                    if result:
                        start_index = i
                        current_regex = regex
                        break
            else:
                continue_flag = False
                for regex in self._regexes:
                    if regex.check(text[start_index:i + 1]) and regex != current_regex:
                        continue_flag = True
                        current_regex = regex
                    elif current_regex.check(text[start_index:i + 1]):
                        continue_flag = True
                    if continue_flag:
                        break
                if not continue_flag: #todo: for things that are not whitespace but haven't been lexed add an undefined token.
                    tokens.append(Token(current_regex.name, text[start_index:i]))
                    # start_index = -1
                    # current_regex = None
                    tokens += self.scan(text[i:])
                    return tokens
        if start_index != -1 and current_regex:
            tokens.append(Token(current_regex.name, text[start_index:]))
        return tokens

class StandardLexer(Lexer):
    """
    Defines a standard lexer, sufficient for a default wide-range use.
    """

    def __init__(self):
        super().__init__(rgx.VARIABLE, rgx.FLOAT, rgx.INTEGER, rgx.LPARAM,
                         rgx.RPARAM, rgx.LBRACKET, rgx.RBRACKET, rgx.ASSIGN,
                         rgx.EQUALITY)