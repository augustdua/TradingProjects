import numpy as np

# Parameters
grid_size = 10  # 10x10 grid
num_simulations = 100000  # Number of simulations to get an average search time

def random_search(grid_size, num_simulations):
    total_time = 0  # Total time to find the object in all simulations

    for _ in range(num_simulations):
        # Generate random positions for the object and the searcher
        object_pos = np.random.randint(0, grid_size, size=2)
        searcher_pos = np.random.randint(0, grid_size, size=2)

        visited = set()  # Keep track of visited cells
        time_taken = 0  # Time taken to find the object in this simulation

        while not np.array_equal(searcher_pos, object_pos):
            visited.add(tuple(searcher_pos))  # Mark the current cell as visited
            # Find the next move among non-visited cells
            possible_moves = [
                (searcher_pos[0] + dx, searcher_pos[1] + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if 0 <= searcher_pos[0] + dx < grid_size
                and 0 <= searcher_pos[1] + dy < grid_size
                and (searcher_pos[0] + dx, searcher_pos[1] + dy) not in visited
            ]
            if possible_moves:
                searcher_pos = np.array(possible_moves[np.random.randint(len(possible_moves))])
            else:
                # Reset if no unvisited cell is available (to avoid deadlock)
                searcher_pos = np.array([np.random.randint(grid_size), np.random.randint(grid_size)])
                visited.clear()

            time_taken += 1

        total_time += time_taken

    return total_time / num_simulations  # Average time

average_time = random_search(grid_size, num_simulations)
print(average_time)
