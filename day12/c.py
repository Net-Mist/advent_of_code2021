from collections import defaultdict


def get_graph(file_path: str) -> defaultdict:
    """graph will be a dict encoding for each node, the list of reachable_node"""
    graph = defaultdict(list)
    with open(file_path) as f:
        for line in f.readlines():
            a, b = line.strip().split("-")
            if b != "start":
                graph[a].append(b)
            if a != "start":
                graph[b].append(a)
    return graph


def find_path(first_node: str, graph: defaultdict, visited_node: list[str], seen_twice: bool) -> list[list[str]]:
    if first_node in small_cave and first_node in visited_node:
        if seen_twice:
            return []
        seen_twice = True

    visited_node = visited_node + [first_node]
    if first_node == "end":
        return [visited_node]

    r = []
    for visitable_node in graph[first_node]:
        r += find_path(visitable_node, graph, visited_node, seen_twice)
    return r


graph = get_graph("input.txt")
small_cave = [cave for cave in graph.keys() if cave != cave.upper()]
paths = find_path("start", graph, [], True)
print("part1:", len(paths))
paths = find_path("start", graph, [], False)
print("part2:", len(paths))
