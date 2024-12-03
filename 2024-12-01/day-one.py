#!/env/bin/python3

left_set = []
right_set = []

with open(file="./input", mode="r") as input_file:
    for line in input_file:
        elements = line.split()
        left_set.append(int(elements[0]))
        right_set.append(int(elements[1]))

left_list = sorted(left_set)
right_list = sorted(right_set)

distance = 0
for left_value, right_value in zip(left_list, right_list):
    distance += abs(left_value - right_value)

print(f"distance: {distance}")

occurences = dict()
for right_value in right_list:
   occurences[right_value] = occurences.get(right_value, 0) + 1

similarity = 0
for left_value in left_list:
    similarity += occurences.get(left_value, 0) * left_value

print(f'similarity: {similarity}')
