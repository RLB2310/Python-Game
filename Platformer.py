# importing the modules that i will be using #
import pygame, sys, random

# Functions that must be declared before constants #

def get_outline(image, color=(255,255,255), threshold=127):
    mask = pygame.mask.from_surface(image,threshold)
    outline_image = pygame.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0,0,0,0))
    for point in mask.outline():
        outline_image.set_at(point,color)
    return outline_image

# Function to read the map #
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
# setting up pygame and the window #
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init() # initiates pygame
pygame.display.set_caption('Pygame Platformer')
WINDOW_SIZE = (1920,1080)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((465,270))
# Lighting implementation #
fog = pygame.Surface((WINDOW_SIZE))

# Constants and globals #
base_font = pygame.font.Font(None, 30)
jParticles = False
in_air = False
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
true_scroll = [0,0]
direction = 'right'
jump_count = 0
air_done = False
LIGHT_RADIUS = (100 ,100)
alpha = 255
count = 0
screen_shake = 0
particles = []
text_done = False
Dash_last = pygame.time.get_ticks()
Dash_timer = 0

# loading the map path #
game_map = load_map('Assets/map')
game_map1 = load_map('Assets/map1')
# Tile's textures #
grass_img = pygame.image.load('Assets/grass.png')
dirt_img = pygame.image.load('Assets/dirt.png')
wall_img = pygame.image.load('Assets/wall.png')
wall_window_img = pygame.image.load('Assets/wall_window.png')
wall_torch_img = pygame.image.load('Assets/wall_torch.png')

# Loading player images, backgrounds and objects #
background_img = pygame.image.load('Assets/bg.png').convert()
tree_img = pygame.image.load('Assets/tree.png').convert()
player_img = pygame.image.load('Assets/player.png').convert()
pIdle0_img = pygame.image.load('Assets/p_idle0.png').convert()
pIdle1_img = pygame.image.load('Assets/p_idle1.png').convert()
pIdle2_img = pygame.image.load('Assets/p_idle2.png').convert()
pIdle3_img = pygame.image.load('Assets/p_idle3.png').convert()
pIdle4_img = pygame.image.load('Assets/p_idle4.png').convert()
pJump_img = pygame.image.load('Assets/jump.png').convert()
Air_img0 = pygame.image.load('Assets/air1.png').convert_alpha()
light_mask = pygame.image.load('Assets/light_350_med.png').convert_alpha()
gate = pygame.image.load('Assets/gate.png').convert()
Right_img = pygame.image.load('Assets/right.png').convert()
Right1_img = pygame.image.load('Assets/right1.png').convert()
Right2_img = pygame.image.load('Assets/right2.png').convert()
tree_back = tree_img.copy()

# Scaling the images #
background_img = pygame.transform.scale(background_img, (465, 270))
player_img = pygame.transform.scale(player_img, (25, 30))
pIdle0_img = pygame.transform.scale(pIdle0_img, (25, 30))
pIdle1_img = pygame.transform.scale(pIdle1_img, (25, 30))
pIdle2_img = pygame.transform.scale(pIdle2_img, (25, 30))
pIdle3_img = pygame.transform.scale(pIdle3_img, (25, 30))
pIdle4_img = pygame.transform.scale(pIdle4_img, (25, 30))
Right_img = pygame.transform.scale(Right_img, (25, 30))
Right1_img = pygame.transform.scale(Right1_img, (25, 30))
Right2_img = pygame.transform.scale(Right2_img, (25, 30))
pJump_img = pygame.transform.scale(pJump_img, (25, 30))
Air_img0 = pygame.transform.scale(Air_img0, (60, 40))
light_mask = pygame.transform.scale(light_mask, (LIGHT_RADIUS))
tree_back = pygame.transform.scale(tree_back, (100, 150))
light_mask1 = light_mask.copy()
light_mask2 = light_mask.copy()
moon_mask = light_mask.copy()

