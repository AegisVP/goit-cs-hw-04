from threading import Thread, Semaphore, RLock

THREADS = 10
lock = RLock()
result_files = []

def worker(s: Semaphore,file, query):
    with open(file, 'r') as f:
        try:
            for line in f.readlines():
                if query in line:
                    with lock:
                        result_files.append(file)
                    break

        except Exception as e:
            pass

def show_results(query):
    if len(result_files) == 0:
        print("No results found")
        return

    print(f"Found search query '{query}' in {len(result_files)} file{('s' if len(result_files) > 1 else '')}:")
    for file in result_files:
        print(f"| {file.parent}/{file.name}")

def search_t(files, query):
    s = Semaphore(THREADS)
    for file in files:
        t = Thread(target=worker, args=(s, file, query))
        t.start()
        t.join()

    show_results(query)