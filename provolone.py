import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'ID',
    'NUMBER',
    'EQUALS',
    'PLUS',
    'TIMES',   # Token para '*'
    'COMMA',
    'LPAREN',  # Token para '('
    'RPAREN',  # Token para ')'
    'INICIO',
    'MONITOR',
    'EXECUTE',
    'TERMINO',
    'ZERO'
)

# Expressões regulares para tokens simples
t_EQUALS = r'='
t_PLUS = r'\+'
t_TIMES = r'\*'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

# Palavras-chave
keywords = {
    'INICIO': 'INICIO',
    'MONITOR': 'MONITOR',
    'EXECUTE': 'EXECUTE',
    'TERMINO': 'TERMINO',
    'ZERO': 'ZERO'
}

# Tabela de símbolos
symbol_table = {}

# Código Python gerado
python_code = []

# Regras para palavras-chave e identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

# Regra para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regra para novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para caracteres inválidos
def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

# Construção do lexer
lexer = lex.lex()

# Regras de gramática (sintáticas)
def p_programa(p):
    'programa : INICIO varlist MONITOR varlist EXECUTE cmds TERMINO'
    python_code.insert(0, "# Programa gerado a partir de Provol-One")
    python_code.insert(1, "# Declaração de variáveis")
    declarations = [f"{var} = 0" for var in symbol_table.keys()]
    for decl in reversed(declarations):
        python_code.insert(2, decl)
    python_code.append("\n# Execução do código")
    print("Programa reconhecido com sucesso!")

def p_varlist(p):
    '''
    varlist : ID COMMA varlist
            | ID
    '''
    if len(p) == 4:
        symbol_table[p[1]] = 0
        p[0] = {p[1]: 0, **p[3]}
    else:
        symbol_table[p[1]] = 0
        p[0] = {p[1]: 0}

def p_cmds(p):
    '''
    cmds : cmd cmds
         | cmd
    '''
    # Continuação das regras para comandos

def p_cmd(p):
    '''
    cmd : ID EQUALS expr
        | ZERO LPAREN ID RPAREN
    '''
    if p[1] == 'ZERO':
        symbol_table[p[3]] = 0
        python_code.append(f"{p[3]} = 0")
        print(f"Zerando variável: {p[3]}")
    else:
        symbol_table[p[1]] = p[3]
        python_code.append(f"{p[1]} = {p[3]}")
        print(f"Atribuição: {p[1]} = {p[3]}")

def p_expr(p):
    '''
    expr : expr PLUS expr
         | expr TIMES expr
         | ID
         | NUMBER
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = f"({p[1]} + {p[3]})"
        elif p[2] == '*':
            p[0] = f"({p[1]} * {p[3]})"
    else:
        if isinstance(p[1], int):
            p[0] = p[1]
        else:
            p[0] = symbol_table.get(p[1], 0)

def p_error(p):
    print("Erro de sintaxe!")

# Construção do parser
parser = yacc.yacc()

# Função principal
def main():
    data = """
    INICIO X, Y
    MONITOR Z
    EXECUTE
    Y = 2
    X = 5
    Z = Y
    ZERO(X)
    Z = Z + X + Y + 1
    Z = Z * Y
    TERMINO
    """
    
    parser.parse(data, lexer=lexer)

    # Exibindo a saída gerada em Python
    print("\nCódigo Python gerado:\n")
    for line in python_code:
        print(line)

    # Exibindo a tabela de símbolos
    print("\nTabela de Símbolos:")
    for var, val in symbol_table.items():
        print(f"{var}: {val}")

if __name__ == "__main__":
    main()
