from pyamaze import maze , COLOR , agent , textLabel
from collections import deque
import tkinter as tk
import sys


def DFS(m):
    start = (m.rows, m.cols)  # Starting point at the bottom-right corner
    frontier = [start]
    explored = [start]
    dfsPath = {} # Dictionary to store the path taken


    while len(frontier) > 0:
        current = frontier.pop()

        if current == (1, 1):
            break

        for d in 'ESNW':  # Explore in this order
            if m.maze_map[current][d]:
                if d == 'E':
                    next_cell = (current[0], current[1] + 1)
                elif d == 'W':
                    next_cell = (current[0], current[1] - 1)
                elif d == 'N':
                    next_cell = (current[0] - 1, current[1])
                elif d == 'S':
                    next_cell = (current[0] + 1, current[1])

                if next_cell not in explored:
                    frontier.append(next_cell)
                    explored.append(next_cell)
                    dfsPath[next_cell] = current # Store the path taken    

    fwdPath = {}  # Dictionary to store the forward path
    cell = (1, 1)  # Starting from the top-left corner
    while cell != start:    #Key of the dfsPath turns into the value of fwdPath
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    
    return fwdPath  # Return the path from start to finish

def BFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols) #Starting point at the bottom-right corner
    frontier = deque()  # Use deque for efficient pop from the left
    frontier.append(start)
    explored = [start]
    bfsPath = {}  # Dictionary to store the path taken
    bSearch = []  # List to store the cells visited in BFS order

    while len(frontier) > 0 :
        current = frontier.popleft()  # Pop from the left for BFS
        if current == (1, 1):
            break
        for d in 'ESNW':
            if m.maze_map[current][d]:
                if d == 'E':
                    next_cell = (current[0], current[1] + 1)
                elif d == 'W':
                    next_cell = (current[0], current[1] - 1)
                elif d == 'N':
                    next_cell = (current[0] - 1, current[1])
                elif d == 'S':
                    next_cell = (current[0] + 1, current[1])

                if next_cell not in explored:
                    frontier.append(next_cell)
                    explored.append(next_cell)
                    bfsPath[next_cell] = current 
                    bSearch.append(next_cell)  # Store the path taken and the cells visited in BFS order

    fwdPath = {}  # Dictionary to store the forward path
    cell = (1, 1)  # Starting from the top-left corner
    while cell != start:  # Key of the bfsPath turns into the value of fwdPath
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    return bSearch,bfsPath,fwdPath  # Return the path from start to finish

def main():
    #Create Tkinter root window
    root = tk.Tk()
    root.title("Maze Solver using DFS and BFS")
    root.geometry("300x200")  # Set the size of the window
     
    choice = tk.StringVar(value="DFS")  # Default choice is DFS
    tk.Label(root, text="Choose Algorithm:").pack()
    tk.Radiobutton(root, text="DFS", variable=choice, value="DFS").pack(anchor=tk.W) # Radio button for DFS
    tk.Radiobutton(root, text="BFS", variable=choice, value="BFS").pack(anchor=tk.W) # Radio button for BFS
    tk.Button(root, text="Run", command=root.destroy).pack()
    tk.Button(root, text="Exit", command=sys.exit).pack()  # Button to exit the program
    
    root.mainloop()  # Wait for user input to choose the algorithm
    
    m = maze(20,20)
    m.CreateMaze(theme= COLOR.light)
    
    dfs_path = DFS(m)
    if dfs_path is None:
        print("No path found using DFS.")
        return
    bSearch, bfsPath, fwdPath = BFS(m)  # Get the path using BFS
    if bSearch is None or bfsPath is None or fwdPath is None:
        print("No path found using BFS.")
        return

    if choice.get() == "DFS":
        #Visualise the DFS path
        a = agent(m,footprints=True, color=COLOR.red)
        m.tracePath({a: dfs_path}, delay=100)
        l1 = textLabel(m, 'TotalCells' , m.rows * m.cols)  # Display the total number of cells in the maze
    elif choice.get() == "BFS":
        #Visualise the BFS path
        a = agent(m,footprints=True, color=COLOR.yellow)
        b = agent(m,footprints=True, color=COLOR.cyan)
        c = agent(m,1,1, filled = True, footprints=True, color=COLOR.green, goal=(m.rows, m.cols))  # Agent at the start position with goal at the end

        l1 = textLabel(m, 'TotalCells' , m.rows * m.cols)  # Display the total number of cells in the maze
        l2 = textLabel(m, 'The Shortest Path', len(fwdPath) + 1)  # Display the length of the shortest path found
        m.tracePath({a: bSearch}, delay=25)
        m.tracePath({b: fwdPath}, delay=100)
        m.tracePath({c: bfsPath}, delay=300)  # Visualise the BFS path taken by the agent
    else:
        print("Invalid choice. Please run the program again and select either DFS or BFS.")
        return

    m.run()

if __name__ == "__main__":
    main()
