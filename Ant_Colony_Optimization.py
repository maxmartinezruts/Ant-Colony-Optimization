"""
Author: Max Martinez Ruts
Date: September 2018
Description:

Idea: Path
"""

import pygame
import numpy as np
import random

# Screen parameters
width = 800
height = 800
center = np.array([width/2, height/2])
screen = pygame.display.set_mode((width, height))

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255,255, 0)
fpsClock = pygame.time.Clock()
fps = 400


def cartesian_to_screen(car_pos):
    factor = 0.02
    screen_pos = np.array([center[0] * factor + car_pos[0], center[1] * factor - car_pos[1]]) / factor
    screen_pos = screen_pos.astype(int)
    return screen_pos

# Convert coordinates form screen to cartesian  (used to draw in pygame screen)
def screen_to_cartesian(screen_pos):
    factor = 0.02
    car_pos = np.array([screen_pos[0] - center[0], center[1] - screen_pos[1]]) * factor
    car_pos = car_pos.astype(float)
    return car_pos

class Graph:
    def __init__(self, n, n_ants):
        self.t = 0
        self.n = n
        self.grid = [[None for i in range(n)] for j in range(n)]
        self.nodes = []
        self.edges = []
        self.ants = []
        xs = np.linspace(-7,7,n)
        ys = np.linspace(-7,7,n)
        for i in range(n):
            for j in range(n):
                node = self.Node(np.array([xs[i],ys[j]]))
                self.grid[i][j] = node
                self.nodes.append(node)

        # All possible directions
        near_pos = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for i in range(n):
            for j in range(n):
                for pos in near_pos:
                    i_ = i+pos[0]
                    j_ = j+pos[1]
                    if self.index_is_valid(i_) and self.index_is_valid(j_):
                        # Connect
                        edge = self.Edge(self.grid[i][j], self.grid[i_][j_])
                        self.edges.append(edge)
                        self.grid[i][j].connections.append(edge)


        for _ in range(n_ants):
            self.ants.append(self.Ant(self.grid[0][0]))

    def search(self, d):
        self.d = d
        self.min_dist = np.linalg.norm(self.grid[0][0].pos- d.pos)
        while True:
            self.t += 1

            # if self.t % 100 == 0:

            self.draw()
            for a in self.ants:
                a.navigate(d, self)
            for e in self.edges:
                e.pheromone = min(max(e.pheromone*.9, 0.005),100000)



    def index_is_valid(self, i):
        if 0<=i<self.n:
            return True
        else:
            return False


    class Node:
        def __init__(self, pos):
            self.pos = pos
            self.connections = []

    class Edge:
        def __init__(self, A, B):
            self.nodes = [A,B]
            self.A = A
            self.B = B
            self.pheromone = 1
            self.weight = np.linalg.norm(A.pos-B.pos)

    class Ant:
        def __init__(self, start):
            self.start = start
            self.current = start
            self.trace = []

        def navigate(self, d, g):
            p = []
            for connection in self.current.connections:
                p.append(connection.pheromone + np.random.rand()*0.12)
            p = np.array(p)
            p = p / np.sum(p)
            edge =np.random.choice(self.current.connections, p=p)

            self.current = edge.B
            self.trace.append(edge)

            # If arrived to destiny
            if self.current == d:
                w = self.get_weight()
                self.update_pheromes(w, g)
                self.current = self.start
                self.trace = []


        def update_pheromes(self, w, g):
            for edge in self.trace:
                edge.pheromone += 10/(w-g.min_dist)

        def get_weight(self):
            w = 0
            for edge in self.trace:
                w+= edge.weight
            return w




    def draw(self):
        pygame.event.get()
        screen.fill((0, 0, 0))

        for node in self.nodes:
            pygame.draw.circle(screen, red, cartesian_to_screen(node.pos), 1)



        for edge in self.edges:
            pygame.draw.line(screen, red, cartesian_to_screen(edge.nodes[0].pos),cartesian_to_screen(edge.nodes[1].pos), min(int((edge.pheromone)*5),8))

        for ant in self.ants:
            pygame.draw.circle(screen, green, cartesian_to_screen(ant.current.pos), 5)

        pygame.draw.circle(screen, yellow, cartesian_to_screen(self.d.pos), 9)

        pygame.display.flip()


graph = Graph(20, 1000)

graph.search(graph.grid[15][15])