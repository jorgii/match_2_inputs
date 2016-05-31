import threading


input1 = open('input1.csv', 'r').read().split('\n')
input2 = open('input2.csv', 'r').read().split('\n')
result = open('result.csv', 'w')
lock = threading.Lock()
number_of_threads = 8


def calculate(suppliers):
    global result
    for line1 in suppliers:
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
    try:
        input1.remove('')
        input2.remove('')
    except ValueError:
        print('file(s) do not have empty lines')
    result.write('Supplier,Number of relations,list of lines\n')
    threads = [threading.Thread(target=f, args=(
        int(thread*len(input1)/number_of_threads),
        int((thread+1)*len(input1)/number_of_threads))) for
        thread in range(number_of_threads)]
    for t in threads:
        t.start()
        print(t)
    for t in threads:
        t.join()

    print('Threads finished')
    print(result)
