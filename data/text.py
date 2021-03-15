import pygame


class Text:
    hovered = False

    def __init__(self, text, font, pos, color=None, center=True):
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos

        # Default render text initialization
        self.screen = pygame.display.get_surface()
        self.rend = self.font.render(str(self.text), True, (255, 255, 255))
        self.rect = self.rend.get_rect()

        if center:
            self.rect.center = pos

    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(str(self.text), True, self.get_color())

    def get_color(self):
        if self.color is not None:
            return self.color

        if self.hovered:
            return 255, 255, 255
        else:
            return 100, 100, 100

    def recenter(self):
        self.rend = self.font.render(str(self.text), True, (255, 255, 255))
        self.rect = self.rend.get_rect()
        self.rect.center = self.pos
