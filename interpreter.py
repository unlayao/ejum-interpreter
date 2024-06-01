# Open the file in read mode

while True:
    file_name = input("Enter the file name with .ejum extension: ")
    if not file_name.endswith('.ejum'):
        print("Invalid file extension. Please enter a file with the .ejum extension.")
        continue
    try:
        with open(file_name, 'r') as file:
            content = file.readlines()
            file.close()
        print(f"File found. Now running: {file_name}")
        break
    except FileNotFoundError:
        print("File not found. Please try again.")

in_quote = False
TOKENS = []
LINE_PROGRAM = []
PROGRAM = []
KEYWORDS = ["display", "input", "let", "plus", "minus", "times", "divide"]

variables = {}

for line in content:
    if line == '\n':
        continue
    else:
        line = line.strip()
        current_word = ""
        for ch in line:
            if ch == '"':
                in_quote = not in_quote
            if ch.isspace() and not in_quote:
                if current_word:
                    TOKENS.append(current_word)
                    current_word = ""
            else:
                current_word += ch

        if current_word:
            TOKENS.append(current_word)

        for token in TOKENS:
            if token[0] == '"' and token[-1] == '"':
                LINE_PROGRAM.append(("str_literal", token))
            elif token in KEYWORDS:
                LINE_PROGRAM.append(("keyword", token))
            elif token.isdigit():
                LINE_PROGRAM.append(("int_literal", int(token)))
            elif token.replace('.', '', 1).isdigit():
                LINE_PROGRAM.append(("float_literal", float(token)))
            elif token.isidentifier():
                LINE_PROGRAM.append(("variable", token))
            else:
                LINE_PROGRAM.append(("unknown", token))

        TOKENS = []
        PROGRAM.append(LINE_PROGRAM)
        LINE_PROGRAM = []

def evaluate_expression(expression):
    if len(expression) == 1:
        token_type, value = expression[0]
        if token_type == "variable":
            return variables.get(value, f"Undefined variable: {value}")
        elif token_type in ["int_literal", "float_literal", "str_literal"]:
            return value.strip('"') if token_type == "str_literal" else value
    elif len(expression) == 3:
        operand1_type, operand1 = expression[0]
        operator_type, operator = expression[1]
        operand2_type, operand2 = expression[2]

        if operand1_type == "variable":
            operand1 = variables.get(operand1, f"Undefined variable: {operand1}")
        if operand2_type == "variable":
            operand2 = variables.get(operand2, f"Undefined variable: {operand2}")

        if operator_type == "keyword":
            if not isinstance(operand1, (int, float)) or not isinstance(operand2, (int, float)):
                raise ValueError("Error: Cannot perform arithmetic on non-numeric values")

            if operator == "plus":
                return operand1 + operand2
            elif operator == "minus":
                return operand1 - operand2
            elif operator == "times":
                return operand1 * operand2
            elif operator == "divide":
                if operand2 == 0:
                    raise ZeroDivisionError("Error: Division by zero")
                return operand1 / operand2
    raise ValueError("Invalid expression")

for line in PROGRAM:
    if line[0][0] == "keyword":
        keyword = line[0][1]
        if keyword == "display":
            expression = line[1:]
            try:
                result = evaluate_expression(expression)
                print(result)
            except Exception as e:
                print(e)
        elif keyword == "input":
            var_name = line[1][1]
            var_value = input(f"Enter value for {var_name}: ")
            if var_value.isdigit():
                variables[var_name] = int(var_value)
            elif var_value.replace('.', '', 1).isdigit():
                variables[var_name] = float(var_value)
            else:
                variables[var_name] = var_value
        elif keyword == "let":
            var_name = line[1][1]
            expression = line[2:]
            try:
                result = evaluate_expression(expression)
                variables[var_name] = result
            except Exception as e:
                print(e)

#print(variables)
