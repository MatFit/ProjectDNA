# Command Line Interface file
import argparse
import detector


def main():
    # Parser
    p = argparse.ArgumentParser()
    p.add_argument("bam", help="Input BAM")
    p.add_argument("-o", "--out", default="csvs/circles.csv", help="Output CSV")
    p.add_argument("--min-score", type=float, default=2.0, help="Minimum circle score")
    args = p.parse_args()

    # Call circles
    circles = detector.call_circles(args.bam, min_score=args.min_score)
    detector.to_csv(circles, args.out)
    print(f"Wrote {len(circles)} circles into {args.out}")


if __name__ == "__main__":
    main()
