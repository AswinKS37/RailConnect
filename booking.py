"""
booking.py

Handles seat validation and booking simulation.
"""
from graph import network

def validate_seats(path):
    """
    Checks if all segments in the given path have at least 1 available seat.
    path is a list of segment dictionaries.
    """
    for segment in path:
        if segment['seats_available'] <= 0:
            return False
    return True

def book_route(path):
    """
    Simulates a booking by reducing the seat count by 1 for all segments in the path.
    path: list of dictionaries representing the segments.
    Returns: A boolean indicating success, and an updated path with new seat counts.
    """
    # Double check validation first
    if not validate_seats(path):
        return False, None
        
    # Proceed to book
    updated_path = []
    for requested_segment in path:
        # Find the actual segment in the network to update it
        source = requested_segment['source']
        train_id = requested_segment['train_id']
        
        if source in network:
            for actual_segment in network[source]:
                if actual_segment.train_id == train_id:
                    # Decrement seat count
                    actual_segment.seats_available -= 1
                    updated_path.append(actual_segment.to_dict())
                    break
                    
    return True, updated_path
