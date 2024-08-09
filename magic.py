import pygame
import neat
import time
import os
import random 
import pickle
import visualize
#  the font of init
pygame.font.init()
# define the size of the screen
WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730



# change the picrture to the 2x
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png")))
             ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png")))
             ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

# define the picture of pipe
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

# define the picture of base
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

# define the picture of background
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png"))) 

STAT_FONT=pygame.font.SysFont("comicsans",50)

DRAW_LINES = True
# set the dize of the screen
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# set the title of the game
pygame.display.set_caption("Flappy Bird")

# set for how many genaration
gen=0



class Bird:
    IMGS = BIRD_IMGS
    # the max degree will the picture turn
    MAX_ROTATION = 25 
    # rotation velocity
    ROT_VEL = 20
    # ANIMATION time means how faster of the rotation spin
    ANIMATION_TIME=5
    def __init__(self,x,y):
        #  the x and the y set the initialize various of the bird
        self.x=x
        self.y=y
        #  set the tilt of the birds
        self.tilt=0
        #  this was cauculate how many frames 帧数
        self.tick_count = 0
        #  vel-velocity --speed
        self.vel = 0
        #  the height of the last jump
        self.height = self.y
        # calculate the frames --see the line 28
        self.img_count = 0
        # save the picture for the screen
        self.img = self.IMGS[0]


    def jump(self):
        # set the speed = -10.5
        self.vel = -10.5
        # can calculate the time of the jump
        self.tick_count = 0
        # get the speed 
        self.height = self.y


    def move(self):
        #  add tbe frames
        self.tick_count+=1 
        # the speed calculate 
        # speed * frames the 3 is the speed add 
        # s=ut + 0.5at**2
        d = self.vel * (self.tick_count) + 0.5 * (3) * ( self.tick_count) **2 
        # if move more than 16 pc make that = 16
        if d >=16:
            d=16
        # if move to sky add 2 in the spped
        if d<0:
            d -= 2
        # update the place on the y
        self.y=self.y+d
        # if the high didnt get the heigh+50 turn the templtes to the 25 to show the up fly
        if d < 0 or self.y<self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
             # if the high didnt get the -90 turn the templtes to the -20 to show the down fly
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL


    def draw(self,win):
        # for rach frames change one picture
        self.img_count +=1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            # reset the count and will for a loop for the 5 frames each pictures
            self.img_count = 0
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotate the picture (the picture,how many angles you want rotate)
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        #  make the rotation picture to the place in the picture  set they place for the topleft
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        #  draw the pciture to the old place
        win.blit(rotated_image, new_rect.topleft)


    def get_mask(self):
        # return the mask of the picture and can check is that touch the mask
        # mask-- set a place of the object and can check crash
        return pygame.mask.from_surface(self.img)
    

class Pipe:
    # was the distance between two Pipe
    GAP=200
    # was the velitation--speed  of the Pipe move for 5 fremes- maybe
    VEL=5


    def __init__(self,x):
        # the x of the picture
        self.x=x
        #  set the height of the pipe
        self.height = 0
        # set the top ad bottom place
        self.top=0
        self.bottom=0
        # reserve the picture (picture,Horizontal,Vertical)
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()  


    def set_height(self):
        self.height = random.randrange(50,450)
        # height get an random and - the picture actually size like actually 500 randomg 100 and the place in the picture is the -400
        self.top = self.height - self.PIPE_TOP.get_height()
        #  bottom_top = 100+200=300 in the place
        self.bottom = self.height + self.GAP


    def move(self):
        #  for each call the move will move to the left
        self.x -= self.VEL


    def draw(self,win):
        # for the top PIPE
        win.blit(self.PIPE_TOP,(self.x,self.top))
        # buttom
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
        

    def collide(self, bird,win):
        # because the line 127 have the bird so can call the method from the class Bird
        # get the mask to check was that have the crash
        bird_mask = bird.get_mask()
        #  this is the why can call the bird method lmao
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # check the distance with the top and bird
        top_offset = (self.x - bird.x, self.top-round(bird.y))
        # check the bottom 
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # check the mask size and the offset was that happend the crash
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if b_point or t_point:
            # happend crash
            return True

        return False
