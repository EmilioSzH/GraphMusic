# GraphMusic

GraphMusic is an innovative project that uses graph theory and algorithmic techniques to generate and merge MIDI music tracks. It integrates components such as chords, melody, drums, and lyrics to create a cohesive musical piece, with visualizations for each track's graph structure.
This project was developed as the **Final Project for CS5002: Discrete Structures**, demonstrating the power of graph theory in musical creativity.

---

## Features

- **Chords Generation**: Creates MIDI files for chord progressions based on graph-based transitions.
- **Melody Composition**: Generates melody MIDI files using graph structures and note relationships.
- **Drum Patterns**: Produces rhythmic drum sequences saved as MIDI files with corresponding transition graphs.
- **Lyrics Integration**: Utilizes lyrics to guide the structure of musical tracks and highlights lyrical paths in graph visualizations.
- **Track Merging**: Combines chords, melody, and drum tracks into a single cohesive MIDI file.
- **Graph Visualizations**: Displays and saves graph structures for each musical component, showcasing transitions and relationships.
- **Automated Workflow**: Use a YAML configuration file with sequence.py to execute the complete workflow.

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/EmilioSzH/GraphMusic
    cd GraphMusic
    ```

2. **Set up a Python environment**:
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    Required libraries:
    - `mido`
    - `pygame`
    - `matplotlib`
    - `networkx`
    - `pyyaml`
    - `midiutil`

4. **Verify installation**:
    Ensure you have the required environment to run the project:
    ```bash
    python --version  # Should be 3.11 or compatible
    ```

---

## Usage
### 1. Running the Complete Workflow
The project is designed to run automatically using a YAML configuration file and the `sequence.py` script.

1. **Edit the YAML configuration file** (`program_sequence.yml`):
    ```yaml
    sequence:
      - name: "Run Lyrics Processor"
        description: "Process lyrics."
        script: "python lyrics.py"
        output: "lyrics.txt"

      - name: "Run Chords Generator"
        description: "Generate the chords MIDI file."
        script: "python chords.py"
        output: "chords.mid"

      - name: "Run Melody Generator"
        description: "Generate the melody MIDI file."
        script: "python melody.py"
        output: "melody.mid"

      - name: "Run Drum Generator"
        description: "Generate the drum MIDI file."
        script: "python drum.py"
        output: "drum_pattern.mid"

      - name: "Merge MIDI Files"
        description: "Combine all generated MIDI tracks into a single file."
        script: "python merge_tracks.py"
        output: "merged_song.mid"
    ```

2. **Run the sequence script**:
    ```bash
    python sequence.py
    ```
    This will:
    - Generate individual MIDI files for chords, melody, and drums.
    - Create visualizations for each component.
    - Merge the generated tracks into a single MIDI file.
    - Play the final merged MIDI file.

---

### 2. Running Individual Components
You can also generate individual components separately by running their respective scripts.

- **Lyrics**:
    ```bash
    python lyrics.py
    ```
    Outputs:
    - `createdFiles/lyrics.text`
    - `createdFiles/lyrics_verse1_graph.png`
    - `createdFiles/lyrics_bridge_graph.png`
    - `createdFiles/lyrics_verse2_graph.png`
    - `createdFiles/lyrics_chorus_graph.png`
    

- **Chords**:
    ```bash
    python chords.py
    ```
    Outputs:
    - `createdFiles/chords.mid`
    - `createdFiles/chord_graph_combined.png`

- **Melody**:
    ```bash
    python melody.py
    ```
    Outputs:
    - `createdFiles/melody.mid`
    - `createdFiles/melody_Verse_1_graph.png`
    - `createdFiles/melody_Bridge_graph.png`
    - `createdFiles/melody_Verse_2_graph.png`
    - `createdFiles/melody_Chorus_graph.png`

- **Drums**:
    ```bash
    python drums.py
    ```
    Outputs:
    - `createdFiles/drum_pattern.mid`
    - `createdFiles/comprehensive_drum_graph.png`
    - `createdFiles/drum_verse_1_graph.png`
    - `createdFiles/drum_bridge_graph.png`
    - `createdFiles/drum_verse_2_graph.png`
    - `createdFiles/drum_chorus_graph.png`

### 2. Merging Tracks
Once all components are generated, run the `merge_tracks.py` script to merge them:
```bash
python merge_tracks.py
```
Outputs:
- `createdFiles/merged_song.mid`


## Acknowledgements

This project was developed as part of **CS5002: Discrete Structures**, showcasing the application of algorithms and graph theory to creative tasks like music generation. Special thanks to **Dr. Amjad** for the inspiration and guidance throughout the course.
