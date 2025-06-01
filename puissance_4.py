from timeit import default_timer as timer

from board import init_board, print_board, play, terminal, j2, j1, winner, human, alea, j1_str, j2_str,min_max,min_max_trans,alpha_beta,alpha_beta_trans,alea



b = init_board()
print_board(b)
player = j1
transposition_table={}
transposition_table2={}

alpha=float('-inf')
beta=float('+inf') 


ai_functions = {
    "0": lambda b, player: alea(b,player),
    "1": lambda b, player: min_max_trans(b, 6, player, transposition_table),
    "2": lambda b, player: min_max(b, 6, player),
    "3": lambda b, player: alpha_beta(b, 6, player, alpha, beta),
    "4": lambda b, player: alpha_beta_trans(b, 6, player, transposition_table2, alpha, beta),
}

# Ask the user to select the AI function at the start of the game
print("Choose the AI function:")
print("0:  (RANDOM)")
print("1:  (MIN MAXwith transposition table)")
print("2:  (MINMAX AI)")
print("3:  (Alpha-Beta pruning )")
print("4:  (Alpha-Beta pruning with transpositions)")
selected_function = input("Enter the number of your choice: ")

# Check if the selected function is valid
if selected_function not in ai_functions:
    print("Invalid choice. Exiting.")
    exit()
                

while not terminal(b):
    if player == j1:
        start = timer()
        m = human(b, player)
        end = timer()
        print(f'humain a joué en {end - start:.2f}s')
    else:
        start = timer()
        m = ai_functions[selected_function](b, player)
        end = timer()
        print(f'IA aléatoire a joué en {end  - start:.2f}s')

    b = play(b, m, player)
    print_board(b)
    print()
    player = -player

print('Vainqueur: ', end='')
w = winner(b)
if w == j2:
    print(j2_str + " (j2)")
elif w == j1:
    print(j1_str + " (j1)")
else:
    print('égalité')
