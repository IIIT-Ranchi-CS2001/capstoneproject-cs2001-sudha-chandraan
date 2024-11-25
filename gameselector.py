import pygame
import sys
import threading
import pyttsx3
from snake import game_loop as snake_game
from tictacto import tic_tac_toe


pygame.init()
engine = pyttsx3.init()


width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Selector")


white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 128, 255)
gray = (169, 169, 169)
green = (0, 255, 0)
red = (255, 0, 0)


font = pygame.font.SysFont("bahnschrift", 50)
button_font = pygame.font.SysFont("comicsansms", 30)


button_width, button_height = 300, 80
snake_button = pygame.Rect(width // 2 - button_width // 2, height // 3, button_width, button_height)
tictactoe_button = pygame.Rect(width // 2 - button_width // 2, height // 2, button_width, button_height)


def speak(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run_speech).start()


def draw_buttons():
    """Draws the buttons for selecting games."""
    pygame.draw.rect(screen, green, snake_button)
    pygame.draw.rect(screen, blue, tictactoe_button)

    
    snake_label = button_font.render("Play Snake Game", True, black)
    tictactoe_label = button_font.render("Play Tic-Tac-Toe", True, black)

    
    snake_text_rect = snake_label.get_rect(center=snake_button.center)
    tictactoe_text_rect = tictactoe_label.get_rect(center=tictactoe_button.center)

    screen.blit(snake_label, snake_text_rect)
    screen.blit(tictactoe_label, tictactoe_text_rect)


def game_selector():
    """Main loop for the game selector."""
    running = True
    speak("Welcome to the game selector. Choose a game to play.")

    while running:
        screen.fill(white)

        
        title = font.render("Choose Your Game!", True, black)
        title_rect = title.get_rect(center=(width // 2, height // 6))
        screen.blit(title, title_rect)

        
        draw_buttons()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()


                if snake_button.collidepoint(mouse_pos):
                    speak("Starting Snake Game.")
                    snake_game()  
                    running = False


                elif tictactoe_button.collidepoint(mouse_pos):
                    speak("Starting Tic-Tac-Toe.")
                    tic_tac_toe()  
                    running = False


if __name__ == "__main__":
    game_selector() 