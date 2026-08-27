import pgzrun
import random
import math
from pgzhelper import *

# Setup screen size
WIDTH = 1200
HEIGHT = 600

# Game Sprite
ice_pickup_img = 'ice' 
life_pickup_img = 'life' 
background = Actor('background', (WIDTH/2, HEIGHT/2))
music.play('bg')
music.set_volume(0.2)

player = Actor('p0', (WIDTH/2, HEIGHT/2))
player.fps = 10
player.angle = 0

# List for multiple units
icegolem = []
ices = []
ice_pickups = []
love_list = []
life_pickups = []

# Starting Variables
score = 0
highest_score = 0  
life = 5
ice_holdoff = 0
golem_timeout = 0
key_condition = 0
ice_amount = 100
ice_pickups_timeout = 1
ice_pickups_timeout_duration = 0
life_pickups_timeout = 1
life_pickups_timeout_duration = 0
draw_love = True
no_key_pressed = True
game_over = True
player.x = WIDTH/2
player.y = HEIGHT/2

def draw():
    background.draw()
    if game_over:
        for love in love_list:
            love_list.remove(love)
        for golem in icegolem:
            icegolem.remove(golem)
        for ice in ices:
            ices.remove(ice)
        for pickup in ice_pickups:
            ice_pickups.remove(pickup)
        for life_pickup in life_pickups:
            life_pickups.remove(life_pickup)
        screen.draw.text("The Golem's Wrath", centerx=WIDTH/2, centery=170, color="black", fontsize=60)
        screen.draw.text('Press Enter to start', centerx=WIDTH/2, centery=270, color="black", fontsize=30)
        screen.draw.text('Score: ' + str(score), centerx=WIDTH/2, centery=330, color="black", fontsize=60)
        screen.draw.text('Highest Score: ' + str(highest_score), centerx=WIDTH/2, centery=400, color="black", fontsize=40)
    else: 
        player.draw()

        for love in love_list:
            love.draw()
        for golem in icegolem:
            golem.draw()
        for ice in ices:
            ice.draw()
        for pickup in ice_pickups:
            pickup.draw()
        for life_pickup in life_pickups:
            life_pickup.draw()
        screen.draw.text("Score: " + str(score), (10, 10), color="black")
        screen.draw.text("Life: " + str(life), (10, 30), color="black")
        screen.draw.text("Ice Mana Amount: " + str(ice_amount), (10, 50), color="black")
        screen.draw.text("Highest Score: " + str(highest_score), (10, 70), color="white")


