import csv
from queue import PriorityQueue


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("%s does not exist" % city)

# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    
    graph = {}
    with open(path, 'r',newline='',encoding='UTF-8') as csv_file:
        reader = csv.reader(csv_file,delimiter=',')
        if next(reader) != ['city1', 'city2', 'distance']:
            raise ValueError("Invalid CSV format.")
        for row in reader:
            city1, city2, distance = map(str.strip, row)
            distance = int(distance)
            graph.setdefault(city1, {})
            graph.setdefault(city2, {})
            graph[city1][city2] = distance
            graph[city2][city1] = distance
    return graph

# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    
    if start not in graph or end not in graph:
        raise CityNotFoundError(start) if start not in graph else CityNotFoundError(end)

    queue = PriorityQueue()

    queue.put((0, start))

    visited = set()

    cost = {start: 0}

    path = {start: []}

    while not queue.empty():
        currentCost, currentNode = queue.get()

        if currentNode == end:
            return path[currentNode], cost[currentNode]

        visited.add(currentNode)

        for neighbor, distance in graph[currentNode].items():
            new_cost = currentCost + distance

            if neighbor not in visited and new_cost < cost.get(neighbor, float('inf')):
                cost[neighbor] = new_cost
                path[neighbor] = path[currentNode] + [(currentNode, neighbor)]
                queue.put((new_cost, neighbor))

    raise CityNotFoundError(end)

# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    try:
        csvPath = input("Enter CSV file path: ")
        
        graph = build_graph(csvPath)

        start_city = input("Enter starting city: ")
        end_city = input("Enter ending city: ")

        path, total_cost = uniform_cost_search(graph, start_city, end_city)

        path_cities = [city for city, _ in path]
        print("Optimal path:", ' >> '.join(path_cities))
        print("Cost of total:", total_cost)

    except FileNotFoundError:
        print("CSV file not found.")

    except CityNotFoundError as e:
        pass