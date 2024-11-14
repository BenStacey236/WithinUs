import pygame
import os

class Player:
    def __init__(self, startX: int, startY: int, colour: str | tuple[int], spriteFolder: str):
        self.__x = startX
        self.__y = startY
        self.__colour = colour
        self.facingRight = True
        
        self.frame_files = os.listdir(spriteFolder)
        self.baseFrame = pygame.image.load(f'{spriteFolder}/BaseFrame.png')
        self.movingFrames = []
        for frame in self.frame_files:
            if frame != 'BaseFrame.png':
                self.movingFrames.append(pygame.image.load(f'{spriteFolder}/{frame}'))
        self.currentImage = self.baseFrame


    def change_colour(self, colour: str | tuple[int]):
        self.__colour = colour


    def get_pos(self):
        return self.__x, self.__y


    def set_pos(self, x: int, y: int):
        self.__x, self.__y = x, y


    def move(self, xChange: int = 0, yChange: int = 0):
        self.__x += xChange
        self.__y += yChange


    def draw(self, surface: pygame.surface, pos: tuple[int]):
        if self.facingRight:
            surface.blit(self.currentImage, (pos[0]-self.currentImage.get_width()/2, pos[1]-self.currentImage.get_height()/2))
        else:
            surface.blit(pygame.transform.flip(self.currentImage, True, False), (pos[0]-self.currentImage.get_width()/2, pos[1]-self.currentImage.get_height()/2))
        #pygame.draw.circle(surface, self.__colour, pos, 10)