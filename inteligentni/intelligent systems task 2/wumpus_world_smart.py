import sys
from collections import deque

class WumpusWorld:
    def __init__(self, filename):
        self.grid = {}
        self.M = 0
        self.N = 0
        self.agent_pos = (1, 1)
        self.gold = set()
        self.pits = set()
        self.wumpus = None
        self.visited = set()
        self.safe = set()
        self.frontier = set()
        self.read_world("wumpus_world.txt")

    def read_world(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                code = line[0]
                coords = tuple(map(int, list(line[1:])))
                if code == 'M':  # Map size
                    self.M, self.N = coords
                elif code == 'A':  # Agent start
                    self.agent_pos = coords
                    self.safe.add(coords)
                elif code == 'P':  # Pit
                    self.pits.add(coords)
                elif code == 'W':  # Wumpus
                    self.wumpus = coords
                elif code == 'G':  # Gold
                    self.gold.add(coords)

    def in_bounds(self, pos):
        x, y = pos
        return 1 <= x <= self.M and 1 <= y <= self.N

    def adjacent_cells(self, pos):
        x, y = pos
        moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [m for m in moves if self.in_bounds(m)]

    def percepts(self, pos):
        """Return (breeze, stench, glitter) for the given position."""
        breeze = any(adj in self.pits for adj in self.adjacent_cells(pos))
        stench = (self.wumpus in self.adjacent_cells(pos))
        glitter = (pos in self.gold)
        return breeze, stench, glitter

    def mark_safe_from_percepts(self, pos):
        breeze, stench, glitter = self.percepts(pos)
        # If no breeze and no stench, mark all adjacent as safe
        if not breeze and not stench:
            for cell in self.adjacent_cells(pos):
                if cell not in self.visited:
                    self.safe.add(cell)
                    self.frontier.add(cell)

    def move_agent(self):
        self.visited.add(self.agent_pos)
        self.mark_safe_from_percepts(self.agent_pos)

        # Pick up gold if here
        if self.agent_pos in self.gold:
            print(f"💰 Gold collected at {self.agent_pos}!")
            self.gold.remove(self.agent_pos)

        # Choose next move: nearest safe unvisited
        if self.frontier:
            next_cell = self.frontier.pop()
            print(f"➡️ Moving from {self.agent_pos} to {next_cell}")
            self.agent_pos = next_cell
        else:
            print("✅ No more safe moves. Agent will stop.")
            return False
        return True

    def run(self):
        print(f"Starting at {self.agent_pos}")
        while self.move_agent():
            pass
        print("🏁 Exploration ended.")


if __name__ == "__main__":
    world = WumpusWorld("wumpus_world.txt")
    world.run()
