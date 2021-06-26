'''PONG
requirements
    -Keep track of score
        -if the ball leaves the window, increase opponents score
        -reset game after a point is scored
    -Moving game ball
    -paddles that move up and down
    -make ball bounce off paddle
    -
    
'''
import pygame

class Scoreboard:
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0
    def update_player_1(self):
        self.player_1_score = self.player_1_score + 1
    def update_player_2(self):
        self.player_2_score = self.player_2_score + 1
    def draw_scoreboard(self, screen):
        score_str = f"{self.player_1_score} - {self.player_2_score}"
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render(score_str, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (350, 400)
        screen.blit(text, text_rect)


class GameBall:
    def __init__(self, x, y, radius, x_velocity, y_velocity, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.colour = colour
    def draw_ball(self, screen):
        self.x = self.x + self.x_velocity
        self.y = self.y + self.y_velocity
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
    def bounce_off_paddle(self):
        print("bounce off paddle")
        self.x_velocity = self.x_velocity * -1
    def bounce_off_window(self):
        print("bounce off window")
        self.y_velocity = self.y_velocity * -1

class Paddle:
    def __init__(self, x, y, y_velocity, height, width, colour):
        self.x = x
        self.y = y
        self.y_velocity = y_velocity
        self.height = height
        self.width = width
        self.colour = colour
        self.is_moving_up = False
        self.is_moving_down = False
    def draw_paddle(self, screen):
        if self.is_moving_up:
            self.y -= self.y_velocity
        if self.is_moving_down:
            self.y += self.y_velocity
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))
    def start_move_up(self):
        self.is_moving_up = True
    def start_move_down(self):
        self.is_moving_down = True
    def stop_move_up(self):
        self.is_moving_up = False
    def stop_move_down(self):
        self.is_moving_down = False


     
class GameMaster:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([700, 500])
        self.colour = (255, 255, 255)
        self.scoreboard = Scoreboard()
        self.gameball = GameBall(250, 250, 15, 0.15, 0.15, self.colour)
        # to-do: make similar numbers into variables
        self.left_paddle = Paddle(50, 250, .1, 80, 10, self.colour)
        self.right_paddle = Paddle(650, 250, .1, 80, 10, self.colour)
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                # moving paddles up and down
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.left_paddle.start_move_up()
                    elif event.key == pygame.K_s:
                        self.left_paddle.start_move_down()
                    elif event.key == pygame.K_UP:
                        self.right_paddle.start_move_up()
                    elif event.key == pygame.K_DOWN:
                        self.right_paddle.start_move_down()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.left_paddle.stop_move_up()
                    elif event.key == pygame.K_s:
                        self.left_paddle.stop_move_down()
                    elif event.key == pygame.K_UP:
                        self.right_paddle.stop_move_up()
                    elif event.key == pygame.K_DOWN:
                        self.right_paddle.stop_move_down()
                
                if event.type == pygame.QUIT:
                    running = False


            # make balls bounce off window or paddle
            # This happens regardless of events

            #Bug: sometimes goes through paddle on the right
            if self.gameball.y - self.gameball.radius <= 0 or\
                self.gameball.y + self.gameball.radius >= 500:
                self.gameball.bounce_off_window()
            if self.left_paddle.x + self.left_paddle.width - 5 <= self.gameball.x - self.gameball.radius <= self.left_paddle.x + self.left_paddle.width and\
                self.left_paddle.y < self.gameball.y < self.left_paddle.y + self.left_paddle.height:
                self.gameball.bounce_off_paddle()
            if self.right_paddle.x < self.gameball.x + self.gameball.radius < self.right_paddle.x + 2 and\
                self.right_paddle.y < self.gameball.y < self.right_paddle.y + self.right_paddle.height:
                self.gameball.bounce_off_paddle()
            

            # update score if score happens
            while self.gameball.x - self.gameball.radius <= 0:
                self.scoreboard.update_player_2()
                self.gameball.__init__(250, 250, 15, -0.15, 0.15, self.colour)
                print("score")
            while self.gameball.x - self.gameball.radius >= 700:
                self.scoreboard.update_player_1()
                self.gameball.__init__(250, 250, 15, 0.15, -0.15, self.colour)
                print("score")

            self.screen.fill((0, 0, 0))
            self.left_paddle.draw_paddle(self.screen)
            self.right_paddle.draw_paddle(self.screen)
            self.gameball.draw_ball(self.screen)
            self.scoreboard.draw_scoreboard(self.screen)






            pygame.display.flip()
            




        pygame.quit()





game = GameMaster()
game.run()


    