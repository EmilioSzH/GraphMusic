import yaml
import subprocess

# Load the YAML file
with open('program_sequence.yml', 'r') as f:
    sequence = yaml.safe_load(f)['sequence']

# Execute each step in the sequence
for step in sequence:
    print(f"Step: {step['name']}")
    print(f"Description: {step['description']}")
    
    # Run the script
    result = subprocess.run(step['script'], shell=True)
    
    # Check if the step succeeded
    if result.returncode != 0:
        print(f"Error: Step '{step['name']}' failed!")
        break
    
    print(f"Output file: {step['output']}\n")
