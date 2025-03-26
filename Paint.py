'''E  ластик
R  красный
G  зелёный
B  синий
C  круг
T  прямоугольник
F кисть
S квадрат
Y прямоугольный треугольник
Q равносторонний треугольник
H ромб
'''

import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    shape = 'free'
    points = []
    start_pos = None
    drawing = False
    shapes = []
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_c:
                    shape = 'circle'
                elif event.key == pygame.K_t:
                    shape = 'rectangle'
                elif event.key == pygame.K_s:
                    shape = 'square'
                elif event.key == pygame.K_y:
                    shape = 'right_triangle'
                elif event.key == pygame.K_v:
                    shape = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    shape = 'rhombus'
                elif event.key == pygame.K_f:
                    shape = 'free'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos
                    drawing = True
                    if shape == 'free':
                        points.append(start_pos)
                elif event.button == 3:
                    radius = max(1, radius - 1)
                elif event.button == 4:
                    radius = min(200, radius + 1)
                elif event.button == 5:
                    radius = max(1, radius - 1)
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    if start_pos and shape in ['circle', 'rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                        end_pos = pygame.mouse.get_pos()
                        shapes.append((start_pos, end_pos, shape, mode, radius))
                    start_pos = None
            
            if event.type == pygame.MOUSEMOTION and drawing:
                position = event.pos
                if shape == 'free':
                    points.append(position)
                    points = points[-256:]
                elif shape in ['circle', 'rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    end_pos = position
        
        screen.fill((0, 0, 0))
        
        for s in shapes:
            drawShape(screen, *s)
        
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1
        
        if drawing and start_pos and shape in ['circle', 'rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
            end_pos = pygame.mouse.get_pos()
            drawShape(screen, start_pos, end_pos, shape, mode, radius)
        
        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    color = getColor(index, color_mode)
    dx, dy = start[0] - end[0], start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(screen, color, (x, y), width)

def drawShape(screen, start, end, shape, color_mode, width):
    color = getColor(128, color_mode)
    if shape == 'circle':
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        radius = max(abs(end[0] - start[0]) // 2, abs(end[1] - start[1]) // 2)
        pygame.draw.circle(screen, color, center, radius, width)
    elif shape == 'rectangle' or shape == 'square':
        size = min(abs(end[0] - start[0]), abs(end[1] - start[1])) if shape == 'square' else (end[0] - start[0], end[1] - start[1])
        rect = pygame.Rect(start, (size, size) if shape == 'square' else size)
        pygame.draw.rect(screen, color, rect, width)
    elif shape == 'right_triangle':
        pygame.draw.polygon(screen, color, [start, (end[0], start[1]), end], width)
    elif shape == 'equilateral_triangle':
        height = abs(end[1] - start[1])
        pygame.draw.polygon(screen, color, [start, (start[0] + height, start[1]), ((start[0] + height // 2), start[1] - height)], width)
    elif shape == 'rhombus':
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        pygame.draw.polygon(screen, color, [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)], width)

def getColor(index, mode):
    c1, c2 = max(0, min(255, 2 * index - 256)), max(0, min(255, 2 * index))
    if mode == 'blue':
        return (c1, c1, c2)
    elif mode == 'red':
        return (c2, c1, c1)
    elif mode == 'green':
        return (c1, c2, c1)
    elif mode == 'eraser':
        return (0, 0, 0)

main()