class Base:
    # define the floor
    # speed of the floor
    VEL=5

    # get the width of the picture
    WIDTH = BASE_IMG.get_width()
    IMG=BASE_IMG


    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self):
        # 
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # if first done put it into right
        # because the x1 will -5 to the negative
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
            # same 
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw(self, win):
        #  put the two picture one by one 
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
       
def draw_window(win, birds,pipes,base,score,gen,pipe_ind):
    # set the game begain from the generation1
    if gen == 0:
        gen =1
    # blite the bg file the background to the 0,0 place in the windows
    win.blit(BG_IMG,(0,0))
    # draw each pipe from the pipes
    for pipe in pipes:
        pipe.draw(win)
    # draw the object bird to the windows
    base.draw(win)
    # use loop for each birds
    for bird in birds:
        # see the line 19 
        # this means not draw the line from the birds to the pipe
        if DRAW_LINES:
            try:
                # pygame.line is a method to draw an line(win-windows,(color) from--- to ----)
                pygame.draw.line(win, (255,0,0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), 
                                 (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                
                pygame.draw.line(win, (255,0,0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), 
                                 (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)

    # set the text for the scrore
    text = STAT_FONT.render("Score:" + str(score),1,(255,255,255))
    # blit the windows (what you want bilt,(x place of the window,y place of the windows))
    win.blit(text, (WIN_WIDTH - text.get_width() - 15, 10))
    # write the generate in the screen
    score_label = STAT_FONT.render("Gens: " + str(gen-1), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))
    # write how many birds live
    score_label = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(score_label, (10, 50))
    pygame.display.update()
def eval_genomes(genomes, config):
    #  call the golobal virable 
    global WIN, gen
    win = WIN
    #  i think it was call each this function
    gen +=1
    nets = []
    birds = []
    ge = []


    for genome_id,genome in genomes:
        # set the genomes fitness=0
        genome.fitness = 0
        # creat the neural network connecet with the
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        # add to the list
        nets.append(net)
        # add the birds
        birds.append(Bird(230,350))
        # add the genetics
        ge.append(genome)


    base=Base(FLOOR)
    pipes = [Pipe(700)]
    score=0
    clock = pygame.time.Clock()
    run = True
    # if the run and the birds numbers >0


    while run and len(birds)>0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        # focus on the first
        pipe_ind = 0 
        #  if the birds still live
        if len(birds) > 0:
            # and more than i pipe and pass the first one we should care about the second pipe
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
            


        #  for the the birds been enumerate
        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            # give they more fitness and can generate more longtime 
            ge[x].fitness += 0.1

            bird.move()
            # the birds.index(bird) return the place of the bird
            # the pipe_ind is the index of the  and show the result of the x between the bird.y and pipes
            #  the abs is calculate the ||
            #  first arguement is y,second distance x between the bird and pipes third is the bird with the bottom y
            # to determind should they jump
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))


            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()
            # make the background move
            base.move()
            # make the list need remove for the Pipe
            rem = []
            # check should that add pipe
            add_pipe = False

            for pipe in pipes:
                pipe.move()
                for bird in birds:
                    if pipe.collide(bird,win):
                        # if dead reduce the fitness
                        ge[birds.index(bird)].fitness-=1
                        # the pop function is means delect the element and return the list
                        nets.pop(birds.index(bird))
                        ge.pop(birds.index(bird))
                        birds.pop(birds.index(bird))


                # if the pipe leave the screen from the left
                if pipe.x + pipe.PIPE_TOP.get_width()<0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    #  this was define at the init in the pipe so each time call that the passed will bacome false
                    pipe.passed = True
                    add_pipe=True


            if add_pipe:
                score +=1
                for genome in ge:
                    # the generate get the award from the system because alive
                    genome.fitness +=5
                pipes.append(Pipe(WIN_WIDTH))


            for r in rem:
                pipes.remove(r)


            for bird in birds:
                if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                    # remove the birds because more high than the floor or touch the ground
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
            draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)



def run(config_file):
    # defaultgenome=structure of the neural network
    # defaultreproduction=control how to choose and mix the genetics
    # defaultspeciesset= control the virable of the group
    # default stagnation = check the group grow slowly
    #  the config define the all the default setting of the genome
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_file)
    p = neat.Population(config)
    # this will give the reporter to the information
    p.add_reporter(neat.StdOutReporter(True))
    #  reporter the ever generation information
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # open the 50 times for the eval_genomes
    winner = p.run(eval_genomes,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
