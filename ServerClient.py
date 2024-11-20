import socket


class Client():
    def __init__(self, serverIP: str, port: int) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = serverIP
        self.port = port
        self.address = (self.serverIP, self.port)
        self.playerNum = self.connect()
        print(self.playerNum)

        self.players = {}


    def connect(self) -> str:
        try:
            self.client.connect(self.address)
            return self.client.recv(1024).decode('utf-8')

        except Exception as e:
            print(e)


    def process_packet(self, data: str):
        players = data.split('|')
        
        for player in players:
            if len(player) != 0:
                playerName, playerPos, facingRight, isMoving = player.split(':')

                playerX, playerY = playerPos.strip('()').split(',')
                playerX = int(float(playerX))
                playerY = int(float(playerY))
                
                if facingRight == '1':
                    facingRight = True
                else:
                    facingRight = False

                if isMoving == '1':
                    isMoving = True
                else:
                    isMoving = False

                self.players[playerName] = [(playerX, playerY), facingRight, isMoving]

    
    def send_pos(self, playerName:str, pos: tuple[int, int], facingRight: bool, isMoving):
        try:
            x, y = pos
            self.client.send(str.encode(f'{playerName}:({x},{y}):{1 if facingRight else 0}:{1 if isMoving else 0}|'))
            
            self.process_packet(self.client.recv(1024).decode('utf-8'))
            print(self.players)

        except socket.error as e:
            print(e)


if __name__ == "__main__":
    client = Client("10.3.219.94", 5555)
    print(client.send_pos('Ben', (100, 100)))
    print(client.send_pos('Ella', (200, 200)))
    print(client.send_pos('Ben', (300, 300)))