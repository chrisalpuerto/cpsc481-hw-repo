# HW2 — Search Algorithms on the Romania Map

## Overview

This assignment explores three search algorithms on the classic Romania map problem from *Artificial Intelligence: A Modern Approach*. The goal is to find a path from **Arad** to **Bucharest** and compare how each algorithm performs in terms of the path it finds, the cost of that path, and the number of nodes it explores.

The map is represented as a weighted adjacency list (`romania_map`) and each city has a precomputed straight-line distance to Bucharest (`heuristic`), used as the admissible heuristic h(n).

---

## Algorithms

### 1. Breadth-First Search (BFS)
BFS explores nodes level by level using a FIFO queue. It expands the shallowest unexpanded node first, ignoring edge costs entirely. BFS is guaranteed to find the path with the fewest hops, but because it ignores costs it does not guarantee the lowest-cost path.

### 2. Greedy Best-First Search
Greedy search uses a priority queue ordered by the heuristic value h(n) — the straight-line distance from a node to Bucharest. It always expands whichever node appears closest to the goal. This makes it fast, but because it ignores the actual cost g(n) to reach a node, it can commit to a suboptimal path.

### 3. A\* Search
A\* combines the actual cost from the start g(n) with the heuristic estimate h(n), prioritizing nodes by f(n) = g(n) + h(n). Because the heuristic is admissible (it never overestimates the true cost), A\* is guaranteed to find the optimal (lowest-cost) path.

---

## Results

| Algorithm | Path | Path Cost | Nodes Expanded | Nodes Visited | Optimal? |
|-----------|------|-----------|----------------|---------------|----------|
| BFS | Arad → Sibiu → Fagaras → Bucharest | 450 | 9 | 9 | No |
| Greedy Best-First | Arad → Sibiu → Fagaras → Bucharest | 450 | 4 | 4 | No |
| A\* | Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest | **418** | 6 | 6 | **Yes** |

### Nodes Expanded (in order)

**BFS:**
Arad → Zerind → Sibiu → Timisoara → Oradea → Fagaras → Rimnicu Vilcea → Lugoj → Bucharest

**Greedy:**
Arad → Sibiu → Fagaras → Bucharest

**A\*:**
Arad → Sibiu → Rimnicu Vilcea → Fagaras → Pitesti → Bucharest

---

## Analysis

**BFS** finds the fewest-hop path (3 edges) but expands 9 nodes along the way, including several that are far from the goal (Zerind, Timisoara, Lugoj). It explores by layer outward from Arad, so it wastes time on nodes in the wrong direction. The resulting path costs 450, which is not the cheapest route.

**Greedy** is the most efficient in terms of nodes expanded — just 4. By always following the city with the smallest straight-line distance to Bucharest, it zeroes in on the goal quickly. However, it finds the same suboptimal 450-cost path as BFS because it greedily picks Fagaras (h=176) over Rimnicu Vilcea (h=193), even though going through Rimnicu Vilcea leads to a cheaper total path.

**A\*** expands 6 nodes and finds the optimal path at cost 418 (Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest). By balancing actual travel cost and heuristic estimate, it avoids the greedy mistake: when Fagaras is dequeued, Pitesti's f-score is lower, so A\* correctly pursues that branch instead. The admissibility of the heuristic guarantees that no cheaper path was overlooked.

### Summary

- Greedy is fastest but sacrifices optimality.
- BFS is systematic but ignores costs, leading to a suboptimal and relatively expensive search.
- A\* strikes the best balance: it expands only slightly more nodes than Greedy while guaranteeing the optimal solution.
