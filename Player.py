import pygame
import os

class Player:
    def __init__(self, startX: int, startY: int, colour: str | tuple[int], spriteFolder: str) -> None:
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


    def change_colour(self, colour: str | tuple[int]) -> None:
        self.__colour = colour


    def get_pos(self) -> tuple[int]:
        return (self.__x, self.__y)


    def set_pos(self, x: int, y: int) -> None:
        self.__x, self.__y = x, y

        self.centre = (self.__x, -self.__y)
        self.midTop = (self.__x, self.__y-(self.currentImage.get_height()/2))


    def move(self, xChange: int = 0, yChange: int = 0) -> None:
        self.__x += xChange
        self.__y += yChange

        # Set edge values for collision detection
        self.leftTop = (self.__x-self.currentImage.get_width()/2, -(self.__y+(self.currentImage.get_height()/2)))
        self.midTop = (self.__x, -(self.__y+(self.currentImage.get_height()/2)))
        self.rightTop = (self.__x+self.currentImage.get_width()/2, -(self.__y+(self.currentImage.get_height()/2)))

        self.leftMid = (self.__x-self.currentImage.get_width()/2, -self.__y)
        self.centre = (self.__x, -self.__y)
        self.rightMid = (self.__x+self.currentImage.get_width()/2, -self.__y)

        self.leftBottom = (self.__x-self.currentImage.get_width()/2, -(self.__y-(self.currentImage.get_height()/2)))
        self.midBottom = (self.__x, -(self.__y-(self.currentImage.get_height()/2)))
        self.rightBottom = (self.__x+self.currentImage.get_width()/2, -(self.__y-(self.currentImage.get_height()/2)))


    def draw(self, surface: pygame.surface, pos: tuple[int]) -> None:
        if self.facingRight:
            surface.blit(self.currentImage, (pos[0]-self.currentImage.get_width()/2, pos[1]-self.currentImage.get_height()/2))
        else:
            surface.blit(pygame.transform.flip(self.currentImage, True, False), (pos[0]-self.currentImage.get_width()/2, pos[1]-self.currentImage.get_height()/2))