"""
Mystery 2D Game

Kịch bản này triển khai một trò chơi 2D bằng thư viện Pygame. Nó bao gồm di chuyển nhân vật, sử dụng vũ khí, thu thập vật phẩm, tương tác với kẻ thù, tiến triển qua các cấp độ và các phần giao diện người dùng đồ họa.

Modules:
    - pygame: Thư viện chính cho phát triển trò chơi.
    - csv: Module để đọc các tệp CSV.
    - constants: Module hằng số tùy chỉnh.
    - character: Module xác định các nhân vật trong trò chơi.
    - weapon: Module xác định vũ khí và mũi tên.
    - items: Module xác định các vật phẩm có thể thu thập.
    - world: Module xác định thế giới trò chơi.
    - button: Module xác định các nút tương tác.

Classes:
    - DamageText: Lớp sprite để hiển thị số sát thương.
    - Screenfade: Lớp để tạo hiệu ứng mờ màn hình.

Functions:
    - scale_img: Hàm để tỉ lệ hình ảnh.
    - draw_text: Hàm để vẽ văn bản trên màn hình.
    - reset_level: Hàm để thiết lập lại cấp độ trò chơi.
    - draw_info: Hàm để hiển thị thông tin trò chơi trên màn hình.

Use:
    - mixer: Module Pygame để xử lý âm thanh.
    - screen: Bề mặt hiển thị Pygame để vẽ đồ họa.
    - clock: Đối tượng Đồng hồ Pygame để điều khiển tốc độ khung hình.
    - level: Số nguyên đại diện cho cấp độ trò chơi hiện tại.
    - start_game: Boolean cho biết trò chơi đã bắt đầu chưa.
    - pause_game: Boolean cho biết trò chơi đã tạm dừng chưa.
    - start_intro: Boolean cho biết màn hình giới thiệu đã xuất hiện chưa.
    - screen_scroll: Danh sách chứa giá trị cuộn màn hình theo chiều ngang và dọc.
    - moving_left, moving_right, moving_up, moving_down: Boolean cho biết hướng di chuyển của người chơi.
    - font: Đối tượng font Pygame để vẽ văn bản.
    - shot_fx, hit_fx, coin_fx, heal_fx: Đối tượng âm thanh Pygame cho các hiệu ứng âm thanh khác nhau của trò chơi.
    - start_img, exit_img, restart_img, resume_img: Đối tượng Bề mặt Pygame cho hình ảnh nút tương tác.
    - heart_empty, heart_half, heart_full: Đối tượng Bề mặt Pygame cho biểu tượng trái tim đại diện cho máu của người chơi.
    - coin_images, red_potion: Danh sách đối tượng Bề mặt Pygame đại diện cho các vật phẩm có thể thu thập.
    - bow_image, arrow_image, fireball_image: Đối tượng Bề mặt Pygame đại diện cho hình ảnh vũ khí và mũi tên.
    - tile_list: Danh sách các đối tượng Bề mặt Pygame đại diện cho các loại ô trong thế giới trò chơi.
    - world_data: Danh sách đại diện cho bố cục của thế giới trò chơi.
    - player: Thể hiện của lớp nhân vật đại diện cho người chơi.
    - enemy_list: Danh sách thể hiện của lớp nhân vật đại diện cho kẻ thù.
    - mob_animations: Danh sách các danh sách chứa các khung hình hoạt ảnh nhân vật.
    - intro_fade, death_fade: Thể hiện của lớp Screenfade để tạo hiệu ứng mờ màn hình.
    - start_button, exit_button, restart_button, resume_button: Thể hiện của lớp Button để tạo các nút tương tác.

Sử dụng:
    - Chạy mã để bắt đầu trò chơi.
    - Sử dụng các phím mũi tên để di chuyển nhân vật.
    - Nhấn phím Escape để tạm dừng trò chơi.
    - Theo dõi các hướng dẫn trên màn hình cho tương tác tiếp theo.
"""
import pygame
import csv
from pygame import mixer
from constants import *
from character import character
from weapon import Weapon
from items import Item
from world import World
from button import Button

mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Mystery 2D GAME")

#tao ra clock giu cho frame ko di chuyen
clock = pygame.time.Clock()
#level cua game
level = 1
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0,0]
#tao ra di chuyen nhan vat
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#Font chu
font = pygame.font.Font("fonts/AtariClassic.ttf",20)

###ham scale image
def scale_img(image,scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image,(w * scale, h * scale))

