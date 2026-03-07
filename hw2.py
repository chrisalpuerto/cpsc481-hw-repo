# HW 2
# Chris Alpuerto

"""
GOAL: Explore Greedy, BFS and A* search algorithms on the Romania map problem.

3 POSSIBLE PATHS: 
Arad -> Sibiu -> Fagaras -> Bucharest
Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
Arad -> Timisoara -> Lugoj -> Mehadia -> Drobeta -> Craiova -> Pitesti -> Bucharest

"""

romania_map = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Vaslui", 92), ("Neamt", 87)],
    "Neamt": [("Iasi", 87)]
}

heuristic = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

start = "Arad"
goal = "Bucharest"


# Helper: compute path cost from the graph
def path_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        src, dst = path[i], path[i + 1]
        for neighbor, cost in graph[src]:
            if neighbor == dst:
                total += cost
                break
    return total


# 1. Breadth-First Search
def bfs(graph, start, goal):
    from collections import deque

    frontier = deque()
    frontier.append((start, [start]))
    visited = set()
    nodes_expanded = []

    while frontier:
        node, path = frontier.popleft()

        if node in visited:
            continue
        visited.add(node)
        nodes_expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "cost": path_cost(graph, path),
                "nodes_expanded": nodes_expanded,
                "nodes_visited": len(visited),
            }

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                frontier.append((neighbor, path + [neighbor]))

    return None

# 2. Greedy Best-First Search
def greedy(graph, heuristic, start, goal):
    import heapq

    # (h(node), node, path)
    frontier = [(heuristic[start], start, [start])]
    visited = set()
    nodes_expanded = []

    while frontier:
        _, node, path = heapq.heappop(frontier)

        if node in visited:
            continue
        visited.add(node)
        nodes_expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "cost": path_cost(graph, path),
                "nodes_expanded": nodes_expanded,
                "nodes_visited": len(visited),
            }

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                heapq.heappush(frontier, (heuristic[neighbor], neighbor, path + [neighbor]))

    return None

# 3. A* Search
def astar(graph, heuristic, start, goal):
    import heapq

    # (f, g, node, path)
    frontier = [(heuristic[start], 0, start, [start])]
    visited = set()
    nodes_expanded = []

    while frontier:
        _, g, node, path = heapq.heappop(frontier)

        if node in visited:
            continue
        visited.add(node)
        nodes_expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "cost": g,
                "nodes_expanded": nodes_expanded,
                "nodes_visited": len(visited),
            }

        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                new_g = g + edge_cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))

    return None

# Runner
def print_result(name, result, optimal):
    print(f"Algorithm : {name}")
    print(f"Nodes expanded : {result['nodes_expanded']}")
    print(f"Nodes visited  : {result['nodes_visited']}")
    print(f"Path           : {' -> '.join(result['path'])}")
    print(f"Path cost      : {result['cost']}")
    print(f"Optimal?       : {'Yes' if optimal else 'No'}")


if __name__ == "__main__":
    bfs_result    = bfs(romania_map, start, goal)
    greedy_result = greedy(romania_map, heuristic, start, goal)
    astar_result  = astar(romania_map, heuristic, start, goal)

    optimal_cost = astar_result["cost"]

    print_result("BFS", bfs_result, bfs_result["cost"] == optimal_cost)
    print_result("Greedy Best-First", greedy_result, greedy_result["cost"] == optimal_cost)
    print_result("A*", astar_result,  True)