def update():
    global game_over, score, highest_score, life, key_condition, no_key_pressed, draw_love
    global golem_timeout
    global ice_holdoff, ice_amount, ice_pickups_timeout, ice_pickups_timeout_duration
    global life_pickups_timeout, life_pickups_timeout_duration

    if game_over == False:
        if keyboard.left or keyboard.right or keyboard.up or keyboard.down or keyboard.w or keyboard.a or keyboard.s or keyboard.d:
            if key_condition == 0:
                player.images = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
                player.fps = 10
            key_condition = 1 
            no_key_pressed = True
        else:
            if no_key_pressed:
                player.fps = 2
                player.images = ['p8', 'p9']
            no_key_pressed = False
            key_condition = 0

        if keyboard.left or keyboard.a:
            player.x -= 5
            player.angle = 180
            player.flip_y = True

        elif keyboard.right or keyboard.d:
            player.x += 5
            player.angle = 0
            player.flip_y = False

        elif keyboard.up or keyboard.w:
            player.y -= 5
            if player.angle == 180:
                player.flip_y = True
            elif player.angle == 0:
                player.flip_y = False   

        elif keyboard.down or keyboard.s:
            player.y += 5
            if player.angle == 180:
                player.flip_y = True
            elif player.angle == 0:
                player.flip_y = False   
        else:
            if player.angle == 180:
                player.flip_y = True
            elif player.angle == 0:
                player.flip_y = False        

        player.animate()

        # Update ices
        if ice_holdoff == 0 and ice_amount > 0:
            if keyboard.space:
                sounds.ice.set_volume(0.2)
                sounds.ice.play()
                ice = Actor('ice')
                ice.scale = 0.1
                if player.angle == 180:
                    ice.angle = player.angle 
                    ice.x = player.x - 30
                elif player.angle == 0:
                    ice.angle = player.angle
                    ice.x = player.x + 30           
                ice.y = player.y + 10
                ices.append(ice)
                ice_holdoff = 30
                ice_amount -= 1

        elif ice_holdoff > 0:
            ice_holdoff -= 1

        for ice in ices:
            if ice.angle == 0:
                ice.x = ice.x + 20
            elif ice.angle == 180:
                ice.x = ice.x - 20
            
            # Check for collision with icegolem
            for golem in icegolem:
                if ice.colliderect(golem):
                    golem.life -= 1
                    ices.remove(ice)  # Remove the ice
                    if golem.life <= 0:
                        icegolem.remove(golem)  # Remove the golem
                    score += 1
                    break  # Exit the loop after removing the golem to avoid errors

        # Spawn icegolem
        golem_timeout += 1
        if golem_timeout > 100:
            golem = Actor('g0')
            golem.images = ['g0','g1','g2','g3','g4','g5','g6','g7','g8','g9']
            golem.y = random.randint(0, HEIGHT)
            golem.x_random = random.randint(0, 1)
            if golem.x_random == 0:
                golem.x = 0
            elif golem.x_random == 1:
                golem.x = WIDTH
            golem.type = random.randint(0, 1)
            if golem.type == 0:
                golem.life = 3
            elif golem.type == 1:
                golem.life = 1
            golem.fps = 5
            icegolem.append(golem)
            golem_timeout = 0
        
        # Update golem positions
        for golem in icegolem:
            if golem.type == 0:
                golem.scale = 0.4
            elif golem.type == 1:
                golem.scale = 0.3
            golem.animate()
            if golem.x_random == 0:
                golem.flip_x = False
            if golem.x_random == 1:
                golem.flip_x = True
            angle = math.atan2(player.y - golem.y, player.x - golem.x)
            speed = 1
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            golem.x += dx
            golem.y += dy

        # Check for collision with player
        for golem in icegolem:
            if player.colliderect(golem):
                life -= 1
                draw_love = True
                icegolem.remove(golem)
                if life <= 0:
                    game_over = True

        # Update ice pickups
        if ice_pickups_timeout == 0:
            ice_pickups_timeout_duration += 1
        elif ice_pickups_timeout_duration == 0:
            ice_pickups_timeout += 1
        
        for pickup in ice_pickups:

            # Pick up and add ices
            if player.colliderect(pickup):
                ice_amount += 10
                ice_pickups.remove(pickup)     

        # Remove the oldest ice pickup if any exist
        if ice_pickups_timeout_duration > 400:
            if ice_pickups:
                ice_pickups.pop(0)  
            
            ice_pickups_timeout_duration = 0  
            ice_pickups_timeout = 1   

        # Spawn ice pickups
        if ice_pickups_timeout > 300:
            ice_pickup = Actor(ice_pickup_img)
            ice_pickup.scale = 0.1
            ice_pickup.x = random.randint(0, WIDTH)
            ice_pickup.y = random.randint(0, HEIGHT)
            ice_pickups.append(ice_pickup)
            ice_pickups_timeout = 0


        if life_pickups_timeout == 0:
            life_pickups_timeout_duration += 1
        elif life_pickups_timeout_duration == 0:
            life_pickups_timeout += 1
        
        for life_pickup in life_pickups:

            # Pick up and add life
            if player.colliderect(life_pickup):
                if life < 5:
                    life += 1
                    draw_love = True
                life_pickups.remove(life_pickup)     

        # Remove the oldest life pickup if any exist
        if life_pickups_timeout_duration > 400:
            if life_pickups:
                life_pickups.pop(0)  
            life_pickups_timeout_duration = 0  
            life_pickups_timeout = 1 

        # Spawn life pickups
        if life_pickups_timeout > 300:
            life_pickup = Actor(life_pickup_img)
            life_pickup.scale = 0.1
            life_pickup.x = random.randint(0, WIDTH)
            life_pickup.y = random.randint(0, HEIGHT)
            life_pickups.append(life_pickup)
            life_pickups_timeout = 0

        # Draw life program
        if draw_love == True:
            for love in love_list:
                love_list.remove(love)
            if life > 1:
                for i in range(life):
                    love = Actor('life')
                    love.x = 1100 - 50*i
                    love.y = 50
                    love.scale = 0.1
                    love_list.append(love)
            draw_love = False
    else:
        if keyboard.RETURN:
            # Update highest score if the current score is greater
            if score > highest_score:
                highest_score = score

            # Starting Variables
            score = 0
            life = 5
            ice_holdoff = 0
            golem_timeout = 0
            key_condition = 0
            ice_amount = 100
            ice_pickups_timeout = 1
            ice_pickups_timeout_duration = 0
            life_pickups_timeout = 1
            life_pickups_timeout_duration = 0
            draw_love = True
            no_key_pressed = True
            game_over = False
            player.x = WIDTH/2
            player.y = HEIGHT/2

pgzrun.go()
