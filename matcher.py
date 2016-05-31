input1 = open('input1.csv', 'r+')
input2 = open('input2.csv', 'r+')
result = open('result.csv', 'w')

result.write('Supplier,Number of relations,list of lines\n')

for num1, line1 in enumerate(input1, 1):
    list_of_lines = []
    relations = 0
    input2.seek(0, 0)
    for num2, line2 in enumerate(input2, 1):
        if line1.strip() in line2:
            relations += 1
            list_of_lines.append(num2)
    if relations > 1:
        result.write(
            line1.strip() +
            ',' + str(relations) +
            ',' + str(list_of_lines) + '\n')
