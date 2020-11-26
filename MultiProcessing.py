import time
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Process


def complex_calc():
    start_time = time.time()
    print('Starting calculation...')
    [x**2 for x in range(20000000)]
    print(f"Execution time of complex_calc: {time.time() - start_time}")


start_time = time.time()

complex_calc()
complex_calc()
print(f"Single thread total time: {time.time()-start_time}")


# process1 = Process(target=complex_calc)
# process2 = Process(target=complex_calc)
#
# process1.start()
# process2.start()
#
# start_time = time.time()
#
# process1.join()
# process2.join()
#
# print(f"Two processs total time: {time.time() - start_time}")



# with ProcessPoolExecutor(max_workers=2) as pool:
#     pool.submit(complex_calc)
#     pool.submit(complex_calc)
#
# print(f"Two processs total time: {time.time() - start_time}")

