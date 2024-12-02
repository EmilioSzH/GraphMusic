from mido import MidiFile, MidiTrack, MetaMessage
import pygame
from time import sleep
import os

def merge_midi_files(input_files, output_file):
    """
    Merge multiple MIDI files into a single MIDI file.
    """
    # Check if all input files exist
    for file in input_files:
        if not os.path.exists(file):
            print(f"Error: File '{file}' not found.")
            return
    
    # Create a new MIDI file for merging
    merged_midi = MidiFile()

    # Iterate through each input file and add its tracks to the merged MIDI
    for file in input_files:
        midi = MidiFile(file)
        for i, track in enumerate(midi.tracks):
            merged_track = MidiTrack()
            merged_track.append(MetaMessage('track_name', name=f"{file}-Track-{i}"))
            merged_track.extend(track)
            merged_midi.tracks.append(merged_track)
    
    # Save the merged MIDI file
    merged_midi.save(output_file)
    print(f"Merged MIDI file saved as '{output_file}'")

def play_midi_file(filename):
    """
    Play a MIDI file using pygame.
    """
    print(f"Playing MIDI file: {filename}")
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            sleep(1)
    except Exception as e:
        print(f"Error playing MIDI file: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()

# Specify the input files
input_files = [
    'createdFiles/chords.mid',
    'createdFiles/melody.mid',
    'createdFiles/drum_pattern.mid'
]

# Specify the output file
output_file = 'createdFiles/merged_song.mid'

# Merge the files
merge_midi_files(input_files, output_file)

# Play the merged MIDI file if it exists
if os.path.exists(output_file):
    play_midi_file(output_file)
else:
    print(f"Error: Merged file '{output_file}' not created.")
