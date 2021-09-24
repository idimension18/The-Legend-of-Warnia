from typing import Optional

import arcade
from enum import Enum
import main


class Direction(Enum):
    """
    Enum for define a direction
    """
    front = 0
    left = 1
    back = 3
    right = 2


class Player(arcade.Sprite):
    """
    the player
    """

    def __init__(self):
        # Set up parent class
        super().__init__()

        # ----------info de base---------------
        self.tag = "Stan"
        self.size = 32
        self.scale = 1.4 * main.SCALE
        self.speed = 3 * main.SCALE
        self.nbFrame = 4
        self.ID = "player"

        # -------------physics info-----------
        # set hit box
        self.hit_box = ((-self.size / 2.0, -self.size / 2.0),
                        (self.size / 2.0, -self.size / 2.0),
                        (self.size / 2.0, 0),
                        (-self.size / 2.0, 0))
        self.isUnderLayers = False
        self.isUnderObjects = False
        self.isStuck = False
        self.floor = 0
        self.isChangingFloor = False
        # -------command info------
        self.keyPile = []
        self.isMoving = False

        # -----------------graphics and animation--------------------------
        # ////texture////
        self.nothingTimer = 0
        self.nothingTime = 60
        self.currentDirection = Direction.front.value
        self.previousDirection = Direction.front.value
        self.textures = []
        self.animCursor = 0
        self.sheet = "data/images/Sprite Sheet/PIPOYA FREE RPG Character Sprites 32x32/Male/Male 02-1.png"

        # /////animation/////
        self.textures = [[] for i in range(8)]
        for i in range(4):
            self.textures[i].append(arcade.load_texture(self.sheet, self.size, i * self.size, self.size, self.size))

        for i in range(4):
            for k in range(3):
                self.textures[i + 4].append(
                    arcade.load_texture(self.sheet, k * self.size, i * self.size, self.size, self.size))

        for i in range(4):
            self.textures[i + 4].append(arcade.load_texture(self.sheet, self.size, i * self.size, self.size, self.size))

        # default
        self.texture = self.textures[self.currentDirection][0]

    def update(self, delta_time: float = 1 / 60):
        """
        update the player state
        """
        # to know what to do
        self.check_action()
        # check change
        if self.isMoving:
            self.moving()

    def update_animation(self, delta_time: float = 1 / 60):
        """
        update easely the sprite animation
        """
        if self.isMoving:
            self.texture = self.textures[4 + self.currentDirection][int(self.animCursor)]
        else:
            self.texture = self.textures[self.currentDirection][0]

    def keyPileADDKey(self, key):
        """
        add a key to the key pile
        :param key:
        """
        if key not in self.keyPile:
            self.keyPile.append(key)

    def keyPileRemoveKey(self, key):
        """
        remove a key from the key pile
        :param key:
        """
        if key in self.keyPile:
            self.keyPile.remove(key)

    def check_action(self):
        """
        check what the player is going to do
        """
        if self.keyPile:
            self.isMoving = True
            # do something
            self.currentDirection = self.keyPile[0]
        else:
            self.isMoving = False

    # code qui bouge
    def moving(self):
        """
        move the player and master animation
        """
        # ---------------animation------------
        self.nothingTimer = 0

        self.animCursor += (self.speed * 0.05)
        if self.animCursor > self.nbFrame:
            self.animCursor = 0

        # ------------------move---------------
        if self.currentDirection == Direction.front.value or self.keyPile[-1] == Direction.front.value:
            self.center_y -= self.speed

        if self.currentDirection == Direction.left.value or self.keyPile[-1] == Direction.left.value:
            self.center_x -= self.speed

        if self.currentDirection == Direction.back.value or self.keyPile[-1] == Direction.back.value:
            self.center_y += self.speed

        if self.currentDirection == Direction.right.value or self.keyPile[-1] == Direction.right.value:
            self.center_x += self.speed

    def talkingWay(self, sprite: arcade.Sprite) -> Optional[int]:
        if self.currentDirection == 0 and \
                arcade.get_distance(self.center_x, self.center_y, sprite.center_x, sprite.center_y + 50) < 50:
            return 3
        elif self.currentDirection == 1 and \
                arcade.get_distance(self.center_x, self.center_y, sprite.center_x + 50, sprite.center_y) < 50:
            return 2
        elif self.currentDirection == 2 and \
                arcade.get_distance(self.center_x, self.center_y, sprite.center_x - 50, sprite.center_y) < 50:
            return 1
        elif self.currentDirection == 3 and \
                arcade.get_distance(self.center_x, self.center_y, sprite.center_x, sprite.center_y - 50) < 50:
            return 0
        else:
            return None
