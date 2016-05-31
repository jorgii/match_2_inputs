import threading
import time


input1 = open('input1.csv', 'r').read().split('\n')
input2 = open('input2.csv', 'r').read().split('\n')
result = open('result.csv', 'w')
lock = threading.Lock()
number_of_threads = 8


def calculate(start, end):
    global result
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
                print("Discovered match for " + line1.strip())
                result.write(
                    line1.strip() +
                    ',' + str(relations) +
                    ',' + str(list_of_lines) + '\n')


if __name__ == '__main__':
    start_time = time.time()
    try:
        input1.remove('')
        input2.remove('')
    except ValueError:
        print('Some file(s) do not have empty lines but that\'s ok.\
        I can handle it')
    result.write('Supplier,Number of relations,list of lines\n')
    threads = [threading.Thread(target=calculate, args=(
        int(thread*len(input1)/number_of_threads),
        int((thread+1)*len(input1)/number_of_threads))) for
        thread in range(number_of_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Executed in %s seconds" % (time.time() - start_time))