#load nhac va sound effect
pygame.mixer.music.load("audio/music_effect.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,5000)
shot_fx = pygame.mixer.Sound("audio/arrow_shot_effect.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("audio/arrow_hit_effect.mp3")
hit_fx.set_volume(0.3)
coin_fx = pygame.mixer.Sound("audio/coin_effect.mp3")
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound("audio/heal_effect.mp3")
heal_fx.set_volume(5)

#load hinh anh button
start_img = scale_img(pygame.image.load("buttons/button_start.png"),BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("buttons/button_exit.png"),BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("buttons/button_restart.png"),BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("buttons/button_resume.png"),BUTTON_SCALE)

#anh trai tim ( lam thanh mau )
heart_empty = scale_img(pygame.image.load("items/heart_empty.png"),ITEM_SCALE)
heart_half = scale_img(pygame.image.load("items/heart_half.png"),ITEM_SCALE)
heart_full = scale_img(pygame.image.load("items/heart_full.png"),ITEM_SCALE)

#load hinh anh coin
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"items/coin_f{x}.png"),ITEM_SCALE)
    coin_images.append(img)

#load hinh anh potion
red_potion = scale_img(pygame.image.load("items/potion_red.png"),POTION_SCALE)
item_images = []
item_images.append(coin_images)
item_images.append(red_potion)


#load hinh anh vu khi
bow_image = scale_img(pygame.image.load("weapons/bow.png"),WEAPON_SCALE )
arrow_image = scale_img(pygame.image.load("weapons/arrow.png"),WEAPON_SCALE )
fireball_image = scale_img(pygame.image.load("weapons/fireball.png"),WEAPON_SCALE )

#load pixel map
tile_list = []
for x in range(TILE_TYPES):
    tile_image = pygame.image.load(f"tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE,TILE_SIZE))
    tile_list.append(tile_image)

#ham hien thi diem thuong
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img, (x,y))


# def draw_grid():
#     for x in range(30):
#         pygame.draw.line(screen, WHITE, (x * TILE_SIZE,0),(x*TILE_SIZE,SCREEN_HEIGHT))
#         pygame.draw.line(screen, WHITE, (0,x * TILE_SIZE), (SCREEN_WIDTH,x * TILE_SIZE))

#hien thi so mau mat di
class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    def update(self):
        # tao lai vi tri khi screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        #xoa text sau moi lan update
        self.rect.y -= 1
        #xoa counter sau vai giay
        self.counter +=1
        if self.counter > 30:
            self.kill()
