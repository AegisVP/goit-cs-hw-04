from multiprocessing import Process, Semaphore, Manager
import logging

PROCESSES = 4

logging.basicConfig(format="%(processName)s %(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

def worker(s, file, query, result_files: list):
    with s:
        with open(file, 'r') as f:
            try:
                for line in f.readlines():
                    if query in line:
                        result_files.append(file)
                        break

            except Exception as e:
                pass

def show_results(result_files, query):
    if len(result_files) == 0:
        print("No results found")
        return

    print(f"Found search query '{query}' in {len(result_files)} file{('s' if len(result_files) > 1 else '')}:")
    for file in result_files:
        print(f"| {file.parent}/{file.name}")

def search_m(files, query):
    s = Semaphore(PROCESSES)
    with Manager() as m:
        result_files = m.list()

        # processes=[]
        # for file in files:
        #     pr = Process(target=worker, args=(s, file, query, result_files))
        #     pr.start()
        #     processes.append(pr)

        # [pr.join() for pr in processes]

        # show_results(result_files, query)

        for file in files:
            pr = Process(target=worker, args=(s, file, query, result_files))
            pr.start()
            pr.join()

        show_results(result_files, query)
