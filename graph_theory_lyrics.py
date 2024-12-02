import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import cycle

# Define rhyme groups and their phrases (graph theory themes)
rhyme_groups = {
    "A": ["CS 5002 leads the way", "Graphs connect, concepts stay", "Paths align, logic at play", "Dr. Amjad guides our day"],
    "B": ["Trees reach high, edges call", "Cycles spin, graphs enthrall", "Sorting schemes that solve it all", "Functions rise, answers fall"],
    "C": ["Shortest paths, we compute", "Nodes refine, roots astute", "Weights align, data resolute", "Graphs design, goals pursuit"],
    "D": ["Counting dreams, logic supreme", "Graphs reveal a hidden theme", "Sorting flows like data streams", "Structures guide our greatest scheme"],
    "E": ["Spanning free, matchings decree", "CS 5002 builds unity", "Graphs agree, complexity foresee", "Dr. Amjad inspires me"]
}

# Create a graph with rhyme groups
def create_lyrics_graph(rhyme_groups):
    G = nx.DiGraph()

    # Add nodes for each phrase with their group
    for group, phrases in rhyme_groups.items():
        for phrase in phrases:
            G.add_node(phrase, rhyme_group=group)

    # Add directed edges based on rhyme group transitions
    for group, phrases in rhyme_groups.items():
        for phrase in phrases:
            # Connect to other phrases in the same rhyme group
            same_group = [p for p in phrases if p != phrase]
            for target in random.sample(same_group, min(2, len(same_group))):
                G.add_edge(phrase, target)

            # Connect to random phrases in other groups for variety
            other_groups = [p for g, ps in rhyme_groups.items() if g != group for p in ps]
            for target in random.sample(other_groups, min(3, len(other_groups))):
                G.add_edge(phrase, target)

    return G

# Generate lyrics based on a rhyme scheme and record the path
def generate_lyrics(graph, rhyme_scheme="AABB", num_lines=8):
    lyrics = []
    path = []  # To record the sequence of phrases
    rhyme_order = cycle(rhyme_scheme)  # Create a cycle of the rhyme scheme

    # Initialize the starting group and phrase
    current_group = next(rhyme_order)
    current_phrase = random.choice([
        n for n, attr in graph.nodes(data=True) if attr["rhyme_group"] == current_group
    ])

    for _ in range(num_lines):
        lyrics.append(current_phrase)
        path.append(current_phrase)

        # Update the rhyme group for the next line
        current_group = next(rhyme_order)

        # Find possible next phrases in the current group
        possible_phrases = [
            neighbor for neighbor in graph.neighbors(current_phrase)
            if graph.nodes[neighbor]["rhyme_group"] == current_group
        ]

        # Choose the next phrase, or fallback to any node in the same group
        if possible_phrases:
            current_phrase = random.choice(possible_phrases)
        else:
            current_phrase = random.choice([
                n for n, attr in graph.nodes(data=True) if attr["rhyme_group"] == current_group
            ])

    return "\n".join(lyrics), path

# Visualize the graph and highlight the generated lyrics
def visualize_lyrics_graph(graph, path):
    pos = nx.spring_layout(graph)  # Layout for positioning nodes

    # Draw all nodes and edges
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_color="lightgray", edge_color="lightgray", node_size=2000, font_size=10)

    # Highlight the nodes and edges in the generated lyrics path
    path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color="orange", node_size=2500)
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="red", width=2)

    # Display the graph
    plt.title("Lyrics Generation Path in the Graph", fontsize=16)
    plt.show()

# Main function
if __name__ == "__main__":
    # Create the graph
    lyrics_graph = create_lyrics_graph(rhyme_groups)
    print("Lyrical Graph created")

    # Define a rhyme scheme and generate lyrics
    # Song format: Verse / Chorus / Verse / Chorus / Bridge / Chorus
    verse1 = "BBCC"
    num_lines = 4
    verse1_lyrics, verse1_path = generate_lyrics(lyrics_graph, verse1, num_lines)

    verse2 = "BBCC"
    num_lines = 4
    verse2_lyrics, verse2_path = generate_lyrics(lyrics_graph, verse2, num_lines)

    chorus = "AAAA"  # Example rhyme scheme
    num_lines = 4
    chorus_lyrics, chorus_path = generate_lyrics(lyrics_graph, chorus, num_lines)

    bridge = "DDEE"
    num_lines = 4
    bridge_lyrics, bridge_path = generate_lyrics(lyrics_graph, bridge, num_lines)

    # Output the generated lyrics
    print("[Verse 1]")
    print(verse1_lyrics)
    print("[Chorus]")
    print(chorus_lyrics)
    print("[Verse 2]")
    print(verse2_lyrics)
    print("[Chorus]")
    print(chorus_lyrics)
    print("[Bridge]")
    print(bridge_lyrics)
    print("[Chorus]")
    print(chorus_lyrics)

    # Visualize the graph with the generated lyrics path
    visualize_lyrics_graph(lyrics_graph, verse1_path)
    visualize_lyrics_graph(lyrics_graph, chorus_path)
    visualize_lyrics_graph(lyrics_graph, verse2_path)
    visualize_lyrics_graph(lyrics_graph, bridge_path)