import json
import sys

running = True
FILE_NAME = 'bet.json'


def add_new_bet():
    print(
        'Digite sua aposta separando os números com espaços ou virgulas\n'
        'Digite enter para encerrar\n\n>> Ex. 1 2 3 4 5 6 ou 1,2,3,4,5,6'
    )

    bet_input = input('>> ').strip()
    bet_input = bet_input.replace(',', ' ')

    try:
        aposta = [int(x) for x in bet_input.split()]
    except ValueError:
        print("Aposta deve conter apenas números")
        return

    registro = {"bet": aposta}

    with open(FILE_NAME, 'a', encoding='utf-8') as f:
        f.write(json.dumps(registro) + '\n')

    print("Bet adicionado com sucesso\n\n")


def verify_results():
    try:
        resultado = [
            int(x) for x in input(
                'Insira as dezenas sorteadas separadas por espaço ou '
                'vírgula\n\n>> '
            ).replace(',', ' ').split()
        ]
    except ValueError:
        print("Os resultados devem ser com números")
        return

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        for index, line in enumerate(f, 1):
            try:
                registro = json.loads(line)
                bet = registro["bet"]
            except (json.JSONDecodeError, KeyError):
                print(f"Aposta inválida na linha {index}, ignorando")
                continue

            hits = set(bet).intersection(resultado)
            num_hits = len(hits)

            print(f"Aposta {index}: {bet} → {num_hits} acertos")

            if num_hits < 4:
                print('Que pena! Não foi dessa vez... :(')
            elif num_hits == 4:
                print(f'Você tirou uma quadra com {bet}!!\nParabéns\n')
            elif num_hits == 5:
                print(f'Você tirou uma quina com {bet}!!\nParabéns\n')
            elif num_hits == 6:
                print(f'Você tirou a sorte grande {bet}!!\nParabéns\n')


while running:
    option = input(
        "Digite sua opção:\n"
        "1 - cadastrar nova aposta\n"
        "2 - verificar resultado\n"
        "0 - sair\n\n>> "
    )

    try:
        option = int(option)
    except ValueError:
        print("Digite uma opção válida")
        continue

    if option == 1:
        add_new_bet()
    elif option == 2:
        verify_results()
    elif option == 0:
        sys.exit(0)
