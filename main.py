from scr.configuration import Config
from scr.manager import Manager
from scr.gui import GUI, Sprite

import pygame
import random
import time


pygame.init()
pygame.mixer.init()

conf = Config('config.json')

clock = pygame.time.Clock()
FPS = conf()['fps']

score = 0

start_time = time.time()
time_played = 0

running = True

# setting display size / initialization of display 
display = pygame.display.set_mode((
    conf()['field_size_x'] * conf()['block_size'],
    conf()['field_size_y'] * conf()['block_size'] + conf()['footer_height'],
))

pygame.display.set_caption('Minesweeper')

# initialization of all the sprites
sprites = {
    'block': pygame.transform.scale(pygame.image.load('static/block.jpg').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'flag': pygame.transform.scale(pygame.image.load('static/flag.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'bomb': pygame.transform.scale(pygame.image.load('static/bomb.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'one': pygame.transform.scale(pygame.image.load('static/block_one.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'two': pygame.transform.scale(pygame.image.load('static/block_two.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'three': pygame.transform.scale(pygame.image.load('static/block_three.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'four': pygame.transform.scale(pygame.image.load('static/block_four.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'five': pygame.transform.scale(pygame.image.load('static/block_five.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'six': pygame.transform.scale(pygame.image.load('static/block_six.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'seven': pygame.transform.scale(pygame.image.load('static/block_seven.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
    'eight': pygame.transform.scale(pygame.image.load('static/block_eight.png').convert_alpha(),
    (conf()['block_size'], conf()['block_size'])),
}

# initialization of all the sounds
sounds = {
    'win': pygame.mixer.Sound('static/win.wav'),
    'num': pygame.mixer.Sound('static/num.wav'),
    'flag': pygame.mixer.Sound('static/flag.wav'),
    'boom': pygame.mixer.Sound('static/boom.wav'),
    'start': pygame.mixer.Sound('static/start.wav'),
}

pygame.display.set_icon(sprites['block'])

gui = GUI(display, conf())
manager = Manager(conf())

def complete_visual_field() -> None:
    for x_key, x_value in manager.get_field().items():
        for y_key, y_value in x_value.items():
            sprite = Sprite(
                sprites['block'],
                pygame.Vector2(y_value['x'], y_value['y']),
                (conf()['block_size'], conf()['block_size'])
            )
            # checking for the sprite info
            # and adding an appropriate sub sprites
            if y_value['is_bomb']:
                sprite.add_sub_sprite(sprites['bomb'])
            # the maximum amount of bombs
            # around a single block is eight
            elif y_value['num'] == 1:
                sprite.add_sub_sprite(sprites['one'])
            elif y_value['num'] == 2:
                sprite.add_sub_sprite(sprites['two'])
            elif y_value['num'] == 3:
                sprite.add_sub_sprite(sprites['three'])
            elif y_value['num'] == 4:
                sprite.add_sub_sprite(sprites['four'])
            elif y_value['num'] == 5:
                sprite.add_sub_sprite(sprites['five'])
            elif y_value['num'] == 6:
                sprite.add_sub_sprite(sprites['six'])
            elif y_value['num'] == 7:
                sprite.add_sub_sprite(sprites['seven'])
            elif y_value['num'] == 8:
                sprite.add_sub_sprite(sprites['eight'])
            gui.add_sprite(sprite)

complete_visual_field()

def update_time_played() -> None:
    """update time you have played
    the game"""
    global time_played
    time_played = int(time.time() - start_time)

def check_zero_block(coordinates: tuple) -> None:
    """a function which is used to check
    all of the blocks around a block with
    num equal to zero"""
    global score
    is_zero = True
    block = manager.get_field()[str(int(coordinates[0]))][str(int(coordinates[1]))]
    if block['is_bomb']:
        return
    if not block['num'] == 0:
        is_zero = False
    # this one takes quite a lot
    # of time to perform on big fields
    for sprite in gui.sprites:
        if sprite.coordinates.x == block['x'] and sprite.coordinates.y == block['y']:
            if sprite.sub_sprites_visible or not sprite.visible:
                return
            sprite.can_collide = False
            if is_zero:
                sprite.visible = False
                score += 1
            else:
                sprite.sub_sprites_visible = True
                score += block['num']
                return
            break
    # now this part is tricky. the
    # code is going to try and perform
    # the check_zero_block on all eight
    # surrounding blocks' coordinates
    try:
        new_block = manager.get_field()[str(int(coordinates[0] - conf()['block_size']))][str(int(coordinates[1]))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0] + conf()['block_size']))][str(int(coordinates[1]))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0] - conf()['block_size']))][str(int(coordinates[1] - conf()['block_size']))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0]))][str(int(coordinates[1] - conf()['block_size']))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0] + conf()['block_size']))][str(int(coordinates[1] - conf()['block_size']))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0] - conf()['block_size']))][str(int(coordinates[1] + conf()['block_size']))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0]))][str(int(coordinates[1] + conf()['block_size']))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass
    try:
        new_block = manager.get_field()[str(int(coordinates[0] + conf()['block_size']))][str(int(coordinates[1] + conf()['block_size']))]
        check_zero_block((new_block['x'], new_block['y']))
    except KeyError:
        pass

def restart() -> None:
    """restart the whole game"""
    global score, start_time, time_played, running, gui, manager
    score = 0

    start_time = time.time()
    time_played = 0

    running = True

    gui = GUI(display, conf())
    manager = Manager(conf())

    complete_visual_field()

    gui.draw_all_visuals(str(score), str(time_played))
    sounds['start'].play()  

gui.draw_all_visuals(str(score), str(time_played))
sounds['start'].play()

while True:

    mouse_pos = None
    clicks = [False, False]

    if running:
        update_time_played()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
    	        clicks[0] = True
            elif event.button == 3:
                clicks[1] = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
    
    if mouse_pos:
        for sprite in gui.sprites:
            hovered = gui.mouse_over_sprite(sprite, mouse_pos)
            if hovered:
                block = manager.get_field()[str(int(sprite.coordinates[0]))][str(int(sprite.coordinates[1]))]
                if clicks[0]:
                    sounds['num'].play()
                    check_zero_block((block['x'], block['y']))
                    sprite.sub_sprites_visible = True
                    sprite.can_collide = False
                    score += block['num']
                    # sprite is right clicked
                    if block['is_bomb']:
                        # lose if the block is bomb
                        running = False
                        try:
                            sounds['num'].stop()
                        except Exception:
                            pass
                        sounds['boom'].play()
                        for sprite in gui.sprites:
                            if not sprite.sub_sprites:
                                sprite.visible = False
                                sprite.can_collide = False
                            else:
                                sprite.sub_sprites_visible = True
                                sprite.can_collide = False
                        gui.draw_all_visuals(str(score), str(time_played))
                        gui.update_footer(str(score), str(time_played), 'lost :(')

                elif clicks[1]:
                    if not sprite.sub_sprites_visible:
                        if not block['marked']:
                            manager.set_key((block['x'], block['y']), 'marked', True)
                            sprite.add_sub_sprite(sprites['flag'], forced=True)
                            if manager.game_finished():
                                # all of the mines are covered with flags
                                # so the player has won
                                running = False
                                try:
                                    sounds['flag'].stop()
                                except Exception:
                                    pass
                                sounds['win'].play()
                                for sprite in gui.sprites:
                                    if not sprite.sub_sprites:
                                        sprite.visible = False
                                        sprite.can_collide = False
                                    else:
                                        sprite.sub_sprites_visible = True
                                        sprite.can_collide = False
                                gui.draw_all_visuals(str(score), str(time_played))
                                gui.update_footer(str(score), str(time_played), 'won :)')
                        else:
                            manager.set_key((block['x'], block['y']), 'marked', False)
                            sprite.forced_sub_sprites.pop(-1)
                        sounds['flag'].play()
        if running:
            gui.draw_all_visuals(str(score), str(time_played))
    if running:
        gui.update_footer(str(score), str(time_played))

    clock.tick(FPS)
