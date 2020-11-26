import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def ask_user():
    start_time = time.time()
    user_input = input("Enter your name: ")
    greet = f"Hello, {user_input}"
    print(greet)
    print(f"Execution time of ask_user: {time.time() - start_time}")


def complex_calc():
    start_time = time.time()
    print('Starting calculation...')
    [x**2 for x in range(20000000)]
    print(f"Execution time of complex_calc: {time.time() - start_time}")


start_time = time.time()
ask_user()
complex_calc()
print(f"Single thread total time: {time.time()-start_time}")


# thread1 = Thread(target=complex_calc)
# thread2 = Thread(target=ask_user)
#
# start_time = time.time()
#
# thread1.start()
# thread2.start()
#
# thread1.join()
# thread2.join()
#
# print(f"Two threads total time: {time.time()-start_time}")
#
#
# with ThreadPoolExecutor(max_workers=2) as pool:
#     pool.submit(complex_calc)
#     pool.submit(complex_calc)
#
# print(f"Two threads total time: {time.time()-start_time}")