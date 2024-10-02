import osmnx as ox
import networkx as nx
import folium

# Get the road network for a broader area
place_name = "San Francisco, California, USA"
graph = ox.graph_from_place(place_name, network_type='drive')

# Define two nearby coordinates in San Francisco
start_point = (37.7749, -122.4194)  # Downtown SF
end_point = (37.7793, -122.4187)    # A nearby location

# Get the nearest nodes to the start and end points
start_node = ox.distance.nearest_nodes(graph, start_point[1], start_point[0])
end_node = ox.distance.nearest_nodes(graph, end_point[1], end_point[0])

# Try to find the shortest path between the nodes
try:
    shortest_route = nx.shortest_path(graph, start_node, end_node, weight='length')

    # Get the coordinates of the shortest path
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_route]

    # Create a map
    m = folium.Map(location=start_point, zoom_start=15)

    # Add the shortest route to the map
    folium.PolyLine(locations=route_coords, color="blue", weight=5).add_to(m)

    # Add markers for start and end points
    folium.Marker(location=start_point, popup="Start").add_to(m)
    folium.Marker(location=end_point, popup="End").add_to(m)

    # Save and display the map
    m.save('shortest_path_map.html')
    print("Map saved as 'shortest_path_map.html'. Open it in a browser.")

except nx.NetworkXNoPath:
    print(f"No path found between {start_node} and {end_node}.")
