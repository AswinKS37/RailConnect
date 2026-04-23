from graph import init_graph, find_routes, network
from booking import validate_seats, book_route

def run_tests():
    init_graph()
    
    print("--- Test 1: Direct Route ---")
    routes_a_b = find_routes("Station A", "Station B")
    for r in routes_a_b:
        print("Path:", [s['train_id'] for s in r], "Seats Valid:", validate_seats(r))

    print("\n--- Test 2: Indirect Route (A -> E) ---")
    routes_a_e = find_routes("Station A", "Station E")
    for r in routes_a_e:
        print("Path:", [s['train_id'] for s in r], "Seats Valid:", validate_seats(r))

    print("\n--- Test 3: Route with No Seats (A -> D -> B) ---")
    # T302 (D -> B) has 0 seats initially
    for r in routes_a_b:
        if len(r) > 1 and r[0]['dest'] == 'Station D':
             print("Path:", [s['train_id'] for s in r], "Seats Valid:", validate_seats(r))
             
    print("\n--- Test 4: Booking a Route ---")
    # Book A -> B direct
    book_route_target = routes_a_b[0]
    print("Before booking, seats on T101:", book_route_target[0]['seats_available'])
    success, updated = book_route(book_route_target)
    print("Booking success:", success)
    print("After booking, seats on T101:", updated[0]['seats_available'])
    
    # Verify in graph directly
    for seg in network["Station A"]:
        if seg.train_id == "T101":
            print("Graph check seats on T101:", seg.seats_available)
            break

if __name__ == "__main__":
    run_tests()
