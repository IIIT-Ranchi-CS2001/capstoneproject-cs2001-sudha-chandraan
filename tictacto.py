import pygame
import sys
import pyttsx3


pygame.init()
engine = pyttsx3.init()


screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic-Tac-Toe")


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
green = (0, 255, 0)
dark_red = (255, 0, 0)


font = pygame.font.SysFont("comicsansms", 50)
input_font = pygame.font.SysFont("comicsansms", 30)


board = [[" " for _ in range(3)] for _ in range(3)]
cell_size = screen_width // 3  
current_player = "X"


def speak(text):
    """Speaks the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()


def draw_board():
    """Draws the game board."""
    screen.fill(white)

   
    for i in range(1, 3):
        pygame.draw.line(screen, black, (0, i * cell_size), (screen_width, i * cell_size), 3)
        pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, screen_height), 3)

   
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                draw_x(row, col)
            elif board[row][col] == "O":
                draw_o(row, col)


def draw_x(row, col):
    """Draws an X at the given cell."""
    padding = 30
    x_start = col * cell_size + padding
    y_start = row * cell_size + padding
    x_end = (col + 1) * cell_size - padding
    y_end = (row + 1) * cell_size - padding

    pygame.draw.line(screen, red, (x_start, y_start), (x_end, y_end), 5)
    pygame.draw.line(screen, red, (x_end, y_start), (x_start, y_end), 5)


def draw_o(row, col):
    """Draws an O at the given cell."""
    center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2)
    radius = cell_size // 2 - 30
    pygame.draw.circle(screen, blue, center, radius, 5)


def check_winner(player):
    """Checks if the current player has won."""
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([row[col] == player for row in board]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all(
        [board[i][2 - i] == player for i in range(3)]
    ):
        return True
    return False


def show_message(text, color):
    """Displays a message on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)


def get_player_names():
    """Asks for player names on the screen."""
    input_box = pygame.Rect(screen_width // 4, screen_height // 3, screen_width // 2, 50)
    active = False
    player_x_name, player_o_name = "", ""
    current_input = "X"
    input_text = ""  

    while True:
        screen.fill(white)
        message = f"Enter Player {current_input} Name:"
        text_surface = font.render(message, True, black)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(text_surface, text_rect)

        
        pygame.draw.rect(screen, gray if not active else blue, input_box, 2)

        
        input_surface = input_font.render(input_text, True, black)
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if current_input == "X":
                        player_x_name = input_text
                        current_input = "O"
                        input_text = "" 
                    elif current_input == "O":
                        player_o_name = input_text
                        return player_x_name, player_o_name
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode


def show_restart_options():
    """Displays the restart options after the game ends."""
    font_small = pygame.font.SysFont("comicsansms", 40)

    
    play_again_text = font_small.render("Play Again", True, green)
    quit_text = font_small.render("Quit", True, dark_red)

    play_again_rect = play_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    screen.fill(white)
    screen.blit(play_again_text, play_again_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.update()

    return play_again_rect, quit_rect


def tic_tac_toe():
    """Main game loop for Tic-Tac-Toe."""
    global board, current_player

    player_x_name, player_o_name = get_player_names()
    players = {"X": player_x_name, "O": player_o_name}

    running = True
    winner = None
    moves = 0

    while running:
        draw_board()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                x, y = pygame.mouse.get_pos()
                col = x // cell_size
                row = y // cell_size

                if board[row][col] == " ":
                    board[row][col] = current_player
                    moves += 1

                    
                    if check_winner(current_player):
                        winner = current_player

                    current_player = "O" if current_player == "X" else "X"

        
        if winner:
            winner_name = players[winner]
            draw_board()
            show_message(f"{winner_name} wins!", red if winner == "X" else blue)
            speak(f"Congratulations, {winner_name}! You are the winner!")
            play_again_rect, quit_rect = show_restart_options()

            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_again_rect.collidepoint(event.pos):
                            board = [[" " for _ in range(3)] for _ in range(3)]  
                            tic_tac_toe()  
                        elif quit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

        elif moves == 9:
            draw_board()
            show_message("It's a tie!", gray)
            speak("It's a tie!")
            play_again_rect, quit_rect = show_restart_options()

           
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_again_rect.collidepoint(event.pos):
                            board = [[" " for _ in range(3)] for _ in range(3)]  
                            tic_tac_toe()  
                        elif quit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
