from multiprocessing import Process, Semaphore, Manager
import logging

PROCESSES = 4

logging.basicConfig(format="%(processName)s %(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

def worker(s, file, query, result_files: list):
    query = query.casefold()
    with s:
        with open(file, 'r') as f:
            try:
                for line in f.readlines():
                    if query in line.casefold():
                        result_files.append(file)
                        break

            except Exception as e:
                pass


def search_m(files, query, result_files):
    s = Semaphore(PROCESSES)
    with Manager() as m:
        search_result_files = m.list()

        for file in files:
            pr = Process(target=worker, args=(s, file, query, search_result_files))
            pr.start()
            pr.join()

        result_files[query] = list(search_result_files)
