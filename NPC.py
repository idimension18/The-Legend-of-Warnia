import arcade

import main


class NPC(arcade.Sprite):
    """
    NPCs
    """

    def __init__(self, sprite: arcade.Sprite):
        # Set up parent class
        super().__init__()
        self.sprite = sprite

        # -------some info-------
        try:
            self.ID = self.sprite.properties["ID"]
            self.name = self.sprite.properties["Name"]
        except KeyError:
            self.ID = None
            self.name = None

        self.scale = 1.4*main.SCALE
        try:
            self.speed = self.sprite.properties["speed"]*main.SCALE
        except KeyError:
            self.speed = 0

        self.center_y = self.sprite.center_y
        self.center_x = self.sprite.center_x
        self.isInDialogue = False
        self.dialogueSens = 0

        # -------------physics info-----------
        self.hit_box = ((-16.0, -16.0), (16.0, -16.0), (16.0, 0.0), (-16.0, 0.0))  # set hit box
        self.isUnderLayers = False
        self.isUnderObjects = False
        self.isStuck = False

        # ------ load textures -------
        self.animTime = 10
        self.animTimer = 0
        self.sheet = "data\\" + str(sprite.properties["sheet"])[2:]

        self.textures = [[] for i in range(8)]
        for i in range(4):
            self.textures[i].append(arcade.load_texture(self.sheet, 32, i * 32, 32, 32))

        for i in range(4):
            for k in range(3):
                self.textures[i + 4].append(arcade.load_texture(self.sheet, k * 32, i * 32, 32, 32))

        for i in range(4):
            self.textures[i + 4].append(arcade.load_texture(self.sheet, 32, i * 32, 32, 32))

        # -----some property-------
        try:
            self.hasDialogue = self.sprite.properties["Has Dialogue"]
        except KeyError:
            self.hasDialogue = False

        # ------load patern-----
        try:
            self.actionNumber = sprite.properties["Action Number"]
        except KeyError:
            self.actionNumber = 0

        self.actions = []

        for i in range(1, self.actionNumber + 1):
            self.actions.append(sprite.properties["A" + str(i)])
        self.currentAction = 0
        self.textAction = ""
        self.actionTime = 0
        self.actionTimer = 0
        self.isMoving = False
        self.sens = 0
        self.animationIndex = 0
        self.texture = self.textures[self.sens][0]

    def update(self, delta_time: float = 1 / 60):
        if self.actionNumber != 0 and self.actionTime == self.actionTimer:
            self.changeAction()

        if not self.isStuck:
            self.actionTimer += 1
            if self.isMoving:
                # ------moving------
                if self.sens == 0:
                    self.center_y -= self.speed
                elif self.sens == 1:
                    self.center_x -= self.speed
                elif self.sens == 2:
                    self.center_x += self.speed
                else:
                    self.center_y += self.speed

    def update_animation(self, delta_time: float = 1 / 60):
        if not self.isInDialogue:
            if self.isMoving:

                if self.animTimer == 0:
                    self.animTimer = self.animTime

                    self.animationIndex += 1
                    if self.animationIndex == 4:
                        self.animationIndex = 0

                    self.texture = self.textures[self.sens + 4][self.animationIndex]
                self.animTimer -= 1
            else:
                self.animationIndex = 0
                self.animTimer = 0
                self.texture = self.textures[self.sens][0]

        else:
            self.texture = self.textures[self.dialogueSens][0]

    def changeAction(self):
        # reset
        self.animTimer = 0
        self.actionTimer = 0
        # increment action
        self.currentAction += 1
        if self.currentAction >= self.actionNumber:
            self.currentAction = 0

        # get values
        self.textAction = self.actions[self.currentAction]
        seconde = int(self.textAction[2:])
        self.actionTime = seconde * 60

        # is moving
        if self.textAction[0] == "W":
            self.isMoving = True
        else:
            self.isMoving = False

        # get sens
        if self.textAction[1] == "F":
            self.sens = 0
        elif self.textAction[1] == "L":
            self.sens = 1
        elif self.textAction[1] == "R":
            self.sens = 2
        else:
            self.sens = 3
