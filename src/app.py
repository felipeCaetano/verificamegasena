import ast
import sys

running = True


def add_new_bet():
    with open('bet.dat', 'a') as f:
        print('Digite sua aposta separando os números com espaços\nDigite '
              'enter para encerrar\n\n>>Ex. 1 2 3 4 5 6<ENTER>')
        bet = input('>> ')
        try:
            aposta = [int(x) for x in bet.split()]
            f.writelines(f'{str(aposta)}\n')
        except ValueError:
            print("Aposta deve ser com numeros")
            return
        print("Bet adicionado com sucesso")


def verify_results():
    with open('bet.dat', 'r') as f:
        try:
            resultado = [
                int(x) for x in input('insira as dezenas sorteadas '
                                             'separadas por espaço e pressione '
                                               'Enter\n\n>>'). strip().split()
            ]

            for index, bet in enumerate(f.readlines(), 1):
                print(index, bet)
                bet = ast.literal_eval(bet.strip())
                hits = set(bet).intersection(set(resultado))
                num_hits = len(hits)
                print(resultado, bet, num_hits)
                if num_hits < 4:
                    print('Que pena! Não foi dessa vez... :(')
                elif num_hits == 4:
                    print(f'Você tirou uma quadra com {bet}!!\nParabéns')
                elif num_hits == 5:
                    print(f'Você tirou uma quina com {bet}!!\nParabéns')
                elif num_hits == 6:
                    print(f'Você tirou a sorte grande {bet}!!\nParabéns')
        except ValueError:
            print("Os resultados devem ser com números")



while running:
    option = input("Digite sua opção:\n 1 - cadastrar nova aposta\n 2 - "
                   "Verificar resultado\n 0 - Sair\n\n>>")
    try:
        option = int(option)
        if option == 1:
            add_new_bet()
        if option == 2:
            verify_results()
        if option == 0:
            running = False
            sys.exit(0)
    except ValueError:
        print("Digite uma opção válida")
