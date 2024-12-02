import mido
from mido import Message, MidiFile, MidiTrack
import networkx as nx
import matplotlib.pyplot as plt
import random
import pygame

# Updated drum notes map
DRUM_NOTES = {
    "Bass": 35,    # Acoustic Bass Drum
    "Snare": 38,   # Acoustic Snare
    "Hi-Hat": 42,  # Closed Hi-Hat
    "Clap": 39,    # Hand Clap
    "Tom": 45,     # Low Tom
    "Cymbal": 49,  # Crash Cymbal 1
}

EDGE_WIDTH = 2
DEFAULT_NODE_COLOR = "orange"
NODE_SIZE = 2000

def generate_drum_pattern(lyrics):
    """
    Generate a semi-random drum pattern based on lyrical structure
    """
    drum_mapping = {
        'Verse 1': ['Bass', 'Snare', 'Hi-Hat', 'Tom'],
        'Chorus': ['Bass', 'Snare', 'Cymbal', 'Clap'],
        'Verse 2': ['Bass', 'Snare', 'Hi-Hat', 'Tom'],
        'Bridge': ['Bass', 'Snare', 'Cymbal', 'Clap']
    }
    
    drum_sequence = []
    current_section = None
    
    for line, section in lyrics:
        if section != current_section:
            current_section = section
        
        # Choose 2-3 drum notes for each line
        line_drums = random.choices(drum_mapping.get(section, ['Bass', 'Snare']), k=random.randint(2, 3))
        drum_sequence.extend(line_drums)
    
    return drum_sequence

