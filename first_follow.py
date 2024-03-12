def calculate_first(grammar):
    # criei um dicionário para armazenar os conjuntos de FIRST de cada símbolo não terminal
    first_sets = {}
    epsilon = None

    # botando os conjuntos de FIRST com conjuntos vazios
    for rule in grammar:
        non_terminal = rule['left']
        first_sets[non_terminal] = set()

    # verifica se um símbolo é terminal
    def is_terminal(symbol):
        return symbol not in first_sets
    # calcula o FIRSt
    def calculate_symbol_first(symbol, visited=None):
        # Se visited ta vazio, inicializa como um conjunto vazio
        if visited is None:
            visited = set()

        # Se o simbolo já foi visitado, retorna um conjunto vazio para evitar recursão infinita
        if symbol in visited:
            return set()

        # Adiciona o símbolo na lista de visitados
        visited.add(symbol)

        # coloca o conjunto de FIRST como vazio
        first = set()

        # Anda pelas regras
        for rule in grammar:
            # Separa o lado esquerdo e direito da gramática
            left_symbol = rule['left']
            right_symbols = rule['right']

            # Se a regra corresponde ao símbolo atual
            if left_symbol == symbol:
                # Obtém o primeiro símbolo da regra
                first_symbol = right_symbols[0]

                # Se o primeiro símbolo for terminal, adiciona-o ao conjunto de FIRST
                if is_terminal(first_symbol):
                    first.add(first_symbol)
                else:
                    # Se o primeiro símbolo for não-terminal, calcula o conjunto de FIRST recursivamente
                    if first_symbol not in visited:
                        first |= calculate_symbol_first(first_symbol, visited)

                    # Remove a produção vazia se estiver presente no conjunto de FIRST
                    if epsilon in first_sets[first_symbol]:
                        first -= {epsilon}

        # Remove o símbolo atual da lista de visitados antes de retornar
        visited.remove(symbol)
        return first

    # Itera sobre os conjuntos de FIRST
    while True:
        changes = False
        for rule in grammar:
            left_symbol = rule['left']
            current_first = first_sets[left_symbol].copy()
            new_first = calculate_symbol_first(left_symbol)
            first_sets[left_symbol] |= new_first
            if current_first != first_sets[left_symbol]:
                changes = True

        if not changes:
            break

    return first_sets

def calculate_follow(grammar, first_sets):
    # Inicializa os conjuntos de FOLLOW com conjuntos vazios
    follow_sets = {}
    epsilon = None
    for rule in grammar:
        non_terminal = rule['left']
        follow_sets[non_terminal] = set()

    # Ve se símbolo é terminal
    def is_terminal(symbol):
        return symbol not in follow_sets
    # Calcula o FOLLOW de um símbolo
    def calculate_symbol_follow(symbol):
        follow = set()

        # Se o símbolo inicial, adiciona o $ 
        if symbol == grammar[0]['left']:
            follow.add('$')

        # Anda pelas regras
        for rule in grammar:
            left_symbol = rule['left']
            right_symbols = rule['right']

            # Itera sobre os símbolos do lado direito da regra
            for i in range(len(right_symbols)):
                if right_symbols[i] == symbol:
                    # Se o símbolo atual é o último na regra, adicione o conjunto FOLLOW do símbolo esquerdo
                    if i == len(right_symbols) - 1:
                        if left_symbol != symbol:
                            follow |= follow_sets[left_symbol]
                    else:
                        # Se o próximo símbolo é um terminal, adicione-o ao conjunto de FOLLOW
                        if is_terminal(right_symbols[i + 1]):
                            follow.add(right_symbols[i + 1])
                        else:
                            # Se o próximo símbolo é um não-terminal, adicione o conjunto FIRST dele ao conjunto de FOLLOW
                            follow |= first_sets[right_symbols[i + 1]]

                            # Se o conjunto de FIRST do próximo símbolo contém épsilon, adicione o conjunto FOLLOW do símbolo esquerdo
                            if epsilon in first_sets[right_symbols[i + 1]]:
                                follow -= {epsilon}
                                if left_symbol != symbol:
                                    follow |= follow_sets[left_symbol]

        return follow

    # Itera até que não haja mais alterações nos conjuntos de FOLLOW
    while True:
        changes = False
        for rule in grammar:
            left_symbol = rule['left']
            current_follow = follow_sets[left_symbol].copy()
            new_follow = calculate_symbol_follow(left_symbol)
            follow_sets[left_symbol] |= new_follow
            if current_follow != follow_sets[left_symbol]:
                changes = True

        if not changes:
            break

    return follow_sets

