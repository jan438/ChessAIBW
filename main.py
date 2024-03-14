import boardai, piecesai, ai
from move import Move
import os
import sys
import platform
import sysconfig
import csv
import time

# Returns a move object based on the users input. Does not check if the move is valid.
def get_user_move():
    print("Example Move: A2 A4")
    move_str = input("Your Move: ")
    move_str = move_str.replace(" ", "")

    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2]) # The boardai is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4]) # The boardai is drawn "upside down", so flip the y coordinate.
        return Move(xfrom, yfrom, xto, yto)
    except ValueError:
        print("Invalid format. Example: A2 A4")
        return get_user_move()

# Returns a valid move based on the users input.
def get_valid_user_move(boardai):
    while True:
        move = get_user_move()
        valid = False
        possible_moves = boardai.get_possible_moves(piecesai.Piece.WHITE)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                valid = True
                break

        if (valid):
            break
        else:
            print("Invalid move.")
    return move

# Converts a letter (A-H) to the x position on the chess boardai.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7

    raise ValueError("Invalid letter.")

#
# Entry point.
#
boardai = boardai.Boardai.new()
print("Human ", boardai.human)
print(boardai.to_string())

if boardai.human == "White":
    hmcolor = piecesai.Piece.WHITE
    aicolor = piecesai.Piece.BLACK
    while True:
        move = get_valid_user_move(boardai)
        if (move == 0):
            if (boardai.is_check(hmcolor)):
                print("Checkmate. Black Wins.")
                break
            else:
                print("Stalemate.")
                break

        boardai.perform_move(move)

        print("User move: " + move.to_string())
        print(boardai.to_string())

        ai_move = ai.AI.get_ai_move(boardai, [])
        if (ai_move == 0):
            if (boardai.is_check(aicolor)):
                print("Checkmate. White wins.")
                break
            else:
                print("Stalemate.")
                break

        boardai.perform_move(ai_move)
        print("AI move: " + ai_move.to_string())
        print(boardai.to_string())
