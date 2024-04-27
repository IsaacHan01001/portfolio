#save for now
def solve():
    N, strList, E_N = initialize()
    only_cows = run_preprocessing(strList, E_N)
    if len(only_cows[0]) > 1 or len(only_cows[1]) >1:
        raise Exception
    leader_g = None if len(only_cows[0]) ==0 else only_cows[0]
    leader_h = None if len(only_cows[1]) == 0 else only_cows[1]
    count = calculate_candidates(strList, E_N, leader_g, leader_h)
    print(count)

def initialize():
    N = int(input())
    strList = input()
    E_N = list(map(int, input().split()))
    return N, strList, E_N
def run_preprocessing(strList, E_N):
    initial = [[], []] #G, H
    for cow_ind, type in enumerate(strList):
        if (cow_ind + 1) <= E_N[cow_ind] <= len(strList):
            pass
        else:
            if strList[cow_ind] == "G":
                initial[0].append(cow_ind)
            else:
                initial[1].append(cow_ind)
    return initial
def calculate_candidates(strList, E_N, leader_g, leader_h):
    count = 0
    gcow_ridx, hcow_ridx = strList.rfind("G") + 1, strList.rfind("H") + 1
    gcow_lidx, hcow_lidx = strList.find("G") + 1, strList.find("H") + 1
    if (leader_g is not None) and (leader_h is not None):
        return 1
    elif (leader_g is not None) or (leader_h is not None):
        leader_determined = leader_h if (leader_g is None) else leader_g
        read_E_N = E_N[leader_determined] # contains all colors of same kind or ind of other leader
        idx = gcow_ridx if (strList[leader_determined] == "G") else hcow_ridx
        lidx = gcow_lidx if (strList[leader_determined] == "G") else hcow_lidx
        if (strList[read_E_N - 1] != strList[leader_determined]):
            return 1
        elif (read_E_N >= idx) and (leader_determined == lidx):
            for ind, value in enumerate(strList):
                if value != strList[leader_determined]:
                    idx = gcow_ridx if (strList[ind] == "G") else hcow_ridx
                    lidx = gcow_lidx if (strList[ind] == "G") else hcow_lidx
                    if E_N[ind] == ind + 1:
                        count += 1
                    elif (ind + 1 == lidx) and (E_N[ind] >= idx):
                        count += 1
        else:
            raise Exception
    else:
        for ind, value in enumerate(strList):
            E1 = E_N[ind]
            ridx, lidx = (gcow_ridx, gcow_lidx) if (strList[ind] == "G") else (hcow_ridx, hcow_lidx)
            if (strList[E1 - 1] != value):
                ridx2, lidx2 = (gcow_ridx, gcow_lidx) if (strList[E1 - 1] == "G") else (hcow_ridx, hcow_lidx)
                E2 = E_N[E1 - 1]
                if (lidx2 == E1) and (E2 >= ridx2):
                    count += 1
                    continue
                elif E2 == ind + 1:
                    count += 1
                    continue
            if (E1 >= ridx) and (ind + 1 == lidx):
                for other_cow in range(ind + 1, len(strList)):
                    if strList[other_cow] != value:
                        ridx2, lidx2 = (gcow_ridx, gcow_lidx) if (strList[other_cow] == "G") else (hcow_ridx, hcow_lidx)
                        E2 = E_N[other_cow]
                        if (lidx2 == other_cow + 1) and (E2 >= ridx2):
                            count += 1
                            continue
                        elif E2 == ind + 1:
                            count += 1
                            continue
    return count



if __name__ == '__main__':
    solve()
