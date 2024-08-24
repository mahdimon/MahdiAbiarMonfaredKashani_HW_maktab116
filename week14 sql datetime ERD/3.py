#!/usr/bin/env python3
from argparse import ArgumentParser
import os
import humanize


def main():
    args = argument_parser()
    if args.dir_path:
        print(humanize.naturalsize(directory_size(args.dir_path , args.file_format),binary=True))
    elif args.file_path:
        print(humanize.naturalsize(file_size(args.file_path),binary=True))


def argument_parser():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', help="dirctory path", dest="dir_path")
    group.add_argument('-f', help="file path", dest="file_path")
    parser.add_argument('-F', help="file format", dest="file_format")

    args = parser.parse_args()
    return args


# def directory_size(dir_path, file_format):
#     total_size = 0
#     for dirpath, _, filenames in os.walk(dir_path):
#         for filename in filenames:
#             _, ext = os.path.splitext(filename)
#             if ext[1:].lower() != file_format.lower():
#                 continue
#             print(filename)
#             filepath = os.path.join(dirpath, filename)
#             try:
#                 total_size += os.path.getsize(filepath)
#             except (FileNotFoundError, PermissionError) as e:
#                 print(f"Error accessing file {filepath}: {e}")
#                 continue
#     return total_size

def directory_size(dir_path, file_format):

    total_size = 0
    try:
        for entry in os.scandir(dir_path):
            
            if entry.is_dir(follow_symlinks=False):
                total_size += directory_size(entry.path, file_format)
                

            elif entry.is_file(follow_symlinks=False):
                _, ext = os.path.splitext(entry.name)
                if file_format and ext[1:].lower() == file_format.lower():
                    total_size += entry.stat().st_size
                elif not file_format:
                    total_size += entry.stat().st_size
                

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing directory {entry.path}: {e}")

    return total_size


def file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing directory {file_path}: {e}")


main()