# Creating a copy of each character sprite for directional movements #
player_img_copy = player_img.copy()
pIdle0_img_copy = pIdle0_img.copy()
pIdle1_img_copy = pIdle1_img.copy()
pIdle2_img_copy = pIdle2_img.copy()
pIdle3_img_copy = pIdle3_img.copy()
pIdle4_img_copy = pIdle4_img.copy()
pJump_img_copy = pJump_img.copy()
Left_img = Right_img.copy()
Left1_img = Right1_img.copy()
Left2_img = Right2_img.copy()

# Flipping each copy of the images #
player_img_copy = pygame.transform.flip(player_img_copy, True, False)
pIdle0_img_copy = pygame.transform.flip(pIdle0_img_copy, True, False)
pIdle1_img_copy = pygame.transform.flip(pIdle1_img_copy, True, False)
pIdle2_img_copy = pygame.transform.flip(pIdle2_img_copy, True, False)
pIdle3_img_copy = pygame.transform.flip(pIdle3_img_copy, True, False)
pIdle4_img_copy = pygame.transform.flip(pIdle4_img_copy, True, False)
pJump_img_copy = pygame.transform.flip(pJump_img_copy, True, False)
Left_img = pygame.transform.flip(Left_img, True, False)
Left1_img = pygame.transform.flip(Left1_img, True, False)
Left2_img = pygame.transform.flip(Left2_img, True, False)

# Settting a white colour key for each image. This will remove outside exccess white pixels that are drawn as a background essentially created a absolute PNG image #
player_img.set_colorkey((255,255,255))
pIdle0_img.set_colorkey((255,255,255))
pIdle1_img.set_colorkey((255,255,255))
pIdle2_img.set_colorkey((255,255,255))
pIdle3_img.set_colorkey((255,255,255))
pIdle4_img.set_colorkey((255,255,255))
pJump_img.set_colorkey((255,255,255))
Right_img.set_colorkey((255,255,255))
Right1_img.set_colorkey((255,255,255))
Right2_img.set_colorkey((255,255,255))
Left_img.set_colorkey((255,255,255))
Left1_img.set_colorkey((255,255,255))
Left2_img.set_colorkey((255,255,255))
player_img_copy.set_colorkey((255,255,255))
pIdle0_img_copy.set_colorkey((255,255,255))
pIdle1_img_copy.set_colorkey((255,255,255))
pIdle2_img_copy.set_colorkey((255,255,255))
pIdle3_img_copy.set_colorkey((255,255,255))
pIdle4_img_copy.set_colorkey((255,255,255))
pJump_img_copy.set_colorkey((255,255,255))
Air_img0.set_colorkey((255,255,255))
gate.set_colorkey((255,255,255))
tree_img.set_colorkey((255,255,255))
tree_back.set_colorkey((255,255,255))
gate_outline = get_outline(gate)

# Getting rectangles. (Most likely for hitboxes)
playerRect = player_img.get_rect()
light_rect = light_mask.get_rect()
light_rect1 = light_rect.copy()
light_rect2 = light_rect.copy()
moon_rect = light_rect.copy()
player_rect = pygame.Rect(300,100,15,29)
pygame.draw.rect(display, (255,255,255), player_rect)



