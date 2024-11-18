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

    # Drawing barriers (temporary)
    for barrier in gameMap.barriers:
        for i, point in enumerate(barrier.points):
            pygame.draw.line(win, 'Blue', (barrier.points[i-1][0]-currentPlayer.get_pos()[0]+width/2, -(abs(currentPlayer.get_pos()[1])-abs(barrier.points[i-1][1]+height/2))), (point[0]-currentPlayer.get_pos()[0]+width/2, -(abs(currentPlayer.get_pos()[1])-abs(point[1]+height/2))), 2)

    # Drawing mouse clicks (temporary)
    for i, point in enumerate(points):
        pygame.draw.circle(win, 'Red', (point[0]-currentPlayer.get_pos()[0]+width/2, -(abs(currentPlayer.get_pos()[1])-abs(point[1]+height/2))), 4)
        print(f'{i}: ({point[0]},{point[1]})')
    
    # Draw players
    for player in enemyPlayers:
        player.draw(win, (player.get_pos()[0]-currentPlayer.get_pos()[0]+width/2, -(abs(currentPlayer.get_pos()[1])-abs(player.get_pos()[1]+height/2))), 8)

    currentPlayer.draw(win, (width/2, height/2), 8)

    pygame.display.update()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    currentPlayer = Player(4344, -1008, 'Blue', 'GUI/Assets/CharacterFrames')

    enemyPlayers = [Player(4344, 1008, 'Red', 'GUI/Assets/CharacterFrames')]

    speed = 8
    
    cameraXOffset = 0
    cameraYOffset = 0

    points = []

    up = False
    down = False
    left = False
    right = False

    gameMap = Map('GUI/Assets/Backgrounds/TheSkeld/TheSkeldMap.png', 'GUI/Assets/barriers.txt')

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

                if event.key == pygame.K_BACKSPACE:
                    if len(points) != 0:
                        points.pop(-1)

            if event.type == pygame.KEYUP:
                currentPlayer.stop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append((pygame.mouse.get_pos()[0]+currentPlayer.get_pos()[0]-width/2, (abs(currentPlayer.get_pos()[1])+abs(pygame.mouse.get_pos()[1]-height/2))))
            
            # Handles resizing of window
            if event.type == pygame.VIDEORESIZE:
                cameraXOffset += -(event.size[0] - width)/2
                cameraYOffset += (event.size[1] - height)/2
                width, height = event.size

        # Handle movement
        keys = pygame.key.get_pressed()  # Check all keys' states

        if keys[pygame.K_w]:  # Move up
            currentPlayer.move(yChange=speed)
            # Check for collision with barriers
            for barrier in gameMap.barriers:
                if barrier.is_collided(currentPlayer.leftTop) or barrier.is_collided(currentPlayer.midTop) or barrier.is_collided(currentPlayer.rightTop):
                    currentPlayer.move(yChange=-speed)
                    break

        if keys[pygame.K_s]:  # Move down
            currentPlayer.move(yChange=-speed)
            # Check for collision with barriers
            for barrier in gameMap.barriers:
                if barrier.is_collided(currentPlayer.leftBottom) or barrier.is_collided(currentPlayer.midBottom) or barrier.is_collided(currentPlayer.rightBottom):
                    currentPlayer.move(yChange=speed)
                    break

        if keys[pygame.K_a]:  # Move left
            currentPlayer.move(xChange=-speed)
            currentPlayer.facingRight = False
            # Check for collision with barriers
            for barrier in gameMap.barriers:
                if barrier.is_collided(currentPlayer.leftTop) or barrier.is_collided(currentPlayer.leftMid) or barrier.is_collided(currentPlayer.leftBottom):
                    currentPlayer.move(xChange=speed)
                    break

        if keys[pygame.K_d]:  # Move right
            currentPlayer.move(xChange=speed)
            currentPlayer.facingRight = True
            # Check for collision with barriers
            for barrier in gameMap.barriers:
                if barrier.is_collided(currentPlayer.rightTop) or barrier.is_collided(currentPlayer.rightMid) or barrier.is_collided(currentPlayer.rightBottom):
                    currentPlayer.move(xChange=-speed)
                    break

        gameMap.set_offsets(-currentPlayer.get_pos()[0]-cameraXOffset, currentPlayer.get_pos()[1]+cameraYOffset)

        draw_window(gameMap)