import sys
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QColor, QPainter, QFont
from PyQt6.QtCore import Qt, QTimer, QCoreApplication
import socket

player_a_score = 0
player_b_score = 0

class Paddle(QGraphicsRectItem):
    def __init__(self, x, y):
        super().__init__(0, 0, 20, 100)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("green")))

    def move_up(self):
        if self.y() > -250:
            self.setPos(self.x(), self.y() - 20)

    def move_down(self):
        if self.y() < 150:
            self.setPos(self.x(), self.y() + 20)

class Ball(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__(0, 0, 20, 20)
        self.setPos(0, 0)
        self.setBrush(QBrush(QColor("red")))
        self.x_direction = 1.5  # Increase the speed
        self.y_direction = 1.5  # Increase the speed


class PongGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.paddle_a = Paddle(-350, 0)
        self.paddle_b = Paddle(330, 0)
        self.ball = Ball()
        self.score_text = None

        self.scene.addItem(self.paddle_a)
        self.scene.addItem(self.paddle_b)
        self.scene.addItem(self.ball)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setWindowTitle("Pong Game")
        self.setFixedSize(800, 600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.paddle_a.setFocus()

        self.show()

        # Set the initial position for the ball
        self.ball.setPos(0, 0)

        # Call update_game() repeatedly
        self.update_game()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_1:
            self.paddle_a.move_up()
        elif event.key() == Qt.Key.Key_2:
            self.paddle_a.move_down()
        elif event.key() == Qt.Key.Key_Up:
            self.paddle_b.move_up()
        elif event.key() == Qt.Key.Key_Down:
            self.paddle_b.move_down()

    def update_game(self):
        global player_a_score, player_b_score  # Use global scores

        # Move the ball
        self.ball.setPos(self.ball.x() + self.ball.x_direction, self.ball.y() + self.ball.y_direction)

        # Check for collisions with the top and bottom walls
        if self.ball.y() > 290 or self.ball.y() < -290:
            self.ball.y_direction *= -1

        # Check for collisions with the paddles
        if self.ball.collidesWithItem(self.paddle_a) or self.ball.collidesWithItem(self.paddle_b):
            self.ball.x_direction *= -1

        # Check for scoring conditions
        if self.ball.x() > 390:
            self.ball.setPos(0, 0)
            self.ball.x_direction *= -1
            player_a_score += 1
            self.update_score()

        if self.ball.x() < -390:
            self.ball.setPos(0, 0)
            self.ball.x_direction *= -1
            player_b_score += 1
            self.update_score()

        # Call update_game() repeatedly
        QTimer.singleShot(10, self.update_game)

    def update_score(self):
        if self.score_text is not None:
            self.scene.removeItem(self.score_text)
        self.score_text = self.scene.addText(f"Player A: {player_a_score}    Player B: {player_b_score}",
                                             font=QFont("Arial", 24))
        self.score_text.setPos(-200, 250)


# ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = PongGame()
    sys.exit(app.exec())


def get_side_choice():
    print("Welcome to the Pong Game!")
    print("Choose your side:")
    print("1. Player A")
    print("2. Player B")

    while True:
        side_choice = input("Enter your choice (1 or 2): ").strip()
        if side_choice in {'1', '2'}:
            return side_choice.upper()
        else:
            print("Invalid choice. Please enter '1' or '2'.")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))

    side = get_side_choice()
    client.sendall(side.encode('utf-8'))

    while True:
        message = input("Enter a message (type 'exit' to quit, 'score' to check scores): ")
        if message.lower() == 'exit':
            break
        elif message.lower() == 'score':
            client.sendall(message.encode('utf-8'))
            response = client.recv(1024)
            print(response.decode('utf-8'))
        else:
            client.sendall(message.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    start_client()
















