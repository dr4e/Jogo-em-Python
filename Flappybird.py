from ast import Global
from turtle import width
import pygame
import os
import random

SCREEN_WID = 500
SCREEN_HEI = 800

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('arial', 50)

IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('Flappybird/imgs', 'pipe.png'))) 
IMG_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('Flappybird/imgs', 'base.png')))
IMG_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('Flappybird/imgs', 'bg.png')))
IMG_BIRDS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('Flappybird/imgs', 'bird1.png'))), 
    pygame.transform.scale2x(pygame.image.load(os.path.join('Flappybird/imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('Flappybird/imgs', 'bird3.png')))
]

class Bird:
    #Rotating Animations
    ROTATING_MAX = 25
    ROTATING_SPEED = 20
    TIME_ANIMATION = 5
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        
        self.time = 0
        self.img_score = 0
        self.image = IMG_BIRDS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        #Calc displacement
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        #Restrict displacement
        if displacement  > 16:
            displacement = 16
        elif displacement < 0:
            displacement -=2

        self.y += displacement

        #Angle of the Bird
        if displacement <0 or self.y < (self.height + 50):
            if self.angle < self.ROTATING_MAX:
                self.angle = self.ROTATING_MAX
        elif self.angle > -90:
            self.angle -= self.ROTATING_SPEED

    def drawing(self, screen):
        #Define image
        self.img_score += 1

        if self.img_score < self.TIME_ANIMATION:
            self.image = IMG_BIRDS[0]
        elif self.img_score < self.TIME_ANIMATION*2:
            self.image = IMG_BIRDS[1]
        elif self.img_score < self.TIME_ANIMATION*3:
            self.image = IMG_BIRDS[2]
        elif self.img_score < self.TIME_ANIMATION*4:
            self.image = IMG_BIRDS[1]
        elif self.img_score < self.TIME_ANIMATION*4 +1:
            self.image = IMG_BIRDS[0]

        self.img_score = 0

        #If bird fall, no wings
        if self.angle <= -80:
            self.image = IMG_BIRDS[1]
            self.img_score = self.TIME_ANIMATION*2

        #Draw Image
        image_rotating = pygame.transform.rotate(self.image, self.angle)
        pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = image_rotating.get_rect(center=pos_center_image)
        screen.blit(image_rotating, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
        
class Pipe:
    PIPE_DISTANCE = 230
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.hight = 0
        self.pos_top = 0 
        self.pos_bot = 0
        self.PIPE_BOT = IMG_PIPE
        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)
        self.birdpass = False
        self.define_height()

    def define_height(self):
        #Define Random Pipe
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.PIPE_TOP.get_height()
        self.pos_bot = self.height + self.PIPE_DISTANCE

    def move(self):
        self.x -= self.SPEED

    def drawing(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.pos_top))
        screen.blit(self.PIPE_TOP, (self.x, self.pos_bot))

    def collide(self, bird):
        #Get Masks
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bot_mask = pygame.mask.from_surface(self.PIPE_BOT)

        #Calc Distance
        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_bot = (self.x - bird.x, self.pos_bot - round(bird.y))

        #Verify Collide
        top_point = bird_mask.overlap(top_mask, distance_top)
        bot_point = bird_mask.overlap(bot_mask, distance_bot)

        if top_point or bot_point:
            return True
        else:
            return False

class Floor:
    SPEED = 5
    WIDTH = IMG_FLOOR.get_width()
    
    def __init__(self, y):
        #x0 First Floor; x1 Second Floor
        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH #self.x0 (0) + self.WIDTH

    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        if self.x0 + self.WIDTH < 0:
            self.x0 = SCREEN_WID

        if self.x1 + self.WIDTH < 0:
            self.x1 = SCREEN_WID

    def drawing(self, screen):
        screen.blit(IMG_FLOOR, (self.x0, self.y))
        screen.blit(IMG_FLOOR, (self.x1, self.y))

def drawing_at_screen(screen, birds, pipes, floor, points):
    screen.blit(IMG_BG, (0, 0))

    for bird in birds:
        bird.drawing(screen)

    for pipe in pipes:
        pipe.drawing(screen)

    text = FONT_POINTS.render(f"Points: {points}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WID - 10 - text.get_width(), 10))

    floor.drawing(screen)

    pygame.display.update()

def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WID, SCREEN_HEI))
    points = 0
    clock = pygame.time.Clock()

    running_game = True
    while running_game:
        clock.tick(30)

        #Interact with the user
        for  event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game: False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        #Move all
        for bird in birds:
            bird.move()
        floor.move()
        
        #Move and Remove Pipe
        add_pipe = False
        remove_pipe = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                    running_game = False
                
                if not pipe.birdpass and bird.x > pipe.x:
                    pipe.birdpass = True
                    add_pipe = True
            
            pipe.move()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipe.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
        for pipe in remove_pipe:
            pipes.remove(pipe)

        #No Birde if touch sky or floor
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                running_game = False  

        drawing_at_screen(screen, birds, pipes, floor, points)


if __name__ == "__main__":
    main()