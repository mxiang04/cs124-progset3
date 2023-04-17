import heapq
import sys
import random
import time
import math


max_iter = 25000
num_instances = 50


def generate_test(size=100):
    arr = []
    for i in range(size):
        arr.append(random.randint(1, 10 ** 12))
    return arr


def kk(arr):
    n = len(arr)
    neg_arr = [-num for num in arr]
    heapq.heapify(neg_arr)
    for i in range(n - 1):
        n1 = heapq.heappop(neg_arr)
        n2 = heapq.heappop(neg_arr)
        heapq.heappush(neg_arr, (n1 - n2))
    return -neg_arr[0]


def generate_random_assignment(arr, is_pre):
    n = len(arr)
    random_sol = []
    for i in range(n):
        if not is_pre:
            random_choice = random.choice([1, -1])
            random_sol.append(random_choice)
        else:
            rand_int = random.randint(0, n - 1)
            random_sol.append(rand_int)
    return random_sol


def calculate_residue(arr, signs, is_pre):
    n = len(arr)
    assert (n == len(signs))
    if not is_pre:
        residue = 0
        for i in range(n):
            residue += (signs[i] * arr[i])

        return abs(residue)
    else:
        # Signs in this case is P from the progset
        modified_arr = [0] * n
        for i in range(n):
            modified_arr[signs[i]] += arr[i]
        return kk(modified_arr)


def find_neighbor(signs, is_pre):
    n = len(signs)
    rand_indices = random.sample(range(n), 2)
    neighbor = signs.copy()
    i = rand_indices[0]
    j = rand_indices[1]
    if is_pre:
        neighbor[i] = -signs[i]
        neighbor[j] = random.choice([signs[j], -signs[j]])
    else:
        neighbor[i] = j
    return neighbor


def repeated_random(arr, is_pre):
    n = len(arr)
    result = generate_random_assignment(arr, is_pre)
    for i in range(max_iter):
        rand_sign = generate_random_assignment(arr, is_pre)
        if calculate_residue(arr, rand_sign, is_pre) < calculate_residue(arr, result, is_pre):
            for i in range(n):
                result[i] = rand_sign[i]
    return calculate_residue(arr, result, is_pre)


def hill_climbing(arr, is_pre):
    n = len(arr)
    result = generate_random_assignment(arr, is_pre)
    for i in range(max_iter):
        rand_neighbor = find_neighbor(result, is_pre)
        if calculate_residue(arr, rand_neighbor, is_pre) < calculate_residue(arr, result, is_pre):
            for i in range(n):
                result[i] = rand_neighbor[i]
    return calculate_residue(arr, result, is_pre)


def cooldown(iter):
    # Recommended from the progset description.
    exp = iter // 300
    return (10 ** 10) * (0.8 ** exp)


def sa_prob_calculator(arr, iter, cur, neighbor, is_pre):
    res_cur = calculate_residue(arr, cur, is_pre)
    res_neighbor = calculate_residue(arr, neighbor, is_pre)
    nominator = math.exp(-(res_neighbor - res_cur))
    denominator = cooldown(iter)
    return nominator / denominator


def simulated_annealing(arr, is_pre):
    n = len(arr)
    cur = generate_random_assignment(arr, is_pre)
    result = cur.copy()
    for i in range(1, max_iter + 1):
        neighbor = find_neighbor(cur, is_pre)
        if calculate_residue(arr, neighbor, is_pre) < calculate_residue(arr, cur, is_pre):
            for i in range(n):
                cur[i] = neighbor[i]
        else:
            threshold = sa_prob_calculator(arr, i, cur, neighbor, is_pre)
            p = random.random()
            if p < threshold:
                for i in range(n):
                    cur[i] = neighbor[i]
        if calculate_residue(arr, cur, is_pre) < calculate_residue(arr, result, is_pre):
            for i in range(n):
                result[i] = cur[i]
    return calculate_residue(arr, result, is_pre)


def main(args):
    # # FOR TESTING PURPOSES IN WRITEUP
    # kk_results = open("kk_results.txt", "w+")
    # rr_0_results = open("rr_0_results.txt", "w+")
    # rr_1_results = open("rr_1_results.txt", "w+")
    # hc_0_results = open("hc_0_results.txt", "w+")
    # hc_1_results = open("hc_1_results.txt", "w+")
    # sa_0_results = open("sa_0_results.txt", "w+")
    # sa_1_results = open("sa_1_results.txt", "w+")
    # all_results = [kk_results, rr_0_results,
    #                rr_1_results, hc_0_results, hc_1_results, sa_0_results, sa_1_results]

    # for file in all_results:
    #     file.write("residue, time\n")

    # for i in range(num_instances):
    #     arr = generate_test()

    #     # For kk
    #     start = time.perf_counter()
    #     residue = kk(arr)
    #     end = time.perf_counter()
    #     kk_results.write(str(residue) + ", " + str(end - start) + "\n")

    #     # For rr0
    #     start = time.perf_counter()
    #     residue = repeated_random(arr, False)
    #     end = time.perf_counter()
    #     rr_0_results.write(str(residue) + ", " + str(end - start) + "\n")

    #     # For rr1
    #     start = time.perf_counter()
    #     residue = repeated_random(arr, True)
    #     end = time.perf_counter()
    #     rr_1_results.write(str(residue) + ", " + str(end - start) + "\n")

    #     # For hc0
    #     start = time.perf_counter()
    #     residue = hill_climbing(arr, False)
    #     end = time.perf_counter()
    #     hc_0_results.write(str(residue) + ", " + str(end - start) + "\n")

    #     # For hc1
    #     start = time.perf_counter()
    #     residue = hill_climbing(arr, True)
    #     end = time.perf_counter()
    #     hc_1_results.write(str(residue) + ", " + str(end - start) + "\n")

    #     # For sa0
    #     start = time.perf_counter()
    #     residue = simulated_annealing(arr, False)
    #     end = time.perf_counter()
    #     sa_0_results.write(str(residue) + ", " + str(end - start) + "\n")

    #     # For sa1
    #     start = time.perf_counter()
    #     residue = simulated_annealing(arr, True)
    #     end = time.perf_counter()
    #     sa_1_results.write(str(residue) + ", " + str(end - start) + "\n")

    # for file in all_results:
    #     file.close()

    # FOR AUTOGRADER!!!
    if len(args) != 3:
        print("ERROR: NOT ENOUGH ARGUMENTS")
        return

    arr = []
    try:
        file = open(args[2], 'r')
        for num in file:
            arr.append(int(num))
        file.close()
    except:
        print("ERROR IN READING INPUT")

    if len(arr) == 0:
        print("ERROR IN READING FILE")
        return

    # Cases for algorithms
    algorithm_type = int(args[1])
    match algorithm_type:
        case 0:
            print(kk(arr))
        case 1:
            print(repeated_random(arr, False))
        case 2:
            print(hill_climbing(arr, False))
        case 3:
            print(simulated_annealing(arr, False))
        case 11:
            print(repeated_random(arr, True))
        case 12:
            print(hill_climbing(arr, True))
        case 13:
            print(simulated_annealing(arr, True))


if __name__ == "__main__":
    main(sys.argv[1:])
