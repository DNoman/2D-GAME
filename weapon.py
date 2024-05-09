import random
import random
import pygame
import math
from constants import *

class Weapon():
    """
    Đại diện cho vũ khí của người chơi.

    Attributes:
    - original_image: Hình ảnh gốc của vũ khí.
    - angle (float): Góc quay của vũ khí.
    - image : Hình ảnh hiện tại của vũ khí sau khi được quay.
    - arrow_image : Hình ảnh của mũi tên.
    - rect (list): Hình chữ nhật bao quanh vũ khí.
    - fired (bool): Xác định xem vũ khí đã được bắn ra hay chưa.
    - last_shot (int): Thời điểm cuối cùng vũ khí được bắn ra.

    Methods:
    - update(player): Cập nhật trạng thái của vũ khí.
    - draw(surface): Vẽ vũ khí lên màn hình.
    """
    def __init__(self,image,arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
    def update(self,player):
        shot_cooldown = 300
        arrow = None
        self.rect.center = player.rect.center
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist,x_dist))

        #nhap chuot
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks()- self.last_shot) >= shot_cooldown:
            arrow = Arrow(self.arrow_image,self.rect.centerx,self.rect.centery,self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        return arrow

    def draw(self,surface):
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)) , self.rect.centery - int(self.image.get_height()/2)))

class Arrow(pygame.sprite.Sprite):
    """
    Đại diện cho mũi tên trong trò chơi.

    Attributes:
    - original_image: Hình ảnh gốc của mũi tên.
    - angle (float): Góc quay của mũi tên.
    - image : Hình ảnh hiện tại của mũi tên sau khi được quay.
    - rect : Hình chữ nhật bao quanh mũi tên.
    - dx (float): Vận tốc theo phương ngang của mũi tên.
    - dy (float): Vận tốc theo phương dọc của mũi tên.

    Methods:
    - update(screen_scroll, obstacle_titles, enemy_list): Cập nhật trạng thái của mũi tên.
    - draw(surface): Vẽ mũi tên lên màn hình.
    """
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image,self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #tinh toan goc
        self.dx = math.cos(math.radians(self.angle)) * ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * ARROW_SPEED)
    def update(self,screen_scroll,obstacle_titles,enemy_list):
        #tao bien
        damage = 0
        damage_pos = None

        #dinh lai vi tri dua vao toc do
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y +=screen_scroll[1] +  self.dy
        #kiem tra collision voi buc tuong
        for obstacle in obstacle_titles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        #kiem tra mui ten di ra khoi map hay chua
        if self.rect.right < 0 or self.rect.left >  SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        #kiem tra mui ten dinh ke dich hay khong ?
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5,5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break

        return damage,damage_pos
    def draw(self,surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))


class Fireball(pygame.sprite.Sprite):
    """
    Đại diện cho quả cầu lửa trong trò chơi.

    Attributes:
    - original_image: Hình ảnh gốc của quả cầu lửa.
    - angle (float): Góc quay của quả cầu lửa.
    - image : Hình ảnh hiện tại của quả cầu lửa sau khi được quay.
    - rect : Hình chữ nhật bao quanh quả cầu lửa.
    - dx (float): Vận tốc theo phương ngang của quả cầu lửa.
    - dy (float): Vận tốc theo phương dọc của quả cầu lửa.

    Methods:
    - update(screen_scroll, player): Cập nhật trạng thái của quả cầu lửa.
    - draw(surface): Vẽ quả cầu lửa lên màn hình.
    """
    def __init__(self,image,x,y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist,x_dist))
        self.image = pygame.transform.rotate(self.original_image,self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        #tinh toan van toc theo phuong thang dung hoac nam ngang dua vao goc
        self.dx = math.cos(math.radians(self.angle)) * FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * FIREBALL_SPEED)
    def update(self,screen_scroll,player):
        #reset bien
        damage = 0
        damage_pos = None

        #dinh lai vi tri dua vao toc do
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y +=screen_scroll[1] +  self.dy

        #kiem tra fireball di ra khoi map hay chua
        if self.rect.right < 0 or self.rect.left >  SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        #kiem tra o giua player va doi tuong co buc tuong khong
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -=10
            self.kill()


    def draw(self,surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))

