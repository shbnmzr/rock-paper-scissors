import pygame
from Network import Network
from Button import Button
pygame.font.init()

width = 1000
height = 1000

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')


def redraw_window(win, game, p):
    win.fill((128, 128, 128))
    if not game.are_players_connected():
        font = pygame.font.SysFont('Roboto', 80)
        text = font.render('Waiting for player...', 1, (255, 0, 0), True)
        win.blit(text, ((width/2 - text.get_width())/2, (height/2 - text.get_height())/2))
    else:
        font = pygame.font.SysFont('Roboto', 60)
        text = font.render('Your move', 1, (0, 255, 255))
        win.blit(text, (80, 200))
        text = font.render('Opponent\'s ', 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_moves(0)
        move2 = game.get_player_moves(1)

        if game.did_both_go():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))

        else:
            if game.player1_went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.player1_went:
                text1 = font.render('Locked In', 1, (0, 0, 0))

            else:
                text1 = font.render('Waiting...', 1, (0, 0, 0))

            if game.player2_went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.player2_went:
                text2 = font.render('Locked In', 1, (0, 0, 0))

            else:
                text2 = font.render('Waiting...', 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for button in buttons:
            button.draw(win)

    pygame.display.update()


buttons = [Button('Rock', 50, 500, (0, 0, 0)),
           Button('Paper', 250, 500, (255, 0, 0)),
           Button('Scissors', 450, 500, (0, 255, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.get_p())
    print('You are player ', player)
    while run:
        clock.tick(60)
        try:
            game = network.send('get')
        except:
            run = False
            print('Could not get a game\n')
            break

        if game.did_both_go():
            redraw_window(win, game, player)
            pygame.time.delay(1000)
            try:
                game = network.send('reset')
            except:
                run = False
                print('Could not get a game\n')
                break

            font = pygame.font.SysFont('Roboto', 90)
            if (game.determine_winner() == 1 and player == 1) or (game.determine_winner() == 0 and player == 0):
                text = font.render('YOU WON!!', 1, (255, 255, 0))
            elif game.determine_winner() == -1:
                text = font.render('IT\'S A TIE!', 1, (255, 0, 255))
            else:
                text = font.render('YOU LOST!!', 1, (255, 0, 0))

            win.blit(text, ((width / 2 - text.get_width() / 2), (height - text.get_height() / 2)))

            pygame.display.update()
            pygame.time.delay(5000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos) and game.are_players_connected():
                        if player == 0:
                            if not game.player1_went:
                                network.send(button.text)
                        else:
                            if not game.player2_went:
                                network.send(button.text)

        redraw_window(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("Roboto", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
