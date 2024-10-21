import json
import sys
import os


def load_json_file(filepath):
    """Load and return content from a JSON file."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON file '{filepath}'. {e}")
            sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <proof_file.json> <cairo_verifier_input.json>")
        sys.exit(1)

    proof_file = sys.argv[1]
    verifier_file = sys.argv[2]

    proof_content = load_json_file(proof_file)

    with open(verifier_file, "w") as f:
        json.dump({"proof": proof_content}, f, indent=4)

    print(f"Successfully updated '{verifier_file}' with the proof from '{proof_file}'.")


if __name__ == "__main__":
    main()
