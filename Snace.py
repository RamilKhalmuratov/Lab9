import pygame
import random

# Define colors
blue = (50, 153, 213)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

# Screen size and snake block size
dis_width = 600
dis_height = 400
snake_block = 10

# Display and font
display = pygame.display.set_mode((dis_width, dis_height))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("bahnschrift", 20)

def message(msg, color, x, y):
    text = font.render(msg, True, color)
    display.blit(text, [x, y])

# Function to generate a random food position and type
def random_food_position(snake_list):
    while True:
        food_x = random.randrange(0, dis_width - snake_block, snake_block)
        food_y = random.randrange(0, dis_height - snake_block, snake_block)
        if [food_x, food_y] not in snake_list:
            weight = random.choice([(red, 1), (green, 2), (yellow, 3)]) 
            return food_x, food_y, weight

# Main game function
def main():
    game_over = False
    x1, y1 = dis_width / 2, dis_height / 2
    x1_change, y1_change = 0, 0
    snake_list = []
    snake_length = 1
    food_x, food_y, food_type = random_food_position(snake_list)
    score = 0
    level = 1
    speed = 10
    food_timer = 300 # Timer for food disappearance

    while not game_over:
        display.fill(blue)
        message(f"Score: {score}  Level: {level}", white, 10, 10)
        pygame.draw.rect(display, food_type[0], [food_x, food_y, snake_block, snake_block])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -snake_block, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = snake_block, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -snake_block
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, snake_block

        x1 += x1_change
        y1 += y1_change

 # Check if the snake hits the wall
        if x1 < 0 or x1 >= dis_width or y1 < 0 or y1 >= dis_height:
            game_over = True
            break

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
 # Check if the snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True
                break

        for x in snake_list:
            pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

        pygame.display.update()

        # Check if the snake eats the food
        if x1 == food_x and y1 == food_y:
            snake_length += 1
            score += food_type[1]
            food_x, food_y, food_type = random_food_position(snake_list)
            food_timer = 300  
            
            if score % 4 == 0:
                level += 1
                speed += 2

        # Food disappearance timer
        food_timer -= 1
        if food_timer <= 0:
            food_x, food_y, food_type = random_food_position(snake_list)
            food_timer = 300

        clock.tick(speed)
    
    pygame.quit()

main()
