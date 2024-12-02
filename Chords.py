import networkx as nx
import matplotlib.pyplot as plt
import random
from midiutil import MIDIFile
import pygame
import os
from time import sleep

class ChordProgressionGenerator:
    def __init__(self):
        # Previous initialization code remains the same
        self.keys = {
            'C': {
                'I': ['C', 'E', 'G'],
                'ii': ['D', 'F', 'A'],
                'iii': ['E', 'G', 'B'],
                'IV': ['F', 'A', 'C'],
                'V': ['G', 'B', 'D'],
                'vi': ['A', 'C', 'E'],
                'viio': ['B', 'D', 'F']
            },
            'Am': {  # Relative minor of C
                'i': ['A', 'C', 'E'],
                'iio': ['B', 'D', 'F'],
                'III': ['C', 'E', 'G'],
                'iv': ['D', 'F', 'A'],
                'v': ['E', 'G', 'B'],
                'VI': ['F', 'A', 'C'],
                'VII': ['G', 'B', 'D'],
                'V': ['E', 'G#', 'B']  # Added dominant with raised third
            }
        }
        
        self.note_to_midi = {
            'C': 60, 'D': 62, 'E': 64, 'F': 65,
            'G': 67, 'G#': 68, 'A': 69, 'B': 71
        }
        
        self.create_chord_graphs()
        
    def create_chord_graphs(self):
        """Create directed graphs for different keys"""
        self.graphs = {}
        
        # Create graph for C major
        self.graphs['C'] = nx.DiGraph()
        c_major_edges = [
            ('I', 'IV', 0.3), ('I', 'V', 0.3), ('I', 'vi', 0.2),
            ('ii', 'V', 0.5), ('ii', 'IV', 0.3),
            ('iii', 'vi', 0.4), ('iii', 'IV', 0.3),
            ('IV', 'V', 0.4), ('IV', 'I', 0.3),
            ('V', 'I', 0.5), ('V', 'vi', 0.3),
            ('vi', 'IV', 0.3), ('vi', 'ii', 0.3), ('vi', 'V', 0.2),
            ('viio', 'I', 0.6), ('viio', 'V', 0.2)
        ]
        self.graphs['C'].add_weighted_edges_from(c_major_edges)
        
        # Create graph for A minor
        self.graphs['Am'] = nx.DiGraph()
        a_minor_edges = [
            ('i', 'iv', 0.3), ('i', 'V', 0.3), ('i', 'VII', 0.2),
            ('iio', 'V', 0.4), ('iio', 'i', 0.3),
            ('III', 'VI', 0.3), ('III', 'iv', 0.3),
            ('iv', 'V', 0.4), ('iv', 'i', 0.3),
            ('v', 'i', 0.4), ('v', 'VI', 0.3),
            ('VI', 'III', 0.3), ('VI', 'iio', 0.2), ('VI', 'V', 0.2),
            ('VII', 'III', 0.3), ('VII', 'i', 0.4),
            ('V', 'i', 0.5), ('V', 'VI', 0.3)  # Added dominant chord transitions
        ]
        self.graphs['Am'].add_weighted_edges_from(a_minor_edges)
    
    def visualize_graphs(self, save_path_prefix='chord_graph', display=True):
        """Visualize and save chord progression graphs for both keys"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        # Draw C major graph
        pos_c = nx.spring_layout(self.graphs['C'])
        ax1.set_title("C Major Chord Progression Graph", pad=20)
        
        # Draw nodes for C major
        nx.draw_networkx_nodes(self.graphs['C'], pos_c, node_color='lightblue', 
                             node_size=2000, alpha=0.7, ax=ax1)
        
        # Draw edges for C major
        edges_c = self.graphs['C'].edges()
        weights_c = [self.graphs['C'][u][v]['weight'] * 2 for u, v in edges_c]
        nx.draw_networkx_edges(self.graphs['C'], pos_c, width=weights_c, alpha=0.6, 
                             edge_color='gray', arrows=True, arrowsize=20, ax=ax1)
        
        # Add labels for C major
        nx.draw_networkx_labels(self.graphs['C'], pos_c, font_size=12, ax=ax1)
        
        # Draw A minor graph
        pos_am = nx.spring_layout(self.graphs['Am'])
        ax2.set_title("A Minor Chord Progression Graph", pad=20)
        
        # Draw nodes for A minor
        nx.draw_networkx_nodes(self.graphs['Am'], pos_am, node_color='lightpink', 
                             node_size=2000, alpha=0.7, ax=ax2)
        
        # Draw edges for A minor
        edges_am = self.graphs['Am'].edges()
        weights_am = [self.graphs['Am'][u][v]['weight'] * 2 for u, v in edges_am]
        nx.draw_networkx_edges(self.graphs['Am'], pos_am, width=weights_am, alpha=0.6, 
                             edge_color='gray', arrows=True, arrowsize=20, ax=ax2)
        
        # Add labels for A minor
        nx.draw_networkx_labels(self.graphs['Am'], pos_am, font_size=12, ax=ax2)
        
        ax1.axis('off')
        ax2.axis('off')
        
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(f'{save_path_prefix}_combined.png', bbox_inches='tight', dpi=300)
        
        if display:
            plt.show()
        else:
            plt.close()

    # Rest of the class methods remain the same
    def generate_section(self, key, length=4, start=None):
        """Generate a chord progression in specified key"""
        if start is None:
            start = 'I' if key == 'C' else 'i'
            
        progression = [start]
        current = start
        graph = self.graphs[key]
        
        for _ in range(length - 1):
            neighbors = list(graph.neighbors(current))
            if not neighbors:
                break
                
            weights = [graph[current][next_chord]['weight'] for next_chord in neighbors]
            current = random.choices(neighbors, weights=weights)[0]
            progression.append(current)
            
        return progression
    
    def create_multi_section_midi(self, sections, filename='full_progression.mid'):
        """Create a MIDI file with multiple sections"""
        mf = MIDIFile(1)
        track = 0
        time = 0
        mf.addTrackName(track, time, "Multi-Section Progression")
        mf.addTempo(track, time, 120)
        
        for section_key, progression in sections:
            # Add each chord to the MIDI file
            for chord_numeral in progression:
                chord_notes = self.keys[section_key][chord_numeral]
                for note in chord_notes:
                    midi_note = self.note_to_midi[note]
                    mf.addNote(track, 0, midi_note, time, 2, 100)
                time += 2
            
            # Add a slight pause between sections
            time += 1
            
        with open(filename, 'wb') as outf:
            mf.writeFile(outf)
    
    def play_midi(self, filename='full_progression.mid'):
        """Play the generated MIDI file"""
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            sleep(1)

def main():
    # Initialize the generator
    generator = ChordProgressionGenerator()
    
    # Generate sections
    verse = generator.generate_section('C', length=4)
    chorus = generator.generate_section('C', length=4)
    bridge = generator.generate_section('Am', length=4)
    
    # Print the progressions
    print(f"Verse (C major): {' -> '.join(verse)}")
    print(f"Chorus (C major): {' -> '.join(chorus)}")
    print(f"Bridge (A minor): {' -> '.join(bridge)}")
    
    # Visualize and display the graphs
    print("\nDisplaying chord progression graphs...")
    generator.visualize_graphs(display=True)
    print("Graph visualization saved as 'chord_graph_combined.png'")
    
    # Create and play complete progression
    sections = [
        ('C', verse),
        ('C', chorus),
        ('Am', bridge),
        ('C', chorus)
    ]
    
    generator.create_multi_section_midi(sections)
    print("\nMIDI file created as 'full_progression.mid'")
    print("Playing full progression...")
    generator.play_midi()

if __name__ == "__main__":
    main()
