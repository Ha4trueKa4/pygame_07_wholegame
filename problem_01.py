import os
import sys
import pygame

pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
pygame.display.set_caption('mario game')
clock = pygame.time.Clock()
FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def main_screen():
    lvl = load_level('lvl.txt')
    print(lvl)
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mario.png')

    tile_width = tile_height = 50

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.image = player_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 15, tile_height * pos_y + 5)

        def update(self, *args):
            if args and args[0].key == pygame.K_RIGHT:
                if self.pos_x + 1 <= level_x:
                    if lvl[self.pos_y][self.pos_x + 1] != '#':
                        self.pos_x += 1

            elif args and args[0].key == pygame.K_LEFT:
                if self.pos_x - 1 >= 0:
                    if lvl[self.pos_y][self.pos_x - 1] != '#':
                        self.pos_x -= 1

            if args and args[0].key == pygame.K_UP:
                if self.pos_y - 1 >= 0:
                    if lvl[self.pos_y - 1][self.pos_x] != '#':
                        self.pos_y -= 1

            if args and args[0].key == pygame.K_DOWN:
                if self.pos_y + 1 <= level_y:
                    if lvl[self.pos_y + 1][self.pos_x] != '#':
                        self.pos_y += 1
            print(self.pos_x, self.pos_y)
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    player = None

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        return new_player, x, y

    player, level_x, level_y = generate_level(load_level('lvl.txt'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                player.update(event)

        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
screen.fill((0, 0, 0))
pygame.display.flip()
main_screen()
