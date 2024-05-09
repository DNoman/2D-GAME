"""
    Đại diện cho một nhân vật trong trò chơi.

    Attributes:
    - x (int): Tọa độ x của nhân vật trên màn hình.
    - y (int): Tọa độ y của nhân vật trên màn hình.
    - health (int): Mức điểm máu của nhân vật.
    - mob_animations (dict): Danh sách các animation của nhân vật.
    - char_type (int): Loại nhân vật.
    - boss (bool): Xác định xem nhân vật có phải là boss hay không.
    - size (int): Kích thước của nhân vật.
    - score (int): Điểm số của nhân vật.
    - animation_list (list): Danh sách các frame trong animation của nhân vật.
    - flip (bool): Xác định xem nhân vật có đang bị lật ngược hay không.
    - frame_index (int): Chỉ số của frame hiện tại đang được sử dụng trong animation.
    - action (int): Hành động hiện tại của nhân vật (0: hoạt ảnh đứng yên, 1: hoạt ảnh chạy).
    - running (bool): Xác định xem nhân vật có đang chạy hay không.
    - alive (bool): Xác định xem đối tượng còn sống hay không.
    - hit (bool): Xác định xem nhân vật đã bị tấn công hay không và đối tượng bị tấn công hay không.
    - last_hit (int): Thời điểm nhân vật bị tấn công gần nhất.
    - last_attack (int): Thời điểm cuối cùng boss tấn công.
    - stunned (bool): Xác định xem đối tượng có bị choáng hay không.
    - update_time (int): Thời điểm cập nhật gần nhất của animation.
    - image (list): Hình ảnh hiện tại của nhân vật.
    - rect : Tọa độ hình chữ nhật bao quanh nhân vật trên màn hình.

    Methods:
    - move(dx, dy, obstacle_tile,exit_tile): Di chuyển nhân vật trên màn hình, di chuyển đến địa điểm chỉ định được qua màn chi khác
    - ai(player, obstacle_tiles, screen_scroll, fireball_image): Xử lý trí tuệ nhân tạo cho nhân vật.
    - update(): Cập nhật trạng thái của nhân vật.
    - update_action(new_action): Cập nhật hành động của nhân vật.
    - draw(surface): Vẽ nhân vật lên màn hình.
"""

import math

import pygame
import math
import weapon

import constants
from constants import *
class character():
    def __init__(self,x,y,health,mob_animations,char_type,boss,size):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.animation_list = mob_animations[char_type]
        self.flip = False
        self.frame_index = 0
        self.action = 0 # 0: hoat anh dung yen,1: hoat anh chay
        self.running = False
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False

        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,TILE_SIZE  *size,TILE_SIZE * size)
        self.rect.center = (x,y)

    def move(self,dx,dy,obstacle_tile,exit_tile = None):
        screen_scroll = [0,0]
        level_complete = False
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        #dieu khien duong cheo
        if dx != 0 and dy !=0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        for obstacle in obstacle_tile:
            #kiem tra va cham trai va phai
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tile:
            #kiem tra va cham tren va duoi
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        if self.char_type == 0:
            # kiem tra nhan vat tuong tac voi exit gate hay chua
            if exit_tile[1].colliderect(self.rect):
                #dam bao rang player den gan voi loi exit
                exit_dist = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2))
                if exit_dist < 30:
                    level_complete = True
            #cap nhat scoll (di chuyen camera)
            # trai va phai
            if self.rect.right > (SCREEN_WIDTH - SCROLL_THRESH):
                screen_scroll[0] = (SCREEN_WIDTH - SCROLL_THRESH) - self.rect.right
                self.rect.right = SCREEN_WIDTH - SCROLL_THRESH
            if self.rect.left < SCROLL_THRESH:
                screen_scroll[0] = SCROLL_THRESH - self.rect.left
                self.rect.left = SCROLL_THRESH

            #len va xuong
            if self.rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESH):
                screen_scroll[1] = (SCREEN_HEIGHT - SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = SCREEN_HEIGHT - SCROLL_THRESH
            if self.rect.top < SCROLL_THRESH:
                screen_scroll[1] = SCROLL_THRESH - self.rect.top
                self.rect.top = SCROLL_THRESH

            return screen_scroll,level_complete

    def ai(self,player,obstacle_tiles,screen_scroll,fireball_image):
        clipped_line = []
        stun_cooldown = 100
        ai_dx = 0
        ai_dy = 0
        fireball = None

        #dinh vi lai mob dua tren scroll man hinh
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #tao ra duong quan sat cua doi tuong
        line_of_sight = ((self.rect.centerx,self.rect.centery), (player.rect.centerx, player.rect.centery))
        #kiem tra xem duong quan sat qua duoc buc tuong hay khong
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        #toa do cua doi tuong so voi player, khien cac doi tuong huong ve player
        #kiem tra khoang cach giua doi tuong va player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2) + ((self.rect.centery - player.rect.centery)**2))
        if not clipped_line and dist > RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = ENEMY_SPEED

        if self.alive:
            if not self.stunned:

                #Tien toi player
                self.move(ai_dx, ai_dy,obstacle_tiles)

                #tan cong player
                if dist < ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit =pygame.time.get_ticks()

                #boss enemies fireball
                fireball_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                            fireball = weapon.Fireball(fireball_image,self.rect.centerx,self.rect.centery,player.rect.centerx,player.rect.centery)
                            self.last_attack = pygame.time.get_ticks()

            #kiem tra xem hit True hay False
            if self.hit ==True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.update_action(0)

            if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False
        return fireball
    def update(self):
        #kiem tra xem doi tuong da chet hay khong
        if self.health <= 0:
            self.health = 0
            self.alive = False
        #reset thoi gian attack player
        hit_cooldown =500
        if self.char_type == 0:
            if self.hit == True and pygame.time.get_ticks() - self.last_hit > hit_cooldown:
                self.hit = False
        #kiem tra nhan vat dang o trang thai action nao
        if self.running == True:
            self.update_action(1) #1 : hoat anh chay
        else:
            self.update_action(0) #0 : hoat anh dung yen
        animation_cooldown = 70
        # tao ra animation
        #update hinh anh
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self,new_action):
        #kiem tra action moi co khac so voi action cu
        if new_action != self.action:
            self.action = new_action
        # #cap nhat animation
        # self.frame_index = 0
        # self.update_time = pygame.time.get_ticks()

    def draw(self,surface):
        flipped_image = pygame.transform.flip(self.image,self.flip,False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x + SCALE*2,self.rect.y - SCALE * OFFSET))
        elif self.char_type == 1:
            surface.blit(flipped_image,(self.rect.x - SCALE * 8,self.rect.y - SCALE * 20))
        elif self.char_type == 2:
            surface.blit(flipped_image, (self.rect.x- SCALE * 6,self.rect.y - SCALE * 7))
        elif self.char_type == 3:
            surface.blit(flipped_image, (self.rect.x- SCALE * 4,self.rect.y - SCALE * 7))
        elif self.char_type == 4:
            surface.blit(flipped_image, (self.rect.x- SCALE *3,self.rect.y - SCALE * 5))
        elif self.char_type == 5:
            surface.blit(flipped_image, (self.rect.x- SCALE *3,self.rect.y - SCALE * 5))
        elif self.char_type == 6:
            surface.blit(flipped_image, (self.rect.x- SCALE * 4,self.rect.y - SCALE * 4))
        else :
            surface.blit(flipped_image, (self.rect.x, self.rect.y))
