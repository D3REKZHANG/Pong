import pygame
from pygame.locals import *
import random
import sys

                                                #C O M P L E T E

pygame.init()
pygame.font.init()

#COLOURS
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
aqua = (0,255,255)
lightaqua = (150,255,255)
green = (0,255,0)
yellow = (255,255,0)

#images
title = pygame.image.load( '2P_Pong title.png' )
paddle = pygame.image.load( 'paddle.png' )
ball_image = pygame.image.load( 'ball.png' )
bg = pygame.transform.scale( pygame.image.load('background.jpg'),(800,500) )

class Ball( pygame.sprite.Sprite ):

    def __init__( self, colour = white, width = 20, height = 20 ):

        super( Ball, self ).__init__()

        self.width = width
        self.height = height
        self.image = pygame.Surface( ( width,height ) )
        self.image.fill( colour )

        self.rect = self.image.get_rect()

        self.rect.x = window_width/2 - width/2
        self.rect.y = window_height/2 - height/2

        self.speed = 4
        self.speed_xy = [0,0]
        self.speed_gain = 0.5
        self.speed_cap = 10
        self.speed_tick = False
        self.speed_save = self.speed

        self.direction = None

        self.right_wall_hit = False
        self.left_wall_hit = False

    def start(self):
        global start

        if ( time >= 3000 and start ):
            a = random.randint( 0,3 )
            if ( a == 0 ):
                self.direction = down_right
            elif ( a == 1 ):
                self.direction = down_left
            elif ( a == 2 ):
                self.direction = up_right
            elif ( a == 3 ):
                self.direction = up_left

            self.speed_xy[0] = self.speed
            self.speed_xy[1] = self.speed
            start = False

    def reset(self):
        global start,time

        start = True

        time = 0

        self.speed = 3
        self.speed_gain = 0.5

        self.rect.x = window_width/2 - self.width/2
        self.rect.y = window_height/2 - self.height/2

    def lock(self):

        self.speed = 0
        self.rect.x = window_width/2 - self.width/2
        self.rect.y = window_height/2 - self.height/2
        self.move_y = 0
        self.move_x = 0

    def speedup(self):
        self.speed_tick = True
        if ( self.speed_tick and self.speed < self.speed_cap ):
            self.speed += self.speed_gain
            self.speed_tick = False

        if( self.speed >= 5 ):
            self.speed_gain = 1

    def reverse(self):

        self.direction[0] = -self.direction[0]
        self.direction[1] = -self.direction[1]

    def bounce(self,surface, angle):

        if ( surface == vertical ):
            if ( angle == '90' ):
                self.direction[0] = -self.direction[0]
        else:
            if ( angle == '90' ):
                self.direction[1] = -self.direction[1]

        if ( angle == 'reverse' ):
            self.reverse()

    def update(self):
        if not ( start ):
            self.speed_xy[0] = self.speed
            self.speed_xy[1] = self.speed
        try:
            self.speed_xy[0] *= self.direction[0]
            self.speed_xy[1] *= self.direction[1]
        except:
            pass
        self.move_x,self.move_y = self.speed_xy
        self.rect.x += self.move_x
        self.rect.y += self.move_y

        if ( self.rect.left <= 0 ):
            self.bounce( vertical, '90' )
            self.left_wall_hit = True
        elif ( self.rect.right >= window_width ):
            self.bounce( vertical, '90' )
            self.right_wall_hit =  True
        else:
            self.right_wall_hit, self.left_wall_hit = False, False

        if ( self.rect.top < 0 ):
            self.bounce( horizontal, '90')
        elif ( self.rect.bottom > window_height ):
            self.bounce( horizontal, '90' )

    def render(self):
        global window
        window.blit( ball_image,(self.rect.x,self.rect.y))

class Player( pygame.sprite.Sprite ):

    def __init__( self, wall, x, y, colour, paddle_type, ball_obj ):

        super( Player, self ).__init__()

        self.ball_obj = ball_obj
        self.player_wall = wall

        self.width,self.height = 20,100

        self.image = pygame.Surface( ( self.width,self.height ) )
        self.image.fill( colour )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = 0
        self.move_y = 0

        self.collision = pygame.sprite.collide_rect( self, self.ball_obj )

        self.speed = 3

        self.points = 0
        self.win = False

    def lock(self):
        self.speed = 0
        self.move_x = 0
        self.move_y = 0

    def reset(self):

        self.speed = 3
        self.points = 0
        self.win = False

    def update(self):

        self.speed = (self.ball_obj.speed - 3) + 4

        self.rect.x += self.move_x
        self.rect.y += self.move_y

        if ( self.rect.y >= window_height ):
            self.rect.y = -self.height
        elif ( self.rect.y <= -self.height ):
            self.rect.y = window_height

        self.collision = pygame.sprite.collide_rect( self.ball_obj, self )

        if not ( start ):
            if ( self.collision ):

                if ( self.ball_obj.rect.y < self.rect.y + self.height/2 and self.ball_obj.direction[1] == -1  ):
                    self.ball_obj.speedup()
                    self.ball_obj.bounce( vertical,'90' )
                elif( self.ball_obj.rect.y < self.rect.y + self.height/2 and self.ball_obj.direction[1] == 1 ):
                    self.ball_obj.speedup()
                    self.ball_obj.reverse()

                elif ( self.ball_obj.rect.y > self.rect.y + self.height/2 and self.ball_obj.direction[1] == -1 ):
                    self.ball_obj.speedup()
                    self.ball_obj.reverse()
                elif (self.ball_obj.rect.y > self.rect.y + self.height/2 and self.ball_obj.direction[1] == 1 ):
                    self.ball_obj.speedup()
                    self.ball_obj.bounce( vertical, '90' )
                else:
                    self.ball_obj.speedup()
                    self.ball_obj.bounce( horizontal, '90' )

        if ( self.player_wall == 'left' ):
            if ( self.ball_obj.right_wall_hit ):
                self.points += 1
                self.ball_obj.reset()
        else:
            if ( self.ball_obj.left_wall_hit ):
                self.points += 1
                self.ball_obj.reset()

        if ( self.points == 10 ):
             self.win = True


