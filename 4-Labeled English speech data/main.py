import sys
import pandas as pd
from threads import downloadScripts


def generate_threads(num_threads, input_links, output_loc):
    """
    Instantiate the threads and returns a dict of the threads.
    Each thread will only work on size of `input_links`
    divided by `num_threads`.
    """

    # Get the input file, there are several examples
    input_file = pd.read_csv(input_links, index_col=0)
    num_links = len(input_file)

    # Size of each partition, which the thread will be woking on
    part_size = num_links // num_threads
    threads = {}

    # Threads instantiation
    for th in range(num_threads):
        if th == num_threads - 1:
            threads[f"thread_{th+1}"] = downloadScripts(
                th + 1, input_file.iloc[(th+1) * part_size:], output_loc)
        else:
            threads[f"thread_{th+1}"] = downloadScripts(
                th + 1,
                input_file.iloc[th * part_size: (th + 1) * part_size],
                output_loc)

    # A dict of threads
    return threads


def start_threads(threads):
    """
    Spins off each thread, and waits for them to join the parent.
    """
    for i in threads.values():
        i.start()
    for i in threads.values():
        i.join()
    return


if __name__ == "__main__":
    # The input file, in csv format. must have two columns:
    # title, and link.
    input_links = sys.argv[1]

    # The directory where the files will be stored at.
    output_loc = sys.argv[2]

    # The number of threads that will be working on the task
    num_threads = sys.argv[3]

    # Thread instantiation
    threads = generate_threads(num_threads, input_links, output_loc)

    # Threads working
    start_threads(threads)
