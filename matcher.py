import threading
import time


input1 = open('input1.csv', 'r').read().split('\n')
input2 = open('input2.csv', 'r').read().split('\n')
result = open('result.csv', 'w')
lock = threading.Lock()
number_of_threads = 8
delimiter = ';'


def calculate(start, end):
    global result
    for line1 in input1[start:end]:
        list_of_bps_codes = []
        relations = 0
        for line2 in input2:
            if line1.strip() in line2:
                relations += 1
                list_of_bps_codes.append(get_bps_code(line2))
        if relations > 1:
            with lock:
                print("Discovered match for " + line1.strip())
                result.write(
                    line1.strip() +
                    delimiter + str(relations) +
                    delimiter + str(list_of_bps_codes) + '\n')


def get_bps_code(string):
    return string[
        string.index('"b')+1:
        string.index('"', string.index('"b')+1)]

if __name__ == '__main__':
    start_time = time.time()
    try:
        input1.remove('')
        input2.remove('')
    except ValueError:
        print('Some file(s) do not have empty lines but that\'s ok. \
I can handle it')
    result.write(
        'Supplier' +
        delimiter +
        'Number of relations' +
        delimiter +
        'list of buyers\n')
    threads = [threading.Thread(target=calculate, args=(
        int(thread*len(input1)/number_of_threads),
        int((thread+1)*len(input1)/number_of_threads))) for
        thread in range(number_of_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Executed in %s seconds" % (time.time() - start_time))
