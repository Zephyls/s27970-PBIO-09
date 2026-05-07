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

def ask_yes_no(prompt: str) -> bool:
    """Return True for a yes answer and False for a no answer."""
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False

        print("Error: enter 'y' or 'n'.")

#5.2
def read_nucleotide_distribution() -> dict:
    """Read and validate the percentage distribution of A, C, G and T from the user."""
    while True:
        distribution = {}

        try:
            for nucleotide in NUCLEOTIDES:
                user_input = input(f"Enter percentage for {nucleotide}: ").strip().replace(",", ".")
                value = float(user_input)
                if value < 0:
                    raise ValueError
                distribution[nucleotide] = value
        except ValueError:
            print("Error: enter non-negative numeric values.")
            continue

        total = sum(distribution.values())
        if abs(total - 100.0) < 0.0001:
            return distribution

        print(f"Error: the total percentage must be 100, but now it is {total:.2f}.")

def generate_sequence_with_distribution(length: int, distribution: dict) -> str:
    """Generate a random DNA sequence using a user-defined nucleotide distribution."""
    weights = [distribution[nucleotide] for nucleotide in NUCLEOTIDES]
    return "".join(random.choices(NUCLEOTIDES, weights=weights, k=length))

#5.3
def get_motif_from_user() -> str:
    """Read a DNA motif from the user; an empty input means that motif search is skipped."""
    while True:
        motif = input("Enter a motif to search for, for example ATG, or press Enter to skip: ").strip().upper()

        if motif == "":
            return ""

        if all(char in NUCLEOTIDES for char in motif):
            return motif

        print("Error: the motif can contain only A, C, G and T.")

def find_motif_positions(sequence: str, motif: str) -> list:
    """Return all motif positions in the sequence using 1-based biological indexing."""
    motif = motif.upper()
    positions = []

    for index in range(0, len(sequence) - len(motif) + 1):
        if sequence[index:index + len(motif)] == motif:
            positions.append(index + 1)

    return positions

#5.4
def complement_sequence(sequence: str) -> str:
    """Return the complementary DNA strand."""
    translation_table = str.maketrans("ACGT", "TGCA")
    return sequence.translate(translation_table)

def reverse_complement_sequence(sequence: str) -> str:
    """Return the reverse complementary DNA strand."""
    return complement_sequence(sequence)[::-1]

#5.5
def transcribe_dna_to_mrna(sequence: str) -> str:
    """Return an mRNA sequence created by replacing T with U."""
    return sequence.replace("T", "U")
