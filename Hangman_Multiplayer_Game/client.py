import socket
import threading
import tkinter as tk
from tkinter import messagebox

class HangmanClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.root = tk.Tk()
        self.root.title("Hangman")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.word_label = tk.Label(self.root, text="", font=("Arial", 24, "bold"))
        self.word_label.pack()

        self.guess_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.guess_label.pack()

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()

        self.letter_entry = tk.Entry(self.input_frame, font=("Arial", 16))
        self.letter_entry.pack(side=tk.LEFT)

        self.guess_button = tk.Button(self.input_frame, text="Guess", font=("Arial", 16),
                                      command=self.send_guess)
        self.guess_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(self.root, text="Quit", font=("Arial", 16),
                                     command=self.quit_game)
        self.quit_button.pack()

    def start(self):
        self.connect_to_server()
        self.receive_game_state()
        self.root.mainloop()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            self.show_error_message("Could not connect to the server.")
            self.root.destroy()

    def receive_game_state(self):
        try:
            player_id = int(self.client_socket.recv(1024).decode())
            word_length = int(self.client_socket.recv(1024).decode())
            self.guesses = ['_'] * word_length
            self.max_guesses = 6

            self.update_word()
            self.update_guesses()

            threading.Thread(target=self.receive_updates).start()

        except ConnectionError:
            self.show_error_message("Server disconnected.")
            self.root.destroy()

    def receive_updates(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if data == "win":
                    self.show_message("Congratulations! You won the game.")
                    break
                elif data == "lose":
                    self.show_message("Game over! You lost the game.")
                    break
                elif data == "invalid":
                    self.show_message("Invalid guess. Please enter a single letter.")
                elif data == "repeat":
                    self.show_message("You already guessed that letter. Try another one.")
                else:
                    self.max_guesses = int(data)
                    self.guesses = self.client_socket.recv(1024).decode()
                    self.update_word()
                    self.update_guesses()
        except ConnectionError:
            self.show_error_message("Server disconnected.")
            self.root.destroy()

    def send_guess(self):
        guess = self.letter_entry.get()
        self.letter_entry.delete(0, tk.END)
        self.client_socket.send(guess.encode())

    def update_word(self):
        self.word_label.config(text=' '.join(self.guesses))

    def update_guesses(self):
        self.guess_label.config(text=f"Guesses left: {self.max_guesses}")

    def show_message(self, message):
        messagebox.showinfo("Hangman", message)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def quit_game(self):
        self.client_socket.sendall(b"quit")
        self.client_socket.close()
        self.root.destroy()

    def on_closing(self):
        self.quit_game()

if __name__ == '__main__':
    client = HangmanClient('localhost', 5555)
    client.start()
