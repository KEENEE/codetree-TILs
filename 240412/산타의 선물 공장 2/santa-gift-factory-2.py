from collections import deque
import time
# input = open("input.txt").readline
q = int(input())

belts = []
n = -1
m = -1

# 0-99999:벨트, 100000-199999:선물
prevs = [None] * 100000
nexts = [None] * 100000


len_belts = [0] * 100000
belts_starts = [None] * 100000
belts_ends = [None] * 100000   

def printbelt():
    print("prevs", prevs)
    print("nexts", nexts)
    print("belts_starts", belts_starts)
    print("belts_ends", belts_ends)
    print("len_belts", len_belts)




def build(info):    # 100, n, m, b_1 b_2, ... , b_m
    global n, m

    n, m, *presents = info
    # n개의 벨트를 설치하고, 총 m개의 물건을 해당하는 번호의 벨트에 올려줌
    # 각 선물의 번호는 오름차순으로 벨트에 쌓입니다.

    for i in range(m):
        pid = i
        bid = presents[i] - 1

        if len_belts[bid] > 0:
            prevs[pid] = belts_ends[bid]
            nexts[belts_ends[bid]] = pid
        else:
            prevs[i] = -1    # 첫번째 노드는 prev가 -1
            belts_starts[bid] = pid

        len_belts[bid] += 1
        belts_ends[bid] = pid



def move(info):
    # 200, src, dst
    # m_src번째 벨트에 있는 선물들을 모두 m_dst번째 벨트의 선물들로 옮깁니다. 
    # 옯겨진 선물들은 m_dst 벨트 앞에 위치합니다. 
    # 만약 m_src번째 벨트에 선물이 존재하지 않다면 아무것도 옮기지 않아도 됩니다. 
    # 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력합니다.
    src, dst = info[0]-1, info[1]-1

    # src 벨트의 첫번째, 끝번째 선물 아이디 가져오기
    if len_belts[src] != 0:
        src_first = belts_starts[src]
        src_end = belts_ends[src]

        # 벨트 비우기
        belts_starts[src] = None
        belts_ends[src] = None

        # src 벨트 첫, 끝 선물들을 dst벨트와 연결
        dst_first = belts_starts[dst]
        belts_starts[dst] = src_first

        nexts[src_end] = dst_first
        prevs[dst_first] = src_end


    len_belts[dst] += len_belts[src]
    len_belts[src] = 0

    # while belts[src]:
    #     cur = belts[src].pop()
    #     pidx_to_bidx[cur] = dst
    #     belts[dst].appendleft(cur)

    print(len_belts[dst])


def change(info):
    # 300, src, dst
    # m_src번째 벨트에 있는 선물 중 가장 앞에 있는 선물을 m_dst번째 벨트의 선물들 중 가장 앞에 있는 선물과 교체합니다. 
    # 둘 중 하나의 벨트에 선물이 아예 존재하지 않다면 교체하지 않고 해당 벨트로 선물을 옮기기만 합니다. 
    # 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력합니다.
    src, dst = info[0]-1, info[1]-1

    # src 벨트에 선물이 있는경우
    if len_belts[src] != 0:
        # dst 벨트에 선물이 없는경우
        if len_belts[dst] == 0:
            src_first = belts_starts[src]
            src_first_next = nexts[src_first]
            nexts[src_first] = None
            belts_starts[src] = src_first_next    # 만약 next가 None이었으면 그대로 start도 None이 됨
            if len_belts[src] == 1:
                belts_ends[src] = None
            else:
                prevs[src_first_next] = -1
            belts_starts[dst] = src_first
            belts_ends[dst] = src_first
            len_belts[src] -= 1
            len_belts[dst] += 1
        # dst 벨트에 선물이 있는경우
        else:
            src_first = belts_starts[src]
            dst_first = belts_starts[dst]
            belts_starts[src] = dst_first
            belts_starts[dst] = src_first

            # 기존에 길이가 1이었던 경우, end좌표도 바꿔줘야 함
            if len_belts[src] == 1:
                belts_ends[src] = dst_first
            if len_belts[dst] == 1:
                belts_ends[dst] = src_first

            dst_first_next = nexts[dst_first]
            src_first_next = nexts[src_first]
            nexts[dst_first] = src_first_next
            nexts[src_first] = dst_first_next
    else:   # src 벨트에 선물이 없는경우
        if len_belts[dst] != 0:
            dst_first = belts_starts[dst]
            dst_first_next = nexts[dst_first]
            nexts[dst_first] = None
            
            belts_starts[dst] = dst_first_next    # 만약 next가 None이었으면 그대로 start도 None이 됨
            if len_belts[dst] == 1:
                belts_ends[dst] = None
            else:
                prevs[dst_first_next] = -1
            belts_starts[src] = dst_first
            belts_ends[src] = dst_first
            len_belts[src] += 1
            len_belts[dst] -= 1
    
    print(len_belts[dst])


