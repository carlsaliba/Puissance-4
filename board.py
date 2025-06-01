"""
Author: Didier Lime
Course: Game Theory
Year: 2024-2025
Note: The base of the code was provided by Didier Lime.
"""
from random import randint
from copy import deepcopy
import random

width= 7
height = 6

j2 = -1
j1 = 1


j2_str = " O"
j1_str = " X"
# j2_str = "\x1b[1m\x1b[31m O\x1b[0m"
# j1_str = "\x1b[1m\x1b[33m O\x1b[0m"

empty = 0
border = 100

dirs = [ 1, width + 2, width + 3, width + 1 ]

class Board:
    def __init__(self):
        self.grid = [empty for i in range((height + 2)* (width + 2))]
        for i in range(width + 2):
            self.grid[i] = border
            self.grid[(height + 1) * (width + 2) + i] = border

        for i in range(height + 2):
            self.grid[i * (width + 2)] = border
            self.grid[i * (width + 2) + width + 1] = border

        self.win = 0
        self.played = 0
        self.eval=0


def init_board():
    return Board()

# copy for MCTS
def copy_board(board):
    return deepcopy(board)

# get a key for transposition tables
def board_key(board):
    return tuple(board.grid)

def print_board(board):
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            k = i * (width + 2) + j
            if board.grid[k] == j1:
                print(j1_str, end='')
            elif board.grid[k] == j2:
                print(j2_str, end='')
            else:
                print(' .', end='')

        print()
    for i in range(1, width+ 1):
        print(f' {i}', end='')
    print()




def play_(board, position, player):
    board.grid[position] = player
    board.played = board.played + 1
    for d in dirs:
        # is the new sequence extensible (left or right)?
        extl = 0
        extr = 0
        
        # compte les pions de la couleur du joueur dans la direction d et après la position courante
        sum_right = 0
        k = 1
        while board.grid[position + k * d] == player:
            k = k + 1
            sum_right = sum_right + 1

        if board.grid[position + k * d] == empty:
            extl = 1
            
        # compte les pions de la couleur du joueur dans l'opposé de la direction d et avant la position courante
        sum_left = 0
        k = 1
        while board.grid[position - k * d] == player:
            k = k + 1
            sum_left = sum_left + 1

        if board.grid[position - k * d] == empty:
            extr = 1
            
        # on a créé une nouvelle séquence de taille sum_left + sum_right + 1
        if sum_right + sum_left + 1 >= 4:
            board.win = player
    
        # évaluation incrémentale
        # il n'y a une séquence à enlever que si sum_right > 1
        # cette séquence était forcément extensible à gauche, puisqu'on y met un pion
        if sum_right > 1:
            board.eval = board.eval - player * 100**(sum_right + extr + 1)

        # symétrique        
        if sum_left > 1:
            board.eval = board.eval - player * 100**(sum_left + extl + 1)
            
        # on ne compte pas les pions tout seuls, ce qui évite de 
        # les compter une fois par direction
        # on veut aussi que la séquence obtenue soit extensible
        if sum_right + sum_left > 0 and extl + extr > 0:
            board.eval = board.eval + player * 100**(sum_right + sum_left + extl + extr + 1)    

# La fonction d'évaluation proprement dite
# Le cas de la victoire/défaite doit être plus important que tout le reste
def evaluate(board):
    if board.win != empty:
        return (10**16)*board.win
    else:
        return board.eval



# Successeur avec copie
def play(board, position, player):
    r = deepcopy(board)
    play_(r, position, player)

    return r

def terminal(board):
    return winner(board) != 0 or board.played == height * width

def winner(board):
    return board.win

def legal_moves(board, player):
    L = []
    for i in range(width):
        k = height * (width + 2) + i + 1
        while k >= 0 and board.grid[k] != empty:
            k = k - (width + 2)

        if k >= 0:
            L.append(k)

    return L

def human(board, player):
    while (True):
        i = int(input('Votre coup (numéro de colonne):'))
        k = height * (width + 2) + i
        while k >= 0 and board.grid[k] != empty:
            k = k - (width + 2)

        if k >= 0:
            return k
        else:
            print('Coup invalide')


