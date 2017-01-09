from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import codecs
import csv

def str2bool(val):
    """
    Helper method to convert string to bool
    """
    if val is None:
        return False
    val = val.lower().strip()
    if val in ['true', 't', 'yes', 'y', '1', 'on']:
        return True
    elif val in ['false', 'f', 'no', 'n', '0', 'off']:
        return False

def main():
    """
    Selects the specified columns from the input file
    """

    # Parse command line args
    parser = argparse.ArgumentParser(description='Selects the given columns')

    parser.add_argument(
        '-i', '--input', required=True,
        help='Path to input file')
    parser.add_argument(
        '-c', '--cols', required=True, type=str, default=0, 
        help='Comma separated list of columns indices to select')
    parser.add_argument(
        '-d', '--delimiter', required=True, default='\t', 
        help='Column delimiter')
    parser.add_argument(
        '-header', '--hasheader', required=False, type=str2bool,
        default='False', help='File has header row?')
    parser.add_argument('-o', '--output', required=True, help='Path to output file')

    args = parser.parse_args()
    # Unescape the delimiter
    args.delimiter = codecs.decode(args.delimiter, "unicode_escape")
    # Parse cols into list of ints
    args.cols = [int(x) for x in args.cols.split(',')]

    # Convert args to dict
    vargs = vars(args)

    print("\nArguments:")
    for arg in vargs:
        print("{}={}".format(arg, getattr(args, arg)))

    # Read the input file
    with open(args.input, 'r') as inputfile:
        with open(args.output, 'w') as outputfile:
            
            reader = csv.reader(inputfile, delimiter=args.delimiter)
            writer = csv.writer(outputfile, delimiter=args.delimiter)

            # If has header, write it unprocessed
            if args.hasheader:
                headers = next(reader, None)
                if headers:
                    writer.writerow(headers)

            print("\nProcessing input")
            for row in reader:
                cols = []
                for idx, col in enumerate(row):
                    if idx in args.cols:
                        cols.append(col)
                writer.writerow(cols)

    print("\nDone. Bye!")

if __name__ == '__main__':
    main()