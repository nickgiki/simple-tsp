import numpy as np
from itertools import permutations
from math import factorial
from datetime import datetime


def dist(x1, y1, x2, y2):
    """Euclidian distance"""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def measure_hamiltonian(path, dist_dict):
    """Measures length of hamiltonian path using a distance dictionary"""
    d = 0
    for i, node in enumerate(path[:-1]):
        nodes = tuple(sorted([path[i], path[i + 1]]))
        d += dist_dict[nodes]
    nodes = tuple(sorted([path[-1], path[0]]))
    d += dist_dict[nodes]
    return d


def node_permutations(vector: list, max_iter: int):
    """Yields all permutations of size 'size' if size < max_iter else max_iter random ones"""
    if factorial(len(vector)) > max_iter:
        i = 0
        while True:
            perm = np.random.permutation(vector)
            if list(perm) != list(vector):
                i += 1
                yield perm
            if i >= max_iter:
                break
    else:
        for perm in permutations(vector):
            if list(perm) != list(vector):
                yield perm


class TSPSolver:
    """Class that solves the TSP problem using the LNS algorithm"""

    def __init__(self, distance_dict: dict):
        """Initialization using a distance dictionary"""
        self.n_cities = len({x[0] for x in distance_dict.keys()})
        self.distance_dict = distance_dict
        self.curr_x = np.array(
            [0] + np.random.permutation(range(1, self.n_cities)).tolist()
        )
        self.best_x = self.curr_x.copy()
        self.curr_y = measure_hamiltonian(self.curr_x, self.distance_dict)
        self.best_y = self.curr_y
        self.best_sol_log = []
        self.all_sol_log = []

    def log_best(self):
        self.best_sol_log += [
            {
                "t": str(datetime.now()),
                "x": self.best_x,
                "y": self.best_y,
                "n": self.neighboors,
            }
        ]

    def calc(self, verbose=True):
        """Evaluation of current solution"""
        self.curr_y = measure_hamiltonian(self.curr_x, self.distance_dict)
        if self.curr_y < self.best_y:
            if verbose:
                print(
                    f"New best: {round(self.curr_y, 2)} - New solution: {self.curr_x.tolist()}"
                )
            self.best_x = self.curr_x.copy()
            self.best_y = self.curr_y
            self.log_best()

    def destroy_and_repair(self, size: int, max_iter: int = 1000):
        """Implements the destroy and repair algorithm"""
        self.neighboors = np.random.choice(
            range(1, self.n_cities), size=size, replace=False
        )
        original_vals = self.curr_x[self.neighboors]
        for perm in node_permutations(original_vals, max_iter):
            for i, j in enumerate(self.neighboors):
                self.curr_x[j] = perm[i]
            self.calc()
            self.curr_x, self.curr_y = self.best_x.copy(), self.best_y
            self.n_iter += 1

    def lns(self, rounds=10, neighborhood_size=3):
        """Implements the LNS algorithm"""
        if not hasattr(self, "n_iter"):
            self.n_iter = 0
        for i in range(rounds):
            self.destroy_and_repair(size=neighborhood_size)
