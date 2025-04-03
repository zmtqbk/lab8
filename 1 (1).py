import pygame
import sys
import math

pygame.init()

WIDTH = 960
HEIGHT = 640

# color palette
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))

done = False

LMBpressed = False
current_shape = "rectangle"  # Initial shape
current_color = colorBLACK  # Initial drawing color
eraser = False  # Initial eraser mode
thickness = 20  # Initial drawing thickness

prevX = 0
prevY = 0

currX = 0
currY = 0

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def calculate_rhombus(x1, y1, x2, y2):
    # Calculate the coordinates of the rhombus vertices
    x_mid = (x1 + x2) // 2
    y_mid = (y1 + y2) // 2

    return [(x1, y_mid), (x_mid, y1), (x2, y_mid), (x_mid, y2)]

def calculate_square(x1, y1, x2, y2):
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    size = min(width, height)
    x2 = x1 + size if x2 > x1 else x1 - size
    y2 = y1 + size if y2 > y1 else y1 - size
    return pygame.Rect(x1, y1, size, size)

def calculate_circle(x1, y1, x2, y2):
    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

def calculate_equilateral_triangle(x1, y1, x2, y2):
    side_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    height = side_length * math.sqrt(3) / 2
    half_side_length = side_length / 2
    return [
        (x1, y1),
        (x2, y1),
        ((x1 + x2) / 2, y1 - height),
        (x1, y1)
    ]

def calculate_right_triangle(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2)]

def draw_shape(x1, y1, x2, y2, shape):
    if shape == "rectangle":
        pygame.draw.rect(screen, current_color, calculate_rect(x1, y1, x2, y2), 2)
    elif shape == "square":
        pygame.draw.rect(screen, current_color, calculate_square(x1, y1, x2, y2), 2)
    elif shape == "rhombus":
        points = calculate_rhombus(x1, y1, x2, y2)
        pygame.draw.polygon(screen, current_color, points, 2)
    elif shape == "circle":
        radius = calculate_circle(x1, y1, x2, y2)
        pygame.draw.circle(screen, current_color, (x1, y1), radius, 2)
    elif shape == "right triangle":
        points = calculate_right_triangle(x1, y1, x2, y2)
        pygame.draw.polygon(screen, current_color, points, 2)
    elif shape == "equilateral triangle":
        points = calculate_equilateral_triangle(x1, y1, x2, y2)
        pygame.draw.polygon(screen, current_color, points, 2)


def draw_palette():
    # Define colors and their positions
    palette_colors = [colorWHITE, colorRED, colorGREEN, colorBLUE, colorYELLOW]
    palette_width = WIDTH // len(palette_colors)
    palette_height = 30
    
    for i, color in enumerate(palette_colors):
        pygame.draw.rect(screen, color, (i * palette_width, HEIGHT - palette_height, palette_width, palette_height))
        pygame.draw.rect(screen, colorBLACK, (i * palette_width, HEIGHT - palette_height, palette_width, palette_height), 2)

def update_color(mouse_x):
    palette_width = WIDTH // 5
    index = mouse_x // palette_width
    if index == 0:
        return colorWHITE
    elif index == 1:
        return colorRED
    elif index == 2:
        return colorGREEN
    elif index == 3:
        return colorBLUE
    elif index == 4:
        return colorYELLOW

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_e: 
                current_color = colorBLACK 
                thickness = 20

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("LMB pressed")
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1]

            # Check if the click is in the palette area
            if event.pos[1] >= HEIGHT - 30:
                current_color = update_color(event.pos[0])

        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
            currX = event.pos[0]
            currY = event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("LMB released")
            LMBpressed = False
            draw_shape(prevX, prevY, currX, currY, current_shape)
            base_layer.blit(screen, (0, 0))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Cycle through shapes
                if current_shape == "rectangle":
                    current_shape = "square"
                elif current_shape == "square":
                    current_shape = "rhombus"
                elif current_shape == "rhombus":
                    current_shape = "circle"
                elif current_shape == "circle":
                    current_shape = "right triangle"
                elif current_shape == "right triangle":
                    current_shape = "equilateral triangle"
                elif current_shape == "equilateral triangle":
                    current_shape = "rectangle"
            elif event.key == pygame.K_e:
                # Toggle eraser mode
                eraser = not eraser

    if LMBpressed:
        screen.blit(base_layer, (0, 0))
        if not eraser:
            draw_shape(prevX, prevY, currX, currY, current_shape)
        else:
            pygame.draw.circle(screen, colorBLACK, (currX, currY), thickness)
            base_layer.blit(screen, (0, 0))
    
    draw_palette()
    pygame.display.flip()