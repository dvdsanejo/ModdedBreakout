import pyxel
import math



# Constants for game settings
SCREEN_WIDTH = 240  # Increased screen width
SCREEN_HEIGHT = 160  # Increased screen height
BALL_RADIUS = 2
PADDLE_WIDTH = BALL_RADIUS * 14  # Paddle width
PADDLE_HEIGHT = BALL_RADIUS * 2  # Paddle height
GRAVITY = 0.0064  # Adjust gravity to make the ball accelerate downward after reaching the peak
BALL_SPEED = 1.4  # Initial ball speed
BALL_DAMPING = 0.8  # Damping factor to slow the ball gradually after bouncing
FPS = 120  # Increased FPS for smoother gameplay
LIVES = 3

class ModifiedBreakout:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS, title="Modified Breakout")
        self.reset_game()
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 5
        self.ball_x = self.paddle_x + PADDLE_WIDTH // 2
        self.ball_y = self.paddle_y - BALL_RADIUS
        self.ball_dx = 0
        self.ball_dy = 0
        self.ball_launched = False
        self.angle_indicator = 0
        self.lives = LIVES
        self.game_over = False
        self.all_bricks_cleared = False
        self.trail = []  # To store the trail positions
        self.powerup_active = False  # Flag to indicate if the power-up is active

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # Toggle paddle length power-up with 'C' key
        if pyxel.btnp(pyxel.KEY_C):
            self.powerup_active = not self.powerup_active

        # Adjust paddle width based on power-up state
        current_paddle_width = PADDLE_WIDTH * 1.5 if self.powerup_active else PADDLE_WIDTH

        if not self.ball_launched:
            self.ball_x = self.paddle_x + current_paddle_width // 2
            self.ball_y = self.paddle_y - BALL_RADIUS
            self.angle_indicator = (self.angle_indicator + 2) % 180
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                angle = math.radians(self.angle_indicator)
                self.ball_dx = math.cos(angle) * BALL_SPEED
                self.ball_dy = -math.sin(angle) * BALL_SPEED  # Start with an upward angle
                self.ball_launched = True

        # Smooth paddle movement with drag
        target_x = pyxel.mouse_x - current_paddle_width // 2  # Target position based on the mouse
        self.paddle_x += (target_x - self.paddle_x) * 0.05  # Smoothly move towards the target position

        # Prevent the paddle from moving off the screen
        if self.paddle_x < 0:
            self.paddle_x = 0
        elif self.paddle_x > SCREEN_WIDTH - current_paddle_width:
            self.paddle_x = SCREEN_WIDTH - current_paddle_width

        # Ball movement
        if self.ball_launched:
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy
            self.ball_dy += GRAVITY  # Apply gravity, accelerating the ball downward

            # Add the ball's position to the trail
            self.trail.append((self.ball_x, self.ball_y))
            if len(self.trail) > 20:  # Limit the size of the trail
                self.trail.pop(0)

            # Check if the ball hits the ceiling (just below the ceiling)
            if self.ball_y - BALL_RADIUS <= 0:  # Ball hits the ceiling
                self.ball_y = BALL_RADIUS  # Keep it from going above the ceiling
                self.ball_dy = abs(self.ball_dy) * BALL_DAMPING  # Reverse and slow the upward velocity

            # Collision with walls (left and right)
            if self.ball_x - BALL_RADIUS <= 0 or self.ball_x + BALL_RADIUS >= SCREEN_WIDTH:
                self.ball_dx *= -1

            # Collision with paddle
            if (
                self.paddle_x <= self.ball_x <= self.paddle_x + current_paddle_width
                and self.paddle_y <= self.ball_y + BALL_RADIUS <= self.paddle_y + PADDLE_HEIGHT
            ):
                offset = (self.ball_x - (self.paddle_x + current_paddle_width / 2)) / (current_paddle_width / 2)
                self.ball_dx = offset * 1.5  # Slightly slower ball speed after hitting paddle
                self.ball_dy = -abs(self.ball_dy)

            # Ball out of bounds (falling below the screen)
            if self.ball_y > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives > 0:
                    self.reset_ball()  # Reset the ball
                else:
                    self.game_over = True  # Set the game over condition

    def reset_ball(self):
        # Reset the ball position and speed
        self.ball_launched = False
        self.ball_dx = 0
        self.ball_dy = 0
        self.ball_x = self.paddle_x + PADDLE_WIDTH // 2
        self.ball_y = self.paddle_y - BALL_RADIUS
        self.trail.clear()  # Clear the trail when resetting the ball

    def draw(self):
        pyxel.cls(0)

        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2, "GAME OVER!", 8)
            pyxel.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 10, "Press R to Restart", 7)
            return

        # Draw the trail
        for (tx, ty) in self.trail:
            pyxel.circ(tx, ty, BALL_RADIUS, 12)  # Draw each trail position with a different color

        # Draw paddle
        current_paddle_width = PADDLE_WIDTH * 1.5 if self.powerup_active else PADDLE_WIDTH
        pyxel.rect(self.paddle_x, self.paddle_y, current_paddle_width, PADDLE_HEIGHT, 9)

        # Draw ball
        pyxel.circ(self.ball_x, self.ball_y, BALL_RADIUS, 7)

        # Draw angle indicator
        if not self.ball_launched:
            line_length = 10
            angle = math.radians(self.angle_indicator)
            line_x = self.ball_x + math.cos(angle) * line_length
            line_y = self.ball_y - math.sin(angle) * line_length
            pyxel.line(self.ball_x, self.ball_y, line_x, line_y, 10)

        # Draw lives
        pyxel.text(5, 5, f"Lives: {self.lives}", 7)

if __name__ == "__main__":
    ModifiedBreakout()
