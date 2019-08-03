#Fruit Tycoon
#The objective in this game is to make as much 
#money as possible by farming trees that drop you fruits.
#Start buy purchasing your first tree to start
#the game.

#Written by Joshua Lee

"""
RESOURCES
http://timefantasy.net/images/trees_2x.png
http://nitrome.wikia.com/wiki/Fruit_(Bad_Ice-Cream)
http://pixeljoint.com/files/icons/full/standoffbg4b.png
https://78.media.tumblr.com/6b1cabe988c3a521bbf8205235aa88f7/tumblr_ornxpa3Cbl1qaja82o1_400.png
http://www.codeskulptor.org/#user16_51xSwE0jKK_0.py
https://dabuttonfactory.com/#t=Upgrade+Fruit&f=Zenhei&ts=18&tc=fff&hp=20&vp=8&c=4&bgt=unicolored&bgc=609fd8&bs=3&bc=569&it=png
https://cooltext.com/Logo-Design-Pixel-Badge

buy button - https://i.imgur.com/wY4WzDv.gif
left  - #3D4F6B
right - #4685B8
"""

import simplegui
import math
import random

CANVAS_WIDTH = 1050
CANVAS_HEIGHT = 650

#loading images
UPGRADE_FRUIT = simplegui.load_image("https://i.imgur.com/ohYnfeM.gif")
UPGRADE_TREE = simplegui.load_image("https://i.imgur.com/h0vUJkt.gif")
PURCHASE_TREE = simplegui.load_image("https://i.imgur.com/ZpcjzyE.gif")
FRUIT_SPRITE = simplegui.load_image("https://i.imgur.com/YDyDioe.png")
APPLE = simplegui.load_image("https://i.imgur.com/XMoH6U6.png")
POMEGRANATE = simplegui.load_image("https://i.imgur.com/OWIqhlo.png")
PEACH = simplegui.load_image("https://i.imgur.com/AvuhPqI.png")
LEMON = simplegui.load_image("https://i.imgur.com/7icEOah.png")
BLUEBERRY = simplegui.load_image("https://i.imgur.com/VbvQQPi.png")
WATERMELON = simplegui.load_image("https://i.imgur.com/82Wrt0q.png")
BANANA = simplegui.load_image("https://i.imgur.com/f0HzSQj.png")
DRAGONFRUIT = simplegui.load_image("https://i.imgur.com/KQSjiEz.png")
CHERRY = simplegui.load_image("https://i.imgur.com/7hpADL2.png")
TREE1 = simplegui.load_image("https://i.imgur.com/ApBvHfm.png")
TREE2 = simplegui.load_image("https://i.imgur.com/bmebP2h.png")
TREE3 = simplegui.load_image("https://i.imgur.com/EgmgrS0.png")
DINO_LEFT = simplegui.load_image("https://i.imgur.com/vB2S4bf.png")
DINO_RIGHT = simplegui.load_image("https://i.imgur.com/UDCC8LD.png")
background = simplegui.load_image("https://i.imgur.com/yRhyQzq.png")
GREY_TRANS = simplegui.load_image("http://inacservices.com/wp-content/uploads/2014/12/grey-transparent.png")
MUSIC_NOTE = simplegui.load_image("https://i.imgur.com/aIUONqb.png")
DINO_SHADOW = simplegui.load_image("https://i.imgur.com/rh7LOYr.png")
BUY_COLLECTOR = simplegui.load_image("https://i.imgur.com/RWVi9Ui.gif")
MUSIC = simplegui.load_sound('http://66.90.93.122/ost/stardew-valley/imjidubl/02%20-%20Cloud%20Country.mp3')
MUSIC.set_volume(0.15)
music_playing = True


while TREE1.get_width() == 0:
    pass
while APPLE.get_width() == 0:
    pass
while UPGRADE_FRUIT.get_width() == 0:
    pass

IMG_SIZES = {TREE1:[104,184], 
             TREE2:[140,200],
             TREE3:[160,208], 
             APPLE:[32,36], 
             POMEGRANATE:[32,34], 
             UPGRADE_FRUIT:[152,30], 
             GREY_TRANS:[2606, 950], 
             UPGRADE_TREE:[146,30], 
             BLUEBERRY:[28,30], 
             DRAGONFRUIT:[24,34], 
             PEACH:[32,32], 
             LEMON:[36,28],
             BANANA:[32,32], 
             CHERRY:[32,34],
             WATERMELON:[36,22],
             FRUIT_SPRITE:((24,24),(384/8, 384/8)),
             DINO_RIGHT:[720,120]}