def divide(info):   # 최대 100번
    # 400, src, dst
    # m_src번째 벨트에 있는 선물들의 개수를 n이라고 할 때 가장 앞에서 floor(n/2)번째까지 있는 선물을 m_dst번째 벨트 앞으로 옮깁니다. 
    # 만약 m_src 벨트에 선물이 1개인 경우에는 선물을 옮기지 않습니다. **
    # 옮긴 뒤에 m_dst번째 벨트에 있는 선물들의 개수를 출력합니다.

    src, dst = info[0]-1, info[1]-1

    n_src = len_belts[src]
    num = n_src // 2

    if n_src > 1:
        src_first = belts_starts[src]

        # num-1 번째 좌표 알아내기
        cur = src_first
        for i in range(num-1):
            new = next[cur]
            cur = new
        
        src_end = cur
        
        src_end_next = nexts[src_end]
        belts_starts[src] = src_end_next
        prevs[src_end_next] = -1
        # next가 무조건 있으므로 1개짜리 벨트의 end 핸들링 안해줘도 됨
        
        dst_first = belts_starts[dst]
        belts_starts[dst] = src_first
        nexts[src_end] = dst_first

        if dst_first != None:
            prevs[dst_first] = src_end

        if len_belts[dst] == 0:
            belts_ends[dst] = src_end
        

        len_belts[src] -= num
        len_belts[dst] += num

    print(len_belts[dst])


def get_present(info):
    # 500, pnum
    # 앞 선물의 번호 a과 뒤 선물의 번호 b라 할 때 a + 2 * b를 출력합니다. 없을 경우에는 각각 -1을 대입합니다.
    # 선물 번호 p_num가 주어질 때, 해당 선물의 앞 선물의 번호 a과 뒤 선물의 번호 b라 할 때 a + 2 * b를 출력합니다. 
    # 만약 앞 선물이 없는 경우에는 a = -1, 뒤 선물이 없는 경우에는 b = -1을 넣어줍니다.
    
    pidx = info[0] - 1

    if prevs[pidx] >= 0:
        a = prevs[pidx] + 1
    else:
        a = -1
    
    if nexts[pidx] != None:
        b = nexts[pidx] + 1
    else:
        b = -1
    # print(a, b)
    score = a + 2 * b
    print(score)


def get_belt(info):
    # 600, bnum
    # 벨트 번호 b_num이 주어질 때, 해당 벨트의 맨 앞에 있는 선물의 번호를 a, 맨 뒤에 있는 선물의 번호를 b, 
    # 해당 벨트에 있는 선물의 개수를 c라고 할 때, a + 2*b + 3*c의 값을 출력합니다. 
    # 선물이 없는 벨트의 경우에는 a와 b 모두 -1이 됩니다.

    bidx = info[0] - 1

    c = len_belts[bidx]
    
    if c == 0:
        a, b = -1, -1
    else:
        a = belts_starts[bidx] + 1
        b = belts_ends[bidx] + 1
    
    print(a + 2*b + 3*c)


for _ in range(q):
    ins, *info = list(map(int, input().split()))
    # print(ins, info)

    if ins == 100:
        build(info)
    if ins == 200:
        move(info)
    if ins == 300:
        change(info)
    if ins == 400:
        divide(info)
    if ins == 500:
        get_present(info)
    if ins == 600:
        get_belt(info)
    

    # printbelt()
    # print()