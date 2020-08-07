import pygame
import math
import random

# Game Display
pygame.init()

# Fonts
letter_Font = pygame.font.SysFont('comicsansms', 20)
word_Font = pygame.font.SysFont('comicsansms', 40)
title_Font = pygame.font.SysFont('Arial', 50)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 700, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# loading Images
images = []
for i in range(7):
    image = pygame.image.load('Images\hangman' + str(i) + '.png')
    images.append(image)

# Button
Rad = 15
Gap = 15
cordinates = []
startX = round((WIDTH - (Rad * 2 + Gap) * 13) / 2)
startY = 550

for i in range(26):
    x = startX + ((Rad * 2 + Gap) * (i % 13))
    y = startY + ((Rad * 2 + Gap) * (i // 13))
    cordinates.append([x, y, chr(65 + i), True])

# Game variables
hangman_status = 0
words = ["EYE", "ME", "MYSELF", "EGG", "FATHER", "MOTHER", "BROTHER", "SISTER", "YOU", "ALWAYS", "GREAT", "DIPTAM",
         "MOHINI", "DILIP", "MINATI", "PAPU", "PATTON", "MINI", "GOPA", "HALDIA", "INDIA", "DEMONS", "KICHIKICHI",
         "MOTILAL", "MOTU"]
word = random.choice(words)
guessed = []


def next_move():
    global hangman_status
    global word
    guessed.clear()
    hangman_status = 0
    for c in cordinates:
        c[3] = True
    word = random.choice(words)
    main()


def display_message(message, color, w):  # Displaying the results
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = word_Font.render(message, 1, color)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 - 100))
    if color == RED:
        t = word_Font.render("The word is:" + w, 1, BLUE)
        win.blit(t, (WIDTH / 2 - text.get_width() / 2 - 50, HEIGHT / 2 - text.get_height() / 2))

    t = word_Font.render("Do You Want Play More?", 1, BLACK)
    win.blit(t, (WIDTH / 2 - text.get_width() / 2 - 80, HEIGHT / 2 - text.get_height() / 2 + 100))
    pygame.draw.rect(win, BLACK, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 + 200, 60, 40),
                     1)
    txt = letter_Font.render("YES", 1, BLACK)
    win.blit(txt, (WIDTH / 2 - text.get_width() / 2 + 10, HEIGHT / 2 - text.get_height() / 2 + 200))
    pygame.draw.rect(win, BLACK,
                     (WIDTH / 2 - text.get_width() / 2 + 120, HEIGHT / 2 - text.get_height() / 2 + 200, 60, 40), 1)
    txt = letter_Font.render("NO", 1, BLACK)
    win.blit(txt, (WIDTH / 2 - text.get_width() / 2 + 130, HEIGHT / 2 - text.get_height() / 2 + 200))

    pygame.display.update()
    pygame.time.delay(10000)
    for events in pygame.event.get():
        if events.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if (WIDTH / 2 - text.get_width() / 2 <= x <= WIDTH / 2 - text.get_width() / 2 + 60) and (
                    (HEIGHT / 2 - text.get_height() / 2 + 200) <= y <= (HEIGHT / 2 - text.get_height() / 2 + 240)):
                next_move()
            if (WIDTH / 2 - text.get_width() / 2 + 120 <= x <= WIDTH / 2 - text.get_width() / 2 + 180) and (
                    (HEIGHT / 2 - text.get_height() / 2 + 200) <= y <= (HEIGHT / 2 - text.get_height() / 2 + 240)):
                pygame.quit()


def draw():
    win.fill(WHITE)  # fr white background

    # Display Words
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = word_Font.render(display_word, 1, BLACK)
    win.blit(text, (200, 400))
    text = title_Font.render("HANGMAN GAME", 1, BLUE)
    win.blit(text, (100, 10))

    # Draw Button
    for c in cordinates:
        x1, y1, letter, visible = c
        if visible:
            pygame.draw.circle(win, BLACK, (x1, y1), Rad, 1)  # For the circle
            txt = letter_Font.render(letter, 1, BLACK)
            win.blit(txt, (x1 - txt.get_width() / 2, y1 - txt.get_height() / 2))  # For the texts inside the circle

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def main():
    # Game timing
    FPS = 60  # 60 frames per second
    clock = pygame.time.Clock()
    run = True  # until a outcome is there it will run

    # game loop
    while run:
        clock.tick(FPS)
        global hangman_status
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False
            if events.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for c in cordinates:
                    x, y, ltr, visible = c
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < Rad:
                            c[3] = False  # Making visible variable false to vanish that letter
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()
        won = True
        for letters in word:
            if letters not in guessed:
                won = False
                break
        if won:
            display_message("YOU WON!!", GREEN, word)
            break
        if hangman_status == 6:
            display_message("YOU LOSE!!", RED, word)
            break


main()
pygame.quit()
