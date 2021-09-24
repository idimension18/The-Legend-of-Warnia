# -------import some librari------------
import arcade

# ------other import--------------
import Views

WIDTH = 1400
HEIGHT = 700
SCALE = 1.5


def main():
    """ Main method """
    window = arcade.Window(WIDTH, HEIGHT, "The Legend of Warnia", resizable=True)
    menu_view = Views.MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