def alea(board, player):
    L = legal_moves(board, player)
    print(L)
    x = randint(0, len(L) - 1)

    return L[x]



def min_max(board,depth,player):
#minmax normal
    max_score, best_position=minimax(board, depth, player)
    

    return best_position


def min_max_trans(board,depth,player,transposition_table):
    #this is minmax with transposition
    max_score, best_position=minimax_tr(board, depth, player,transposition_table)
    

    return best_position


def alpha_beta(board,depth,player,alpha,beta):
#elegage alpha beta
    max_score, best_position=alphabeta(board, depth, player, alpha,beta)
    

    return best_position



def alpha_beta_trans(board,depth,player,transpos,alpha,beta):
#elegage alpha beta with transpositioin
    max_score, best_position=alphabeta_trans(board, depth, player,transpos, alpha,beta)
    

    return best_position

      

def minimax(board, depth, player):
    """
    Implémentation de l'algorithme Minimax sans élagage alpha-beta.

    Args:
        board (Board): L'état actuel du plateau de jeu.
        depth (int): La profondeur maximale de recherche.
        player (int): Le joueur actuel (+1 pour MAX, -1 pour MIN).

    Returns:
        tuple: (meilleur_score, meilleure_position)
    """

    # Vérifier si on atteint un état terminal ou la profondeur maximale
    if depth == 0 or terminal(board):
        return evaluate(board), None

    max_score = float('-inf') if player == 1 else float('inf')
    best_position = None

    for pos in legal_moves(board, player):
        # Appliquer le mouvement et obtenir un nouvel état
        new_state = play(board, pos, player)

        # Appel récursif pour l'adversaire
        score, _ = minimax(new_state, depth - 1, -player)

        if player == 1:  # Maximiser pour le joueur MAX
            if score > max_score:
                max_score = score
                best_position = pos
        else:  # Minimiser pour le joueur MIN
            if score < max_score:
                max_score = score
                best_position = pos

    return max_score, best_position

def minimax_tr(board, depth, player, transposition_table):
    """
    Implémentation de l'algorithme Minimax avec une table de transpositions.

    Args:
        board (Board): L'état actuel du plateau de jeu.
        depth (int): La profondeur maximale de recherche.
        player (int): Le joueur actuel (+1 pour MAX, -1 pour MIN).
        transposition_table (dict): La table de transpositions.

    Returns:
        tuple: (meilleur_score, meilleure_position)
    """
    # Générer une clé unique pour l'état actuel (exemple: tuple de la grille et joueur)
    key = (tuple(board.grid), player)

    # Vérifier si la position est déjà dans la table de transpositions
    if key in transposition_table:
        saved_depth, saved_score, saved_move = transposition_table[key]
        # Utiliser l'évaluation seulement si elle a été réalisée à une profondeur suffisante
        if saved_depth >= depth:
            return saved_score, saved_move

    # Vérifier si on atteint un état terminal ou la profondeur maximale
    if depth == 0 or terminal(board):
        score = evaluate(board)
        transposition_table[key] = (depth, score, None)
        return score, None

    max_score = float('-inf') if player == 1 else float('inf')
    best_position = None

    for pos in legal_moves(board, player):
        # Appliquer le mouvement et obtenir un nouvel état
        new_state = play(board, pos, player)

        # Appel récursif pour l'adversaire
        score, _ = minimax_tr(new_state, depth - 1, -player, transposition_table)

        if player == 1:  # Maximiser pour le joueur MAX
            if score > max_score:
                max_score = score
                best_position = pos
        else:  # Minimiser pour le joueur MIN
            if score < max_score:
                max_score = score
                best_position = pos

    # Stocker le résultat dans la table de transpositions
    transposition_table[key] = (depth, max_score, best_position)

    return max_score, best_position
     

