import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Run TriplexFPP DNA triplex prediction on a FASTA file.'
    )
    parser.add_argument('--triplex-lib', required=True,
                        help='Directory containing triplex_util.py')
    parser.add_argument('--data-path', required=True,
                        help='Directory where input and output files are stored.')
    parser.add_argument('--input-file', required=True,
                        help='Name of the input FASTA.')
    parser.add_argument('--output-file', required=True,
                        help='Name of the output CSV.')
    args = parser.parse_args()

    lib = Path(args.triplex_lib)
    if not (lib / 'triplex_util.py').exists():
        parser.error(f'triplex_util.py not found in {lib}')
    if not (Path(args.data_path) / args.input_file).exists():
        parser.error(f'Input FASTA not found: {args.input_file}')

    sys.path.insert(0, str(lib))
    from triplex_util import triplex_lncRNA, triplex_DNA, cis_trans

    triplex_DNA(args.input_file, args.data_path, args.output_file)


if __name__ == '__main__':
    main()