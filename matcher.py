import threading
import time


delimiter = ';'
input1 = open('input1.csv', 'r').read().split('\n')
input2 = open('input2.csv', 'r').read().split('\n')
input3 = open('input3.csv', 'r').read().split(delimiter)
result = open('result.csv', 'w')
lock = threading.Lock()
number_of_threads = 8


def calculate(start, end):
    global result
    for line1 in input1[start:end]:
        list_of_bps_codes = []
        relations = 0
        b2wd_relations = 0
        buyers_count = 0
        for line2 in input2:
            if line1.strip() in line2:
                relations += 1
                bps_code = get_bps_code(line2)
                if bps_code[:4] == 'b2WD':
                    b2wd_relations += 1
                list_of_bps_codes.append(bps_code)
        buyers_count = count_buyers(list_of_bps_codes, input3)
        with lock:
            print("Discovered match for " + line1.strip())
            result.write(
                line1.strip() +
                delimiter +
                str(relations) +
                delimiter +
                str(list_of_bps_codes) +
                delimiter +
                str(b2wd_relations) +
                delimiter +
                str(buyers_count) +
                '\n')


def count_buyers(buyers_list, buyers_to_check_from):
    count = 0
    for buyer in buyers_list:
        if buyer in buyers_to_check_from:
            print("Buyer: ", buyer)
            count += 1
    return count


def get_bps_code(string):
    return string.split('","')[1]

if __name__ == '__main__':
    start_time = time.time()
    try:
        input1.remove('')
        input2.remove('')
        input3.remove('')
    except ValueError:
        print('Some file(s) do not have empty lines but that\'s ok. \
I can handle it')
    result.write(
        'Supplier' +
        delimiter +
        'Number of relations' +
        delimiter +
        'List of buyers' +
        delimiter +
        'Number of 2WD relations' +
        delimiter +
        'Buyers from Input3\n')
    threads = [threading.Thread(target=calculate, args=(
        int(thread*len(input1)/number_of_threads),
        int((thread+1)*len(input1)/number_of_threads))) for
        thread in range(number_of_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Executed in %s seconds" % (time.time() - start_time))
