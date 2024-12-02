from mido import MidiFile, MidiTrack, MetaMessage
import pygame
from time import sleep

def merge_midi_files(input_files, output_file):
    """
    Merge multiple MIDI files into a single MIDI file.

    Args:
        input_files (list): List of MIDI file paths to merge.
        output_file (str): Path for the output merged MIDI file.
    """
    # Create a new MIDI file for merging
    merged_midi = MidiFile()

    # Iterate through each input file and add its tracks to the merged MIDI
    for file in input_files:
        midi = MidiFile(file)
        for i, track in enumerate(midi.tracks):
            # Create a new track in the merged MIDI file
            merged_track = MidiTrack()
            # Add a track name meta message
            merged_track.append(MetaMessage('track_name', name=f"{file}-Track-{i}"))
            # Copy all events from the current track
            merged_track.extend(track)
            # Add the track to the merged MIDI
            merged_midi.tracks.append(merged_track)
    
    # Save the merged MIDI file
    merged_midi.save(output_file)
    print(f"Merged MIDI file saved as '{output_file}'")

def play_midi_file(filename):
    """
    Play a MIDI file using pygame.

    Args:
        filename (str): Path to the MIDI file to play.
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
input_files = ['full_progression.mid', 'melody.mid', 'drum_pattern.mid']  # Replace with your actual file names

# Specify the output file
output_file = 'merged_song.mid'

# Merge the files
merge_midi_files(input_files, output_file)

# Play the merged MIDI file
play_midi_file(output_file)
