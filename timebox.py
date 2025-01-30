import os
import random
import turtle
import time
import math
from popup import show_game_over_dialog

turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("starfield-edited.gif")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)
turtle.title("Space Wars")


turtle.register_shape('galaga.gif')


# Difficulty constants
BASE_SPEED = 1  # Initial speed of enemies
MAX_SPEED = 10  # Maximum speed of enemies
K = 0.01        # Growth rate for logistic function
t0 = 50         # Midpoint of difficulty increase


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

        # if self.xcor() < screen.window_width // 2:
        #     self.setx(screen.window_width // 2)
        #     self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
            (self.xcor() <= (other.xcor() + 20)) and \
            (self.ycor() >= (other.ycor() - 20)) and \
            (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.7, stretch_len=1.3, outline=None)
        self.speed = 5
        self. lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def move_up(self):
        self.setheading(90)
        # self.speed += 1

    def move_down(self):
        self.setheading(270)
        # self.speed -= 1

    # Function to restore the original color
    def restore_color(self):
        self.color("white")

    # Function to temporarily change the color
    def flash_color(self):
        self.color("red")  # Change to the flash color
        turtle.ontimer(self.restore_color, 200)  # Restore color after 300 milliseconds


class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 5
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0
        
    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1
    
    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1
        
        if self.frame > 7:
            self.frame = 0
            self.goto(-1000, -1000)

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"
    
    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)

        # Checking for borders
        if self.xcor() < -290 or self.xcor() > 290 or \
        self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = f"Score: {self.score}"
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    # Game over logic
    def game_over(self):
        # Stop the game and display "Game Over"
        # self.pen.penup()
        # self.pen.goto(0, 0)
        # self.pen.color("red")
        # self.pen.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
        # show_game_over_dialog(self.restart_game, turtle.bye)


        # Prompt user to restart or quit
        # choice = turtle.textinput("Game Over", "Restart? (yes or no): ")
        # if choice and choice.lower() == "yes":
        #     self.restart_game()
        # else:
        #     turtle.bye()

        
    # Prevent multiple popups by ensuring this is called only once
        self.state = "gameover"  # Redundant but ensures state consistency
        elapsed_time = time.time() - start_time
        show_game_over_dialog(self.restart_game, turtle.bye, elapsed_time)

    def restart_game(self):
        # Reset the game state
        self.score = 0
        player.lives = 3
        self.state = "playing"
        self.pen.clear()
        self.draw_border()
        self.show_status()

        game_loop()
        
        # global start_time, game, player, missile, enemies, allies, enemy_particles, ally_particles

        # # Reset the game score and states
        # game.score = 0
        # game.show_status()

        # # Reset player position and lives
        # player.goto(0, 0)
        # player.lives = 3

        # # Reset all enemy and ally positions
        # for enemy in enemies:
        #     x = random.randint(-250, 250)
        #     y = random.randint(-250, 250)
        #     enemy.goto(x, y)

        # for ally in allies:
        #     x = random.randint(-250, 250)
        #     y = random.randint(-250, 250)
        #     ally.goto(x, y)

        # Reset the game timer
        # start_time = time.time()



# Logistic function that gradually increases game difficulty with time
def calculate_speed():
    elapsed_time = time.time() - start_time
    return BASE_SPEED + (MAX_SPEED - BASE_SPEED) / (1 + math.exp(-K * (elapsed_time - t0)))

# Creating game object
game = Game()

# Draw the game border
game.draw_border()

# Game status
game.show_status()

# Creating game sprites
player = Player("turtle", "white", 0, 0)
# enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
# ally = Ally("square", "blue", 100, 0)

enemies = []
allies = []
enemy_particles = []
ally_particles = []

for i in range(5):
    enemies.append(Enemy("circle", "red", -100, 0))

for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

for i in range(20):
    enemy_particles.append(Particle("circle", "orange", 0, 0))

for i in range(20):
    ally_particles.append(Particle("square", "cyan", 0, 0))

# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.move_up, "Up")
turtle.onkey(player.move_down, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

# Capturing start time of game
start_time = time.time()

# Main game loop
def game_loop():
    global start_time  # Ensure the start time is global
    start_time = time.time()

    while game.state == "playing":
        turtle.update()
        time.sleep(0.03)

        player.move()
        missile.move()

        # Adjusting speed of sprites according to time
        current_speed = calculate_speed()

        for enemy in enemies:
            enemy.speed = current_speed
            enemy.move()

            # Collision detection with the player
            if player.is_collision(enemy):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x, y)
                game.score -= 100  # Decreasing game score
                player.lives -= 1  # Decreasing lives
                game.show_status()
                player.flash_color()

                if player.lives <= 0 or game.score <= 0:
                    game.state = "gameover"

            if missile.is_collision(enemy):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x, y)
                missile.status = "ready"
                game.score += 100  # Increasing score
                game.show_status()
                # Explosion
                for particle in enemy_particles:
                    particle.explode(missile.xcor(), missile.ycor())

        # Handle allies
        for ally in allies:
            ally.move()
            if missile.is_collision(ally):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                ally.goto(x, y)
                missile.status = "ready"
                game.score -= 50  # Penalty for hitting an ally
                game.show_status()
                # Explosion
                for particle in ally_particles:
                    particle.explode(missile.xcor(), missile.ycor())

                if player.lives <= 0 or game.score <= 0:
                    game.state = "gameover"
        
        for particle in enemy_particles:
            particle.move()

        for particle in ally_particles:
            particle.move()

    # Exit the game loop and call game over
    if game.state == "gameover":
        game.game_over()

game_loop()



