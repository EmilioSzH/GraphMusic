from mido import Message, MidiFile, MidiTrack
import random
import pygame

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

DRUM_NOTES = {
    "Bass": 35,    # Acoustic Bass Drum
    "Snare": 38,   # Acoustic Snare
    "Hi-Hat": 42,  # Closed Hi-Hat
    "Clap": 39,    # Hand Clap
    "Tom": 45,     # Low Tom
    "Cymbal": 49,  # Crash Cymbal 1
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

def create_combined_midi_file(melody_notes, drum_sequence):
    """
    Combine melody and drum tracks into a single MIDI file.
    Args:
        melody_notes (list): A list of dictionaries for melody notes.
        drum_sequence (list): A list of drum note names.
    Returns:
        str: The filename of the combined MIDI file.
    """
    mid = MidiFile()
    
    # Create the melody track
    melody_track = MidiTrack()
    mid.tracks.append(melody_track)
    for note_data in melody_notes:
        # Append the 'note_on' message
        melody_track.append(Message('note_on', note=note_data["note"], velocity=note_data["velocity"], time=0))
        # Append the 'note_off' message after the specified duration
        melody_track.append(Message('note_off', note=note_data["note"], velocity=note_data["velocity"], time=note_data["duration"]))
    
    # Create the drum track
    drum_track = MidiTrack()
    mid.tracks.append(drum_track)
    for note_name in drum_sequence:
        note = DRUM_NOTES[note_name]
        drum_track.append(Message('note_on', note=note, velocity=64, time=0, channel=9))
        drum_track.append(Message('note_off', note=note, velocity=64, time=480, channel=9))
    
    # Save the combined MIDI file
    combined_midi_filename = 'combined_song.mid'
    mid.save(combined_midi_filename)
    return combined_midi_filename


def play_midi_pygame(midi_file):
    """
    Play MIDI file using pygame
    """
    pygame.init()
    pygame.mixer.init()
    
    try:
        pygame.mixer.music.load(midi_file)
        pygame.mixer.music.play()
        
        # Wait until playback is complete
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing MIDI: {e}")
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

# Generate melody notes and drum sequence
melody_notes = generate_melody_pattern(lyrics, melody_map)
full_drum_sequence = generate_drum_pattern(lyrics)

# Combine melody and drum tracks into a MIDI file
combined_midi_file = create_combined_midi_file(melody_notes, full_drum_sequence)

# Play the MIDI file
print("Attempting to play the combined MIDI file...")
play_midi_pygame(combined_midi_file)

print(f"Combined MIDI file '{combined_midi_file}' has been created.")