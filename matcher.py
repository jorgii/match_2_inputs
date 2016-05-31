import threading


input1 = open('input1.csv', 'r').read().split('\n')
input2 = open('input21.csv', 'r').read().split('\n')
result = open('result.csv', 'w')
lock = threading.Lock()
number_of_threads = 8

try:
    input1.remove('')
    input2.remove('')
except ValueError:
    print('file(s) do not have empty lines')

result.write('Supplier,Number of relations,list of lines\n')

try:
    for thread in range(number_of_threads):
        start = thread*len(input1)/number_of_threads
        end = (thread+1)*len(input1)/number_of_threads
        threading.start_new_thread(calculate, (input1[start:end]))
except:
    print("Error: unable to start thread")


def calculate(suppliers):
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
            print("Discovered match for " + line1.strip())
            result.write(
                line1.strip() +
                ',' + str(relations) +
                ',' + str(list_of_lines) + '\n')
