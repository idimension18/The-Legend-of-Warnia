import arcade

import main


class Deco(arcade.Sprite):
    """
    interactives decorations
    """
    def __init__(self, sprite: arcade.Sprite):
        super().__init__()
        self.sprite = sprite
        # ----some info------
        try:
            self.ID = self.sprite.properties["ID"]
        except KeyError:
            self.ID = None
        self.scale = main.SCALE
        self.center_y = self.sprite.center_y
        self.center_x = self.sprite.center_x
        self.isUnderLayers = False
        self.isUnderObjects = False
        self.isInDialogue = False

        try:
            self.linked = self.sprite.properties["linked"]
        except KeyError:
            self.linked = None

        # -----some property-------
        try:
            self.hasDialogue = self.sprite.properties["Has Dialogue"]
        except KeyError:
            self.hasDialogue = False
        # ------ load textures -------
        self.texture = self.sprite.texture

        # -----some property------
        try:
            if sprite.properties["Has Dialogue"]:
                self.dialogueID = sprite.properties["dialogue ID"]
            else:
                self.dialogueID = None
        except KeyError:
            self.dialogueID = None

    def update(self):
        pass
