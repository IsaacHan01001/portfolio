def solve():
    n, cow_type, E_N = initialize()
    count = calculate_candidate_pairs(cow_type, E_N)
    print(count)

def initialize():
    n = int(input())
    cow_type = input()
    E_N = list(map(int, input().split()))
    return n, cow_type, E_N

def calculate_candidate_pairs(cow_type, E_N):

    count = 0
    g_lower, g_upper = cow_type.find("G"), cow_type.rfind("G")
    h_lower, h_upper = cow_type.find("H"), cow_type.rfind("H")

    for ind1, cow1 in enumerate(cow_type):
        E1 = E_N[ind1] - 1
        ind1_lower, ind1_upper = (g_lower, g_upper) if cow1 == "G" else (h_lower, h_upper)
        if (ind1 == ind1_lower) and (E1 >= ind1_upper):
            for ind2 in range(ind1 + 1, len(cow_type)):
                if cow_type[ind2] != cow1:
                    E2 = E_N[ind2] - 1
                    ind2_lower, ind2_upper = (g_lower, g_upper) if cow_type[ind2] == "G" else (h_lower, h_upper)
                    if (ind2 == ind2_lower) and (E2 >= ind2_upper):
                        count += 1
                        continue
                    elif (ind2 <= ind1 <= E2):
                        count += 1
                        continue
        else:

            for ind2 in range(ind1 + 1, E_N[ind1]):
                if cow_type[ind2] != cow1:
                    E2 = E_N[ind2] - 1
                    ind2_lower, ind2_upper = (g_lower, g_upper) if cow_type[ind2] == "G" else (h_lower, h_upper)
                    if (ind2 == ind2_lower) and (E2 >= ind2_upper):
                        count += 1
                        continue
                    elif (ind2 <= ind1 <= E2):
                        count += 1
                        continue

    return count




if __name__ == "__main__":
    solve()

