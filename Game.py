# ----------import some library-------------
import arcade
from arcade.experimental.lights import Light, LightLayer
from os import walk
# ---------other import-----------------
import main
import DialogBox
from Player import *
from NPC import *
from DialogBox import *
from Furniture import *
from Deco import *


# ------------------


class GameView(arcade.View):
    """ Main Window """

    def __init__(self):
        """ Create the variables """
        super().__init__()
        # global info
        self.debug = False
        self.inGame = False
        self.cameraX = 0
        self.cameraY = 0
        self.dialogueReady = False
        self.actionTriggered = False
        self.keyA_pressed = False
        self.currentDialogue = None
        self.saveEntities = []
        self.changeMap = False

        # local title
        self.currentLocalTitle = None
        self.titleTimeIndex = 0
        self.titleX = main.WIDTH
        self.isLocalTitleShow = False
        self.textScheduler = False

        # physics
        self.wallsPhysics = None
        self.waterPhysics = None
        self.objectPhysics = None

        # player and sprite
        self.player = None
        self.NPCs = []
        self.entities = []
        self.NPCEngine = None
        self.NPCsprites = arcade.SpriteList()
        self.furnitures = []
        self.furnitureEngine = None
        self.furnitureSprites = arcade.SpriteList()
        self.decos = []

        # map ressource
        self.mapFile = None
        self.mapWidth = 0
        self.mapHeight = 0
        self.level = None
        self.ground = None
        self.onFloor = None
        self.layers = None
        self.frontStage = None
        self.walls = None
        self.water = None
        self.object = None
        self.objectImage = None
        self.floorTriggerUP = None
        self.floorTriggerDown = None
        self.correctifs = None
        self.correctiveLayer = None
        self.soundSource = None

        # utilitaire
        self.shadowGround = None
        self.shadowLayer = None
        self.uppers = None
        self.warpers = None
        self.zoneTriggers = None
        self.inHouse = False

        # loading
        self.loadingScreen = None
        self.loadingDotX = None
        self.loadingTimer = 300
        self.loadingStep = 0
        self.coordStart = (1419, 2359)
        self.sensStart = 0
        self.ressourceReady = False

        # test of light
        self.light_layer = None
        self.player_light = None
        self.light = None

        # soundtest
        self.isMusiqueChanging = False
        self.currentTheme = None
        self.currentSong = None
        self.soundPlayer = None
        self.zoneTriggered = False

        self.soundEffects = {}
        self.soundEffectPlayers = {}

        self.Themes = {}

    # -----------set everything is to be set-------------
    def setup(self):
        """ Set up everything with the game """

        # level
        self.level = "Arckania interiors"
        # load light
        self.light_layer = LightLayer(self.window.width, self.window.height)
        # self.player_light = Light(0, 0, 150, arcade.color.WHITE, "soft")
        # self.light_layer.add(self.player_light)
        self.loadingDotX = self.window.width / 2 - 100

        # get the map
        self.mapFile = arcade.tilemap.read_tmx(f"data/maps/{self.level}.tmx")
        self.mapWidth = self.mapFile.map_size.width * 32
        self.mapHeight = self.mapFile.map_size.height * 32

        for (domains, underDirectory, preFile) in walk("data/music/Themes"):
            for file in preFile:
                self.Themes[file[:len(file) - 4]] = arcade.load_sound(f"data/music/Themes/{file}")

    # ------------------KEY LISTENERS--------------------
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if not self.player.isStuck:
            if key == arcade.key.UP:
                self.player.keyPileADDKey(Direction.back.value)

            if key == arcade.key.DOWN:
                self.player.keyPileADDKey(Direction.front.value)

            if key == arcade.key.LEFT:
                self.player.keyPileADDKey(Direction.left.value)

            if key == arcade.key.RIGHT:
                self.player.keyPileADDKey(Direction.right.value)

        if key == arcade.key.A:
            self.actionTriggered = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.player.keyPileRemoveKey(Direction.back.value)

        if key == arcade.key.DOWN:
            self.player.keyPileRemoveKey(Direction.front.value)

        if key == arcade.key.LEFT:
            self.player.keyPileRemoveKey(Direction.left.value)

        if key == arcade.key.RIGHT:
            self.player.keyPileRemoveKey(Direction.right.value)

    # --------------------------------------------------------

    # --------update everything is to be update------------
    def on_update(self, delta_time):
        """ Movement and game logic """
        # ---------loading---------
        if self.loadingStep != 3:
            self.loading()
        # --------------PLAYER NPC and MAP---------------
        # self.player_light.position = self.player.position
        if self.ressourceReady:
            # update graphics and phisics
            self.player.update(delta_time)
            self.player.update_animation(delta_time)
            self.water.update_animation()
            self.objectImage.update_animation()

            # update songs
            self.updateSoundEffectVolume()
            self.updateSongInfo()
            if self.isMusiqueChanging:
                self.changeTheme()

            # update local title
            self.updateLocalTitleInfo()
            if self.isLocalTitleShow:
                self.updateLocalTitle()

            for sprite in self.entities:
                # ------layer order-------
                if arcade.check_for_collision_with_list(sprite, self.uppers):
                    sprite.isUnderLayers = True
                else:
                    sprite.isUnderLayers = False

                for image in self.objectImage:
                    if arcade.check_for_collision(image, sprite):
                        if image.center_y < sprite.center_y:
                            sprite.isUnderObjects = True
                            break
                        else:
                            sprite.isUnderObjects = False
                    else:
                        sprite.isUnderObjects = False
                # --------check player/NPC collisions--------
                if not isinstance(sprite, Player):
                    if isinstance(sprite, NPC) and not sprite.isInDialogue:
                        sprite.update(delta_time)
                        sprite.isStuck = arcade.check_for_collision(sprite, self.player)

                    sprite.update_animation(delta_time)

                    if not self.dialogueReady and self.actionTriggered and self.player.talkingWay(sprite) is not None \
                            and sprite.ID is not None and sprite.hasDialogue:
                        sprite.isInDialogue = True
                        sprite.stuck = True
                        sprite.dialogueSens = self.player.talkingWay(sprite)
                        self.player.isStuck = True
                        self.currentDialogue = DialogBox(sprite.name, (sprite.ID, 0))
                        self.dialogueReady = True

                    if not self.dialogueReady and sprite.isInDialogue:
                        self.player.isStuck = False
                        sprite.isStuck = False
                        sprite.isInDialogue = False

                # ------------------- player-----------------------
                if isinstance(sprite, Player):

                    # -------------change floor-------------
                    if not sprite.isChangingFloor:
                        if sprite.collides_with_list(self.floorTriggerUP):
                            sprite.isChangingFloor = True
                            sprite.floor = 1
                            self.getFloor()

                        if sprite.collides_with_list(self.floorTriggerDown):
                            sprite.isChangingFloor = True
                            sprite.floor = 0
                            self.getFloor()
                    else:
                        if not sprite.collides_with_list(self.floorTriggerUP) and not sprite.collides_with_list(
                                self.floorTriggerDown):
                            sprite.isChangingFloor = False

                    # ----------------change map (warpers)-------------
                    if not self.dialogueReady:
                        for warper in self.warpers:
                            if arcade.check_for_collision(warper, sprite) \
                                    and (not warper.properties["is Door"]
                                         or (warper.properties["is Door"] and self.actionTriggered)):
                                self.level = warper.properties["Target"]
                                # get the map
                                self.mapFile = arcade.tilemap.read_tmx(f"data/maps/{self.level}.tmx")
                                self.mapWidth = self.mapFile.map_size.width * 32
                                self.mapHeight = self.mapFile.map_size.height * 32

                                if not warper.properties["is Door"]:
                                    if warper.properties["Target Side"] == "UP":
                                        self.coordStart = (sprite.center_x, 3140 * main.SCALE)
                                    elif warper.properties["Target Side"] == "DOWN":
                                        self.coordStart = (sprite.center_x, 60 * main.SCALE)
                                    elif warper.properties["Target Side"] == "LEFT":
                                        self.coordStart = (60 * main.SCALE, sprite.center_y)
                                    else:
                                        self.coordStart = (3140 * main.SCALE, sprite.center_y)

                                else:
                                    self.level = warper.properties["Target"]
                                    # get the map
                                    self.mapFile = arcade.tilemap.read_tmx(f"data/maps/{self.level}.tmx")
                                    self.mapWidth = self.mapFile.map_size.width * 32
                                    self.mapHeight = self.mapFile.map_size.height * 32

                                    self.coordStart = (warper.properties["x"] * main.SCALE,
                                                       (self.mapHeight - (warper.properties["y"])) * main.SCALE)

                                # -------------build a new loading----------
                                self.sensStart = self.player.currentDirection
                                self.loadingTimer = 60
                                self.loadingStep = 0
                                self.inGame = False
                                self.ressourceReady = False
                                self.mapReset()
                                self.loading()
                                self.changeMap = True
                                break

                # ------------stop entities iteration---------
                if self.changeMap:
                    break
                # --------------------------------

            # make perspective between entities
            if not self.changeMap:
                self.saveEntities.extend(self.entities)
                self.entities.sort(key=self.getY, reverse=True)

                # ------- physics engine--------
                self.wallsPhysics.update()
                self.waterPhysics.update()
                self.objectPhysics.update()
                self.furnitureEngine.update()

                if self.player.isMoving:
                    self.NPCEngine.update()
            else:
                self.changeMap = False
        # -------update Camera--------
        if self.inGame:
            self.cameraX = self.player.center_x - self.window.width / 2
            self.cameraY = self.player.center_y - self.window.height / 2

            if self.player.center_x < self.window.width / 2:
                self.cameraX = 0

            elif self.player.center_x > main.SCALE * self.mapWidth - (self.window.width / 2):
                self.cameraX = main.SCALE * self.mapWidth - self.window.width

            if self.player.center_y < self.window.height / 2:
                self.cameraY = 0

            elif self.player.center_y > main.SCALE * self.mapHeight - (self.window.height / 2):
                self.cameraY = main.SCALE * self.mapHeight - self.window.height

        else:
            self.cameraX = 0
            self.cameraY = 0

        arcade.set_viewport(self.cameraX, self.cameraX + self.window.width, self.cameraY,
                            self.cameraY + self.window.height)

        # --------update dialog box--------------
        if self.dialogueReady:
            self.currentDialogue.update()
            if self.currentDialogue.isWaiting and self.actionTriggered:
                self.currentDialogue.changeCase()
                self.currentDialogue.isWaiting = False

            if self.currentDialogue.toDestroy:
                self.dialogueReady = False
            boxGraphic.center_x = self.player.center_x + boxGraphicX
            boxGraphic.center_y = self.player.center_y + boxGraphicY

            nameGraphic.center_x = self.player.center_x + nameGraphicX
            nameGraphic.center_y = self.player.center_y + nameGraphicY

        self.actionTriggered = False

    # ------------draw everything is to be drawing--------------
    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        # draw map
        with self.light_layer:
            if self.ressourceReady:
                self.ground.draw()
                self.water.draw()
                self.onFloor.draw()

                self.shadowGround.draw()

                # draw back
                for sprite in self.entities:
                    if sprite.isUnderLayers:
                        sprite.draw()

                self.layers.draw()

                # draw middle
                for sprite in self.entities:
                    if sprite.isUnderObjects and not sprite.isUnderLayers:
                        sprite.draw()

                self.objectImage.draw()

                # draw up
                for sprite in self.entities:
                    if not sprite.isUnderLayers and not sprite.isUnderObjects:
                        sprite.draw()
                if self.level == "new djeherzis":
                    self.correctifs.draw()

                self.shadowLayer.draw()
                self.correctiveLayer.draw()

        self.light_layer.draw(ambient_color=(255, 255, 255))
        # self.light_layer.draw(ambient_color=(40, 40, 100))

        # -------debug mode--------
        if self.debug and self.ressourceReady:
            for sprite in self.entities:
                sprite.draw_hit_box((0, 0, 255))
            for sprite in self.walls:
                sprite.draw_hit_box((0, 0, 0))

        # --------loading screen-------------
        if self.loadingStep != 3:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height, (0, 0, 0))
            arcade.draw_text("Loading...",
                             (self.window.width / 2) - 100,
                             self.window.height - 300,
                             (255, 255, 255),
                             font_size=50,
                             font_name="data/texts/fonts/comic sans ms.ttf")
            if self.loadingStep > 1:
                arcade.draw_rectangle_filled(self.loadingDotX, self.window.height / 2, 20, 20, (255, 255, 255))

        # --------draw dialog box--------------
        if self.dialogueReady:
            boxGraphic.draw()
            nameGraphic.draw()
            arcade.draw_text(self.currentDialogue.texte_to_show,
                             self.player.center_x - 300,
                             self.player.center_y - self.currentDialogue.y,
                             (110, 30, 20),
                             font_size=30,
                             width=600,
                             font_name="data/texts/fonts/m5x7.ttf")

            arcade.draw_text(self.currentDialogue.name,
                             self.player.center_x - 290,
                             self.player.center_y - 125,
                             (255, 255, 255),
                             font_size=30,
                             width=400,
                             font_name="data/texts/fonts/m5x7.ttf")
        # local title
        if self.textScheduler:
            arcade.draw_text(self.currentLocalTitle,
                             10 + self.cameraX + self.titleX,
                             self.cameraY + main.HEIGHT - 200,
                             (0, 0, 0),
                             font_size=40)
        else:
            arcade.unschedule(self.updateTitle)

    # ----------load the current map-------------------
    def load_level(self):
        # grab ground
        self.ground = arcade.tilemap.process_layer(self.mapFile, "Ground/Ground", main.SCALE)
        self.ground.extend(arcade.tilemap.process_layer(self.mapFile, "Ground/Ground 2", main.SCALE))
        self.ground.extend(arcade.tilemap.process_layer(self.mapFile, "Ground/Relief", main.SCALE))

        # grab floor thing
        self.onFloor = arcade.tilemap.process_layer(self.mapFile, "Water Things/Bridge", main.SCALE)

        # grab many thing
        self.layers = arcade.tilemap.process_layer(self.mapFile, "Layers/Layer Background", main.SCALE)
        self.layers.extend(arcade.tilemap.process_layer(self.mapFile, "Layers/Layer 1", main.SCALE))
        self.layers.extend(arcade.tilemap.process_layer(self.mapFile, "Layers/Layer  inter", main.SCALE))
        self.layers.extend(arcade.tilemap.process_layer(self.mapFile, "Layers/Layer 2", main.SCALE))

        # grab walls
        if self.level != "new djeherzis":
            # grab walls
            self.walls = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Simple Collisions", main.SCALE)
            self.walls.extend(
                arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Affine Collisions", main.SCALE))

            self.uppers = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Simple UPPER", main.SCALE)
            self.uppers.extend(arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Affine UPPER", main.SCALE))

        else:
            self.getFloor()

        self.water = arcade.tilemap.process_layer(self.mapFile, "Water Things/WaterBords", main.SCALE,
                                                  use_spatial_hash=False)
        self.water.extend(
            arcade.tilemap.process_layer(self.mapFile, "Water Things/Water", main.SCALE, use_spatial_hash=False))
        self.water.extend(
            arcade.tilemap.process_layer(self.mapFile, "Water Things/Water Corec", main.SCALE, use_spatial_hash=False))
        self.water.extend(
            arcade.tilemap.process_layer(self.mapFile, "Water Things/WaterFall", main.SCALE, use_spatial_hash=False))

        # grab Object
        self.object = arcade.tilemap.process_layer(self.mapFile, "Objects/Object Physique", main.SCALE,
                                                   use_spatial_hash=False)
        self.objectImage = arcade.tilemap.process_layer(self.mapFile, "Objects/Object Image", main.SCALE,
                                                        use_spatial_hash=False)
        self.objectImage.extend(arcade.tilemap.process_layer(self.mapFile, "Objects/little Object", main.SCALE,
                                                             use_spatial_hash=False))
        # grab shadows
        self.shadowGround = arcade.tilemap.process_layer(self.mapFile, "Ground/Ground shadow", main.SCALE)
        self.shadowLayer = arcade.tilemap.process_layer(self.mapFile, "Shadow layer 2", main.SCALE)
        self.shadowLayer.extend(arcade.tilemap.process_layer(self.mapFile, "Lights", main.SCALE))

        # ----grab floor Trigger-----
        self.floorTriggerUP = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Floor Trigger UP", main.SCALE)
        self.floorTriggerDown = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Floor Trigger Down",
                                                             main.SCALE)

        self.correctiveLayer = arcade.tilemap.process_layer(self.mapFile, "Layers/Corrective Layer 1", main.SCALE)
        self.correctiveLayer.extend(arcade.tilemap.process_layer(self.mapFile, "Layers/Corrective Layer 2", main.SCALE))
        # -----grab warpers-----
        self.warpers = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Warpers", main.SCALE)

        # -------grab zone Trigger------
        self.zoneTriggers = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Zone Triggers", main.SCALE)
        self.soundSource = arcade.tilemap.process_layer(self.mapFile, "Utilitaire/Sound Source", main.SCALE)

        # --------grab sprite-------
        for sprite in arcade.tilemap.process_layer(self.mapFile, "Entities/Sprite", main.SCALE):
            self.NPCs.append(NPC(sprite))

        for sprite in arcade.tilemap.process_layer(self.mapFile, "Entities/Furniture", main.SCALE):
            self.furnitures.append(Furniture(sprite))

        for sprite in arcade.tilemap.process_layer(self.mapFile, "Entities/Deco", main.SCALE):
            self.decos.append(Deco(sprite))

        self.NPCsprites.extend(self.NPCs)
        self.furnitureSprites.extend(self.furnitures)

        self.entities.extend(self.NPCs)
        self.entities.extend(self.furnitures)
        self.entities.extend(self.decos)

        # init physics
        self.wallsPhysics = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.waterPhysics = arcade.PhysicsEngineSimple(self.player, self.water)
        self.objectPhysics = arcade.PhysicsEngineSimple(self.player, self.object)
        self.NPCEngine = arcade.PhysicsEngineSimple(self.player, self.NPCsprites)
        self.furnitureEngine = arcade.PhysicsEngineSimple(self.player, self.furnitureSprites)

        # end
        self.entities.append(self.player)
        self.ressourceReady = True

    # ------loading and other charging stuff------
    def loading(self):
        if self.loadingStep == 1:
            # player
            self.player = Player()
            self.player.set_position(self.coordStart[0], self.coordStart[1])
            self.player.currentDirection = self.sensStart

            # level
            self.load_level()
            for sprite in self.soundSource:
                self.soundEffects[sprite] = arcade.load_sound("data\\" + str(sprite.properties["Sound"])[2:])
                self.soundEffectPlayers[sprite] = arcade.play_sound(self.soundEffects[sprite], volume=0, looping=True)

            self.loadingStep = 2

        if self.loadingStep < 1:
            self.loadingStep += 1

        self.loadingTimer -= 1

        if self.loadingStep > 1:
            self.loadingDotX += 40

            if self.loadingDotX > self.window.width / 2 + 100:
                self.loadingDotX = self.window.width / 2 - 100

        if self.loadingTimer == 0:
            try:
                if not self.currentSong.is_playing(self.soundPlayer):
                    self.soundPlayer = arcade.play_sound(self.currentSong, looping=True)
            except AttributeError:
                self.soundPlayer = arcade.play_sound(self.currentSong, looping=True)

            self.loadingStep = 3
            self.inGame = True

    # -------get the current floor for desert collions-------
    def getFloor(self):
        self.walls = arcade.tilemap.process_layer(
            self.mapFile, f"Utilitaire/Floor {self.player.floor}/Simple Collisions", main.SCALE)
        self.walls.extend(
            arcade.tilemap.process_layer(
                self.mapFile, f"Utilitaire/Floor {self.player.floor}/Affine Collisions", main.SCALE))

        self.uppers = arcade.tilemap.process_layer(
            self.mapFile, f"Utilitaire/Floor {self.player.floor}/Simple UPPER", main.SCALE)
        self.uppers.extend(arcade.tilemap.process_layer(
            self.mapFile, f"Utilitaire/Floor {self.player.floor}/Affine UPPER", main.SCALE))

        self.correctifs = arcade.tilemap.process_layer(
            self.mapFile, f"Utilitaire/Floor {self.player.floor}/Correctifs", main.SCALE)

        self.wallsPhysics = arcade.PhysicsEngineSimple(self.player, self.walls)

    def getY(self, sprite: arcade.Sprite):
        if (isinstance(sprite, Furniture) or isinstance(sprite, Deco)) and sprite.linked is not None:
            return self.getLink(sprite.linked).center_y
        else:
            return sprite.center_y

    def getLink(self, ID: str) -> arcade.Sprite:
        for sprite in self.saveEntities:
            if sprite.ID == ID:
                return sprite

    def mapReset(self):
        # physics
        self.wallsPhysics = None
        self.waterPhysics = None
        self.objectPhysics = None

        # player and sprite
        self.player = None
        self.NPCs = []
        self.entities = []
        self.NPCEngine = None
        self.NPCsprites = arcade.SpriteList()
        self.furnitures = []
        self.furnitureEngine = None
        self.furnitureSprites = arcade.SpriteList()
        self.decos = []

        # map ressource
        self.ground = None
        self.onFloor = None
        self.layers = None
        self.frontStage = None
        self.walls = None
        self.water = None
        self.object = None
        self.objectImage = None
        self.floorTriggerUP = None
        self.floorTriggerDown = None
        self.correctifs = None

        # utilitaire
        self.shadowGround = None
        self.shadowLayer = None
        self.uppers = None
        self.warpers = None
        self.zoneTriggers = None

        # reset sound effects
        for sprite in self.soundSource:
            arcade.stop_sound(self.soundEffectPlayers[sprite])

        self.soundSource = None
        self.soundEffects = {}
        self.soundEffectPlayers = {}

        # test reset
        self.currentLocalTitle = None
        self.titleTimeIndex = 0
        self.titleX = main.WIDTH
        self.isLocalTitleShow = False
        self.textScheduler = False
        arcade.unschedule(self.updateTitle)

    def updateSongInfo(self):
        """
        recherche des mis a jour sur la musique qui doit être jouée
        """
        for sprite in self.zoneTriggers:
            if arcade.check_for_collision(self.player, sprite):
                self.zoneTriggered = True
                try:
                    if sprite.properties["Theme"] != self.currentTheme:
                        self.isMusiqueChanging = True
                        self.currentTheme = sprite.properties["Theme"]
                        break
                except Exception as e:
                    print(e)  # cas où il ne trouve pas le thème

        if not self.isMusiqueChanging and not self.zoneTriggered:
            try:
                if self.mapFile.properties["Theme"] != self.currentTheme:
                    self.isMusiqueChanging = True
                    self.currentTheme = self.mapFile.properties["Theme"]
            except Exception as e:  # cas où il ne trouve pas le thème
                print(e)

        # reset
        self.zoneTriggered = False

    def changeTheme(self):
        """
        fait la transition entre les musiques
        """
        try:
            self.currentSong.set_volume(self.currentSong.get_volume(self.soundPlayer) - 0.01, self.soundPlayer)
            if self.currentSong.get_volume(self.soundPlayer) <= 0:
                arcade.stop_sound(self.soundPlayer)
                self.currentSong = self.Themes[self.currentTheme]
                if self.loadingStep >= 3:
                    self.soundPlayer = arcade.play_sound(self.currentSong, looping=True)

                self.isMusiqueChanging = False

        except AttributeError:  # au cas où la musique n'existe pas encore
            self.currentSong = self.Themes[self.currentTheme]
            if self.loadingStep >= 3:
                self.soundPlayer = arcade.play_sound(self.currentSong, looping=True)

            self.isMusiqueChanging = False

    def updateSoundEffectVolume(self):
        for sprite in self.soundSource:
            self.soundEffects[sprite].set_volume(1 / (arcade.get_distance_between_sprites(self.player, sprite) / 100),
                                                 self.soundEffectPlayers[sprite])

    def updateLocalTitleInfo(self):
        for sprite in self.zoneTriggers:
            if arcade.check_for_collision(self.player, sprite):
                self.zoneTriggered = True
                if sprite.properties["Name"] != self.currentLocalTitle:
                    self.isLocalTitleShow = True
                    self.currentLocalTitle = sprite.properties["Name"]
                    break

        if not self.isLocalTitleShow and not self.zoneTriggered:
            if self.mapFile.properties["Name"] != self.currentLocalTitle:
                self.isLocalTitleShow = True
                self.currentLocalTitle = self.mapFile.properties["Name"]

    def updateLocalTitle(self):
        if not self.isMusiqueChanging and self.loadingStep >= 3:
            self.isLocalTitleShow = False
            arcade.schedule(self.updateTitle, 1 / 60)
            self.textScheduler = True
            if self.titleTimeIndex >= 70:
                arcade.unschedule(self.updateTitle)

    def updateTitle(self, delta_time):
        self.titleTimeIndex += 1
        self.titleX -= self.getTitleX()
        if self.titleTimeIndex >= 70:
            self.titleX = main.WIDTH
            self.titleTimeIndex = 0
            self.isLocalTitleShow = False
            self.textScheduler = False

    def getTitleX(self) -> int:
        if 10 < self.titleTimeIndex < 70:
            return 3 + int(2 * ((self.titleTimeIndex / 25 - 1.2) ** 20))
        else:
            return 65
