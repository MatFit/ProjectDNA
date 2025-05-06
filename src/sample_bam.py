import pysam

# Paths
input_bam = "data/NA12878.chrom20.ILLUMINA.bwa.CEU.low_coverage.20121211.bam"
output_bam = "data/sample.bam"

# Number of reads to commit to repo w/ something for users to test on
SAMPLE_SIZE = 1000

with pysam.AlignmentFile(input_bam, "rb") as in_bam:
    with pysam.AlignmentFile(output_bam, "wb", template=in_bam) as out_bam:
        for i, read in enumerate(in_bam):
            if i >= SAMPLE_SIZE:
                break
            out_bam.write(read)

print(f"Sample BAM created at {output_bam}")