def text( text,font,size,color,x,y ):

    font_style = str(font)
    font_size = size

    text_font = pygame.font.SysFont( font_style,font_size )

    message = text_font.render( text, True, color)

    window.blit(message,(x,y))

def button(x,y,w,h,a_hover,a_click,color,lightcolor,image = None):

    global window,ACTION_HOVER,ACTION_CLICK,CLICK

    if image != None:
        window.blit( image, (x,y) )                #Draw the actual button
    else:
        pygame.draw.rect( window, color, (x,y,w,h) )
    mouse = pygame.mouse.get_pos()                 #Get Mouse Position

    if x+h > mouse[0] > x and y+w > mouse[1] > y:  #If mouse position is inside the box
        ACTION_HOVER = a_hover                     #Set action
        pygame.draw.rect( window, lightcolor, (x,y,w,h) )
        if CLICK:
            ACTION_CLICK = a_click                 #If clicked, set click action

    else:
        ACTION_HOVER = None                        #When mouse leaves box, action resolves
        ACTION_CLICK = None

if (__name__ == "__main__"):

    window_width, window_height = 800,500

    window = pygame.display.set_mode( ( window_width, window_height ) )

    pygame.display.set_caption( "ULTIMATE PONG" )

    clock = pygame.time.Clock()
    fps = 60

    TITLE = "title"
    MENU = "menu"
    GAME = "game"
    ENDSCREEN = 'endscreen'

    GAME_MODE = TITLE

    horizontal = "horizontal"
    vertical = "vertical"

    up_left = [ -1,-1 ]
    up_right = [ 1,-1 ]
    down_left = [ -1,1 ]
    down_right = [ 1,1 ]

    ball = Ball()
    p1 = Player( 'left', 5, window_height/2 - 50, blue, vertical, ball ) # Vertical
    p2 = Player( 'right', window_width - 25, window_height/2 -50, green, vertical, ball )


    active_object_list = pygame.sprite.Group()
    ball_list = pygame.sprite.Group()

    active_object_list.add( p1,p2 )
    ball_list.add(ball)

    ACTION_CLICK = None
    ACTION_HOVER = None
    CLICK = False

    start = True
    running = True


    while ( running ):

        while ( GAME_MODE == TITLE ):

            for event in pygame.event.get():

                if ( event.type == pygame.QUIT ):
                    pygame.quit()
                    sys.exit()

                if ( event.type == pygame.KEYDOWN ):
                    if ( event.key == K_SPACE ):
                        GAME_MODE = GAME

            window.blit(title, (0,0))
            pygame.display.update()
            clock.tick( 60 )

        while ( GAME_MODE == GAME ):

            for event in pygame.event.get():

                if ( event.type == pygame.QUIT ):
                    pygame.quit()
                    sys.exit()
                if ( event != None ):
                    if ( event.type == pygame.KEYDOWN ):
                        if ( event.key == K_SPACE ):
                            if ( p1.win or p2.win ):
                                ball.reset()
                                p1.reset()
                                p2.reset()
                                GAME_MODE = TITLE
                            else:
                                pass
                        if ( event.key == K_w ): #p1
                            p1.move_y = -p1.speed
                        elif ( event.key == K_s ):
                            p1.move_y = p1.speed

                        if ( event.key == K_UP ): #p2
                            p2.move_y = -p1.speed
                        elif ( event.key == K_DOWN ):
                            p2.move_y = p1.speed

                    if ( event.type == pygame.KEYUP ):
                        if ( event.key == K_w ): #p1
                            p1.move_y = 0
                        elif ( event.key == K_s ):
                            p1.move_y = 0
                        if ( event.key == K_UP): #p2
                            p2.move_y = 0
                        elif ( event.key == K_DOWN  ):
                            p2.move_y = 0




            p1.update()
            p2.update()

            time = pygame.time.get_ticks()

            ball.start()
            ball.update()

            ball_list.draw( window )
            window.blit( bg, (0,0) )

            if ( p1.points == 10 ):
                text( str( p1.points ) + ' : ' + str( p2.points ), 'impact', 72, white, window_width/2 - 90, 25 )
            else:
                text( str( p1.points ) + ' : ' + str( p2.points ), 'impact', 72, white, window_width/2 - 65, 25 )

            active_object_list.draw( window )
            ball.render()
            window.blit( paddle, (p1.rect.x, p1.rect.y) )
            window.blit( paddle, ( p2.rect.x, p2.rect.y ) )

            if ( p1.win or p2.win ):
                p1.lock()
                p2.lock()
                ball.lock()
                text('Press \'SPACE\' to rematch','impact',50,white, window_width/2 - 240,window_height*0.8)
            else:
                pass

            clock.tick(fps)
            pygame.display.update()

        while ( GAME_MODE == ENDSCREEN ):

            for event in pygame.event.get():

                if ( event.type == pygame.QUIT ):
                    pygame.quit()
                    sys.exit()

                if ( event.type == pygame.KEYDOWN ):
                    if ( event.key == K_SPACE ):
                        GAME_MODE = MENU

                window.fill( black )

                #button( 150,450,100,30,None,'rematch',aqua,lightaqua )

                clock.tick( 60 )
                pygame.display.update()





































