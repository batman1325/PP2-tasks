import pygame
import sys
from collections import deque
from datetime import datetime
import math

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# STATE
tool = "pencil"

brush_sizes = [2, 5, 10]
brush_index = 1

current_color = (255, 0, 0)
eraser_color = (255, 255, 255)

drawing = False
start_pos = None


# FLOOD FILL
def flood_fill(surface, x, y, new_color):
    w, h = surface.get_size()

    if not (0 <= x < w and 0 <= y < h):
        return

    target = surface.get_at((x, y))[:3]
    if target == new_color:
        return

    queue = deque([(x, y)])

    while queue:
        cx, cy = queue.popleft()

        if surface.get_at((cx, cy))[:3] != target:
            continue

        surface.set_at((cx, cy), new_color)

        for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
            if 0 <= nx < w and 0 <= ny < h:
                queue.append((nx, ny))


# SHAPES
def draw_shape(surface, start, end, tool):
    x1, y1 = start
    x2, y2 = end

    color = current_color

    if tool == "rect":
        pygame.draw.rect(surface, color,
            pygame.Rect(x1, y1, x2-x1, y2-y1), brush_sizes[brush_index])

    elif tool == "square":
        side = min(abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color,
            pygame.Rect(x1, y1, side, side), brush_sizes[brush_index])

    elif tool == "circle":
        r = int(math.hypot(x2-x1, y2-y1))
        pygame.draw.circle(surface, color, start, r, brush_sizes[brush_index])

    elif tool == "triangle":
        pts = [(x1, y2), ((x1+x2)//2, y1), (x2, y2)]
        pygame.draw.polygon(surface, color, pts, brush_sizes[brush_index])

    elif tool == "diamond":
        mx, my = (x1+x2)//2, (y1+y2)//2
        pts = [(mx,y1),(x2,my),(mx,y2),(x1,my)]
        pygame.draw.polygon(surface, color, pts, brush_sizes[brush_index])


# MAIN LOOP
running = True

while running:

    screen.fill((220, 220, 220))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # MOUSE
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "fill":
                flood_fill(canvas, *event.pos, current_color)
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end = event.pos

                if tool in ["rect","square","circle","triangle","diamond"]:
                    draw_shape(canvas, start_pos, end, tool)

                elif tool == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end, brush_sizes[brush_index])

                elif tool == "eraser":
                    pygame.draw.line(canvas, eraser_color, start_pos, end, brush_sizes[brush_index]*2)

            drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil":
                pygame.draw.line(canvas, current_color, start_pos, event.pos, brush_sizes[brush_index])
                start_pos = event.pos

            elif drawing and tool == "eraser":
                pygame.draw.line(canvas, eraser_color, start_pos, event.pos, brush_sizes[brush_index]*2)
                start_pos = event.pos

        # KEYBOARD
        if event.type == pygame.KEYDOWN:

            # tools
            if event.key == pygame.K_p:
                tool = "pencil"
            elif event.key == pygame.K_l:
                tool = "line"
            elif event.key == pygame.K_m:
                tool = "rect"
            elif event.key == pygame.K_q:
                tool = "square"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_t:
                tool = "triangle"
            elif event.key == pygame.K_d:
                tool = "diamond"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_f:
                tool = "fill"

            # colors
            elif event.key == pygame.K_r:
                current_color = (255, 0, 0)
            elif event.key == pygame.K_g:
                current_color = (0, 255, 0)
            elif event.key == pygame.K_b:
                current_color = (0, 0, 255)

            # brush size
            elif event.key == pygame.K_1:
                brush_index = 0
            elif event.key == pygame.K_2:
                brush_index = 1
            elif event.key == pygame.K_3:
                brush_index = 2

            # clear
            elif event.key == pygame.K_x:
                canvas.fill((255, 255, 255))

            # save
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                name = datetime.now().strftime("canvas_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, name)
                print("Saved:", name)

    # PREVIEW
    if drawing and tool in ["rect","square","circle","triangle","diamond"]:
        temp = canvas.copy()
        draw_shape(temp, start_pos, pygame.mouse.get_pos(), tool)
        screen.blit(temp, (0,0))

    if drawing and tool == "line":
        pygame.draw.line(screen, current_color, start_pos, pygame.mouse.get_pos(), brush_sizes[brush_index])

    # UI
    screen.blit(font.render(f"Tool: {tool} | Color RGB | 1/2/3 size | M rect | D diamond | L line | E eraser | T triangle | Q square | C circle |  F fill | X clear", True, (0,0,0)), (10,10))
    pygame.draw.rect(screen, current_color, (10, 40, 40, 40))

    pygame.display.flip()
    clock.tick(60)