from dataclasses import dataclass
from collections import defaultdict
import pysam
import pandas as pd


class Tag:
    def __init__(self, chrom, pos, direction):
        self.chrom = chrom
        self.pos = pos
        self.direction = direction

class Circle:
    def __init__(self, chrom, start, end, support, score):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.support = support
        self.score = score

    def __repr__(self):
        return (f"Circle(chrom={self.chrom}, start={self.start}, "
                f"end={self.end}, support={self.support}, score={self.score})")

    def to_dict(self):
        return {
            "chrom": self.chrom,
            "start": self.start,
            "end": self.end,
            "support": self.support,
            "score": self.score
        }


# Basic CIGAR operations for my sake
# M --> 0 (match)
# I --> 1 (insertion)
# D --> 2 (deletion)
# N --> 3 (skip)
# S --> 4 (soft clip)
# H --> 5 (hard clip)

def softclips(bam_path: str, min_clip: int = 10):
    tags = []

    # Open Bam file
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for read in bam:
            # Skip read if unmapped , 
            if read.is_unmapped or read.is_secondary or read.is_supplementary:
                continue

            # Debug CIGAR operation
            if any(cigar_op[0] == 4 for cigar_op in read.cigartuples):
                print(f"Read {read.query_name} has soft clips: {read.cigarstring}")

            # Fetch CIGAR operations in tuple form (e.g. 5S 90M 5S --> [(4, 5), (0, 90), (4, 5)])
            cigar = read.cigartuples or []

            # Check if soft clipping at start or end is >= min_clip
            # Mark left or right of read
            if cigar and cigar[0][0] == 4 and cigar[0][1] >= min_clip:
                tags.append(Tag(read.reference_name, read.reference_start, "left")) 
            if cigar and cigar[-1][0] == 4 and cigar[-1][1] >= min_clip:
                tags.append(Tag(read.reference_name, read.reference_end, "right"))
    
    return tags

# Circle caller
def call_circles(bam_path: str, window: int = 10, min_support: int = 3, min_score: float = 2.0):
    # Create dictionary bins
    left_bins = defaultdict(list)
    right_bins = defaultdict(list)
    
    # Fetch tags
    tags =  softclips(bam_path)

    for t in tags:
        key = (t.chrom, t.pos // window) 
        (left_bins if t.direction == "left" else right_bins)[key].append(t) # append tuple to it's respective left or right bin

    # Array of circles
    circles = []
    
    for key, ltags in left_bins.items():
        rtags = right_bins.get(key)
        if not rtags:
            continue

        support = len(ltags) + len(rtags)
        if support < min_support:
            continue

        lsorted = sorted(t.pos for t in ltags)
        rsorted = sorted(t.pos for t in rtags)

        lpos = lsorted[len(lsorted) // 2]   # median of left tags
        rpos = rsorted[len(rsorted) // 2]   # median of right tags

        if rpos <= lpos:        # sanity
            continue

        score = support / (rpos - lpos + 1)

        if score < min_score:
            continue
        
        # Store circles
        circles.append(Circle(key[0], lpos, rpos, support, round(score, 3)))

    return circles


# Save to csv
def to_csv(circles, outfile="csvs/circles.csv"):
    pd.DataFrame([c.to_dict() for c in circles]).to_csv(outfile, index=False)
