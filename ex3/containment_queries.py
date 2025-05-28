import sys
import time


def load_transactions(file_path):

    transactions = []
    sigfile = []
    bitslice = {}
    inverted = {}

    with open(file_path, 'r') as file:
        for id, line in enumerate(file):
            items = set(eval(line.strip()))
            transactions.append(items)


            bitmap_int = 0
            for item in items:
                bitmap_int |= (1 << item)

                if item not in bitslice:
                    bitslice[item] = 0

                bitslice[item] |= (1 << id)

                if item not in inverted:
                    inverted[item] = []

                inverted[item].append(id)

            sigfile.append(bitmap_int)


    with open("sigfile.txt", 'w') as file:
        for signature in sigfile:
            file.write(str(signature) + '\n')


    with open("bitslice.txt", 'w') as file:
        for item in sorted(bitslice.keys()):
            file.write(f"{item}: {bitslice[item]}\n")


    with open("invfile.txt", 'w') as file:
        for item in sorted(inverted.keys()):
            file.write(f"{item}: {inverted[item]}\n")

    return transactions, sigfile, bitslice, inverted



def process_query_naive(query, transactions):

    query_set = set(query)
    results = []

    for tid, transaction in enumerate(transactions):
        if query_set.issubset(transaction):
            results.append(tid)

    return results


def process_query_signature(query, sigfile):

    query_bitmap = 0
    for item in query:
        query_bitmap |= (1 << item)


    results = []
    for tid, sig in enumerate(sigfile):

        if (sig & query_bitmap) == query_bitmap:
            results.append(tid)

    return results



def process_query_bitslice(query, bitslice):

    if not query:
        return []

    result_bitmap = bitslice[query[0]]

    for item in query[1:]:
        if item in bitslice:
            result_bitmap &= bitslice[item]
        else:
            return []


    results = []
    current_bitmap = result_bitmap
    tid = 0

    while current_bitmap > 0:
        if current_bitmap & 1:
            results.append(tid)
        current_bitmap >>= 1
        tid += 1


    # Brian Kernighan's algorithm
    # while bitmap:
    #     # Find position of least significant 1-bit
    #     trailing_zeros = (bitmap & -bitmap).bit_length() - 1
    #     tid += trailing_zeros
    #     results.append(tid)
    #     tid += 1
    #     # Clear the least significant 1-bit
    #     bitmap >>= trailing_zeros + 1


    return results


def process_query_inverted(query, inverted):

    if not query:
        return []

    if any(item not in inverted for item in query):
        return []

    for item in inverted:
        inverted[item].sort()


    sorted_query = sorted(query, key=lambda item: len(inverted[item]))
    result = inverted[sorted_query[0]].copy()


    for item in sorted_query[1:]:
        result = merge_intersection(result, inverted[item])
        if not result:
            break


    return result


def merge_intersection(list1, list2):

    result = []
    i = 0
    j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1

    return result



if __name__ == "__main__":

    transactions_file = sys.argv[1]
    queries_file = sys.argv[2]
    qnum = int(sys.argv[3])
    method = int(sys.argv[4])

    transactions, sigfile, bitslice, inverted = load_transactions("transactions.txt")


    with open(queries_file, 'r') as file:
        if qnum == -1:
            if method == 0:
                start_time = time.time()
                for line in file:
                    query = eval(line.strip())
                    results = process_query_naive(query, transactions)
                end_time = time.time()
                print(f"Naive Method computation time = {end_time - start_time}")

            elif method == 1:
                start_time = time.time()
                for line in file:
                    query = eval(line.strip())
                    results = process_query_signature(query, sigfile)
                end_time = time.time()
                print(f"Signature File computation time = {end_time - start_time}")

            elif method == 2:
                start_time = time.time()
                for line in file:
                    query = eval(line.strip())
                    results = process_query_bitslice(query, bitslice)
                end_time = time.time()
                print(f"Bitsliced Signature File computation time = {end_time - start_time}")

            elif method == 3:
                start_time = time.time()
                for line in file:
                    query = eval(line.strip())
                    results = process_query_inverted(query, inverted)
                end_time = time.time()
                print(f"Inverted Index computation time = {end_time - start_time}")

            elif method == -1:
                start_time = time.time()
                for line in file:
                    query = eval(line.strip())
                    results = process_query_naive(query, transactions)
                end_time = time.time()
                print(f"Naive Method computation time = {end_time - start_time}")

                start_time = time.time()
                with open(queries_file, 'r') as file:
                    for line in file:
                        query = eval(line.strip())
                        results = process_query_signature(query, sigfile)
                end_time = time.time()
                print(f"Signature File computation time = {end_time - start_time}")

                start_time = time.time()
                with open(queries_file, 'r') as file:
                    for line in file:
                        query = eval(line.strip())
                        results = process_query_bitslice(query, bitslice)
                end_time = time.time()
                print(f"Bitsliced Signature File computation time = {end_time - start_time}")

                start_time = time.time()
                with open(queries_file, 'r') as file:
                    for line in file:
                        query = eval(line.strip())
                        results = process_query_inverted(query, inverted)
                end_time = time.time()
                print(f"Inverted Index computation time = {end_time - start_time}")
        else:
            for i, line in enumerate(file):
                if i == qnum:
                    query = eval(line.strip())

                    if method == 0:
                        start_time = time.time()
                        results = process_query_naive(query, transactions)
                        end_time = time.time()
                        print(f"Naive Method result:")
                        print(set(results))
                        print(f"Naive Method computation time = {end_time - start_time}")

                    elif method == 1:
                        start_time = time.time()
                        results = process_query_signature(query, sigfile)
                        end_time = time.time()
                        print("Signature File result:")
                        print(set(results))
                        print(f"Signature File result: = {end_time - start_time}")

                    elif method == 2:
                        start_time = time.time()
                        results = process_query_bitslice(query, bitslice)
                        end_time = time.time()
                        print("Bitsliced Signature File result:")
                        print(set(results))
                        print(f"Bitsliced Signature File computation time = {end_time - start_time}")

                    elif method == 3:
                        start_time = time.time()
                        results = process_query_inverted(query, inverted)
                        end_time = time.time()
                        print("Inverted Index result:")
                        print(set(results))
                        print(f"Inverted Index computation time = {end_time - start_time}")

                    elif method == -1:
                        start_time = time.time()
                        results = process_query_naive(query, transactions)
                        end_time = time.time()
                        print(f"Naive Method result:")
                        print(set(results))
                        print(f"Naive Method computation time = {end_time - start_time}")
                        start_time = time.time()
                        results = process_query_signature(query, sigfile)
                        end_time = time.time()
                        print("Signature File result:")
                        print(set(results))
                        print(f"Signature File result: = {end_time - start_time}")
                        start_time = time.time()
                        results = process_query_bitslice(query, bitslice)
                        end_time = time.time()
                        print("Bitsliced Signature File result:")
                        print(set(results))
                        print(f"Bitsliced Signature File computation time = {end_time - start_time}")
                        start_time = time.time()
                        results = process_query_inverted(query, inverted)
                        end_time = time.time()
                        print("Inverted Index result:")
                        print(set(results))
                        print(f"Inverted Index computation time = {end_time - start_time}")

                    break


