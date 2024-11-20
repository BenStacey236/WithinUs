import pygame
import threading

from GUI.Map import Map
from ServerClient import Client
from Player import Player

pygame.init()

FPS = 60

width, height = 1440, 810
win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("WithinUs")


def calc_map_mouse_pos(mousePos: tuple[int, int]) -> tuple[int, int]:
    # Calculate the x position of the mouse
    x = currentPlayer.get_pos()[0] + (mousePos[0] - width/2)

    # Calulate the y position of the mouse
    y = (currentPlayer.get_pos()[1] - (mousePos[1] - height/2))

    return (x, y)


def calc_relative_position(pos: tuple[int, int]) -> tuple[int, int]:
    if currentPlayer.get_pos()[0] * pos[0] > 0:
        x = (pos[0] - currentPlayer.get_pos()[0] + width/2)
    else:
        x = -(currentPlayer.get_pos()[0] - pos[0] - width/2)
    
    # Calulate the y position
    y = (currentPlayer.get_pos()[1] - pos[1] + height/2)

    return (x, y)


def server_loop():
    """Handles communication with the server."""
    while True:
        #try:
        serverConnection.send_pos(currentPlayer.playerName, currentPlayer.get_pos(), currentPlayer.facingRight, currentPlayer.isMoving())

        '''except Exception as e:
            print("Error communicating with server:", e)
            break'''


def draw_window(gameMap:Map):
    win.fill((30, 30, 30))

    gameMap.draw(win)

    # Drawing barriers (temporary)
    for barrier in gameMap.barriers:
        for i, point in enumerate(barrier.points):
            pygame.draw.line(win, 'Blue', calc_relative_position(barrier.points[i-1]), calc_relative_position(point), 2)

    # Drawing mouse clicks (temporary)
    for i, point in enumerate(points):
        pygame.draw.circle(win, 'Red', calc_relative_position(point), 4)
        print(f'{i}: ({point[0]},{point[1]})')
    
    # Draw players
    for player in enemyPlayers:
        player.draw(win, calc_relative_position(player.get_pos()), 8)

    currentPlayer.draw(win, (width/2, height/2), 8)

    pygame.display.update()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    currentPlayer = Player('Ben', 4344, -1000, 'Blue', 'GUI/Assets/CharacterFrames')

    speed = 8
    
    cameraXOffset = 0
    cameraYOffset = 0

    points = []

    gameMap = Map('GUI/Assets/Backgrounds/TheSkeld/TheSkeldMap.png', 'GUI/Assets/theSkeldBarriers.txt')

    serverConnection = Client("10.3.219.203", 5555)
    enemyPlayers = []

    server_loop_thread = threading.Thread(target=server_loop, daemon=True)
    server_loop_thread.start()

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
                #print(currentPlayer.get_pos(), calc_map_mouse_pos(pygame.mouse.get_pos()))
                points.append(calc_map_mouse_pos(pygame.mouse.get_pos()))
            
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

        if (len(enemyPlayers) + 1) != len(serverConnection.players.keys()):
            enemyPlayers = [Player(enemyName, enemyPos[0], enemyPos[1], 'Red', 'GUI/Assets/CharacterFrames') for enemyName, [enemyPos, _, _] in serverConnection.players.items() if enemyName != currentPlayer.playerName]
        else:
            for player in enemyPlayers:
                player.set_pos(serverConnection.players[player.playerName][0])
                player.facingRight = serverConnection.players[player.playerName][1]
                if serverConnection.players[player.playerName][2]:
                    player.move()
                else:
                    player.stop()

        draw_window(gameMap)