from multiprocessing import Process, Value, Lock, Queue, Manager
from ctypes import c_char_p
import time


def calculate(result, input1, input2, lock):
    for line1 in input1[start:end]:
        list_of_lines = []
        relations = 0
        current_line = 0
        for line2 in input2:
            current_line += 1
            if line1.strip() in line2:
                relations += 1
                list_of_lines.append(current_line)
        if relations > 1:
            with lock:
                q.put("Discovered match for " + line1.strip())
                result.value += \
                    line1.strip() + \
                    ',' + str(relations) + \
                    ',' + str(list_of_lines) + '\n'


if __name__ == '__main__':
    q = Queue()
    input1 = open('input1.csv', 'r').read().split('\n')
    input2 = open('input2.csv', 'r').read().split('\n')
    result_file = open('result.csv', 'w')
    manager = Manager()
    result = manager.Value(
        c_char_p,
        'Supplier,Number of relations,list of lines\n')
    lock = Lock()
    number_of_processes = 8
    start_time = time.time()
    try:
        input1.remove('')
        input2.remove('')
    except ValueError:
        print('Some file(s) do not have empty lines but that\'s ok.\
I can handle it')
    processes = [Process(target=calculate, args=(
        result,
        input1[
            int(process*len(input1)/number_of_processes),
            int((process+1)*len(input1)/number_of_processes)],
        input2,
        lock)) for process in range(number_of_processes)]
    for p in processes:
        p.start()
        print(p.get())
    for p in processes:
        p.join()
    print("Executed in %s seconds" % (time.time() - start_time))
