import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'ID',
    'NUMBER',
    'EQUALS',
    'PLUS',
    'TIMES',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'INICIO',
    'MONITOR',
    'EXECUTE',
    'TERMINO',
    'ZERO',
    'IF',
    'THEN',
    'ELSE',
    'FIM',
    'EVAL',
    'VEZES'
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
    'ZERO': 'ZERO',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'FIM': 'FIM',
    'EVAL': 'EVAL',
    'VEZES': 'VEZES'
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
    python_code.insert(0, "#include <stdio.h>\nint main() {\n")
    python_code.insert(1, "\n// Declaração de variáveis\n")
    declarations = [f"int {var} = 0;" for var in symbol_table.keys()]
    for decl in reversed(declarations):
        python_code.insert(2, decl + "\n")
    python_code.append("\n// Execução do código\n")
    python_code.extend(p[6])
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
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_cmd(p):
    '''
    cmd : ID EQUALS expr
        | ZERO LPAREN ID RPAREN
        | IF ID THEN cmds ELSE cmds
        | EVAL cmds VEZES ID FIM
    '''
    if p[1] == 'ZERO':
        symbol_table[p[3]] = 0
        p[0] = [f"{p[3]} = 0;\n"]
        print(f"Zerando variável: {p[3]}")
    elif p[1] == 'IF':
        condition = p[2]
        if_block = ''.join(p[4])
        else_block = ''.join(p[6])
        p[0] = [f"if ({condition})\n{{\n{if_block}}}\nelse\n{{\n{else_block}}}\n"]
        print(f"Estrutura de controle IF-THEN-ELSE processada.")
    elif p[1] == 'EVAL':
        loop_block = ''.join(p[2])
        iterations = p[4]
        p[0] = [f"for (int i = 0; i < {iterations}; i++)\n{{\n{loop_block}}}\n"]
        print(f"Estrutura de controle EVAL processada.")
    else:
        symbol_table[p[1]] = p[3]
        p[0] = [f"{p[1]} = {p[3]};\n"]
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
            p[0] = p[1]

def p_error(p):
    print("Erro de sintaxe!")

# Construção do parser
parser = yacc.yacc()

# Função principal
def main():
    data = """
    INICIO Y, A
    MONITOR Z
    EXECUTE
    A = 1
    Y = 2
    Z = Y
    IF A THEN
    EVAL
    Z = Z + 1
    VEZES
    Y
    FIM
    ELSE
    Z = A + 1
    TERMINO
    """
    
    parser.parse(data, lexer=lexer)

    # Termiando o código Python gerado
    python_code.append("\n// Exibindo valores das variáveis\n")
    printf_statements = 'printf("' + ', '.join([f"{var}=%d" for var in symbol_table.keys()]) + '", ' + ', '.join(symbol_table.keys()) + ');\n'
    python_code.append(printf_statements)
    python_code.append("\nreturn 0;\n}")

    # Exibindo a saída gerada em Python
    print("\nCódigo Python gerado:\n")
    for line in python_code:
        print(line, end='')

if __name__ == "__main__":
    main()