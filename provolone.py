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
    'VEZES',
    'ENQUANTO',
    'FACA'
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
    'VEZES': 'VEZES',
    'ENQUANTO': 'ENQUANTO',
    'FACA': 'FACA'
}

# Tabela de símbolos
symbol_table = {}

# Lista de monitorados
monitorados = []

# Código C gerado
c_code = []

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

lexer = lex.lex()

# Regras de gramática (sintáticas)
def p_programa(p):
    'programa : INICIO varlist MONITOR varlist_m EXECUTE cmds TERMINO'
    # inserção de header e função main
    c_code.insert(0, "#include <stdio.h>\nint main() {\n")
    c_code.insert(1, "\n// Declaração de variáveis\n")
    # Declara cada uma das variáveis inicializadas com valor 0
    declarations = [f"int {var} = 0;" for var in symbol_table.keys()]
    for decl in reversed(declarations):
        c_code.insert(2, decl + "\n")
        # Exibe o valor inicial caso a variável esteja monitorada
        if decl.split()[1] in monitorados:
            c_code.insert(3, f'printf("{decl.split()[1]} = 0\\n");\n')
    c_code.append("\n// Execução do código\n")
    c_code.extend(p[6])
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

def p_varlist_m(p):
    '''
    varlist_m : ID COMMA varlist_m
              | ID
    '''
    if len(p) == 4:
        symbol_table[p[1]] = 0
        p[0] = {p[1]: 0, **p[3]}
        monitorados.append(p[1])
    else:
        symbol_table[p[1]] = 0
        p[0] = {p[1]: 0}
        monitorados.append(p[1])

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
        | IF ID THEN cmds FIM
        | IF ID THEN cmds ELSE cmds FIM
        | EVAL cmds VEZES ID FIM
        | ENQUANTO ID FACA cmds FIM
    '''
    if p[1] == 'ZERO':
        symbol_table[p[3]] = 0
        if p[3] in monitorados:
            p[0] = [f'{p[3]} = 0;\nprintf("{p[3]} = %d\\n",{p[3]});\n']
        else:
            p[0] = [f"{p[3]} = 0;\n"]
        print(f"Zerando variável: {p[3]}")
    elif p[1] == 'IF':
        condition = p[2]
        if_block = ''.join(p[4])
        if len(p)==6:
            p[0] = [f"if ({condition})\n{{\n{if_block}}}\n"]
            print(f"Estrutura de controle IF-THEN processada.")
        else:
            else_block = ''.join(p[6])
            p[0] = [f"if ({condition})\n{{\n{if_block}}}\nelse\n{{\n{else_block}}}\n"]
            print(f"Estrutura de controle IF-THEN-ELSE processada.")
    elif p[1] == 'EVAL':
        loop_block = ''.join(p[2])
        iterations = p[4]
        p[0] = [f"for (int i = 0; i < {iterations}; i++)\n{{\n{loop_block}}}\n"]
        print(f"Estrutura de controle EVAL processada.")
    elif p[1] == 'ENQUANTO':
        condition = p[2]
        loop_block = ''.join(p[4])
        p[0] = [f"while ({condition})\n{{\n{loop_block}}}\n"]
        print(f"Estrutura de controle ENQUANTO-FACA processada.")
    else:
        symbol_table[p[1]] = p[3]
        print(f"Atribuição: {p[1]} = {p[3]}")
        if p[1] in monitorados:
            p[0] = [f'{p[1]} = {p[3]};\nprintf("{p[1]} = %d\\n",{p[1]});\n']
        else:
            p[0] = [f"{p[1]} = {p[3]};\n"]

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
        p[0] = p[1]

def p_error(p):
    print("Erro de sintaxe!")

parser = yacc.yacc()

# Função principal
def main():
    data = """
    INICIO Y
    MONITOR Z, A
    EXECUTE
    Y = 2
    ZERO(A)
    Z = Y
    IF A THEN
    EVAL
    Z = Z * 2
    VEZES
    Y
    FIM
    A = A + 3
    ELSE
    Z = Z * 3
    A = A + 1
    FIM
    TERMINO
    """
    
    parser.parse(data, lexer=lexer)

    c_code.append("\n// Exibindo valores das variáveis\n")
    # Exibir valores finais das variáveis, e fechar a função main
    printf_statements = 'printf("' + ', '.join([f"{var}=%d" for var in symbol_table.keys()]) + '", ' + ', '.join(symbol_table.keys()) + ');\n'
    c_code.append(printf_statements)
    c_code.append("\nreturn 0;\n}")

    arq=open("arquivo_de_saida.c","w")
    # Exibir código final, e transformar em arquivo .c
    print("\nCódigo C gerado:\n")
    for line in c_code:
        arq.write(line)
        print(line, end='')
    arq.close()

if __name__ == "__main__":
    main()
