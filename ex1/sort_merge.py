################################

#####IOANNIS BOUZAS AM:5025#####

################################

def read_line(array_line):
    line = array_line.split('\t')
    key = line[0]
    value = int(line[1])
    return key, value
    
def merge_sort_and_sum(array):

    if len(array) <= 1:
        return array
    
    mid = len(array) // 2
    left = merge_sort_and_sum(array[:mid])
    right = merge_sort_and_sum(array[mid:])

    return merge_and_group(left, right)

def merge_and_group(left, right):
    result = []
    i = j = 0
    current_key = None
    current_sum = 0

    while i < len(left) and j < len(right):
        left_key, left_value = read_line(left[i])
        right_key, right_value = read_line(right[j])

        if left_key < right_key:
            process_key = left_key
            process_value = left_value
            i += 1
        else:
            process_key = right_key
            process_value = right_value
            j += 1
        
        if process_key == current_key:
            current_sum += process_value
        else:
            if current_key is not None:
                result.append(f"{current_key}\t{current_sum}")
            current_key = process_key
            current_sum = process_value
    
    while i < len(left):
        left_key, left_value = read_line(left[i])
        if left_key == current_key:
            current_sum += left_value
        else:
            if current_key is not None:
                result.append(f"{current_key}\t{current_sum}")
            current_key = left_key
            current_sum = left_value
        i += 1

    while j < len(right):
        right_key, right_value = read_line(right[j])
        if right_key == current_key:
            current_sum += right_value
        else:
            if current_key is not None:
                result.append(f"{current_key}\t{current_sum}")
            current_key = right_key
            current_sum = right_value
        j += 1

    if current_key is not None:
        result.append(f"{current_key}\t{current_sum}")
    
    return result

if __name__ == '__main__':
    array = []
    with open("R.tsv", 'r') as r:
        r_line = r.readline().strip()
        while r_line:
            array.append(r_line)
            r_line = r.readline().strip()

    result = merge_sort_and_sum(array)

    with open("Rgroupby.tsv", 'w') as out:
        for line in result:
            out.write(line + '\n')
    
