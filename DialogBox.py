import json
import arcade

DATA = json.load(open("data/texts/Texte DB.json", "rb"), encoding="utf-16")

boxGraphic = arcade.Sprite()
boxGraphic.texture = arcade.load_texture("data/images/Dialogue Boxs.png", 0, 480, 320, 80)
boxGraphic.scale = 2
boxGraphicX = 0
boxGraphicY = -200

nameGraphic = arcade.Sprite()
nameGraphic.texture = arcade.load_texture("data/images/Dialogue Boxs.png", 320, 880, 320, 80)
nameGraphic.scale = 0.5
nameGraphicX = -225
nameGraphicY = -110

beepSong = arcade.load_sound("data/music/Sound Effect/beep.wav")

class DialogBox:
    """
    Dialogue Box
    """
    def __init__(self, name: str, dialog: tuple):
        # setup
        self.ID = dialog[0]
        self.NB = dialog[1]
        self.name = name
        self.toDestroy = False
        self.isWaiting = False
        self.y = 175

        # data
        self.case = 0
        self.texte = iter(DATA[self.ID][f"text {self.NB}"][f"case {self.case}"])
        self.texte_to_show = ""
        self.waitTime = 0

    def changeCase(self):
        self.case += 1
        self.texte_to_show = ""
        self.y = 175
        try:
            self.texte = iter(DATA[self.ID][f"text {self.NB}"][f"case {self.case}"])
        except KeyError:
            self.toDestroy = True

    def update(self):
        if self.waitTime == 0 and not self.isWaiting:
            try:
                nextChar = next(self.texte)

                if nextChar == "\n":
                    self.y += 27
                if nextChar != "$":
                    self.texte_to_show += nextChar
                    if nextChar != ".":
                        beepSong.play(volume=0.05)
                else:
                    self.waitTime = int(next(self.texte) + next(self.texte))

            except StopIteration:
                self.isWaiting = True
        else:
            if self.waitTime != 0:
                self.waitTime -= 1
