import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import argparse
import os

# Confidence score
def compute_confidence(row):
    return row['support'] * row['score']

def main():
    # Parser
    p = argparse.ArgumentParser()
    p.add_argument("csv", help="Input CSV")
    p.add_argument("-o", "--out", default="visuals/circle_confidence.png", help="Output confidence plot path")
    args = p.parse_args()

    # Load CSV
    df = pd.read_csv(args.csv) 

    # Confidence
    df['confidence'] = df.apply(compute_confidence, axis=1)

    # Stem plot of confidence
    plt.figure(figsize=(10, 6))
    plt.stem(df['start'], df['confidence'], basefmt=" ")
    plt.title("Circle Confidence Across Genome")
    plt.xlabel("Genomic Start Position")
    plt.ylabel("Confidence Score")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    plt.savefig(args.out)
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.violinplot(x='score', y='support', data=df, inner='box')
    plt.title("Support Distribution by Score")
    plt.xlabel("Score")
    plt.ylabel("Support")
    plt.tight_layout()
    plt.savefig(os.path.splitext(args.out)[0] + "_violin_support_by_score.png")
    plt.close()

if __name__ == '__main__':
    main()
