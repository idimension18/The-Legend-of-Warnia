# import some lybrary
import arcade

# other import
import Game
import main


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.textAlpha = 255
        self.alphaIncrease = False
        self.image = arcade.Sprite("data/images/title screen.jpg")
        self.image.width = main.WIDTH
        self.image.height = main.HEIGHT
        self.image.set_position(main.WIDTH / 2, main.HEIGHT / 2)
        self.music = arcade.play_sound(arcade.load_sound("data/music/Themes/Title screen.mp3"))

        self.menu = "titre"
        self.cursor = "begin"

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.ENTER:
            if self.cursor == "begin":
                arcade.stop_sound(self.music)
                gameView = Game.GameView()
                gameView.setup()
                self.window.show_view(gameView)
            else:
                self.menu = "credits"

        if key == arcade.key.UP:
            self.cursor = "begin"

        if key == arcade.key.DOWN:
            self.cursor = "credits"

        if key == arcade.key.B:
            self.menu = "titre"

    def on_update(self, delta_time: float):
        if self.alphaIncrease:
            self.textAlpha += 5
            if self.textAlpha == 255:
                self.alphaIncrease = False
        else:
            self.textAlpha -= 5
            if self.textAlpha == 0:
                self.alphaIncrease = True

    def on_draw(self):
        arcade.start_render()
        if self.menu == "titre":
            self.image.draw()

            arcade.draw_text("The Legend of Warnia", main.WIDTH / 2, (main.HEIGHT / 2) + 100,
                             arcade.color.BLUE, font_size=50, anchor_x="center",
                             font_name="data/texts/fonts/TheWildBreathOfZelda-15Lv.ttf")
            if self.cursor == "begin":
                arcade.draw_text("Nouvelle parti!", main.WIDTH / 2, (main.HEIGHT / 2) - 200,
                                 (0, 0, 0, self.textAlpha), font_size=20, anchor_x="center")

                arcade.draw_text("Credits", main.WIDTH / 2, (main.HEIGHT / 2) - 250,
                                 (0, 0, 0), font_size=20, anchor_x="center")
            else:
                arcade.draw_text("Nouvelle parti!", main.WIDTH / 2, (main.HEIGHT / 2) - 200,
                                 (0, 0, 0), font_size=20, anchor_x="center")

                arcade.draw_text("Credits", main.WIDTH / 2, (main.HEIGHT / 2) - 250,
                                 (0, 0, 0, self.textAlpha), font_size=20, anchor_x="center")
        else:
            arcade.set_background_color((0, 0, 0))
            arcade.draw_text("The Legend of Warnia", main.WIDTH / 2, main.HEIGHT-100,
                             (255, 255, 255), font_size=50, anchor_x="center",
                             font_name="data/texts/fonts/TheWildBreathOfZelda-15Lv.ttf")

            arcade.draw_text("créé, programmé et réalisé par : iwan derouet", main.WIDTH / 2, main.HEIGHT-150,
                             (255, 255, 255), font_size=20, anchor_x="center")

            arcade.draw_text("Ressources Graphiques :", main.WIDTH / 2, main.HEIGHT - 250,
                             (255, 255, 255), font_size=20, anchor_x="center")

            arcade.draw_text(u"https://itch.io/game-assets/free", main.WIDTH / 2, main.HEIGHT - 275,
                             (255, 255, 255), font_size=20, anchor_x="center")

            arcade.draw_text(u"https://opengameart.org", main.WIDTH / 2, main.HEIGHT - 300,
                             (255, 255, 255), font_size=20, anchor_x="center")

            arcade.draw_text("Ressources Sonors (effets) :", main.WIDTH / 2, main.HEIGHT - 400,
                             (255, 255, 255), font_size=20, anchor_x="center")

            arcade.draw_text(u"https://freesound.org", main.WIDTH / 2, main.HEIGHT - 425,
                             (255, 255, 255), font_size=20, anchor_x="center")

            arcade.draw_text("Toutes les musiques ont été composés par : Iwan Derouet",
                             main.WIDTH / 2, main.HEIGHT - 475,
                             (255, 255, 255), font_size=20, anchor_x="center")
