# Student number: s27970
# Date: 06-05-2026
# Description: Random DNA sequence generator with FASTA output and additional sequence analyses.

import random
from pathlib import Path

NUCLEOTIDES = "ACGT"

def generate_sequence(length: int) -> str:
    """Return a random DNA sequence of the given length using A, C, G and T."""
    return "".join(random.choice(NUCLEOTIDES) for _ in range(length))

def calculate_stats(sequence: str) -> dict:
    """Return nucleotide percentages and GC-content for a DNA sequence."""
    length = len(sequence)
    stats = {}

    for nucleotide in NUCLEOTIDES:
        stats[nucleotide] = sequence.count(nucleotide) / length * 100

    gc_content = (sequence.count("G") + sequence.count("C")) / length * 100
    stats["GC"] = gc_content
    stats["gc_ratio_A"] = gc_content
    return stats

def insert_name(sequence: str, name: str) -> str:
    """Insert the user's name, written in lowercase, at a random position in the sequence."""
    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]

def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Return one FASTA record as a string with sequence lines split to the given width."""
    clean_description = description.strip()

    if clean_description:
        header = f">{seq_id} {clean_description}"
    else:
        header = f">{seq_id}"

    lines = [header]
    for start in range(0, len(sequence), line_width):
        lines.append(sequence[start:start + line_width])

    return "\n".join(lines)

def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Ask the user for an integer from the selected range and repeat until the value is valid."""
    while True:
        user_input = input(prompt).strip()

        try:
            value = int(user_input)
        except ValueError:
            print(f"Error: the value must be an integer from the range [{min_val}, {max_val}].")
            continue

        if min_val <= value <= max_val:
            return value

        print(f"Error: the value must be an integer from the range [{min_val}, {max_val}].")

def validate_sequence_id(prompt: str) -> str:
    """Ask the user for a FASTA sequence ID and validate that it has no whitespace."""
    forbidden_filename_chars = set('/\\:*?"<>|')

    while True:
        seq_id = input(prompt).strip()

        if not seq_id:
            print("Error: sequence ID cannot be empty.")
            continue

        if any(char.isspace() for char in seq_id):
            print("Error: sequence ID cannot contain whitespace.")
            continue

        # The ID is also used as a file name, so these characters are rejected.
        if any(char in forbidden_filename_chars for char in seq_id):
            print("Error: sequence ID contains a character that is not allowed in file names.")
            continue

        return seq_id
