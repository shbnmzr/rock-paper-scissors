import pygame


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 80

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('Roboto', 20)
        text = font.render(self.text, 1, pygame.Color('white'))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                 self.y + round(self.height / 2) - round(text.get_height())))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        return ((self.x <= x1 <= self.x + self.width) and (self.y <= y1 <= self.y + self.height))
