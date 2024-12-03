from mido import Message, MidiFile, MidiTrack
import random
import pygame
import networkx as nx
import matplotlib.pyplot as plt
import os

# Define melody map
melody_map = {
    "Verse 1": [
        {"note": 69, "velocity": 64, "duration": 480},  # A4
        {"note": 72, "velocity": 80, "duration": 240},  # C5 (staccato)
        {"note": 67, "velocity": 64, "duration": 480},  # G4
        {"note": 69, "velocity": 90, "duration": 480},  # A4 (accent)
        {"note": 74, "velocity": 64, "duration": 480},  # D5
        {"note": 77, "velocity": 64, "duration": 960},  # F5 (legato)
        {"note": 79, "velocity": 64, "duration": 480},  # G5
        {"note": 77, "velocity": 64, "duration": 480},  # F5
    ],
    "Chorus": [
        {"note": 65, "velocity": 64, "duration": 480},  # F4
        {"note": 67, "velocity": 64, "duration": 480},  # G4
        {"note": 69, "velocity": 80, "duration": 960},  # A4 (legato)
        {"note": 71, "velocity": 64, "duration": 480},  # B4
        {"note": 72, "velocity": 100, "duration": 480}, # C5 (trill)
        {"note": 71, "velocity": 64, "duration": 480},  # B4
        {"note": 69, "velocity": 64, "duration": 960},  # A4 (legato)
        {"note": 67, "velocity": 64, "duration": 480},  # G4
        {"note": 65, "velocity": 64, "duration": 480},  # F4
    ],
    "Verse 2": [
        {"note": 72, "velocity": 64, "duration": 480},  # C5
        {"note": 74, "velocity": 80, "duration": 240},  # D5 (staccato)
        {"note": 77, "velocity": 64, "duration": 480},  # F5
        {"note": 79, "velocity": 90, "duration": 480},  # G5 (accent)
        {"note": 81, "velocity": 64, "duration": 480},  # A5
        {"note": 77, "velocity": 64, "duration": 960},  # F5 (legato)
        {"note": 76, "velocity": 64, "duration": 480},  # E5
        {"note": 72, "velocity": 64, "duration": 480},  # C5
    ],
    "Bridge": [
        {"note": 79, "velocity": 64, "duration": 480},  # G5
        {"note": 81, "velocity": 64, "duration": 480},  # A5
        {"note": 84, "velocity": 90, "duration": 480},  # C6 (accent)
        {"note": 81, "velocity": 64, "duration": 480},  # A5
        {"note": 77, "velocity": 64, "duration": 480},  # F5
        {"note": 76, "velocity": 64, "duration": 960},  # E5 (legato)
        {"note": 72, "velocity": 64, "duration": 480},  # C5
        {"note": 74, "velocity": 64, "duration": 480},  # D5
        {"note": 76, "velocity": 64, "duration": 480},  # E5
    ]
}

# Helper function to convert MIDI note numbers to note names
def midi_to_note_name(midi_note):
        NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = midi_note // 12 - 1
        note = NOTE_NAMES[midi_note % 12]
        return f"{note}{octave}"

def generate_melody_pattern_with_recording(lyrics, melody_map):
    """
    Generate a semi-random melody pattern based on lyrical structure and melody map.
    Logs the picked notes for each section in human-readable format (e.g., C4) and
    records them for further use.

    Returns:
        tuple: The melody sequence and a dictionary of picked notes by section.
    """
    melody_sequence = []
    current_section = None
    section_picked_notes = {}  # Dictionary to store picked notes for each section

    def midi_to_note_name(midi_note):
        """Convert a MIDI note number to a human-readable note name."""
        NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = midi_note // 12 - 1
        note = NOTE_NAMES[midi_note % 12]
        return f"{note}{octave}"

    for line, section in lyrics:
        if section != current_section:
            current_section = section
        
        # Fetch the melody for the current section
        section_melody = melody_map.get(section, [])
        
        # Choose 2-4 notes for each line, preserving their articulation if specified
        line_melody = random.choices(section_melody, k=random.randint(2, 4))
        melody_sequence.extend(line_melody)

        # Convert picked notes to human-readable names
        picked_notes = [midi_to_note_name(note["note"]) for note in line_melody]

        # Log and store the picked notes for the current section
        print(f"Section '{section}', Line '{line}': Picked notes: {picked_notes}")
        if section not in section_picked_notes:
            section_picked_notes[section] = []
        section_picked_notes[section].extend(picked_notes)

    return melody_sequence, section_picked_notes



