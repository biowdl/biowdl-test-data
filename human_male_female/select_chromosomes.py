#!/usr/bin/env python3

# Copyright (c) 2020 Leiden University Medical Center
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from typing import Generator, Set

from Bio.SeqIO.FastaIO import FastaIterator
from Bio.SeqRecord import SeqRecord


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prints chromosomes in a "
                                                 "fasta file in a formatted "
                                                 "way.")
    parser.add_argument("fasta", nargs=1,
                        help="The fasta file to collect chromosomes from.")
    parser.add_argument("chromosome", metavar="chrX", nargs="*",
                        help="Chromosome names to be collected. Can be "
                             "specified multiple times. If not specified will "
                             "print all chromosomes.")
    return parser


def select_chromosomes(fasta_file: str, chromosome_ids: Set[str]
                       ) -> Generator[SeqRecord, None, None]:
    with open(fasta_file, "rt") as fasta_handle:
        for record in FastaIterator(fasta_handle):
            if not chromosome_ids or record.id in chromosome_ids:
                yield record


def main():
    args = argument_parser().parse_args()
    chromosomes = select_chromosomes(args.fasta[0], set(args.chromosome))
    for chromosome in chromosomes:
        print(chromosome.format("fasta"), end="")


if __name__ == "__main__":
    main()
