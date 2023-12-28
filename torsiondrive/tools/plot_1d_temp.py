#!/usr/bin/env python
# coding: utf-8

import sys
import argparse


def check_dependencies():
    missing_dependencies = []

    # Check for Seaborn
    try:
        import seaborn
    except ImportError:
        missing_dependencies.append("Seaborn (install via 'conda install seaborn')")

    # Check for Matplotlib
    try:
        import matplotlib
    except ImportError:
        missing_dependencies.append(
            "Matplotlib (install via 'conda install matplotlib')"
        )

    return missing_dependencies


def main(args):
    # Read data from the log file
    energies = {}
    try:
        with open(args.input_file) as file:
            for line in file:
                if "First" in line or "decreased" in line:
                    splitted = line.split()
                    angle_index = 4 if "First" in line else 3
                    energy_index = 6 if "First" in line else 8

                    angle = int(splitted[angle_index].strip("(").strip(")").strip(","))
                    energy = float(splitted[energy_index])
                    energies[angle] = energy
    except FileNotFoundError:
        print(f"Error: The specified log file '{args.input_file}' was not found.")
        return

    # Normalize energies
    minimum = min(energies.values())
    for key in energies:
        energies[key] -= minimum
        energies[key] *= 627.5

    # Prepare data for plotting
    x = list(energies.keys())
    y = list(energies.values())

    # Create a line plot
    sns.set_theme()
    sns.set_style("dark")
    sns.set_context("talk")
    sns.set_palette("muted")
    plt.figure(figsize=(10, 6))
    plot = sns.lineplot(x=x, y=y, marker="o")
    plot.set_xlabel("Angle")
    plot.set_ylabel("Energy (kcal/mol)")
    plt.title("Energy Profile")
    plt.grid(True)

    # Save the plot with the user-specified filename
    plt.savefig(args.output_file)


if __name__ == "__main__":
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        sys.exit("Error: Missing dependencies:\n- " + "\n- ".join(missing_deps))

    import seaborn as sns
    import matplotlib.pyplot as plt

    # Setup argparse for command line arguments
    parser = argparse.ArgumentParser(description="Plot energy profile from a log file.")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="td_log.log",
        help="Path to the input log file. Default is 'td_log.log'.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="scan.pdf",
        help="Path to the output file. Default is 'scan.pdf'.",
    )
    args = parser.parse_args()

    # Run the main function
    main(args)
