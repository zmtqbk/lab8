import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Drawing App")
    clock = pygame.time.Clock()

    radius = 5
    mode = 'blue'  # цвет
    draw_mode = 'line'  # режим рисования: line, rect, circle, eraser
    drawing = False
    start_pos = None
    base_layer = pygame.Surface((640, 480))
    base_layer.fill((0, 0, 0))

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held or \
                   event.key == pygame.K_F4 and alt_held or \
                   event.key == pygame.K_ESCAPE:
                    return

                # Смена цвета
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_y:
                    mode = 'yellow'
                elif event.key == pygame.K_w:
                    mode = 'white'

                # Смена режима рисования
                if event.key == pygame.K_F1:
                    draw_mode = 'line'
                elif event.key == pygame.K_F2:
                    draw_mode = 'rect'
                elif event.key == pygame.K_F3:
                    draw_mode = 'circle'
                elif event.key == pygame.K_e:
                    draw_mode = 'eraser'

                # Изменение радиуса кисти
                if event.key == pygame.K_UP:
                    radius = min(100, radius + 1)
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                end_pos = event.pos
                if draw_mode == 'rect':
                    pygame.draw.rect(base_layer, get_color(mode), get_rect(start_pos, end_pos), radius)
                elif draw_mode == 'circle':
                    center = start_pos
                    radius_circ = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(base_layer, get_color(mode), center, radius_circ, radius)
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if draw_mode == 'line':
                    pygame.draw.circle(base_layer, get_color(mode), event.pos, radius)
                elif draw_mode == 'eraser':
                    pygame.draw.circle(base_layer, (0, 0, 0), event.pos, radius)

        screen.blit(base_layer, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    if mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)
    elif mode == 'blue':
        return (0, 0, 255)
    elif mode == 'yellow':
        return (255, 255, 0)
    elif mode == 'white':
        return (255, 255, 255)
    return (255, 255, 255)

def get_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return pygame.Rect(left, top, width, height)

main()
