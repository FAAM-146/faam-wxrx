import argparse

from wxrx.read_wxrx import process


def main():
    parser = argparse.ArgumentParser(description='Process raw WxRx data from the FAAM aircraft.')

    parser.add_argument('--tmpfile', '-t', metavar='tmpfile', type=str, nargs='+', action='store',
                        required=True, help='One or more raw ARINC 708 tmp file(s)')

    parser.add_argument('--logfile', '-l', metavar='logfile', type=str, nargs=1, action='store',
                        required=True, help='The log file')

    parser.add_argument('--corefile', '-c', metavar='corefile', type=str, nargs=1, action='store',
                        required=True, help='The FAAM (1hz) core file')
    
    parser.add_argument('--output-dir', '-o', metavar='output_dir', type=str, nargs=1, action='store',
                        help='The output directory', default=['.'])

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Run quietly (no consile output)', default=False)

    args = parser.parse_args()
    process(args.tmpfile, args.logfile[0], args.corefile[0], with_progress=not args.quiet)


if __name__ == '__main__':
    main()
