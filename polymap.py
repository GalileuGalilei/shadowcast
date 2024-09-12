from __future__ import annotations
import pygame
from edge import Edge  

class Polymap:
    def __init__(self):
        self.edges = []

    def draw(self, rects : set[pygame.Rect], screen, color):
        for edge in self.edges:
            pygame.draw.line(screen, color, edge.start, edge.end, 2)

    def update(self, rects : set[pygame.Rect]):
        tiles = self.convert_to_tiles(rects)
        self.edges = self.convert_to_polygon(tiles)

    def convert_to_tiles(self, rects, screen_width=800, screen_height=600, tile_size=40) -> set[(int, int)]:
        """
        Convert a set of rectangles to a set of tiles
        """
        tiles = set()

        for rect in rects:
            x, y, w, h = rect

            # Convert top-left and bottom-right corners of the rectangle to tile coordinates
            x1, y1 = x // tile_size, y // tile_size

            tiles.add((x1, y1))

        return tiles



    def convert_to_polygon(self, tiles: set[(int, int)], screen_width=800, screen_height=600, tile_size=40) -> list[Edge]:
        edges = set()

        # Definições das direções das bordas para cada tile (esquerda, direita, cima, baixo)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Função para adicionar ou remover uma borda (escalada para a tela)
        def add_edge(p1, p2):
            # Escalar os pontos para o tamanho da tela
            p1_scaled = (p1[0] * tile_size, p1[1] * tile_size)
            p2_scaled = (p2[0] * tile_size, p2[1] * tile_size)

            edge = Edge(p1_scaled, p2_scaled)
            reverse_edge = Edge(p2_scaled, p1_scaled)
            
            if reverse_edge in edges:
                edges.remove(reverse_edge)  # Se a aresta for compartilhada, removemos
            else:
                edges.add(edge)

        # Para cada tile, verificar as bordas externas
        for tile in tiles:
            x, y = tile
            # Verificar vizinhos em cada uma das quatro direções
            for dx, dy in directions:
                neighbor = (x + dx, y + dy)
                if neighbor not in tiles:
                    # Se não houver um vizinho, essa borda faz parte do contorno
                    if (dx, dy) == (-1, 0):  # Esquerda
                        add_edge((x, y), (x, y + 1))
                    elif (dx, dy) == (1, 0):  # Direita
                        add_edge((x + 1, y), (x + 1, y + 1))
                    elif (dx, dy) == (0, -1):  # Cima
                        add_edge((x, y), (x + 1, y))
                    elif (dx, dy) == (0, 1):  # Baixo
                        add_edge((x, y + 1), (x + 1, y + 1))

        return list(edges)




            



