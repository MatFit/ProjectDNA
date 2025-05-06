import pandas as pd
import matplotlib.pyplot as plt
import argparse

def compute_confidence(row):
    return row['support'] * row['score']

def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv", help="Input BAM")
    p.add_argument("-o", "--out", default="visuals/circle_confidence.png", help="Output CSV")
    args = p.parse_args()

    # Load CSV
    df = pd.read_csv(args.csv) 

    # Confidence
    df['confidence'] = df.apply(compute_confidence, axis=1)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.stem(df['start'], df['confidence'], basefmt=" ")
    plt.title("Circle Confidence Across Genome")
    plt.xlabel("Genomic Start Position")
    plt.ylabel("Confidence Score")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(args.out)
    

if __name__ == '__main__':
    main()
