import socket
import threading

class Server:
    def __init__(self, port: int):
        self.serverIP = self.get_server_ip()
        self.port = port
        self.players = {}

        print(f'Server IP: {self.serverIP}')

        # Initialise server socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.serverIP, self.port))
        except socket.error as e:
            str(e)

        # Start server listening for connections
        self.s.listen()
        print("Waiting for connection, Server Started")

        self.server_loop()
        '''server_thread = threading.Thread(target=self.server_loop, daemon=True)
        server_thread.start()'''

        
    def server_loop(self) -> None:
        while True:
            connection, address = self.s.accept() 
            print(f"Connected to: {address}")

            # Start a new client thread
            client_thread = threading.Thread(target=self.handle_connection, args=(connection,), daemon=True)
            client_thread.start()


    def get_server_ip(self) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        
        except Exception as e:
            print(f"Failed to get local IP: {e}")
            return "127.0.0.1"

    
    def handle_connection(self, connection):
        connection.send(str.encode("Connected"))

        try:
            while True:
                data = connection.recv(1024)
                if not data:
                    print("Disconnected")
                    break

                print(f"Received: {data.decode('utf-8')}")
                self.process_packet(data.decode('utf-8'))
                
                # Send back the locations of all players
                reply = ""
                for playerName, [(x, y), facingRight] in self.players.items():
                    reply += f'{playerName}:({x},{y}):{facingRight}|'

                connection.sendall(str.encode(reply))
        
        except ConnectionResetError:
            print("Connection lost")
        
        finally:
            connection.close()


    def process_packet(self, data: str):
        packets = data.split('|')
        for packet in packets:
            if packet != '':
                playerName, playerPos, facingRight = packet.split(':')

                playerX, playerY = playerPos.strip('()').split(',')
                playerX = int(float(playerX))
                playerY = int(float(playerY))

                self.players[playerName] = [(playerX, playerY), int(facingRight)]


if __name__ == "__main__":
    withinUsServer = Server(5555)