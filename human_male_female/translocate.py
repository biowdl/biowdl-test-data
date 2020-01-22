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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from typing import Iterable, NamedTuple

from Bio.SeqIO.FastaIO import FastaIterator
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("Translocate a part of a "
                                     "chromosome. Prints target chromosome.")
    parser.add_argument("fasta", type=str,
                        help="Fasta file to mutate")
    parser.add_argument("source", type=str,
                        help="which region is translocated. In the following "
                             "format: {CHR}:{START}-{END}. For example: "
                             "chr1:1-20000. Positions are 0-based")
    parser.add_argument("target", type=str,
                        help="Target location on receiving chromosome. In the "
                             "following format: {CHR}:{START}-{END}. For "
                             "example: chr2:123200-123500. Positions are "
                             "0-based. This region will be replaced with src's "
                             "sequence.")
    return parser


class Position(NamedTuple):
    chromosome: str
    start: int
    end: int

    @classmethod
    def from_string(cls, string):
        try:
            chromosome, positions = string.split(":")
            start, end = positions.split("-")
        except ValueError:
            raise ValueError(f"Could not parse {string}. Is it in "
                             f"CHR:START-END format?")
        return cls(chromosome, int(start), int(end))


def mutate(genome: Iterable[SeqRecord], source: Position, target: Position
           ) -> SeqRecord:
    source_seq = None
    original_target_seq = None
    original_target = None
    for chromosome in genome:
        if chromosome.id == source.chromosome:
            source_seq = str(chromosome.seq)[source.start: source.end]
        elif chromosome.id == target.chromosome:
            original_target_seq = str(chromosome.seq)
            original_target = chromosome
        if source_seq is not None and original_target_seq is not None:
            break
    else:  # no break
        if source_seq is None:
            raise ValueError(f"'{source.chromosome}' not found in genome.")
        elif original_target_seq is None:
            raise ValueError(f"'{target.chromosome}' not found in genome.")
        else:
            raise RuntimeError("Unexpected code path. "
                               "Please contact developers.")
    mutated_seq = (original_target_seq[:target.start] + source_seq +
                   original_target_seq[target.end:])
    return SeqRecord(Seq(mutated_seq),
                     id=original_target.id,
                     name=original_target.name,
                     description=original_target.description)


def main():
    args = argument_parser().parse_args()
    source = Position.from_string(args.source)
    target = Position.from_string(args.target)
    with open(args.fasta, "rt") as fasta_h:
        records = FastaIterator(fasta_h)
        result = mutate(records, source, target)
    print(result.format("fasta"), end='')


if __name__ == "__main__":
    main()
