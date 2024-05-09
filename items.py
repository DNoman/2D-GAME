"""
Đại diện cho các vật phẩm trong trò chơi.

Attributes:
- item_type (int): Loại của vật phẩm (0: đồng xu, 1: hồi máu).
- animation_list (list): Danh sách các hình ảnh tạo nên hoạt ảnh của vật phẩm.
- frame_index (int): Chỉ số của hình ảnh hiện tại trong danh sách hoạt ảnh.
- update_time (int): Thời điểm cập nhật cuối cùng của hoạt ảnh.
- image : Hoạt ảnh của hình ảnh hiện tại của vật phẩm tại frame_index nhất định
- rect : Hình chữ nhật bao quanh vật phẩm.
- dummy_coin (bool): Xác định xem vật phẩm có phải là đồng xu giả mạo hay không.

Methods:
- update(screen_scroll, player): Cập nhật trạng thái của vật phẩm.
- draw(surface): Vẽ vật phẩm lên màn hình.
"""
import pygame
class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,item_type,animation_list,dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dummy_coin = dummy_coin
    def update(self,screen_scroll,player,coin_fx,heal_fx):
        #dummy coin
        if not self.dummy_coin:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        #kiem tra xem nhan vat lay item hay chua
        if self.rect.colliderect(player.rect):
            #thu thap coin
            if self.item_type == 0:
                player.score += 1
                coin_fx.play()
            elif self.item_type == 1:
                player.health += 10
                heal_fx.play()
                if player.health > 100:
                    player.health = 100
            self.kill()

        #hoat anh cho item
        animation_cooldown = 150
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self,surface):
        surface.blit(self.image,self.rect)