#Dimensions of collector sprite
DINO_IMG_WIDTH = 720 / 6
DINO_IMG_HEIGHT = 120

FRUIT_VALUES = {APPLE:10, 
                POMEGRANATE:20,
                PEACH:30,
                BANANA:35,
                LEMON:40,
                BLUEBERRY:45, 
                WATERMELON:50,
                CHERRY:55,
                DRAGONFRUIT:200}

#List of all the fruits in order
FRUIT_PROGRESSION = [APPLE,
                     POMEGRANATE,
                     PEACH,
                     BANANA,
                     LEMON,
                     BLUEBERRY, 
                     WATERMELON,
                     CHERRY,
                     DRAGONFRUIT, 
                     ]

money = 0
count = 0 #Number of trees spawned
time = 0
tree_cost = 0
max_fruit_lvl = 3


class Tree:
    
    def __init__(self,
                 fruit,
                 count,
                 level,
                 upgrade,
                 fruit_lvl):
        self.fruit = fruit
        self.count = count
        self.lvl = level
        self.upgrade = upgrade
        self.fruit_lvl = fruit_lvl
        self.fruit_upgrade_cost = (50 + (50 * self.fruit_lvl**2))
        self.upgrade_cost = ((self.upgrade + 1) ** 2)* 100
     
    #Draws the tree
    def spawn_tree(self, canvas):
        canvas.draw_image(self.lvl, 
                      (IMG_SIZES[self.lvl][0]/2, IMG_SIZES[self.lvl][1]/2),
                      (IMG_SIZES[self.lvl][0], IMG_SIZES[self.lvl][1]), 
                      (self.count*200 + 120, 480),
                      (IMG_SIZES[self.lvl][0], IMG_SIZES[self.lvl][1]))
        if self.upgrade >= 3: #Draws bigger trees as you level up
            self.lvl = TREE2
        if self.upgrade >= 6:
            self.lvl = TREE3
            
            
    
    #Appends fruit to fruit list periodically 
    def generate_fruit(self):
        global time 
        global FRUIT_PROGRESSION
            
        if time % (100 -(self.upgrade*100 / (self.upgrade + 1))) == 0:
            x = random.randrange(100 + (200*self.count) , 140 + (200*self.count))
    
            fruit = Fruit(FRUIT_PROGRESSION[self.fruit_lvl], [x, random.randrange(420,470)], -3, 25)
            fruits.append(fruit)
            
    def level_up(self):
        self.upgrade += 1
        self.upgrade_cost = ((self.upgrade + 1) ** 3)* 20
        
    def upgrade_fruit(self):
        self.fruit_lvl += 1
        self.fruit_upgrade_cost = (50 + (5 * self.fruit_lvl**4))


class Fruit:
    
    def __init__(self,
                 species,
                 position,
                 velocity,
                 radius):
        self.species = species
        self.pos = position
        self.vel = velocity
        self.rad = radius


    def draw(self, canvas):
        center_x = IMG_SIZES[self.species][0]/2
        center_y = IMG_SIZES[self.species][1]/2
        canvas.draw_image(self.species,
                          [center_x,center_y],
                          IMG_SIZES[self.species],
                          self.pos,
                          (IMG_SIZES[self.species][0] + 17,IMG_SIZES[self.species][1] + 17))

    #Makes fruits fall and stop at the ground
    def update(self, canvas):
        for i in range(2):
            self.pos[1] += self.vel
            self.vel +=0.2
        if self.pos[1] > 560:
            self.pos[1] = 560
            self.vel *= -0.3
    
    def is_clicked(self, click_pos):
        
        in_x = abs(click_pos[0] - self.pos[0]) < self.rad
        in_y = abs(click_pos[1] - self.pos[1]) < self.rad

        return in_x and in_y
    
    #Checks for collisions of fruits with collector
    def dino_collision(self):
        
        for dino in dinos:
            in_x = abs(dino.pos[0] - self.pos[0]) < self.rad
            in_y = abs(dino.pos[1] - self.pos[1]) < self.rad
            if in_x and in_y:
                self.generate_money()
                fruits.remove(self)

    def generate_money(self):
        global money
        money += FRUIT_VALUES[self.species]

        
