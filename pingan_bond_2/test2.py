
import multiprocessing as mp
import time
import datetime

def foo_pool(x):
    t = 0
    for i in range(x):
        t += i
    return t


result_list = []


def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)


def apply_async_with_callback():
    t_start = datetime.datetime.now()
    pool = mp.Pool()
    pool.apply_async(foo_pool, args=(1000000000,), callback=log_result)
    pool.close()
    pool.join()
    print(result_list)
    t_end = datetime.datetime.now()
    print(t_end - t_start)


if __name__ == '__main__':
    apply_async_with_callback()