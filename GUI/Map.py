import pygame

from GUI.Assets.Barrier import Barrier

class Map:
    def __init__(self, imagePath:str, barrierFilePath:str) -> None:
        try:
            self.image = pygame.image.load(imagePath)
        except:
            raise Exception("Error opening background image")
        
        self.barriers = []
        self.load_barriers(barrierFilePath)

        self.__xOffset = 0
        self.__yOffset = 0


    def load_barriers(self, barrierFilePath) -> None:
        try:
            with open(barrierFilePath) as barrierFile:
                lines = barrierFile.readlines()
                reading = False
                barrierPoints = []
                for barrier in lines:
                    if barrier.startswith("#"):
                        reading = False
                        continue

                    elif barrier.startswith('BStart'):
                        reading = True
                        barrierPoints = []

                    elif barrier.startswith('BEnd'):
                        reading = False 
                        if len(barrierPoints) != 0:
                            self.barriers.append(Barrier(barrierPoints))

                    elif reading:
                        x, y = barrier.strip('()\n').split(',')
                        barrierPoints.append((int(float(x)), int(float(y))))

                    else:
                        continue

        except:
            raise Exception("Error loading barrier file")


    def set_offsets(self, x: int, y: int) -> None:
        '''Sets the x and y offsets of the background
        
        :param int x: The new x offset value
        :param int y: The new y offset value'''

        self.__xOffset = x
        self.__yOffset = y


    def draw(self, surface: pygame.surface):
        '''Draws the map to the screen
        
        :param pygame.surface surface: A pygame surface that the background will be drawn to'''

        surface.blit(self.image, (self.__xOffset, self.__yOffset))