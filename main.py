import pygame
import sys
from polymap import Polymap
from line_of_sight import LineOfSight

# Inicializando o Pygame
pygame.init()

# Dimensões da janela e grid
screen_width, screen_height = 800, 600
tile_size = 40  # Tamanho dos tiles
n = screen_width // tile_size  # Número de tiles por linha

# Configurando a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tile Grid com Bola Arrastável')

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# Variáveis de controle
tiles = []  # Lista de tiles
ball_radius = 10
ball_pos = [screen_width // 2, screen_height // 2]  # Posição inicial da bola
ball_dragging = False  # Se a bola está sendo arrastada
polymap = Polymap()
visibility_polygon = []

# Função para desenhar o grid
def draw_grid():
    for x in range(0, screen_width, tile_size):
        for y in range(0, screen_height, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Função para adicionar um tile ao clicar
def add_tile(pos):
    x, y = pos
    grid_x = (x // tile_size) * tile_size
    grid_y = (y // tile_size) * tile_size
    tile_rect = pygame.Rect(grid_x, grid_y, tile_size, tile_size)
    if tile_rect not in tiles:
        tiles.append(tile_rect)
    polymap.update(tiles)

# Função para desenhar os tiles
def draw_tiles():
    global tiles
    for tile in tiles:
        pygame.draw.rect(screen, GRAY, tile)

    polymap.draw(tiles, screen, RED)
    visibility_triangles = LineOfSight.build_visibility_triangles(polymap.edges, ball_pos, (screen_width, screen_height))
    if visibility_triangles:
        for triangle in visibility_triangles:
            pygame.draw.polygon(screen, (0, 255, 0), triangle)

        

# Função para desenhar a bola
def draw_ball():
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

def threat_exit(event):
    if event.type == pygame.QUIT:
        event.quit()
        sys.exit()

def threat_mouse(event):
    global ball_dragging, ball_pos

    # Verifica se o mouse foi pressionado
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        # Verifica se clicou na bola
        if (ball_pos[0] - mouse_pos[0]) ** 2 + (ball_pos[1] - mouse_pos[1]) ** 2 <= ball_radius ** 2:
            ball_dragging = True
        else:
            add_tile(mouse_pos)  # Adiciona um tile

    # Verifica se o botão do mouse foi solto
    if event.type == pygame.MOUSEBUTTONUP:
        ball_dragging = False

    # Verifica se o mouse está sendo movido enquanto o botão está pressionado
    if event.type == pygame.MOUSEMOTION and ball_dragging:
        ball_pos = list(event.pos)

    

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        threat_exit(event)
        threat_mouse(event)

    # Desenha o cenário
    screen.fill(BLACK)
    draw_grid()
    draw_tiles()
    draw_ball()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
