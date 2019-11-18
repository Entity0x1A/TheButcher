#!/usr/bin/python
import sys
import argparse
import os


def banner():
    banner = '''
 _______ _          ____        _       _
|__   __| |        |  _ \      | |     | |
   | |  | |__   ___| |_) |_   _| |_ ___| |__   ___ _ __
   | |  | '_ \ / _ \  _ <| | | | __/ __| '_ \ / _ \ '__|
   | |  | | | |  __/ |_) | |_| | || (__| | | |  __/ |
   |_|  |_| |_|\___|____/ \__,_|\__\___|_| |_|\___|_|

        >> File Splitting Utility
        >> https://www.github.com/gh0x0st
    '''
    print banner


def split_line(to_split, out_dir):
    print('[*] Splitting {} by line').format(to_split)
    file_count = 0
    for line in open(to_split, 'r'):
        chunk_path = os.path.join(out_dir, os.path.basename(to_split) + '_' + str(file_count))
        with open(chunk_path, 'w') as wf:
            wf.write(line)
            wf.close()
            file_count += 1
    print('[*] Derived {} file(s) from {} in {}').format(file_count, to_split, out_dir)


def split_bytes(to_split, bytes, out_dir):
    print('[*] Splitting {} by {} bytes').format(to_split, bytes)
    file_count = 0
    with open(to_split) as rf:
        chunk = rf.read(bytes)
        while chunk:
            file_count += 1
            chunk_path = os.path.join(out_dir, os.path.basename(to_split) + '_' + str(file_count))
            with open(chunk_path, 'w') as wf:
                wf.write(chunk)
                wf.close()
            chunk = rf.read(bytes)
    print('[*] Derived {} file(s) from {} in {}').format(file_count, to_split, out_dir)


def main():
    # build the arguments
    parser = argparse.ArgumentParser(
        description='A utility to split files into specified byte sized chunks or line-by-line derivatives.')
    parser.add_argument('-t', '--target', action='store', type=str, dest='target_file', help='Target file to be split')
    parser.add_argument('-s', '--split', action='store', type=str, nargs='?', const='line',
                        help='Amount of bytes to split by. Defaults to line-by-line.')
    parser.add_argument('-o', '--output', action='store', type=str,
                        dest='out_dir', help='Output directory for file chunks')
    parser.add_argument('-q', '--quiet', action='store_true', help='Does not print the banner')

    # cycle through argument input
    args = parser.parse_args()

    # check to omit the banner
    if not args.quiet:
        banner()

    # print help and exit if no parameters are given
    if len(sys.argv) == 1:
        parser.print_help()
        example_text = '''\nexamples:
        python thebutcher.py -t binary.exe --split
        python thebutcher.py -t binary.exe --split 100 --output /root/Desktop/split_files
        '''
        print(example_text)
        sys.exit(1)

    # ensure file exists
    if not os.access(args.target_file, os.F_OK):
        print('[!] {} does not exist. Exiting.').format(args.target_file)
        sys.exit(1)

    # ensure we can read the file
    if not os.access(args.target_file, os.R_OK):
        print('[!] {} is not accessible to be read. Exiting.').format(args.target_file)
        sys.exit(1)

    # absolute path for directory
    if args.out_dir:
        out_dir = os.path.abspath(args.out_dir)
    else:
        out_dir = os.path.dirname(os.path.abspath(args.target_file))

    # absolute path for target file
    if args.target_file:
        to_split = os.path.abspath(args.target_file)

    # ensure output directory exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # ahh, fresh meat.
    if args.split is None:
        print('[!] No actions provided. Exiting.')
        sys.exit(1)
    elif args.split == 'line':
        split_line(to_split, out_dir)
    elif int(args.split):
        split_bytes(to_split, int(args.split), out_dir)


if __name__ == '__main__':
    main()
