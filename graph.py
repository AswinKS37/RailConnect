"""
graph.py

Contains the in-memory graph representation of the railway network
and the BFS algorithm to find indirect split-seat routes.
"""
from collections import deque

class TrainSegment:
    def __init__(self, train_id, source, dest, departure_time, arrival_time, seats_available):
        self.train_id = train_id
        self.source = source
        self.dest = dest
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats_available = seats_available

    def to_dict(self):
        return {
            "train_id": self.train_id,
            "source": self.source,
            "dest": self.dest,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "seats_available": self.seats_available
        }

# Global in-memory railway network
# Structure: { source_station: [TrainSegment, ...] }
network = {}

def init_graph():
    """Initialize the graph with some dummy data."""
    network.clear()
    network.update({
        "Station A": [],
        "Station B": [],
        "Station C": [],
        "Station D": [],
        "Station E": []
    })
    
    # Add dummy segments
    # A -> B (Direct)
    network["Station A"].append(TrainSegment("T101", "Station A", "Station B", "08:00", "12:00", 50))
    # A -> C
    network["Station A"].append(TrainSegment("T201", "Station A", "Station C", "09:00", "11:00", 30))
    # C -> B (Indirect route A -> C -> B)
    network["Station C"].append(TrainSegment("T202", "Station C", "Station B", "12:00", "15:00", 20))
    # A -> D
    network["Station A"].append(TrainSegment("T301", "Station A", "Station D", "07:00", "10:00", 10))
    # D -> B
    network["Station D"].append(TrainSegment("T302", "Station D", "Station B", "11:00", "16:00", 0)) # No seats!
    # B -> E
    network["Station B"].append(TrainSegment("T401", "Station B", "Station E", "17:00", "19:00", 40))
    # C -> E
    network["Station C"].append(TrainSegment("T402", "Station C", "Station E", "11:30", "14:30", 15))


def get_stations():
    """Return a list of all station names."""
    return list(network.keys())


def find_routes(source, target):
    """
    Finds all valid paths from source to target using BFS.
    A path is a list of TrainSegment objects.
    Returns: list of paths (each path is a list of dicts for easier rendering)
    """
    if source not in network or target not in network:
        return []

    # Queue stores tuples of (current_station, path_so_far)
    # path_so_far is a list of TrainSegment
    queue = deque([(source, [])])
    valid_routes = []
    
    # We shouldn't revisit stations in a single path to avoid cycles
    # But since we're doing BFS, we can track visited stations per path
    
    while queue:
        current_station, current_path = queue.popleft()
        
        # If we reached the target, add the path to our valid routes
        if current_station == target and len(current_path) > 0:
            valid_routes.append(current_path)
            continue
            
        # Explore neighbors
        for segment in network.get(current_station, []):
            # To avoid cycles, check if the segment's destination is already visited in this path
            visited_stations = [source] + [s.dest for s in current_path]
            if segment.dest in visited_stations:
                continue
                
            # Basic temporal validation: departure logic
            # A connection is only valid if departure of next train is AFTER arrival of previous train
            if current_path:
                prev_arrival = current_path[-1].arrival_time
                if segment.departure_time < prev_arrival:
                    continue # Train departs before the previous one arrives
            
            # Create a new path and add it to queue
            new_path = list(current_path)
            new_path.append(segment)
            queue.append((segment.dest, new_path))
            
    # Convert list of segment objects to dicts for frontend
    result = []
    for path in valid_routes:
        result.append([segment.to_dict() for segment in path])
        
    return result
