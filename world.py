"""
Đại diện cho thế giới trong trò chơi và các phương thức quản lý.

Attributes:
- map_titles (list): Danh sách các ô trên bản đồ.
- obstacle_tiles (list): Danh sách các ô chướng ngại vật trên bản đồ.
- exit_tile (list): Thông tin về ô đích ra khỏi bản đồ.
- item_list (list): Danh sách các vật phẩm trên bản đồ.
- player (character): Thông tin về nhân vật người chơi.
- character_list (list): Danh sách các nhân vật khác trên bản đồ.

Methods:
- process_data(data, tile_list, item_images, mob_animations): Xử lý dữ liệu bản đồ và tạo các đối tượng.
- update(screen_scroll): Cập nhật vị trí của các ô trên bản đồ dựa trên việc di chuyển màn hình.
- draw(surface): Vẽ các ô trên bản đồ lên màn hình trò chơi.

"""
from character import character
from items import Item
from constants import *
class World():
    def __init__(self):
        self.map_titles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list =[]

    def process_data(self,data,tile_list,item_images,mob_animations):
        self.level_length = len(data)
        #lap lai tung data trong file data
        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x,image_y)
                tile_data = [image,image_rect,image_x,image_y]
                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 8:
                    self.exit_tile = tile_data
                elif tile ==9 :
                    coin = Item(image_x,image_y,0,item_images[0])
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[0]
                elif tile ==10:
                    potion = Item(image_x,image_y,1,[item_images[1]])
                    self.item_list.append(potion)
                    tile_data[0] = tile_list[0]
                elif tile ==11 :
                    player = character(image_x,image_y,100,mob_animations,0,False,1.25)
                    self.player = player
                    tile_data[0] = tile_list[0]
                elif tile >= 12 and tile <= 16:
                    enemy = character(image_x,image_y,100,mob_animations,tile -11,False,1)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 17:
                    enemy = character(image_x,image_y,100,mob_animations,6,True,2.5)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                # dua du lieu tu image data vao tile list
                if tile >=0:
                    self.map_titles.append(tile_data)


    def update(self,screen_scroll):
        for tile in self.map_titles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2],tile[3])
    def draw(self,surface):
        for tile in self.map_titles:
            surface.blit(tile[0],tile[1]) #0 load nhan vat, #1 load pixel map