# Animations. Each animation set has an empty list. the images are set as seperate names and used as frames in an animation. They are then appended to the list and an update frame is created which will be compared to a new time to compare to the animation list's cooldown between frames #
#_____________#
# Player Idle #
animation_listIdle = []
Player_Idle_frame_0 = player_img
Player_Idle_frame_1 = pIdle0_img
Player_Idle_frame_2 = pIdle1_img
Player_Idle_frame_3 = pIdle2_img
Player_Idle_frame_4 = pIdle3_img
Player_Idle_frame_5 = pIdle4_img
animation_listIdle.append(Player_Idle_frame_0)
animation_listIdle.append(Player_Idle_frame_1)
animation_listIdle.append(Player_Idle_frame_2)
#animation_listIdle.append(Player_Idle_frame_3)
animation_listIdle.append(Player_Idle_frame_4)
animation_listIdle.append(Player_Idle_frame_5)
last_update = pygame.time.get_ticks()
Player_Idle_animation_cooldown = 190
frame = 0
# Player Idle Flipped #
animation_listIdleFlip = []
Player_Idle_frame_0Flip = player_img_copy
Player_Idle_frame_1Flip = pIdle0_img_copy
Player_Idle_frame_2Flip = pIdle1_img_copy
Player_Idle_frame_3Flip = pIdle2_img_copy
Player_Idle_frame_4Flip = pIdle3_img_copy
Player_Idle_frame_5Flip = pIdle4_img_copy
animation_listIdleFlip.append(Player_Idle_frame_0Flip)
animation_listIdleFlip.append(Player_Idle_frame_1Flip)
animation_listIdleFlip.append(Player_Idle_frame_2Flip)
#animation_listIdleFlip.append(Player_Idle_frame_3Flip)
animation_listIdleFlip.append(Player_Idle_frame_4Flip)
animation_listIdleFlip.append(Player_Idle_frame_5Flip)
last_update = pygame.time.get_ticks()
Player_Idle_animation_cooldown = 190
frame = 0
# Right moving animation
Right_animation_list = []
Right_frame_0 = Right_img
Right_frame_1 = Right1_img
Right_frame_2 = Right2_img
Right_animation_list.append(Right_frame_0)
Right_animation_list.append(Right_frame_1)
Right_animation_list.append(Right_frame_2)
last_update = pygame.time.get_ticks()
Right_animation_cooldown = 175
Right_frame = 0
# Left moving animation
Left_animation_list = []
Left_frame_0 = Left_img
Left_frame_1 = Left1_img
Left_frame_2 = Left2_img
Left_animation_list.append(Left_frame_0)
Left_animation_list.append(Left_frame_1)
Left_animation_list.append(Left_frame_2)
last_update = pygame.time.get_ticks()
Left_animation_cooldown = 175
Left_frame = 0

# Jump Air #
Air_frame_0 = Air_img0

background_trees = [[0.75,[tree_back, random.randint(100, 500), 10]],[0.80,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_img, random.randint(100, 500), 20]],[0.90,[tree_img, random.randint(100, 500), 20]],[1,[tree_img, random.randint(100, 500), 20]],[1,[tree_img, random.randint(100, 500), 20]],[1,[tree_img, random.randint(100, 500), 20]],[1,[tree_img, random.randint(100, 500), 20]],[1,[tree_img, 470, 20]],[1,[tree_img, random.randint(100, 500), 20]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_img, random.randint(100, 500), 20]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_img, random.randint(100, 500), 20]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_img, random.randint(100, 500), 20]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_img, random.randint(100, 500), 20]],[0.90,[tree_back, random.randint(100, 500), 10]],[0.90,[tree_img, random.randint(100, 500), 20]],]
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


# Functions #
#___________#

def textbox(string):
    if '\n' in string:
        new_string, new_string1 = string.split('\n')
    for i in range(len(new_string)):
        text_surface = base_font.render(new_string[i], True, (255, 255, 255))
        screen.blit(text_surface,(750 + (base_font.size(new_string[:i])[0]), 510))
        pygame.display.update()
        clock.tick(30)
    for i in range(len(new_string1)):
        text_surface = base_font.render(new_string1[i], True, (255, 255, 255))
        screen.blit(text_surface,(750 + (base_font.size(new_string1[:i])[0]), 530))
        pygame.display.update()
        clock.tick(30)
    clock.tick(60)


