import pygame
import sys
from game import Game
from couleurs import Colors

# Initialisation de pygame
pygame.init()


# Paramètres de la fenêtre
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 620
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Titre au dessus de la fenêtre
pygame.display.set_caption("Tetris en Python (TFE)")


# Rafraichissement du jeu
clock = pygame.time.Clock()


# Police d'écriture
title_font = pygame.font.Font(None, 40)


# MENU PRINCIPAL ET PAUSE
# tailles des boutons des menus
BUTTON_WIDTH_MAIN = 140
BUTTON_HEIGHT_MAIN = 60
BUTTON_WIDTH_PAUSE = 210
BUTTON_HEIGHT_PAUSE = 60

# Marges pour le centrage
MARGIN_Y_MAIN = 20
MARGIN_Y_PAUSE = 20

# Texte du menu principal
menu_title_surface = title_font.render("Tetris", True, Colors.white)
play_surface = title_font.render("Jouer", True, Colors.white)
quit_surface = title_font.render("Quitter", True, Colors.white)

# Texte du menu de pause
resume_surface = title_font.render("Continuer", True, Colors.white)
menu_surface = title_font.render("Menu principal", True, Colors.white)

# centrage des boutons sur l'écran
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

play_rect = pygame.Rect(
    center_x - BUTTON_WIDTH_MAIN // 2,  # Centre horizontalement
    center_y - MARGIN_Y_MAIN - BUTTON_HEIGHT_MAIN,  # Au-dessus du bouton "Quitter"
    BUTTON_WIDTH_MAIN,
    BUTTON_HEIGHT_MAIN
)

quit_rect = pygame.Rect(
    center_x - BUTTON_WIDTH_MAIN // 2,  # Centre horizontalement
    center_y + MARGIN_Y_MAIN,  # Sous le bouton "Jouer"
    BUTTON_WIDTH_MAIN,
    BUTTON_HEIGHT_MAIN
)

# Rectangles des boutons du menu de pause
resume_rect = pygame.Rect(
    center_x - BUTTON_WIDTH_PAUSE // 2,  # Centre horizontalement
    center_y - MARGIN_Y_PAUSE - BUTTON_HEIGHT_PAUSE,  # Au-dessus du bouton "Menu principal"
    BUTTON_WIDTH_PAUSE,
    BUTTON_HEIGHT_PAUSE
)

menu_rect = pygame.Rect(
    center_x - BUTTON_WIDTH_PAUSE // 2,  # Centre horizontalement
    center_y + MARGIN_Y_PAUSE,  # Sous le bouton "Continuer"
    BUTTON_WIDTH_PAUSE,
    BUTTON_HEIGHT_PAUSE
)


# État du jeu
in_menu = True
is_paused = False
game = Game()

# Événement pour mettre à jour le jeu
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 300)


# Fonction pour démarrer une nouvelle partie
def start_new_game():
    global game, in_menu, is_paused
    game = Game()
    in_menu = False
    is_paused = False


# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not in_menu:
                is_paused = not is_paused  # Basculer en mode pause
            if not in_menu and not is_paused:
                if game.game_over:
                    game.game_over = False
                    game.reset()
                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()
                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()
        elif event.type == GAME_UPDATE and not in_menu and not is_paused and not game.game_over:
            game.move_down()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if in_menu:
                if play_rect.collidepoint(mouse_pos):
                    start_new_game()  # Démarrer une nouvelle partie
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif is_paused:
                if resume_rect.collidepoint(mouse_pos):
                    is_paused = False  # Reprendre le jeu
                elif menu_rect.collidepoint(mouse_pos):
                    in_menu = True  # Retourner au menu principal

    # Dessins
    if in_menu:
        screen.fill(Colors.dark_blue)
        screen.blit(menu_title_surface, (SCREEN_WIDTH // 2 - 40, 150, 100, 50))
        pygame.draw.rect(screen, Colors.light_blue, play_rect, 0, 10)
        screen.blit(play_surface, play_surface.get_rect(centerx=play_rect.centerx, centery=play_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, quit_rect, 0, 10)
        screen.blit(quit_surface, quit_surface.get_rect(centerx=quit_rect.centerx, centery=quit_rect.centery))
    elif is_paused:
        screen.fill(Colors.dark_blue)
        pygame.draw.rect(screen, Colors.light_blue, resume_rect, 0, 10)
        screen.blit(resume_surface, resume_surface.get_rect(centerx=resume_rect.centerx, centery=resume_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, menu_rect, 0, 10)
        screen.blit(menu_surface, menu_surface.get_rect(centerx=menu_rect.centerx, centery=menu_rect.centery))
    else:
        score_surface = title_font.render("Score", True, Colors.white)
        next_surface = title_font.render("Next", True, Colors.white)
        game_over_surface = title_font.render("GAME OVER", True, Colors.white)

        score_rect = pygame.Rect(320, 55, 170, 60)
        next_rect = pygame.Rect(320, 215, 170, 180)

        score_value_surface = title_font.render(str(game.score), True, Colors.white)

        screen.fill(Colors.black)
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (375, 180, 50, 50))

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                      centery=score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)

        if game.game_over:
            screen.blit(game_over_surface, (320, 450, 50, 50))

    pygame.display.update()
    clock.tick(60)
