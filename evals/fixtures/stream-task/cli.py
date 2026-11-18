import argparse

from entries import read_entries


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args(argv)
    print(len(read_entries(args.filename)))


if __name__ == "__main__":
    main()