# Creates a function with parameters rect which will be the player's (or enemie's) rect and whill be used to show the current tiles being hit #
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list
# Function used to determine player's movement. A dictionary with a key for each possible tile collision. Each tile side (Top, Bottom, Left and Right) have multiple conditional statements which are used to determine where the character is colliding #
def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
# This function handles each possible event including player movement from up, left and right as well as the time spent in the air, the player's vertical momentum and jump count. Also handles quit events. #
def handle_events(Dash_timer, Player_tileX):
    global moving_left, moving_right, vertical_momentum, jump_count, direction, screen_shake
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                direction = 'right'
                moving_right = True

            if event.key == K_a:
                direction = 'left'
                moving_left = True
            if event.key == K_LSHIFT:
                if Dash_timer == 0:
                    if direction == 'right':
                        player_movement[0] += 48
                        Player_tileX += 3
                    if direction == 'left':
                        player_movement[0] -= 48
                        Player_tileX += 3
                    Dash_timer = 5
            if event.key == K_SPACE:
                if jump_count == 1:
                    if air_timer < 49:
                        vertical_momentum = -4
                        jump_count += 1
                elif jump_count < 1:
                    vertical_momentum = -4
                    jump_count += 1
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
                direction = 'right'
            if event.key == K_a:
                moving_left = False
                direction = 'left'
    return Dash_timer, Player_tileX
# applies a dark fog effect to the screen on a new surface which is blitted onto the main display surface. Creates a light cirle around the player. #
def render_fog():
    fog.fill((40,40,40))
    if direction == 'right':
        light_rect.center = player_rect.x-scroll[0]+21, player_rect.y-scroll[1]+3
        light_particles(display, (player_rect.x-scroll[0]+23, player_rect.y-scroll[1]+7), (255, 164, 0))
    else:
        light_rect.center = player_rect.x-scroll[0]+3, player_rect.y-scroll[1]+3
        light_particles(display, (player_rect.x-scroll[0]+3, player_rect.y-scroll[1]+7), (255, 164, 0))
    light_rect1.center = 360-scroll[0], 95-scroll[1]
    light_rect2.center = 424-scroll[0], 95-scroll[1]
    moon_rect.center = 410, 45
    fog.blit(light_mask, light_rect)
    fog.blit(light_mask1,light_rect1)
    fog.blit(light_mask2, light_rect2)
    fog.blit(moon_mask, moon_rect)
    display.blit(fog, (0,0),  special_flags=pygame.BLEND_MULT)

