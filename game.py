import tkinter as tk
from tkinter import messagebox
import pygame


pygame.mixer.init()


click_x_sound = pygame.mixer.Sound("click_x.wav")
click_o_sound = pygame.mixer.Sound("click_o.wav")


x_win_row = pygame.mixer.Sound("x_win_row.wav")
x_win_col = pygame.mixer.Sound("x_win_col.wav")
x_win_diag = pygame.mixer.Sound("x_win_diag.wav")


o_win_row = pygame.mixer.Sound("o_win_row.wav")
o_win_col = pygame.mixer.Sound("o_win_col.wav")
o_win_diag = pygame.mixer.Sound("o_win_diag.wav")


x_voice = pygame.mixer.Sound("x_wins_voice.mp3")
o_voice = pygame.mixer.Sound("o_wins_voice.mp3")

draw_sound = pygame.mixer.Sound("draw.wav")

root = tk.Tk()
root.title("Smart Tic Tac Toe")
root.attributes('-fullscreen', True)
root.configure(bg="#121212")

current_player = None
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]


def play_sound(sound):
    pygame.mixer.Sound.play(sound)

def choose_player(choice):
    global current_player
    current_player = choice
    start_frame.pack_forget()
    game_frame.pack(expand=True)

def check_winner():
    
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return ("row", board[i][0])
    
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != "":
            return ("col", board[0][i])
    
    if board[0][0] == board[1][1] == board[2][2] != "":
        return ("diag", board[0][0])
    if board[0][2] == board[1][1] == board[2][0] != "":
        return ("diag", board[0][2])
    return None

def is_draw():
    return all(board[i][j] != "" for i in range(3) for j in range(3))

def play_click_sound(player):
    play_sound(click_x_sound if player == "X" else click_o_sound)

def play_win_sound(player, win_type):
    """Play line-type sound + voice for the winner"""
    
    if player == "X":
        if win_type == "row": play_sound(x_win_row)
        elif win_type == "col": play_sound(x_win_col)
        elif win_type == "diag": play_sound(x_win_diag)
        
        root.after(500, lambda: play_sound(x_voice))
    else:
        if win_type == "row": play_sound(o_win_row)
        elif win_type == "col": play_sound(o_win_col)
        elif win_type == "diag": play_sound(o_win_diag)
        
        root.after(500, lambda: play_sound(o_voice))

def on_click(row, col):
    global current_player
    if board[row][col] == "":
        board[row][col] = current_player
        play_click_sound(current_player)
        buttons[row][col].config(text=current_player, state="disabled",
                                 disabledforeground="white",
                                 bg="#4a90e2" if current_player == "X" else "#f06292")

        result = check_winner()
        if result:
            win_type, winner = result
            play_win_sound(winner, win_type)  
            messagebox.showinfo("Game Over", f" Player {winner} wins!")
            reset_game()
        elif is_draw():
            play_sound(draw_sound)
            messagebox.showinfo("Game Over", " It's a Draw!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"

def reset_game():
    global board, current_player
    current_player = None
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal", bg="#2d2d2d")
    game_frame.pack_forget()
    start_frame.pack(pady=50)

def exit_game():
    root.destroy()


start_frame = tk.Frame(root, bg="#121212")
start_frame.pack(expand=True)

title = tk.Label(start_frame, text="Choose Your Player", font=("Arial", 28, "bold"), fg="white", bg="#121212")
title.pack(pady=20)

btn_x = tk.Button(start_frame, text="Play as X", font=("Arial", 18, "bold"),
                  bg="#4a90e2", fg="white", width=15, height=2, command=lambda: choose_player("X"))
btn_x.pack(pady=10)

btn_o = tk.Button(start_frame, text="Play as O", font=("Arial", 18, "bold"),
                  bg="#f06292", fg="white", width=15, height=2, command=lambda: choose_player("O"))
btn_o.pack(pady=10)

exit_btn = tk.Button(start_frame, text="Exit", font=("Arial", 14),
                     bg="#ff7043", fg="white", width=10, command=exit_game)
exit_btn.pack(pady=30)

# Game Board Frame
game_frame = tk.Frame(root, bg="#121212")

for i in range(3):
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=("Arial", 60, "bold"),
                        width=4, height=2, bg="#2d2d2d", fg="white",
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
        buttons[i][j] = btn
        game_frame.grid_rowconfigure(i, weight=1)
        game_frame.grid_columnconfigure(j, weight=1)

root.mainloop()
