import sqlite3

conexao = sqlite3.connect('clinica.db')
cursor = conexao.cursor()

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente TEXT NOT NULL,
    idade INTEGER NOT NULL,
    procedimento TEXT NOT NULL,
    faltou TEXT NOT NULL,
    valor REAL NOT NULL)
''')

conexao.commit()

cursor.execute('SELECT COUNT(*) FROM agendamentos')
if cursor.fetchone()[0] == 0:
    dados_iniciais = [

        ('ana silva', 25, 'Limpeza', 'Nao', 150.00),
        ('carlos souza', 42, 'Implante', 'Sim', 3000.00),
        ('beatriz lima', 19, 'Aparelho', 'Nao', 80.00),
        ('joao santos', 60, 'Protese', 'Nao', 600.00),
        ('mariana costa', 35, 'Dor de Dente', 'Sim', 100.00),
        ('ricardo oliveira', 55, 'Limpeza', 'Nao', 150.00),
        ('fernanda ribeiro', 69, 'Implante', 'Nao', 3000.00),
    ]
    cursor.executemany('INSERT INTO agendamentos (paciente, idade, procedimento, faltou, valor) VALUES (?, ?, ?, ?, ?)', dados_iniciais)
    conexao.commit()

cursor.execute('SELECT COUNT(*) FROM agendamentos')
total_atendimentos = cursor.fetchone()[0]

while True:
    print('\n' + '=' * 55)
    print('   SISTEMA DE CONSULTA DE HISTÓRICO DE AGENDAMENTOS   ')
    print('\n' + '=' * 55)
    print('[1] media de idade dos pacientes agendados')
    print('[2] quantidade de pacientes que faltaram')
    print('[3] quantidade de pacientes do grupo de risco')
    print('[4] Todos os agendamentos')
    print('[5] Estatisticas de Tratamento e Faturamento')
    print('[6] Sair')
    print('\n' + '=' * 55)

    opcao = input('Doutor(a), digite a opção desejada: ')

    if opcao == '1':
        cursor.execute('SELECT AVG(idade) FROM agendamentos')
        media_idade = cursor.fetchone()[0]
        print('-' * 55)
        print(f'A média de idade dos pacientes agendados é: {media_idade:.1f} anos.')
        print('-' * 55)

    elif opcao == '2':
        cursor.execute('SELECT COUNT(*) FROM agendamentos WHERE LOWER(faltou) = "sim"')
        total_faltas = cursor.fetchone()[0]
        taxa_faltas = (total_faltas / total_atendimentos) * 100
        print('-' * 55)
        print(f'Total de faltas: {total_faltas} de um total de {total_atendimentos} pacientes agendados.')
        print(f'Taxa atual de faltas da clinica: {taxa_faltas:.1f}%.')
        print('-' * 55)

    elif opcao == '3':
        print('-' * 55)
        print('Pacientes do grupo de risco!\nPrecisam de acompanhamento:')
        cursor.execute('SELECT paciente, idade , procedimento FROM agendamentos WHERE idade >= 50 AND LOWER(procedimento) = "implante"')
        registro_risco = cursor.fetchall()
        for r in registro_risco:
            print(f"Paciente: {r[0]}, Idade: {r[1]}, Procedimento: {r[2]}")
        if len(registro_risco) == 0:
            print('Nenhum paciente do grupo de risco encontrado.')
        print('-' * 55)

    elif opcao == '4':
        print('-' * 55)
        print('Todos os agendamentos:')
        cursor.execute('SELECT paciente, idade, procedimento, faltou FROM agendamentos')
        todos_dados=cursor.fetchall()
        for r in todos_dados:
            print(f"Paciente: {r[0]}, Idade: {r[1]}, Procedimento: {r[2]}, Faltou: {r[3]}")
        print('-' * 55)    


    elif opcao == '5':
        print('-' * 55)
        print('Estatísticas de Tratamento e Faturamento:')
        cursor.execute('SELECT procedimento FROM agendamentos GROUP BY procedimento ORDER BY COUNT(*) DESC LIMIT 1')
        tratamento_mais_frequente = cursor.fetchone()[0]
        print(f"Tratamento mais Procurado na clinica: {tratamento_mais_frequente}")
        cursor.execute('SELECT SUM(valor) FROM agendamentos WHERE LOWER(faltou) = "nao"')
        faturamento_total = cursor.fetchone()[0] or 0.0
        cursor.execute('SELECT SUM(valor) FROM agendamentos WHERE LOWER(faltou) = "sim"')
        faturamento_perdido = cursor.fetchone()[0] or 0.0
        print(f"Faturamento total da clinica: R$ {faturamento_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"Faturamento perdido devido a faltas: R$ {faturamento_perdido:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print('-' * 55)


    elif opcao == '6':
        print('Encerrando o painel de consultas. Até logo, Doutor(a)!\n')
        break

    else:
        print('Opção inválida. Por favor, digite um numero de 1 a 6.')

    input('\n pressione ENTER para voltar ao menu principal...')    
