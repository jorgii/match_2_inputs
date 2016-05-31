input1 = open('input1.csv', 'r').read().split('\n')
input2 = open('input2.csv', 'r').read().split('\n')
try:
    input1.remove('')
    input2.remove('')
except ValueError:
    print('file(s) do not have empty lines')
result = open('result.csv', 'w')

result.write('Supplier,Number of relations,list of lines\n')

for line1 in input1:
    list_of_lines = []
    relations = 0
    for line2 in input2:
        if line1.strip() in line2:
            relations += 1
            list_of_lines.append(input2.index(line2))
    if relations > 1:
        print("Discovered match for " + line1.strip())
        result.write(
            line1.strip() +
            ',' + str(relations) +
            ',' + str(list_of_lines) + '\n')