def alphabeta(board, depth, player, alpha=float('-inf'), beta=float('inf')):
    """
    Implémentation de l'algorithme Alpha-Bêta pour optimiser Minimax.

    Args:
        board (Board): L'état actuel du plateau de jeu.
        depth (int): La profondeur maximale de recherche.
        player (int): Le joueur actuel (+1 pour MAX, -1 pour MIN).
        alpha (float): La meilleure valeur connue pour le joueur MAX.
        beta (float): La meilleure valeur connue pour le joueur MIN.

    Returns:
        tuple: (meilleur_score, meilleure_position)
    """
    # Vérifier si on atteint un état terminal ou la profondeur maximale
    if depth == 0 or terminal(board):
        return evaluate(board), None

    best_position = None

    if player == 1:  # Maximiser
        max_score = float('-inf')
        for pos in legal_moves(board, player):
            # Appliquer le mouvement et obtenir un nouvel état
            new_state = play(board, pos, player)

            # Appel récursif pour l'adversaire
            score, _ = alphabeta(new_state, depth - 1, -player, alpha, beta)

            # Mettre à jour le score maximum
            if score > max_score:
                max_score = score
                best_position = pos

            # Mettre à jour alpha et couper si nécessaire
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Coupure bêta

        return max_score, best_position

    else:  # Minimiser
        min_score = float('inf')
        for pos in legal_moves(board, player):
            # Appliquer le mouvement et obtenir un nouvel état
            new_state = play(board, pos, player)

            # Appel récursif pour l'adversaire
            score, _ = alphabeta(new_state, depth - 1, -player, alpha, beta)

            # Mettre à jour le score minimum
            if score < min_score:
                min_score = score
                best_position = pos

            # Mettre à jour beta et couper si nécessaire
            beta = min(beta, score)
            if beta <= alpha:
                break  # Coupure alpha

        return min_score, best_position


def alphabeta_trans(board, depth, player,tranpos_table,alpha=float('-inf'), beta=float('inf')):
    """
    Implémentation de l'algorithme Alpha-Bêta pour optimiser Minimax.
    
    Args:
        board (Board): L'état actuel du plateau de jeu.
        depth (int): La profondeur maximale de recherche.
        player (int): Le joueur actuel (+1 pour MAX, -1 pour MIN).
        alpha (float): La meilleure valeur connue pour le joueur MAX.
        beta (float): La meilleure valeur connue pour le joueur MIN.

    Returns:
        tuple: (meilleur_score, meilleure_position)
    """
    # Vérifier si on atteint un état terminal ou la profondeur maximale
    key = (tuple(board.grid), player)

    # Vérifier si la position est déjà dans la table de transpositions
    if key in tranpos_table:
        saved_depth, saved_score, saved_move = tranpos_table[key]
        # Utiliser l'évaluation seulement si elle a été réalisée à une profondeur suffisante
        if saved_depth >= depth:
            return saved_score, saved_move



    if depth == 0 or terminal(board):
        score = evaluate(board)
        tranpos_table[key] = (depth, score, None)
        return score, None

    best_position = None
   
    if player == 1:  # Maximiser
        max_score = float('-inf')
        for pos in legal_moves(board, player):
            # Appliquer le mouvement et obtenir un nouvel état
            new_state = play(board, pos, player)

            # Appel récursif pour l'adversaire
            score, _ = alphabeta(new_state, depth - 1, -player, alpha, beta)

            # Mettre à jour le score maximum
            if score > max_score:
                max_score = score
                best_position = pos

            # Mettre à jour alpha et couper si nécessaire
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Coupure bêta
        
        tranpos_table[key] = (depth, max_score, best_position)

        return max_score, best_position

    else:  # Minimiser
        min_score = float('inf')
        for pos in legal_moves(board, player):
            # Appliquer le mouvement et obtenir un nouvel état
            new_state = play(board, pos, player)

            # Appel récursif pour l'adversaire
            score, _ = alphabeta(new_state, depth - 1, -player, alpha, beta)

            # Mettre à jour le score minimum
            if score < min_score:
                min_score = score
                best_position = pos

            # Mettre à jour beta et couper si nécessaire
            beta = min(beta, score)
            if beta <= alpha:
                break  # Coupure alpha
        tranpos_table[key] = (depth, min_score, best_position)

        return min_score, best_position



