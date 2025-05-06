# Command Line Interface file
import argparse
import detector


def main():
    p = argparse.ArgumentParser()
    p.add_argument("bam", help="Input BAM (indexed)")
    p.add_argument("-o", "--out", default="visuals/circles.csv",
                   help="Output CSV (default visuals/circles.csv)")
    p.add_argument("--min-score", type=float, default=2.0,
                   help="Minimum circle score")
    args = p.parse_args()

    circles = detector.call_circles(args.bam, min_score=args.min_score)
    detector.to_csv(circles, args.out)
    print(f"Wrote {len(circles)} circles → {args.out}")


if __name__ == "__main__":
    main()