grammar = [
    {'left': 'program', 'right': ['cmds']},
    {'left': 'cmds', 'right': ['cmd', 'cmds2']},
    {'left': 'cmds2', 'right': ['cmd', 'cmds2']},
    {'left': 'cmds2', 'right': [None]},
    {'left': 'cmd', 'right': ['defvar']},
    {'left': 'cmd', 'right': ['atrib']},
    {'left': 'cmd', 'right': ['if2']},
    {'left': 'cmd', 'right': ['while2']},
    {'left': 'cmd', 'right': ['for2']},
    {'left': 'cmd', 'right': ['switch2']},
    {'left': 'cmd', 'right': ['print2']},
    {'left': 'cmd', 'right': ['input2']},
    {'left': 'defvar', 'right': ['tipo', 'id', 'def2']},
    {'left': 'def2', 'right': ['=', 'expr', ';']},
    {'left': 'def2', 'right': [';']},
    {'left': 'atrib', 'right': ['id', '=', 'expr', ';']},
    {'left': 'expr', 'right': ['string']},
    {'left': 'expr', 'right': ['exprArit']},
    {'left': 'exprArit', 'right': ['id', 'exprArit2']},
    {'left': 'exprArit', 'right': ['int', 'exprArit2']},
    {'left': 'exprArit', 'right': ['float', 'exprArit2']},
    {'left': 'exprArit', 'right': ['(', 'exprArit', ')']},
    {'left': 'exprArit2', 'right': ['aritad', 'exprArit']},
    {'left': 'exprArit2', 'right': ['aritmul', 'exprArit']},
    {'left': 'exprArit2', 'right': [None]},
    {'left': 'if2', 'right': ['if', '(', 'exprLog', ')', '{', 'cmds', '}', 'else2']},
    {'left': 'else2', 'right': ['else', '{', 'cmds', '}']},
    {'left': 'else2', 'right': [None]},
    {'left': 'exprLog', 'right': ['exprRela', 'and', 'exprRela']},
    {'left': 'exprLog', 'right': ['exprRela', 'or', 'exprRela']},
    {'left': 'exprRela', 'right': ['exprArit', 'oprel', 'exprArit']},
    {'left': 'while2', 'right': ['while', '(', 'exprLog', ')', '{', 'cmds', 'break2']},
    {'left': 'break2', 'right': ['break', ';']},
    {'left': 'break2', 'right': [None]},
    {'left': 'for2', 'right': ['for', '(', 'varFor', '..', 'varFor', ')', '{', 'cmds', '}']},
    {'left': 'varFor', 'right': ['int']},
    {'left': 'varFor', 'right': ['id']},
    {'left': 'switch2', 'right': ['switch', '(', 'id', ')', '{', 'cases', 'default', '}']},
    {'left': 'cases', 'right': ['case2', 'cases']},
    {'left': 'cases', 'right': ['case2']},
    {'left': 'case2', 'right': ['case', 'int', ':', 'cmds', 'break', ';']},
    {'left': 'default', 'right': ['default', ':', 'cmds']},
    {'left': 'default', 'right': [None]},
    {'left': 'print2', 'right': ['print', '(', 'string', ')', ';']},
    {'left': 'string', 'right': ['string', 'varPrint']},
    {'left': 'varPrint', 'right': [',', 'id', 'varString']},
    {'left': 'varPrint', 'right': [None]},
    {'left': 'varString', 'right': [',', 'varPrint']},
    {'left': 'varString', 'right': [',', 'string']},
    {'left': 'varString', 'right': [None]},
    {'left': 'input2', 'right': ['input', '(', '"%"', ',', 'id', ')', ';']}
]

# Calcula os conjuntos de FIRST e Follow da gramática
first_sets = calculate_first(grammar)
for non_terminal, first_set in first_sets.items():
    print(f'FIRST({non_terminal}): {first_set}')
print("--------------------------------------------------------------------------------------------------------------------")
follow_sets = calculate_follow(grammar, first_sets)
for non_terminal, follow_set in follow_sets.items():
    print(f'FOLLOW({non_terminal}): {follow_set}')