def visualize_melody_graphs(picked_notes_by_section, melody_map, folder_name='createdFiles'):
    """
    Create and save graphs:
    1. Section-specific graphs: Nodes picked for the section are sky blue, other section nodes are gray.
    2. Global graph: All nodes (11) are displayed, and nodes used in all sections are highlighted.

    Args:
        picked_notes_by_section (dict): Notes picked by section from `generate_melody_pattern_with_recording`.
        melody_map (dict): Original mapping of notes for each section.
        folder_name (str): Directory to save the graphs.
    """
    # Convert all section notes in melody_map to human-readable format
    all_section_notes = {
        section: {midi_to_note_name(note["note"]) for note in notes}
        for section, notes in melody_map.items()
    }

    # Section-Specific Graphs
    for section, picked_notes in picked_notes_by_section.items():
        G = nx.DiGraph()

        # Nodes: All section notes in gray, picked notes in sky blue
        section_nodes = all_section_notes.get(section, set())
        G.add_nodes_from(section_nodes)

        # Edges: Connect consecutive picked notes
        picked_edges = [
            (picked_notes[i], picked_notes[i + 1])
            for i in range(len(picked_notes) - 1)
        ]
        G.add_edges_from(picked_edges)

        # Visualization
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.8, iterations=50)

        # Draw gray nodes (all section nodes)
        nx.draw_networkx_nodes(
            G, pos, nodelist=section_nodes, node_color="lightgray", node_size=1000, edgecolors="black"
        )
        # Highlight picked nodes (sky blue)
        nx.draw_networkx_nodes(
            G, pos, nodelist=set(picked_notes), node_color="skyblue", node_size=1000, edgecolors="black"
        )
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color="gray", width=2, arrows=True, arrowsize=20)
        # Add labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

        # Add title
        plt.title(f"Melody Graph - {section}", fontsize=16, fontweight="bold")
        plt.axis("off")

        # Save figure
        file_path = os.path.join(folder_name, f"melody_{section.replace(' ', '_')}_graph.png")
        plt.savefig(file_path, bbox_inches='tight', dpi=300)
        print(f"Graph for section '{section}' saved at: {file_path}")
        plt.close()

    # Global Graph
    all_global_nodes = {midi_to_note_name(note["note"]) for notes in melody_map.values() for note in notes}

    # Combine all picked notes and edges from all sections
    combined_edges = []
    for picked_notes in picked_notes_by_section.values():
        combined_edges.extend(
            (picked_notes[i], picked_notes[i + 1])
            for i in range(len(picked_notes) - 1)
        )

    G_global = nx.DiGraph()
    G_global.add_nodes_from(all_global_nodes)
    G_global.add_edges_from(combined_edges)

    # Visualization for the global graph
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G_global, k=0.8, iterations=50)

    # Draw all nodes in gray
    nx.draw_networkx_nodes(
        G_global, pos, nodelist=all_global_nodes, node_color="lightgray", node_size=1000, edgecolors="black"
    )
    # Highlight nodes used in all sections (sky blue)
    nodes_used = set().union(*[set(picked) for picked in picked_notes_by_section.values()])
    nx.draw_networkx_nodes(
        G_global, pos, nodelist=nodes_used, node_color="skyblue", node_size=1000, edgecolors="black"
    )
    # Draw edges (from combined picked notes across all sections)
    nx.draw_networkx_edges(G_global, pos, edge_color="gray", width=2, arrows=True, arrowsize=20)
    # Add labels
    nx.draw_networkx_labels(G_global, pos, font_size=12, font_weight="bold")

    # Add title
    plt.title("Global Melody Graph", fontsize=18, fontweight="bold")
    plt.axis("off")

    # Save figure
    global_file_path = os.path.join(folder_name, "global_melody_graph.png")
    plt.savefig(global_file_path, bbox_inches='tight', dpi=300)
    print(f"Global melody graph saved at: {global_file_path}")
    plt.close()


def create_midi_file(melody_notes, folder_name='createdFiles', filename='melody.mid'):
    """
    Save the melody to a MIDI file in the specified folder.
    Args:
        melody_notes (list): A list of dictionaries for melody notes.
        folder_name (str): The name of the folder to save the file in.
        filename (str): The name of the MIDI file.
    Returns:
        str: The full path of the saved MIDI file.
    """
    # Ensure the folder exists
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, filename)

    # Create a MIDI file
    mid = MidiFile()
    melody_track = MidiTrack()
    mid.tracks.append(melody_track)

    for note_data in melody_notes:
        melody_track.append(Message('note_on', note=note_data["note"], velocity=note_data["velocity"], time=0))
        melody_track.append(Message('note_off', note=note_data["note"], velocity=note_data["velocity"], time=note_data["duration"]))
    
    # Save the MIDI file
    mid.save(file_path)
    print(f"MIDI file saved as '{file_path}'")
    return file_path


def play_midi_pygame(file_path):
    """
    Play a MIDI file using pygame.
    Args:
        file_path (str): The full path to the MIDI file to play.
    """
    print(f"Playing MIDI file: {file_path}")
    pygame.init()
    pygame.mixer.init()
    
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing MIDI file: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()

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


# Generate melody notes and record picked notes by section
melody_notes, picked_notes_by_section = generate_melody_pattern_with_recording(lyrics, melody_map)

# Visualize and save melody graphs
visualize_melody_graphs(picked_notes_by_section, melody_map)

# Combine melody and drum tracks into a MIDI file
midi_file = create_midi_file(melody_notes)

# Play the MIDI file
print("Attempting to play the combined MIDI file...")
play_midi_pygame(midi_file)
print(f"Combined MIDI file '{midi_file}' has been created.")
