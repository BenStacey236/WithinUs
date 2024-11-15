import pygame


class Map:
    def __init__(self, imagePath:str) -> None:
        try:
            self.image = pygame.image.load(imagePath)
        except:
            raise Exception("Error opening background image")
        
        self.__xOffset = 0
        self.__yOffset = 0


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
    
