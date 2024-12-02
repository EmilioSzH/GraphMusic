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

def generate_melody_pattern(lyrics, melody_map):
    """
    Generate a semi-random melody pattern based on lyrical structure and melody map.
    """
    melody_sequence = []
    current_section = None

    for line, section in lyrics:
        if section != current_section:
            current_section = section
        
        # Fetch the melody for the current section
        section_melody = melody_map.get(section, [])
        
        # Choose 2-4 notes for each line, preserving their articulation if specified
        line_melody = random.choices(section_melody, k=random.randint(2, 4))
        melody_sequence.extend(line_melody)
    
    return melody_sequence


def visualize_melody_with_full_nodes(melody_map, folder_name='createdFiles'):
    """
    Create and save melody graphs for each section, ensuring all nodes appear in all graphs,
    but highlighting only the nodes used in each specific section.

    Args:
        melody_map (dict): A dictionary where keys are sections (e.g., "Verse 1") 
                           and values are lists of dictionaries representing notes.
        folder_name (str): The folder where the graphs will be saved.
    """
    # Ensure the folder exists
    os.makedirs(folder_name, exist_ok=True)

    # Helper function to convert MIDI note numbers to note names
    def midi_to_note_name(midi_note):
        NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = midi_note // 12 - 1
        note = NOTE_NAMES[midi_note % 12]
        return f"{note}{octave}"
    
    # Collect all unique nodes across all sections
    all_notes = set()
    for notes in melody_map.values():
        for note_data in notes:
            all_notes.add(midi_to_note_name(note_data["note"]))

    # Visualize melody graph for each section
    for section, notes in melody_map.items():
        G = nx.DiGraph()
        
        # Add all unique notes as nodes (to ensure all nodes appear in every graph)
        for note in all_notes:
            G.add_node(note)
        
        # Add edges for the section
        section_nodes = set()
        for i in range(len(notes) - 1):
            current_note = midi_to_note_name(notes[i]["note"])
            next_note = midi_to_note_name(notes[i + 1]["note"])
            section_nodes.update([current_note, next_note])
            
            # Add edge
            if G.has_edge(current_note, next_note):
                G[current_note][next_note]["weight"] += 1
            else:
                G.add_edge(current_note, next_note, weight=1)
        
        # Create visualization
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, k=0.8, iterations=50)
        
        # Draw all nodes in gray
        nx.draw_networkx_nodes(
            G, pos, 
            nodelist=all_notes, 
            node_color="lightgray", 
            node_size=1000, 
            edgecolors="black"
        )
        
        # Highlight nodes used in the current section in blue
        nx.draw_networkx_nodes(
            G, pos, 
            nodelist=section_nodes, 
            node_color="skyblue", 
            node_size=1000, 
            edgecolors="black"
        )
        
        # Draw edges with thickness proportional to weight
        edge_weights = [G[u][v]["weight"] for u, v in G.edges()]
        nx.draw_networkx_edges(
            G, pos, 
            edge_color="gray", 
            width=[2 + weight * 0.5 for weight in edge_weights],
            arrows=True, 
            arrowsize=20
        )
        
        # Add labels to nodes
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
        
        # Add title for the section
        plt.title(f"Melody Graph - {section}", fontsize=20, fontweight="bold", pad=20)
        plt.axis("off")

        # Save the graph in the createdFiles folder
        file_path = os.path.join(folder_name, f"melody_{section.replace(' ', '_')}_graph.png")
        plt.savefig(file_path, bbox_inches='tight', dpi=300)
        print(f"Graph for '{section}' saved as '{file_path}'")

        plt.close()

# Example usage
visualize_melody_with_full_nodes(melody_map)


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

# Generate melody notes
melody_notes = generate_melody_pattern(lyrics, melody_map)

# Combine melody and drum tracks into a MIDI file
midi_file = create_midi_file(melody_notes)

# Play the MIDI file
print("Attempting to play the combined MIDI file...")
play_midi_pygame(midi_file)
print(f"Combined MIDI file '{midi_file}' has been created.")