# A function which is used to  create a flame affect. * This might be turned into a class in the future as a framework for multiple particle implementations #
def light_particles(surf, loc, col):
    # Adding to start of list: [0][0] is the x value, [0][1] is y value, [1][0] is horizontal range of particle spread, [1][1] is the height of particles/speed of vertical momentum, [2] is the time range that a particle may be active. #
    particles.append([[loc[0], loc[1]], [random.randint(5, 15) / 10 - 1, -1], random.randint(0, 5)])
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.01
        pygame.draw.circle(surf, (255, random.randint(80, col[1]), 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)


Pixel_count = 0
Player_tileX = 20
# The main game loop where all objects and events are looped, creating a game #
while True:
    player_movement = [0,0]
    display.blit(background_img, (0,0))
    keys = pygame.key.get_pressed()
    if Pixel_count == 16:
        Player_tileX += 1
        Pixel_count = 0
    if Pixel_count == -16:
        Player_tileX -= 1
        Pixel_count = 0
    true_scroll[0] += (player_rect.x-true_scroll[0]-180)/10
    true_scroll[1] += (player_rect.y-true_scroll[1]-137)/10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    if Player_tileX <= 56:
        Current_map = game_map
    if Player_tileX >= 57:
        Current_map = game_map1
    print(Player_tileX)


# Chooses a random integer for the screen to move. The larger the range, the stronger the screen shake will be #
    if screen_shake:
        scroll[0] += random.randint(0, 7) - 4
        scroll[1] += random.randint(0, 7) - 4
# Creates background

# Call event handler
    Dash_timer, Player_tileX  = handle_events(Dash_timer, Player_tileX)

# Timer for the screen shake #
    if screen_shake > 0:
        screen_shake -= 1
# Creates rectangles in the background in the form of layers. Each layer is moved by a multiplier, the multiplier will be larger or smalle rcreating the illusion of distance #
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)
    for tree in background_trees:
        display.blit(tree[1][0], (tree[1][1]-scroll[0]*tree[0], tree[1][2]-scroll[1]))




    # Movement Conditions #
    tile_rects = []
    y = 0
    for layer in Current_map:
        x = 0
        if Current_map == game_map1:
            x += 38
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'g':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'w':
                display.blit(wall_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'b':
                display.blit(wall_window_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 't':
                display.blit(wall_torch_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0' and tile != 'w':
                tile_rects.append(pygame.Rect(x*16,y*16,10,16))

            x += 1
        y += 1

    # object sprite implementation #
    light_particles(display, (360-scroll[0], 95-scroll[1]),(255, 164, 0))
    light_particles(display, (424-scroll[0], 95-scroll[1]),(255, 164, 0))
    gate_rect = pygame.Rect(358.5-scroll[0]+150, -scroll[1]+69,75,75)
    display.blit(gate,(gate_rect.x-150, gate_rect.y))
    if player_rect.colliderect(gate_rect):
        display.blit(gate_outline,(gate_rect.x-150, gate_rect.y))
        if keys[K_e]:
            if text_done == False:
                textbox(('The door is locked,' '\n' 'It needs a key...'))
                text_done = True
    else:
        text_done = False






# Individual blits for each direction and jump #
    if moving_right == True:
        player_movement[0] += 2.5
        Pixel_count += 2
        if moving_left == False:
            direction = 'right'
        if in_air == False:
            if direction == 'right':
                current_time = pygame.time.get_ticks()
                # Right moving animation
                if current_time - last_update >= Right_animation_cooldown:
                        Right_frame += 1
                        last_update = current_time
                        if Right_frame >= len(Right_animation_list):
                            Right_frame = 0
                display.blit(Right_animation_list[Right_frame], (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    if moving_left == True:
        player_movement[0] -= 2
        Pixel_count -= 2
        if moving_right == False:
            direction = 'left'
        if in_air == False:
            if direction == 'left':
                current_time = pygame.time.get_ticks()
                # Left moving animation
                if current_time - last_update >= Left_animation_cooldown:
                        Left_frame += 1
                        last_update = current_time
                        if Left_frame >= len(Left_animation_list):
                            Left_frame = 0
                display.blit(Left_animation_list[Left_frame], (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if air_timer > 5:
        if direction == 'right':
            display.blit(pJump_img, (player_rect.x-scroll[0], player_rect.y-scroll[1]))
        if direction == 'left':
            display.blit(pJump_img_copy, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

        in_air = True
    elif air_timer <= 5:
        in_air = False
    


# cloud image under character #
    if jump_count == 2:
        if air_done == False:
            if air_timer >= 6:
                display.blit(Air_frame_0,(player_rect.x-scroll[0]-20, player_rect.y-scroll[1]+15 + player_movement[1]*3))
                Air_frame_0.set_alpha(alpha)
                alpha -= 15
                count += 1
                if count == 30:
                    air_done = True
                    alpha = 255
                    count = 0

    player_rect,collisions = move(player_rect,player_movement,tile_rects)
# conditional statements for each collision. includes unique effects for each such as screen shake when dropping from large height #
    if collisions['bottom'] == True:
        if air_timer > 60:
            screen_shake = 5
        air_timer = 0
        vertical_momentum = 0
        jump_count = 0
        air_done = False


    elif collisions['top'] == True:
        vertical_momentum += 1
        jump_count = 2
    else:
        air_timer += 1

    
# Character idle animation #
    if in_air == False:
        current_time = pygame.time.get_ticks()
        if moving_left == False:
            if moving_right == False:
                if direction == 'right':
                    if current_time - last_update >= Player_Idle_animation_cooldown:
                        frame += 1
                        last_update = current_time
                        if frame >= len(animation_listIdle):
                            frame = 0
                    display.blit(animation_listIdle[frame], (player_rect.x-scroll[0], player_rect.y-scroll[1]))
                elif direction == 'left':
                    if current_time - last_update >= Player_Idle_animation_cooldown:
                        frame += 1
                        last_update = current_time
                        if frame >= len(animation_listIdleFlip):
                            frame = 0
                    display.blit(animation_listIdleFlip[frame], (player_rect.x-scroll[0], player_rect.y-scroll[1]))
    render_fog()
    if Dash_timer != 0:
        Dash_timer -= 1

# Final checks and display
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