#Class hoat anh chuyen canh moi level
class Screenfade():
    def __init__(self,direction,colour,speed):
        self.direction = direction
        self.colour =colour
        self.speed = speed
        self.fade_counter = 0
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen,self.colour,(0 - self.fade_counter,0,SCREEN_WIDTH // 2 , SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.colour,(SCREEN_WIDTH // 2 + self.fade_counter,0,SCREEN_WIDTH,SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.colour,(0,0 - self.fade_counter,SCREEN_WIDTH,SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen,self.colour,(0, SCREEN_HEIGHT//2 + self.fade_counter,SCREEN_WIDTH,SCREEN_HEIGHT))

        elif self.direction == 2:
            pygame.draw.rect(screen,self.colour,(0,0,SCREEN_WIDTH,0 + self.fade_counter))

        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

#create empty tile list
# world_data = [
#     [7,7,7,7,7,7],
#     [7,0,1,2,4,7],
#     [7,3,1,2,1,7],
#     [7,6,6,6,2,7],
#     [7,0,0,0,3,7],
#     [7,0,0,0,3,7],
#     [7,0,0,0,3,7]
# ]

world_data = []
for row in range(ROW):
    r = [-1] * COLS
    world_data.append(r)
#tao World
with open(f"levels/level{level}_data.csv",newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            world_data[x][y] = int(tile)

#tao vu khi cho nhan vat
bow = Weapon(bow_image,arrow_image)
#tao Sprite group
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(SCREEN_WIDTH - 765,25,0,coin_images,True)
item_group.add(score_coin)


# potion = Item(200,200,1,[red_potion])
# item_group.add(potion)
# coin = Item(400,400,0,coin_images)
# item_group.add(coin)

# print(item_group)

#tao font chu hien thi mau
# damage_text = DamageText(300,400,"15",RED)
# damage_text_group.add(damage_text)

#load hinh anh cac doi tuong trong game
mob_animations = []
mob_types = ["girl","goblin","monster","steal","human_dog","human_cat","Boss"]

animation_type =["idle","run"]
for mob in mob_types:
#load hinh anh
    animation_list =[]
    for animation in animation_type:
        #reset danh sach tam thoi chua hinh anh
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"characters/{mob}/{animation}/{i}.png").convert_alpha()
            if mob == "goblin" :
                img = scale_img(img,SCAlE_GOBLIN)
            elif mob == "monster":
                img = scale_img(img,SCALE_MONSTER)
            elif mob == "steal":
                img = scale_img(img,SCALE_STEAL)
            elif mob == "human_dog":
                img = scale_img(img,SCALE_STEAL)
            elif mob == "human_cat":
                img = scale_img(img,SCALE_STEAL)
            else :
                img = scale_img(img,SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#Ham reset level
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()
    data = []
    for row in range(ROW):
        r = [-1] * COLS
        data.append(r)

    return data

#ham hien thi thong tin game
def draw_info():
    pygame.draw.rect(screen,PANEL,(0,0,SCREEN_WIDTH,50))
    pygame.draw.line(screen,WHITE,(0,50),((SCREEN_WIDTH,50)))
    #mang song
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i+1)*20):
            screen.blit(heart_full, (550 + i * 50,0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (550 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (550 + i * 50, 0))

    #level
    draw_text("LEVEL: "+ str(level),font,WHITE,SCREEN_WIDTH/3,15)
    #diem thuong
    draw_text(f"X{player.score}",font,WHITE,SCREEN_WIDTH-750,15)

#tao the gioi
world = World()
world.process_data(world_data,tile_list,item_images,mob_animations)

#them coin tu level data
for item in world.item_list:
    item_group.add(item)

#Tao nhan vat
player = world.player

#tao ke thu
enemy_list = world.character_list

#Tao screen fade
intro_fade = Screenfade(1,BLACK,4)
death_fade = Screenfade(2,PINK,4)

#Tao Button
start_button = Button(SCREEN_WIDTH//2 - 145,SCREEN_HEIGHT// 2 - 100,start_img)
exit_button = Button(SCREEN_WIDTH//2 - 110,SCREEN_HEIGHT// 2 + 50,exit_img)
restart_button = Button(SCREEN_WIDTH//2 - 175,SCREEN_HEIGHT// 2 - 50,restart_img)
resume_button = Button(SCREEN_WIDTH//2 - 175,SCREEN_HEIGHT// 2 - 100,resume_img)

# main game loop
run = True
while run:

    # dieu khien frame rate
    clock.tick(FPS)
    if start_game == False:
        screen.fill(MENU_BG)
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game == True:
            screen.fill(MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
            screen.fill(BG)
            # draw_grid()
            if player.alive:
                #tinh toan buoc di chuyen nhan vat
                dx = 0
                dy = 0
                if moving_right == True:
                    dx = SPEED
                if moving_left == True:
                    dx = -SPEED
                if moving_up == True:
                    dy = -SPEED
                if moving_down == True:
                    dy = SPEED

                #Di chuyen nhan vat
                screen_scroll,level_complete = player.move(dx,dy,world.obstacle_tiles,world.exit_tile)


                #Cap nhat tat ca doi tuong
                world.update(screen_scroll)
                for enemy in enemy_list:
                    fireball = enemy.ai(player , world.obstacle_tiles,screen_scroll,fireball_image)
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive :
                        enemy.update()
                player.update()
                arrow = bow.update(player)
                bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shot_fx.play()
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(screen_scroll,world.obstacle_tiles,enemy_list)
                    if damage:
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
                        damage_text_group.add(damage_text)
                        hit_fx.play()
                damage_text_group.update()
                fireball_group.update(screen_scroll,player)
                item_group.update(screen_scroll,player ,coin_fx,heal_fx)

            # print(enemy.health)

            #Tao nhan vat tren man hinh
            world.draw(screen)
            for enemy in enemy_list:
                enemy.draw(screen)
            player.draw(screen)
            bow.draw(screen)
            for arrow in arrow_group:
                arrow.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            damage_text_group.draw(screen)
            item_group.draw(screen)
            draw_info()
            score_coin.draw(screen)

            #kiem tra level complete
            if level_complete == True:
                start_intro = True
                level += 1
                world_data = reset_level()
                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                temp_hp = player.health
                temp_score = player.score
                player = world.player
                player.health = temp_hp
                player.score = temp_score
                enemy_list = world.character_list
                score_coin = Item(SCREEN_WIDTH - 765,25,0,coin_images,True)
                item_group.add(score_coin)
                for item in world.item_list:
                    item_group.add(item)

            #intro
            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            #death screen
            if player.alive == False:
                if death_fade.fade():
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        world_data = reset_level()
                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animations)
                        player = world.player
                        enemy_list = world.character_list
                        score_coin = Item(SCREEN_WIDTH - 765, 25, 0, coin_images, True)
                        item_group.add(score_coin)
                        for item in world.item_list:
                            item_group.add(item)

    #duy tri window game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # an nut di chuyen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True

    # tha nut di chuyen
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False


    pygame.display.update()
pygame.quit()
