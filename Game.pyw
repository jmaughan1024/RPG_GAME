# Description: The main game file
# Author: Jacob Maughan

# Sys Imports
import time

# Lib Imports
import pygame

# Local Imports
from Enums import GameState
from JsonHandler import JsonHandler
from Window import Window
from EventHandler import EventHandler
from ObjectHandler import ObjectHandler
from MapHandler import MapHandler
from Player import Player
from TestBlock import TestBlock

class Game():
    def __init__(self):
        # Initilize pygame
        pygame.init()

        # Load settings
        self.settingsFile = JsonHandler('./assets/data/settings.json')
        self.settingsData = self.settingsFile.getJson()

        # Set width and height from settings
        self.width = self.settingsData['width']
        self.height = self.settingsData['height']

        # Sprite scale
        self.scaleFactor = 4

        # Create instance of window and handlers
        self.window = Window(self.width, self.height, 'RPG_GAME', 'assets/art/logo.png')
        self.objectHandler = ObjectHandler(self)
        self.eventHandler = EventHandler(self, self.objectHandler)
        self.mapHandler  = MapHandler(self.scaleFactor, self.objectHandler, self.window)

        # Setup game state
        self.state = None
        self.lastState = None

        # Game speed/Tick speed setup
        self.tickSpeed = 120
        self.ticks = 0

    def tick(self):
        # Setup tick counter | If tick count hit tickSpeed,  1 second has elapsed and set ticks to 0
        self.ticks += 1
        if self.ticks == self.tickSpeed: self.ticks = 0

        # Check if state has changed and load objects if has
        if not self.lastState == self.state:
            self.lastState = self.state
            self.loadObjects()

        # Tick handlers with tick counter as arg
        self.eventHandler.tick(self.ticks)
        self.objectHandler.tick(self.ticks)

    def render(self):
        # Render background
        self.window.fillScreen(0, 0, 0)

        # Render objects
        self.objectHandler.render()

        # Update pygame display
        pygame.display.update()

    def loadObjects(self):
        # Check gamestate and load correct objects
        if self.state == GameState.MAIN_MENU:
            self.objectHandler.clearObjects()
        elif self.state == GameState.GAME:
            self.objectHandler.clearObjects()
            self.mapHandler.loadMap('area_1')
            self.objectHandler.addObject(Player(10 * 16 * self.scaleFactor, 10 * 16 * self.scaleFactor, 16 * self.scaleFactor, 32 * self.scaleFactor, self.window))
            self.objectHandler.addObject(TestBlock(10, 10, 100, 100, self.window))
        elif self.state == GameState.PAUSE:
            pass

    def run(self):
        # Setup delta time to tick specific amount per second
        lastTime = time.time()
        dt = 0
        while self._running:
            # Update delta time
            dt += (time.time() - lastTime) * self.tickSpeed
            lastTime = time.time()
            if(dt >= 1):
                # Tick if enough time passed
                self.tick()
                dt -= 1
            # Render always
            self.render()
        
    def start(self):
        # Init game
        self._running = True
        self.state = GameState.GAME
        self.run()
    
    def stop(self):
        # Stop game
        self._running = False

# Setup main game instance
game = Game()
game.start()