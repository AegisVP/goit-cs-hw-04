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
    return [f for f in path.glob(f"{'**/' if args.recursive else ''}{'*.txt' if args.txtonly else '*'}") if f.is_file()]


def show_results(result_files):
    for search, search_result in result_files.items():
        if len(search_result) == 0:
            print(f"\n'{search}' not found in any of the files.")
            return
        
        print(f"\n'{search}' found in {len(search_result)} file{('s' if len(search_result) > 1 else '')}:")
        for file in search_result:
            if isinstance(file, Path):
                print(f"| {file.parent}/{file.name}")
            else:
                print(f"| {file}")


if __name__ == "__main__":
    start_program = timeit.default_timer()
    file_list = get_files(Path(args.path))

    result_files = dict()
    print(f"Searching for '{args.search}' in '{args.path}/{('**/' if args.recursive else '') + ('*.txt' if args.txtonly else '*')}' using {'multiprocessing' if args.multiprocessor else 'threading'}...")

    searcher = locals()[f"search_{'m' if args.multiprocessor else 't'}"]

    start_search = timeit.default_timer()
    for search_q in args.search.split(','):
        search_q = search_q.strip(',. ').casefold()
        searcher(file_list, search_q, result_files)
    stop_search = timeit.default_timer()

    show_results(result_files)

    stop_program = timeit.default_timer()
    print(f"""\nTime taken:
 {stop_search - start_search:.10f} sec. Search
 {(start_search - start_program) + (stop_program - stop_search):.10f} sec. Other tasks
 {stop_program - start_program:.10f} sec. Total""")
    exit(0)