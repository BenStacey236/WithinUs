import pygame

from GUI.Map import Map
from Player import Player

pygame.init()

FPS = 60

width, height = 1440, 810
win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("WithinUs")


def draw_window(gameMap:Map):
    win.fill((30, 30, 30))

    gameMap.draw(win)
    currentPlayer.draw(win, (width/2, height/2))
    for player in enemyPlayers:
        player.draw(win, (player.get_pos()[0]-currentPlayer.get_pos()[0]+width/2, -(abs(currentPlayer.get_pos()[1])-abs(player.get_pos()[1]+height/2))))

    pygame.display.update()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    currentPlayer = Player(4344, -1008, 'Blue', 'GUI/Assets/CharacterFrames')

    enemyPlayers = [Player(4344, 1008, 'Red', 'GUI/Assets/CharacterFrames')]

    speed = 8
    
    cameraXOffset = 0
    cameraYOffset = 0

    up = False
    down = False
    left = False
    right = False

    gameMap = Map('GUI/Assets/Backgrounds/TheSkeld/TheSkeldMap.png')

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            # Quits if 'x' is pressed on the window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                # Quits if esc key is pressed
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    quit()
            
            # Handles resizing of window
            if event.type == pygame.VIDEORESIZE:
                cameraXOffset += -(event.size[0] - width)/2
                cameraYOffset += (event.size[1] - height)/2
                width, height = event.size

        # Handle movement
        keys = pygame.key.get_pressed()  # Check all keys' states
        if keys[pygame.K_w]:  # Move up
            currentPlayer.move(yChange=speed)
        if keys[pygame.K_s]:  # Move down
            currentPlayer.move(yChange=-speed)
        if keys[pygame.K_a]:  # Move left
            currentPlayer.move(xChange=-speed)
            currentPlayer.facingRight = False
        if keys[pygame.K_d]:  # Move right
            currentPlayer.move(xChange=speed)
            currentPlayer.facingRight = True

        gameMap.set_offsets(-currentPlayer.get_pos()[0]-cameraXOffset, currentPlayer.get_pos()[1]+cameraYOffset)

        draw_window(gameMap)