def create_midi_file(drum_sequence):
    """
    Create a MIDI file with the generated drum sequence
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Add drum track
    for note_name in drum_sequence:
        note = DRUM_NOTES[note_name]
        
        # Note on
        track.append(Message('note_on', note=note, velocity=64, time=0, channel=9))
        # Note off (after 480 ticks, which is one beat)
        track.append(Message('note_off', note=note, velocity=64, time=480, channel=9))
    
    mid.save('drum_pattern.mid')
    return mid

def play_midi_pygame(midi_file):
    """
    Play MIDI file using pygame
    """
    pygame.init()
    pygame.mixer.init()
    
    try:
        pygame.mixer.music.load('drum_pattern.mid')
        pygame.mixer.music.play()
        
        # Wait until playback is complete
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing MIDI: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()

def visualize_lyrics_graph(graph, path):
    """
    Visualize the lyrics graph with improved design and path highlighting
    
    Args:
    - graph: NetworkX graph of lyrics
    - path: Generated path through the graph
    """
    # Use a more sophisticated layout algorithm
    pos = nx.spring_layout(graph, k=0.5, iterations=50)

    # Create figure with a clean, modern look
    plt.figure(figsize=(16, 10), facecolor='#F0F0F0')
    plt.title("Lyrics Generation Path", fontsize=20, fontweight='bold', pad=20)

    # Draw base graph with muted colors
    nx.draw(graph, pos, 
        with_labels=True, 
        node_color=DEFAULT_NODE_COLOR,  # Soft gray for base nodes
        edge_color="#CCCCCC",  # Light gray for base edges
        node_size=NODE_SIZE,  # Maintained node size from original code
        font_size=10,  # Maintained font size
        font_weight='bold',  # Added bold font for better readability
        alpha=0.6  # Added slight transparency
    )

    # Highlight the nodes and edges in the generated lyrics path
    path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    
    # Highlight path nodes with vibrant colors
    nx.draw_networkx_nodes(graph, pos, 
        nodelist=path, 
        node_color=DEFAULT_NODE_COLOR,  # Vibrant orange/red
        node_size=NODE_SIZE,  # Slightly larger than base nodes
        alpha=0.9,
        edgecolors='black'  # Black outline for path nodes
    )

    # Highlight path edges
    nx.draw_networkx_edges(graph, pos, 
        edgelist=path_edges, 
        edge_color='#E74C3C',  # Vibrant red
        width=3,  # Thicker path edges
        arrows=True,
        arrowsize=10
    )

    # Improve overall graph aesthetics
    plt.tight_layout()
    plt.axis('off')  # Hide axes
    plt.gca().set_facecolor('#F0F0F0')  # Light background color

    plt.show()

def create_comprehensive_drum_transition_graph(lyrics):
    """
    Create a comprehensive graph showing transitions between drum notes
    with section edges highlighted and adaptive edge width
    """
    # Group lyrics by section
    sections = {}
    for line, section in lyrics:
        if section not in sections:
            sections[section] = []
        sections[section].append(line)
    
    # Create a comprehensive graph
    G = nx.DiGraph()
    
    # Store section-specific drum sequences
    section_drum_sequences = {}
    
    # Track edge frequencies
    edge_frequencies = {}
    
    # Generate drum sequences for each section
    for section, section_lyrics in sections.items():
        section_drums = generate_drum_pattern([(line, section) for line in section_lyrics])
        section_drum_sequences[section] = section_drums
        
        # Add transitions for this section
        for i in range(len(section_drums) - 1):
            current_note = section_drums[i]
            next_note = section_drums[i+1]
            
            # Track edge frequency
            edge_key = (current_note, next_note)
            edge_frequencies[edge_key] = edge_frequencies.get(edge_key, 0) + 1
            
            if G.has_edge(current_note, next_note):
                G[current_note][next_note]['weight'] += 1
            else:
                G.add_edge(current_note, next_note, weight=1)
    
    # Visualize comprehensive graph with adaptive edge width
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=0.9, iterations=50)
    
    # Determine max frequency for scaling
    max_frequency = max(edge_frequencies.values()) if edge_frequencies else 1
    
    # Draw all nodes with larger size
    nx.draw_networkx_nodes(G, pos, node_color=DEFAULT_NODE_COLOR, node_size=NODE_SIZE)  # Increased node size
    nx.draw_networkx_labels(G, pos)
    
    # Draw edges with adaptive width
    edges = list(G.edges())
    weights = []
    for u, v in edges:
        # Calculate edge width based on frequency, with a minimum width
        freq = edge_frequencies.get((u, v), 1)
        width = max(0.5, 3 * (freq / max_frequency))  # Adaptive width with minimum
        weights.append(width)
    
    # Draw edges with adaptive width
    nx.draw_networkx_edges(G, pos, 
                            edge_color='gray', 
                            width=EDGE_WIDTH, 
                            arrows=True, 
                            arrowsize=10)
    
    # Highlight section edges one by one
    sections_to_highlight = ['Verse 1', 'Verse 2', 'Chorus', 'Bridge']
    colors = ['red', 'green', 'blue', 'purple']
    
    plt.title('Comprehensive Drum Note Transitions')
    
    for section, color in zip(sections_to_highlight, colors):
        # Create a new figure for each section highlight
        plt.figure(figsize=(15, 10))
        
        # Redraw the base graph
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500)
        nx.draw_networkx_labels(G, pos)
        
        # Draw all edges in gray with adaptive width
        nx.draw_networkx_edges(G, pos, 
                                edge_color='gray', 
                                width=EDGE_WIDTH, 
                                arrows=True, 
                                arrowsize=10)
        
        # Highlight section-specific edges
        section_drums = section_drum_sequences[section]
        section_edges = []
        for i in range(len(section_drums) - 1):
            current_note = section_drums[i]
            next_note = section_drums[i+1]
            section_edges.append((current_note, next_note))
        
        # Draw section-specific edges in distinct color
        nx.draw_networkx_edges(G, pos, 
                                edgelist=section_edges, 
                                edge_color=color, 
                                width=EDGE_WIDTH, 
                                arrows=True, 
                                arrowsize=10)
        
        plt.title(f'Drum Note Transitions - {section} Highlighted')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    # Show the comprehensive graph
    plt.figure(figsize=(15, 10))
    nx.draw_networkx_nodes(G, pos, node_color=DEFAULT_NODE_COLOR, node_size=NODE_SIZE)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, 
                            edge_color='gray', 
                            width=EDGE_WIDTH, 
                            arrows=True, 
                            arrowsize=10)
    plt.title('Comprehensive Drum Note Transitions')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    return G

# Main execution
lyrics = [
    ("Cycles spin, graphs enthrall", "Verse 1"),
    ("Sorting schemes that solve it all", "Verse 1"),
    ("Graphs design, goals pursuit", "Verse 1"),
    ("Nodes refine, roots astute", "Verse 1"),
    ("Paths align, logic at play", "Chorus"),
    ("CS 5002 leads the way", "Chorus"),
    ("Graphs connect, concepts stay", "Chorus"),
    ("CS 5002 leads the way", "Chorus"),
    ("Sorting schemes that solve it all", "Verse 2"),
    ("Functions rise, answers fall", "Verse 2"),
    ("Nodes refine, roots astute", "Verse 2"),
    ("Shortest paths, we compute", "Verse 2"),
    ("Paths align, logic at play", "Chorus"),
    ("CS 5002 leads the way", "Chorus"),
    ("Graphs connect, concepts stay", "Chorus"),
    ("CS 5002 leads the way", "Chorus"),
    ("Structures guide our greatest scheme", "Bridge"),
    ("Sorting flows like data streams", "Bridge"),
    ("Dr. Amjad inspires me", "Bridge"),
    ("Graphs agree, complexity foresee", "Bridge"),
    ("Paths align, logic at play", "Chorus"),
    ("CS 5002 leads the way", "Chorus"),
    ("Graphs connect, concepts stay", "Chorus"),
    ("CS 5002 leads the way", "Chorus"),
]

# Generate drum sequence and MIDI
full_drum_sequence = generate_drum_pattern(lyrics)
midi_file = create_midi_file(full_drum_sequence)

# Create comprehensive graph with section highlights
comprehensive_graph = create_comprehensive_drum_transition_graph(lyrics)

# Play the MIDI file
print("Attempting to play the MIDI file...")
play_midi_pygame(midi_file)

print("MIDI file 'drum_pattern.mid' has been created.")