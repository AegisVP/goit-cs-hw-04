import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Search for a string in files')
parser.add_argument('--path', '-p', type=str, required=True, help="Path to search in")
parser.add_argument('--search', '-s', type=str, required=True, help="String to search for")
parser.add_argument('--txtonly', '-t', action='store_true', help="Only show results in text files", default=False)
parser.add_argument('--recursive', '-r', action='store_true', help="Search recursively", default=False)
args = parser.parse_args()

path = Path(args.path)
query = args.search
# txtonly = args.txtonly
# recursive = args.recursive

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
    print(get_files(path))