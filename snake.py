import pygame
import random
import pyttsx3
import threading


pygame.init()


engine = pyttsx3.init()


width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")


white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)


background_image = pygame.image.load("./background.png")  
background_image = pygame.transform.scale(background_image, (width, height))  


clock = pygame.time.Clock()


block_size = 20
initial_speed = 10
speed = initial_speed

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


speech_thread = None


def message(msg, color, x, y):
    """Display a message on the screen."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])


def display_score(score):
    """Display the current score on the screen."""
    value = score_font.render(f"Score: {score}", True, white)
    screen.blit(value, [0, 0])


def speak(text):
    """Function to speak the text using pyttsx3 in a separate thread."""
    global speech_thread
    if speech_thread is None or not speech_thread.is_alive():
        def run_speech():
            engine.say(text)
            engine.runAndWait()

        speech_thread = threading.Thread(target=run_speech)
        speech_thread.start()


def game_loop():
    """Main game loop."""
    global speed

    game_over = False
    game_close = False

    x1, y1 = width // 2, height // 2
    x1_change, y1_change = 0, 0

    snake_list = []
    snake_length = 1

    score = 0  

 
    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:
        while game_close:
            screen.blit(background_image, (0, 0))  
            message("You Lost! Press Q-Quit or C-Play Again", red, width / 6, height / 3)
            message(f"Your final score is: {score}", red, width / 4, height / 2)
            pygame.display.update()

            if speech_thread is None or not speech_thread.is_alive():
                speak(f"Game Over. Your score was {score}")

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -block_size
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = block_size

      
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        screen.blit(background_image, (0, 0)) 

        
        pygame.draw.rect(screen, red, [foodx, foody, block_size, block_size])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(screen, white, [segment[0], segment[1], block_size, block_size])

        display_score(score)  

        pygame.display.update()

    
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1
            score += 10

        clock.tick(speed)

    pygame.quit()
    quit()