#Function to purchase a new tree
def buy_tree(): 
    global money
    global count
    global buttons
    global tree_cost
    global max_fruit_lvl
    tree = Tree(APPLE, count, TREE1, 0, 0)
    trees.append(tree)
    tree_buttons.append(Button(UPGRADE_TREE, IMG_SIZES[UPGRADE_TREE][0], IMG_SIZES[UPGRADE_TREE][1], (120 + count*200, 330), (IMG_SIZES[UPGRADE_TREE][0], IMG_SIZES[UPGRADE_TREE][1]), False, tree))
    fruit_buttons.append(Button(UPGRADE_FRUIT, IMG_SIZES[UPGRADE_FRUIT][0], IMG_SIZES[UPGRADE_FRUIT][1], (120 + count*200, 630), (IMG_SIZES[UPGRADE_FRUIT][0], IMG_SIZES[UPGRADE_FRUIT][1]), False, tree))
    money -= tree_cost
    count += 1
    tree_cost = (250 * (count**3))
    max_fruit_lvl += 1

    
#Collector class 
class Dino:
    
    def __init__(self, image, position, velocity):
        self.image = image
        self.pos = position
        self.vel = velocity
        self.time = 0
        self.direction = "right"
        
    def draw(self, canvas):
        global PLAYER_IMG_WIDTH
        global PLAYER_IMG_HEIGHT
        tile_loc_right = (DINO_IMG_WIDTH/2 + DINO_IMG_WIDTH*int(self.time%6), DINO_IMG_HEIGHT/2)
        tile_loc_left = ((DINO_IMG_WIDTH*6 - DINO_IMG_WIDTH/2) - DINO_IMG_WIDTH*int(self.time%6), DINO_IMG_HEIGHT/2)
        
        canvas.draw_image(DINO_SHADOW, (12,12), (12,24), (self.pos[0], 558), (50,50))
        
        #Flips the image depending on which direction
        #the character is moving
        if self.direction == "right":
            canvas.draw_image(DINO_RIGHT, 
                            tile_loc_right,
                            (DINO_IMG_WIDTH, DINO_IMG_HEIGHT),
                            self.pos,
                            (100,100))
        else:
            canvas.draw_image(DINO_LEFT, 
                            tile_loc_left,
                            (DINO_IMG_WIDTH, DINO_IMG_HEIGHT),
                            self.pos,
                            (100,100))
        
    #Moves character back and forth across the screen
    def update(self):
        self.time += 0.2
        self.time %= 6
       
        if self.direction == "right":
            self.pos[0] += 4   
            if self.pos[0] >= 960:
                self.direction = "left"
        if self.direction == "left":
            self.pos[0] -= 4  
            if self.pos[0] <= 70:
                self.direction = "right"
                
                
class Button:
    
    def __init__(self,
                 image,
                 width,
                 height,
                 position,
                 dimensions,
                 enabled,
                 tree):
        self.image = image
        self.width = width
        self.height = height
        self.pos = position
        self.dim = dimensions
        self.enabled = enabled 
        self.tree = tree
    
    def draw(self, canvas):
        canvas.draw_image(self.image,
                        (self.width/2, self.height/2),
                        (self.width, self.height),
                        (self.pos), 
                        (self.dim))
        if self.enabled == True:
            pass
        else: #shading the image if unclickable
            canvas.draw_image(GREY_TRANS,
                        (self.width/2, self.height/2),
                        (self.width, self.height),
                        (self.pos), 
                        (self.dim))
    
    def is_clicked(self, click_pos):
        
        in_x = abs(click_pos[0] - self.pos[0]) < self.dim[0]/2
        in_y = abs(click_pos[1] - self.pos[1]) < self.dim[1]/2
        
        return in_x and in_y
          
    def upgrade_tree(self):
        self.tree.level_up
    
    def buy_collector(self):
        dinos.append(Dino(DINO_RIGHT, [200, 545], [0, 0]))
                      

