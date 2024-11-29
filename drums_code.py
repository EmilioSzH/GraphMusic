from turtle import width
import networkx as nx
import matplotlib.pyplot as plt
import pygame
import time
from midiutil import MIDIFile

# Define nodes (drum beats) and edges (beat progression)
nodes = ["Bass", "Snare", "Hi-Hat", "Clap", "Tom", "Cymbal"]
edges = [
    ("Bass", "Snare"),
    ("Snare", "Hi-Hat"),
    ("Hi-Hat", "Clap"),
    ("Clap", "Tom"),
    ("Tom", "Cymbal"),
    ("Cymbal", "Bass"),
    ("Hi-Hat", "Hi-Hat"),  # Self-loop for consistent hi-hat patterns
    ("Bass", "Bass"),      # Self-loop for steady bass
    ("Snare", "Hi-Hat"),   # Additional path for variation
    ("Hi-Hat", "Bass"),    # Variation connecting Hi-Hat to Bass
]

# Create the directed multigraph
G = nx.MultiDiGraph()
G.add_edges_from(edges)

# Visualize the graph
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G, pos, with_labels=True, node_size=2500, node_color="lavender", 
    font_size=10, font_weight="bold", edge_color="indigo", width = 1.5,
)
plt.title("Drum Beat Progression Multigraph", fontsize=20)
plt.show()

# Define drum mappings
drum_map = {
    "Bass": 35,    # Acoustic Bass Drum
    "Snare": 38,   # Acoustic Snare
    "Hi-Hat": 42,  # Closed Hi-Hat
    "Clap": 39,    # Hand Clap
    "Tom": 45,     # Low Tom
    "Cymbal": 49,  # Crash Cymbal 1
}

# Define patterns for each section of the lyrics
song_structure = {
    "Verse 1": ["Bass", "Snare", "Hi-Hat", "Clap"],
    "Chorus": ["Hi-Hat", "Snare", "Clap", "Tom", "Cymbal"],
    "Verse 2": ["Bass", "Hi-Hat", "Snare", "Tom"],
    "Bridge": ["Cymbal", "Hi-Hat", "Bass", "Clap"],
}

# Define lyrics with corresponding sections
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

# Function to create the MIDI file
def create_song_midi(graph, drum_map, song_structure, lyrics, filename="song_drums_multigraph.mid", tempo=120):
    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 9  # Drum channel
    volume = 100

    midi.addTempo(track, time, tempo)

    for line, section in lyrics:
        print(f"Processing line: {line} ({section})")
        pattern = song_structure.get(section, [])
        for beat in pattern:
            if beat in drum_map:
                midi.addNote(track, channel, drum_map[beat], time, 0.5, volume)
                time += 0.5

    # Save the MIDI file
    with open(filename, "wb") as f:
        midi.writeFile(f)
    print(f"MIDI file saved as {filename}")

# Create the MIDI file
create_song_midi(G, drum_map, song_structure, lyrics)

# Function to play the MIDI file
def play_midi(filename):
    """Play a MIDI file using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    print(f"Playing {filename}...")
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Play the generated MIDI
play_midi("song_drums_multigraph.mid")
