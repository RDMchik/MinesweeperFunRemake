from typing import Optional

import pygame


class Sprite(object):
    """sprite loader class, all it does is making
    it possible to use a sprite without any pressure
    on the cpu, while also accessing some of the
    essential properties of the sprite for the code to use"""

    def __init__(self, image: pygame.Surface, coordinates: pygame.Vector2, size: tuple, sub_sprites: Optional[list] = None) -> None:
        """not creating any new images in here, just using
        an already existing one, which is loaded already"""
        self.image = image
        self.coordinates = coordinates
        self.size = size

        # a sprite is able to have some sub sprites connected to it
        self.sub_sprites = sub_sprites
        # sub sprites, but are always visible
        self.forced_sub_sprites = []

        self.hit_box = pygame.Rect(
            coordinates.x, coordinates.y,
            size[0], size[1]
        )

        self.visible = True
        self.sub_sprites_visible = False
        self.can_collide = True

    def add_sub_sprite(self, sprite: str, sprites: Optional[list] = None, forced: Optional[bool] = False) -> None:
        # checking if nothing was passed as an arguments
        if not sprite and not sprites:
            raise Exception('Both values are null or incorrect')
        if not self.sub_sprites:
            self.sub_sprites = []
        # when creating a sub sprite, only passing 
        # directory and creating a new sprite. I
        # know there for sure is a better way to
        # get it done, but right now i am sick
        # and dont really want to optimize this part
        sprite = Sprite(
            sprite,
            pygame.Vector2(self.coordinates.x, self.coordinates.y),
            self.size
        )
        if not sprites:
            if forced:
                self.forced_sub_sprites.append(sprite)
            else:
                self.sub_sprites.append(sprite)
        else:
            for sprite in sprites:
                if forced:
                    self.forced_sub_sprites.append(sprite)
                else:
                    self.sub_sprites.append(sprite)


class GUI(object):
    """a class which is responsible for displaying
    all of the visual information for the player"""

    def __init__(self, display: pygame.Surface, conf: dict) -> None:
        self.display = display
        self.conf = conf

        #storing sprites
        self.sprites = []

        # the one and only font which is going to be used
        self.font = pygame.font.Font('static/font.ttf', int(conf['block_size'] * 0.2))

        # coordinates of border lines
        self.border_lines = (
            ((0, self.display.get_height() - self.conf['footer_height']),
            (self.display.get_width(), self.display.get_height() - self.conf['footer_height'])),

            ((self.display.get_width(), self.display.get_height() - self.conf['footer_height']),
            (self.display.get_width(), self.display.get_height())),

            ((self.display.get_width(), self.display.get_height()),
            (0, self.display.get_height())),

            ((0, self.display.get_height()),
            (0, self.display.get_height() - self.conf['footer_height']))
        )

    def add_sprite(self, sprite: Optional[Sprite] = None, sprites: Optional[list] = None) -> None:
        # checking if nothing was passed as an arguments
        if not sprite and not sprites:
            raise Exception('Both values are null or incorrect')
        if not sprites:
            self.sprites.append(sprite)
        else:
            for sprite in sprites:
                self.sprites.append(sprite)

    def update_footer(self, score: str, time_played: str, extra: Optional[str] = None) -> None:
        """a function that only updates the footer"""
        pygame.draw.rect(
            self.display,
            (60, 60, 60),
            (0, self.display.get_height() - self.conf['block_size'], 
            self.display.get_width(), self.conf['block_size'])
        )
        for line in self.border_lines:
            pygame.draw.line(self.display, (200, 200, 200), line[0], line[1], self.conf['border_width'])
        rendered_score = self.font.render(' score: {}; play time: {} {}'.format(score, time_played, '' if not extra else extra), False, (200, 200, 200))
        self.display.blit(rendered_score, (0, self.display.get_height() - int(self.conf['block_size']) + int(self.conf['block_size'] * 0.6 / 2))),
        pygame.display.flip()

    def draw_all_visuals(self, score: str, time_played: str) -> None:
        """drawing the border and all of gui's 
        sprites, of course if they are visible"""
        self.display.fill((60, 60, 60))
        for line in self.border_lines:
            pygame.draw.line(self.display, (200, 200, 200), line[0], line[1], self.conf['border_width'])
        # display score
        rendered_score = self.font.render(' score: {}; play time: {}'.format(score, time_played), False, (200, 200, 200))
        self.display.blit(rendered_score, (0, self.display.get_height() - int(self.conf['block_size']) + int(self.conf['block_size'] * 0.7 / 2))),
        for sprite in self.sprites:
            if not sprite.visible:
                continue
            self.display.blit(sprite.image, (
                sprite.coordinates.x,
                sprite.coordinates.y
            ))
            if sprite.sub_sprites_visible:
                if sprite.sub_sprites:
                    for sub_sprite in sprite.sub_sprites:
                        self.display.blit(sub_sprite.image, (
                            sub_sprite.coordinates.x,
                            sub_sprite.coordinates.y
                        ))
            for forced_sub_sprite in sprite.forced_sub_sprites:
                self.display.blit(forced_sub_sprite.image, (
                    forced_sub_sprite.coordinates.x,
                    forced_sub_sprite.coordinates.y
                ))
        pygame.display.flip()

    def mouse_over_sprite(self, sprite: Sprite, mouse_coordinates: tuple) -> bool:
        """checking if mouse is hovering over the sprite"""
        if not sprite.can_collide:
            return False
        return True if sprite.hit_box.collidepoint(
            mouse_coordinates[0],
            mouse_coordinates[1]
        ) else False
