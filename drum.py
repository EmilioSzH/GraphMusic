import os
from mido import Message, MidiFile, MidiTrack
import networkx as nx
import matplotlib.pyplot as plt
import random
import pygame

# Ensure the directory for saving files exists
SAVE_DIR = "createdFiles"
os.makedirs(SAVE_DIR, exist_ok=True)

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
    
    # Save MIDI file in the createdFiles directory
    midi_path = os.path.join(SAVE_DIR, 'drum_pattern.mid')
    mid.save(midi_path)
    return mid

def play_midi_pygame(midi_file):
    """
    Play MIDI file using pygame
    """
    pygame.init()
    pygame.mixer.init()
    
    try:
        pygame.mixer.music.load('createdFiles/drum_pattern.mid')
        pygame.mixer.music.play()
        
        # Wait until playback is complete
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing MIDI: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()

def save_graph(figure, filename):
    """
    Save a graph visualization to a file.
    """
    filepath = os.path.join(SAVE_DIR, filename)
    figure.savefig(filepath)
    print(f"Graph saved to {filepath}")
    plt.close(figure)

def create_comprehensive_drum_transition_graph(lyrics):
    """
    Create a comprehensive graph showing transitions between drum notes
    with section edges highlighted and adaptive edge width
    """
    sections = {}
    for line, section in lyrics:
        if section not in sections:
            sections[section] = []
        sections[section].append(line)
    
    G = nx.DiGraph()
    section_drum_sequences = {}
    edge_frequencies = {}
    
    for section, section_lyrics in sections.items():
        section_drums = generate_drum_pattern([(line, section) for line in section_lyrics])
        section_drum_sequences[section] = section_drums
        
        for i in range(len(section_drums) - 1):
            current_note = section_drums[i]
            next_note = section_drums[i+1]
            edge_key = (current_note, next_note)
            edge_frequencies[edge_key] = edge_frequencies.get(edge_key, 0) + 1
            
            if G.has_edge(current_note, next_note):
                G[current_note][next_note]['weight'] += 1
            else:
                G.add_edge(current_note, next_note, weight=1)
    
    # Save the comprehensive graph
    fig, ax = plt.subplots(figsize=(15, 10))
    pos = nx.spring_layout(G, k=0.9, iterations=50)
    nx.draw_networkx_nodes(G, pos, node_color=DEFAULT_NODE_COLOR, node_size=NODE_SIZE, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=EDGE_WIDTH, arrows=True, arrowsize=10, ax=ax)
    plt.title('Comprehensive Drum Note Transitions')
    save_graph(fig, "comprehensive_drum_graph.png")

    # Save section-specific graphs
    sections_to_highlight = ['Verse 1', 'Verse 2', 'Chorus', 'Bridge']
    colors = ['red', 'green', 'blue', 'purple']
    for section, color in zip(sections_to_highlight, colors):
        fig, ax = plt.subplots(figsize=(15, 10))
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500, ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='gray', width=EDGE_WIDTH, arrows=True, arrowsize=10, ax=ax)
        
        # Highlight section-specific edges
        section_drums = section_drum_sequences[section]
        section_edges = [(section_drums[i], section_drums[i + 1]) for i in range(len(section_drums) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=section_edges, edge_color=color,
                               width=EDGE_WIDTH, arrows=True, arrowsize=10, ax=ax)
        
        plt.title(f'Drum Note Transitions - {section} Highlighted')
        plt.axis('off')
        plt.tight_layout()
        save_graph(fig, f"drum_{section.replace(' ', '_').lower()}_graph.png")

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