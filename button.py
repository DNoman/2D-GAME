"""
Lớp đại diện cho hình ảnh MENU trong trò chơi.

Attributes:
    x (int): Tọa độ x của nút trên màn hình.
    y (int): Tọa độ y của nút trên màn hình.
    image (pygame.Surface): Hình ảnh của nút.
    rect (pygame.Rect): Hình chữ nhật bao quanh nút.

Methods:
    draw(surface): Vẽ nút lên màn hình và kiểm tra xem các nút Start,Resume,.. có được nhấn hay không.

"""
import pygame
class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft =(x,y)

    def draw(self,surface):
        action = False
        #di chuyen con chuot
        pos = pygame.mouse.get_pos()

        #click chuot
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                action = True

        surface.blit(self.image,self.rect)
        return action
