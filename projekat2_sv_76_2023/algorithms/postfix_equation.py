def tokenize(text):
    def is_logical_operator(token):
        return token in {'AND', 'OR', 'NOT'}
    
    tokens = []
    current_token = []
    
    i = 0
    while i < len(text):
        char = text[i]
        if char in {'(', ')'}:
            if current_token:
                tokens.append(''.join(current_token))
                current_token = []
            tokens.append(char)
        elif char == ' ':
            if current_token:
                tokens.append(''.join(current_token))
                current_token = []
        else:
            current_token.append(char)
        i += 1
    
    if current_token:
        tokens.append(''.join(current_token))
    
    return tokens

        
def infix_to_postfix(text):
    weights = {'NOT':3, 'AND':2, 'OR':1}

    output = []
    operators = []

    tokens = tokenize(text)
    try:
        for token in tokens:
            if token=='(':
                operators.append(token)

            elif token==')':
                while operators and operators[-1]!='(':
                    output.append(operators.pop())

                operators.pop()

            elif token in weights:
                while operators and operators[-1]!='(' and weights[operators[-1]] >= weights[token]:
                    output.append(operators.pop())
                operators.append(token)

            else:
                output.append(token)

        while operators:
            output.append(operators.pop())
        

        return output
    except:
        return False

