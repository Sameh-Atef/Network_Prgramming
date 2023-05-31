import socket
import threading
import random

class HangmanServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []
        self.current_player = 0
        self.words = ["apple", "banana", "carrot", "donkey", "elephant", "flamingo"]
        self.secret_word = ""
        self.guesses = []
        self.max_guesses = 6
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Server started. Waiting for connections...")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Player connected: {address}")
            self.players.append(client_socket)

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        player_id = self.players.index(client_socket)
        client_socket.send(str(player_id).encode())

        if player_id == 0:
            self.secret_word = random.choice(self.words)
            self.guesses = ['_'] * len(self.secret_word)
            client_socket.sendall(str(len(self.secret_word)).encode())
        else:
            client_socket.sendall(str(len(self.guesses)).encode())

        while True:
            try:
                data = client_socket.recv(1024).decode()
                if data == "guess":
                    self.handle_guess(client_socket)
                elif data == "quit":
                    print(f"Player {player_id} quit the game.")
                    self.players.remove(client_socket)
                    client_socket.close()
                    break

            except ConnectionError:
                print(f"Player {player_id} disconnected.")
                self.players.remove(client_socket)
                client_socket.close()
                break

    def handle_guess(self, client_socket):
        player_id = self.players.index(client_socket)

        while True:
            letter = client_socket.recv(1024).decode().lower()
            if len(letter) != 1 or not letter.isalpha():
                client_socket.sendall(b"invalid")
            elif letter in self.guesses:
                client_socket.sendall(b"repeat")
            else:
                break

        with self.lock:
            if letter in self.secret_word:
                for i in range(len(self.secret_word)):
                    if self.secret_word[i] == letter:
                        self.guesses[i] = letter
            else:
                self.max_guesses -= 1

            client_socket.sendall(str(self.max_guesses).encode())
            client_socket.sendall(''.join(self.guesses).encode())

            if '_' not in self.guesses:
                client_socket.sendall(b"win")
                self.reset_game()
            elif self.max_guesses == 0:
                client_socket.sendall(b"lose")
                self.reset_game()

    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.guesses = ['_'] * len(self.secret_word)
        self.max_guesses = 6

        for player in self.players:
            player.sendall(str(len(self.guesses)).encode())

if __name__ == '__main__':
    server = HangmanServer('localhost', 5555)
    server.start()
