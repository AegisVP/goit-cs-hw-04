import argparse
import timeit
from pathlib import Path
from search_t import search_t
from search_m import search_m


parser = argparse.ArgumentParser(description='Search for a string in files')
parser.add_argument('--path', '-p', type=str, required=True, help="Path to search in")
parser.add_argument('--search', '-s', type=str, required=True, help="String to search for")
parser.add_argument('--txtonly', '-t', action='store_true', help="Only show results in text files (default to search all files)", default=False)
parser.add_argument('--recursive', '-r', action='store_true', help="Search subdirectories (default to search only the provided path)", default=False)
parser.add_argument('--multiprocessor', '-m', action='store_true', help="Use multiprocessing (default to threading)", default=False)
args = parser.parse_args()


def get_files(path):
    # files = []
    # s_pref = "**/" if args.recursive else ""
    # s_term = "*.txt" if args.txtonly else "*"
    # s_query = f"{s_pref}{s_term}"
    #
    # for file in path.glob(s_query):
    #     if file.is_file():
    #         files.append(file)
    # return files

    return [f for f in path.glob(f"{'**/' if args.recursive else ''}{'*.txt' if args.txtonly else '*'}") if f.is_file()]


if __name__ == "__main__":
    file_list = get_files(Path(args.path))
    # print(f"Searching for '{query}' in '{path}/{('**/' if args.recursive else '') + ('*.txt' if args.txtonly else '*')}', using {'multiprocessing' if args.multiprocessor else 'threading'}\n")
    # print(file_list)

    start = timeit.default_timer()
    if args.multiprocessor:
        print("Calling multiprocessing search function\n")
        search_m(file_list, args.search)
    else:
        print("Calling threading search function\n")
        search_t(file_list, args.search)

    stop = timeit.default_timer()
    print(f"\nTime taken: {stop - start} seconds")