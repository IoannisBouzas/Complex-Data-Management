import sys
import time
from collections import Counter

def load_transactions(file_path):

    transactions = []

    with open(file_path, 'r') as file:
        for line in file:

            items = eval(line.strip())
            transactions.append(items)


    inverted_file = {}
    item_transaction_count = {}

    for tid, transaction in enumerate(transactions):
        item_counts = Counter(transaction)

        for item, count in item_counts.items():
            if item not in inverted_file:
                inverted_file[item] = []
            inverted_file[item].append((tid, count))

            if item not in item_transaction_count:
                item_transaction_count[item] = 0
            item_transaction_count[item] += 1


    total_transactions = len(transactions)
    idf_values = {}
    for item, count in item_transaction_count.items():
        idf_values[item] = total_transactions / count


    with open("invfileocc.txt", 'w') as file:
        for item in sorted(inverted_file.keys()):
            format = str(inverted_file[item]).replace("(", "[").replace(")", "]")
            file.write(f"{item}: {idf_values[item]}, {format}\n")

    return transactions, inverted_file, idf_values


def process_relevance_query_inverted(query, inverted_file, idf_values, k):

    valid_query_items = [item for item in query if item in inverted_file]

    if not valid_query_items:
        return []


    sorted_query_items = sorted(valid_query_items, key=lambda item: len(inverted_file[item]))


    result = {}


    if sorted_query_items:
        first_item = sorted_query_items[0]
        for tid, occ in inverted_file[first_item]:
            result[tid] = occ * idf_values[first_item]


    for i in range(1, len(sorted_query_items)):
        current_item = sorted_query_items[i]
        current_list = inverted_file[current_item]


        result_tids = sorted(result.keys())
        ptr_result = 0
        ptr_current = 0


        merged_result = {}


        while ptr_result < len(result_tids) and ptr_current < len(current_list):
            result_tid = result_tids[ptr_result]
            current_tid, current_occ = current_list[ptr_current]

            if result_tid < current_tid:

                merged_result[result_tid] = result[result_tid]
                ptr_result += 1
            elif result_tid > current_tid:

                merged_result[current_tid] = current_occ * idf_values[current_item]
                ptr_current += 1
            else:
                merged_result[result_tid] = result[result_tid] + (current_occ * idf_values[current_item])
                ptr_result += 1
                ptr_current += 1


        while ptr_result < len(result_tids):
            result_tid = result_tids[ptr_result]
            merged_result[result_tid] = result[result_tid]
            ptr_result += 1


        while ptr_current < len(current_list):
            current_tid, current_occ = current_list[ptr_current]
            merged_result[current_tid] = current_occ * idf_values[current_item]
            ptr_current += 1


        result = merged_result


    relevance_scores = [(tid, score) for tid, score in result.items()]
    relevance_scores.sort(key=lambda x: x[1], reverse=True)


    if 0 < k < len(relevance_scores):
        relevance_scores = relevance_scores[:k]

    return relevance_scores



def process_relevance_query_naive(query, transactions, idf_values, k):

    relevance_scores = []

    for tid, transaction in enumerate(transactions):
        score = 0

        item_counts = Counter(transaction)


        for item in query:
            if item in item_counts:
                score += item_counts[item] * idf_values[item]

        if score > 0:
            relevance_scores.append((tid, score))


    relevance_scores.sort(key=lambda x: x[1], reverse=True)


    if k is not None and len(relevance_scores) > k:
        relevance_scores = relevance_scores[:k]

    return relevance_scores



if __name__ == "__main__":

    transactions_file = sys.argv[1]
    queries_file = sys.argv[2]
    qnum = int(sys.argv[3])
    method = int(sys.argv[4])
    k = int(sys.argv[5])

    transactions, inverted_file, idf_values = load_transactions(transactions_file)


    with open(queries_file, 'r') as file:
        queries = [eval(line.strip()) for line in file]

        if qnum == -1:

            if method == -1 or method == 0:
                start_time = time.time()
                for query in queries:
                    results = process_relevance_query_naive(query, transactions, idf_values, k)
                end_time = time.time()
                print(f"Naive Method computation time = {end_time - start_time}")

            if method == -1 or method == 1:
                start_time = time.time()
                for query in queries:
                    results = process_relevance_query_inverted(query, inverted_file, idf_values, k)
                end_time = time.time()
                print(f"Inverted File Method computation time = {end_time - start_time}")


        else:
            query = queries[qnum]

            if method == -1 or method == 0:
                start_time = time.time()
                results = process_relevance_query_naive(query, transactions, idf_values, k)
                end_time = time.time()
                print(f"Naive Method results:")
                formatted_results = [[score, tid] for tid, score in results]
                print(formatted_results)
                print(f"Naive Method computation time = {end_time - start_time}")


            if method == -1 or method == 1:
                start_time = time.time()
                results = process_relevance_query_inverted(query, inverted_file, idf_values, k)
                end_time = time.time()
                print(f"Inverted File Method results:")
                formatted_results = [[score, tid] for tid, score in results]
                print(formatted_results)
                print(f"Inverted File Method computation time = {end_time - start_time}")

