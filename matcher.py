input1 = open('input1.csv', 'r+')
input2 = open('input2.csv', 'r+')
result = open('result.csv', 'w')
num1 = 0

result.write('Supplier,Number of relations,list of lines\n')

for line1 in input1:
    num1 += 1
    list_of_lines = []
    relations = 0
    input2.seek(0, 0)
    num2 = 0
    for line2 in input2:
        num2 += 1
        if line1.strip() in line2:
            relations += 1
            list_of_lines.append(num2)
    if relations > 1:
        print("Discovered match for " + line1.strip())
        result.write(
            line1.strip() +
            ',' + str(relations) +
            ',' + str(list_of_lines) + '\n')
