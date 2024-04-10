import heapq

# input = open("input.txt").readline

q = int(input())

n, m, p = -1,-1,-1

pids = [-1] * 2000
distances = [-1] * 2000
jumps = [0] * 2000
locations = [[0,0]] * 2000
id_to_idx = [-1] * 10000000
scores = [0] * 2000

dx = [-1,0,1,0]
dy = [0,1,0,-1]

def prepare(info):
    global n, m, p
    
    n, m, p, *rabbits = info

    for i in range(p):
        pids[i] = rabbits[(i+1)*2-2]
        distances[i] = rabbits[(i+1)*2-1]

        id_to_idx[pids[i]] = i

def run(info):
    k, s = info
    heap = []
    for i in range(p):
        x,y = locations[i]
        # 우선순위는 (총 점프 횟수가 적은, 행 번호 + 열 번호가 작은, 행 번호가 작은, 열 번호가 작은, 고유번호가 작은)
        heapq.heappush(heap, [jumps[i], x+y, x, y, pids[i]])
        
    jumps_k = [0]*2000
    # 가장 우선순위가 높은 토끼를 뽑아 멀리 보내주는 것을 K번 반복합니다.
    for turn in range(k):
        # 우선순위가 가장 높은 토끼를 i번 토끼라 했을 때 
        first = heapq.heappop(heap)
        id_ = id_to_idx[first[4]]
        dist = distances[id_]

        # 상하좌우 네 방향으로 각각 d_ㅑ만큼 이동했을 때의 위치를 구합니다. 
        # 이동하는 도중 그 다음 칸이 격자를 벗어나게 된다면 방향을 반대로 바꿔 한 칸 이동하게 됩니다. 
        x, y = locations[id_]
        cand = []
        for j in range(4):
            nx = (x + dx[j]*dist) % (2*(n-1))
            ny = (y + dy[j]*dist) % (2*(m-1))

            nx = min(nx, 2*(n-1)-nx)
            ny = min(ny, 2*(m-1)-ny)

            heapq.heappush(cand, [-(nx+ny), -nx, -ny])
        
        # 4개의 위치 중 (행 번호 + 열 번호가 큰 칸, 행 번호가 큰 칸, 열 번호가 큰 칸) 순으로 우선순위가 높은 칸을 골라 토끼를 이동시킵니다.
        _, mnx, mny = heapq.heappop(cand)
        nx, ny = -mnx, -mny

        locations[id_] = [nx, ny]
        jumps[id_] += 1
        jumps_k[id_] += 1
        
        heapq.heappush(heap, [jumps[id_], nx+ny, nx, ny, pids[id_]])

        # 이 칸의 위치를 (r_i, c_i)라 했을 때 i번 토끼를 제외한 나머지 P−1마리의 토끼들은 전부 r_i+c_i 만큼의 점수를 동시에 얻게 됩니다
        score = nx+ny+2
        for l in range(p):
            if l != id_:
                scores[l] += score


    # K번의 턴이 모두 진행된 직후에는 (행 번호 + 열 번호가 큰 토끼, 행 번호가 큰 토끼, 열 번호가 큰 토끼, 고유번호가 큰 토끼) 순으로
    # 가장 우선순위가 높은 토끼를 골라 점수 S를 더해주게 됩니다. 단, 이 경우에는 K번의 턴 동안 한번이라도 뽑혔던 적이 있던 토끼를 골라야만 함
    add_score = []
    for o in range(p):
        if jumps_k[o] > 0:
            ox, oy = locations[o]
            heapq.heappush(add_score, [-(ox+oy), -ox, -oy, -pids[o]])

    _, _, _, mpid = heapq.heappop(add_score)

    index = id_to_idx[-mpid]
    scores[index] += s




def change(info):
    pid, l = info
    distances[id_to_idx[pid]] *= l



for _ in range(q):
    ins, *info = list(map(int, input().split()))
    # print(ins, info)

    if ins == 100:
        prepare(info)
    elif ins == 200:
        run(info)
    elif ins == 300:
        change(info)
    elif ins == 400:
        break

# 최고의 토끼 선정
print(max(scores))



# 오답노트
# 1. a, *b로 a를 제외한 모든 요소를 b라는 리스트에 저장할 수 있음.
# 2. id to index 변환할 경우 인덱스 쓰는 부분 변환해야하는지 잘 체크해주기