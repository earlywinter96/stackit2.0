from collections import deque, defaultdict

def GraphChallenge(strArr):
    n = int(strArr[0])
    nodes = strArr[1:n+1]
    connections = strArr[n+1:]

    graph = defaultdict(list)

    for edge in connections:
        u, v = edge.split('-')
        graph[u].append(v)
        graph[v].append(u)

    start = nodes[0]
    end = nodes[-1]

    # BFS for shortest path
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == end:
            return '-'.join(path)
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)

    return "-1"

# Example usage:
print(GraphChallenge(["4","A","B","C","D","A-B","B-D","B-C","C-D"]))  # Output: A-B-D
print(GraphChallenge(["7","A","B","C","D","E","F","G","A-B","A-E","B-C","C-D","D-F","E-D","F-G"]))  # Output: A-E-D-F-G
