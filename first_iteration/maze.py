import sys

from frontiers import FrontierFactory, Node

class Maze():

    def __init__(self, file_path, frontier_enum):
        self.frontier_enum = frontier_enum
        with open(file_path) as f:
            contents = f.read()
        
        if contents.count("A") != 1:
            raise Exception("Maze must contain 1 entry point")
        if contents.count("B") != 1:
            raise Exception("Maze must contain 1 exit")
        
        lines = contents.splitlines()
        self.height = len(lines)
        self.width = max(len(line) for line in lines)

        ## Walls
        self.walls = []
        self.start = ()
        self.goal = ()

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    col = lines[i][j]
                    is_wall = False
                    if col == "A":
                        self.start = (i, j)
                    if col == "B":
                        self.goal = (i, j)
                    if col == "#":
                        is_wall = True
                    row.append(is_wall)
                except IndexError:
                    print("Error",(i,j))
                    row.append(False)

            self.walls.append(row)

        self.solution = None

        # print("Walls", self.walls)
        # print("Start", self.start)
        # print("goal", self.goal)

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def solve(self):
        self.num_explored = 0
        
        frontier = FrontierFactory().create_frontier(self.frontier_enum, goal=self.goal)

        start = Node(state=self.start, parent=None, action=None)
        frontier.add(start)
        self.explored = set()
        while True:
            if frontier.empty():
                raise Exception("no solution")
            
            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not  frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    child.set_distance_traversed(node.distance_traversed+1)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 3:
    sys.exit("Usage: python maze.py maze.txt")
maze = Maze(sys.argv[1], sys.argv[2])
print("Maze:")
maze.print()
print("Solving...")
maze.solve()
print("States Explored:", maze.num_explored)
print("Solution:")
maze.print()
maze.output_image("maze.png")