# Handler to draw on canvas
def draw(canvas):
    global count
    global time
    global money
    canvas.draw_image(background, 
                      (960 / 2, 480 / 2), (960, 480), (CANVAS_WIDTH/2, 700/2), 
                      (1400, 700))
    
    canvas.draw_text("Money: " + "$" + str(money), (30, 80), 70, 'WHITE', 'sans-serif')
    if count < 5:
        canvas.draw_text("$" + str(tree_cost), (280, 145), 50, 'WHITE', 'monospace')
    else:
        canvas.draw_text("Max", (280, 145), 50, 'WHITE', 'monospace')

    for tree in trees: #Draws trees and spawning fruit
        tree.spawn_tree(canvas)
        tree.generate_fruit()   
    for fruit in fruits: #Draws the fruit and checks for collisions
        fruit.draw(canvas)
        fruit.update(canvas)
        fruit.dino_collision()    
    for button in buttons:
        button.draw(canvas)
    
    #Draws buttons to upgrade individual trees and the prices for them
    for button in tree_buttons:
        button.draw(canvas)
        canvas.draw_text("$" + str(button.tree.upgrade_cost), (button.tree.count*200 + 67, 380), 45, '#DD2D4A', 'monospace')
        canvas.draw_text("Level " + str(button.tree.upgrade+1), (button.tree.count*200 + 50, 305), 35, '#880D1E', 'monospace')
        if money >= button.tree.upgrade_cost:
            button.enabled = True
        else:
            button.enabled = False
    #Drawing buttons to upgrade individual fruits on trees and the prices for them
    for button in fruit_buttons:
        button.draw(canvas)
        if button.tree.fruit_lvl < max_fruit_lvl:
            canvas.draw_text("$" + str(button.tree.fruit_upgrade_cost), (button.tree.count*200 + 67, 607), 45, '#F26A8D', 'monospace')
        else:
            canvas.draw_text(("Max Level"), (button.tree.count*200 + 48, 607), 30, '#F26A8D', 'monospace')
        if money >= button.tree.fruit_upgrade_cost and button.tree.fruit_lvl < max_fruit_lvl:
            button.enabled = True
        else:
            button.enabled = False
    
    #Disables button if max number of trees reached
    if money >= tree_cost and count < 5:
        buttons[0].enabled = True
    else:
        buttons[0].enabled = False
    
    #Removes button to buy collector if purchased
    if len(buttons) == 3:
        if money >= 4000:
            buttons[2].enabled = True
        else:
            buttons[2].enabled = False
    if len(buttons) == 3:
        canvas.draw_text("$4000", (370, 215), 50, 'WHITE', 'monospace')    
    for dino in dinos:
        dino.draw(canvas)
        dino.update()    
    if music_playing == True:
        MUSIC.play()
    else:
        MUSIC.pause()
        MUSIC.rewind()

    time += 1
    
def mouse_click(mouse_position):
    global money
    global fruit_upgrade_cost
    global count
    global music_playing
    for fruit in fruits:
        if fruit.is_clicked(mouse_position):
            fruit.generate_money()
            fruits.remove(fruit)
        else:
            pass
    for button in buttons: #functions for premade buttons (purchase tree, mute music, purchase collector)
        if money >= tree_cost and button.image == PURCHASE_TREE and button.is_clicked(mouse_position) and count < 5:
            buy_tree()
        if button.image == MUSIC_NOTE and button.is_clicked(mouse_position):
            music_playing = not music_playing
        if money >= 4000 and button.image == BUY_COLLECTOR and button.is_clicked(mouse_position):
            button.buy_collector()
            buttons.remove(button)
            money -= 4000
    for button in tree_buttons: #upgrades tree if clicked
        if money >= button.tree.upgrade_cost and button.is_clicked(mouse_position):
            money -= button.tree.upgrade_cost
            button.tree.level_up()
    for button in fruit_buttons: #upgrades fruit if clicked
        if money >= button.tree.fruit_upgrade_cost and button.is_clicked(mouse_position) and button.tree.fruit_lvl < max_fruit_lvl:
            money -= button.tree.fruit_upgrade_cost
            button.tree.upgrade_fruit()


buttons = [Button(PURCHASE_TREE, 237, 45, (150, 130), (237, 45), False, 0), Button(MUSIC_NOTE, 512, 512, (1000, 50), (70,70), True, 0), Button(BUY_COLLECTOR, 324, 45, (193,200), (324, 45), False, 0)]
dinos = []
tree_buttons = []
fruit_buttons = []
trees = []
fruits = []

frame = simplegui.create_frame("Fruit Tycoon", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_click)

frame.start()
