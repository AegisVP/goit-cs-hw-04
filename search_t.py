from threading import Thread, Semaphore

THREADS = 10
search_result_files = dict()

def worker(s: Semaphore, file, query):
    query = query.casefold()
    with s:
        with open(file, 'r') as f:
            try:
                for line in f.readlines():
                    if query in line.casefold():
                        search_result_files[query].append(file)
                        break

            except Exception as e:
                pass


def search_t(files, query, result_files):
    search_result_files[query] = list()

    s = Semaphore(THREADS)
    for file in files:
        t = Thread(target=worker, args=(s, file, query))
        t.start()
        t.join()
    result_files[query] = search_result_files[query]
    