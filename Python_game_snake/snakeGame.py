from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "#00FF00"
FOOD_COLOUR = "#FF0000"
BAKGROUND_COLOUR = "#000000"

class Snake:
    def __init__(self) -> None:
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range (0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="string of snake")
            self.squares.append(square)
        
class Food:
    def __init__(self) -> None:
        x = random.randint(0, int((GAME_WIDTH/SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT/SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert new head position
    snake.coordinates.insert(0, (x, y))

    # Create new square for the head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)
    snake.squares.insert(0, square) 

    # Check if snake has eaten the food
    if (x, y) == tuple(food.coordinates):
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()  # Generate new food
    else:
        # Remove the last square of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions with the wall or self
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    # Prevent snake from reversing
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check collision with walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check collision with self
    if (x, y) in snake.coordinates[1:]:
        return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, text="GAME OVER", fill="red", font=('consolas', 70))


window = Tk()
window.title("Snake game")
window.resizable(False, False)

# Handle key presses for direction changes
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BAKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()