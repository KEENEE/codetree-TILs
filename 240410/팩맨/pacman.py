import copy
# input = open("input.txt").readline
m, t = map(int, input().split())

packman = list(map(int, input().split()))

monsters = [list(map(int, input().split())) for _ in range(m)]
monsters = [[x,y,d-1] for x,y,d in monsters]
dead = []

dx = [-1,-1,0,1,1,1,0,-1]
dy = [0,-1,-1,-1,0,1,1,1]

max_ate = 0
max_route = []

def available(nx, ny):
    return 1<=nx<5 and 1<=ny<5 and [nx,ny] != packman


def monster_move():
    for i, monster in enumerate(monsters):
        x, y, d = monster
        if d < 0:
            continue
        nx = x+dx[d]
        ny = y+dy[d]

        cur_d = d
        while not available(nx, ny):
            cur_d = (cur_d+1) % 8
            nx = x+dx[cur_d]
            ny = y+dy[cur_d]
            
            if cur_d == d:
                break

        if available(nx, ny):
            monsters[i] = [nx, ny, cur_d]



dxp = [-1,1,0,0]
dyp = [0,0,-1,1]

def dfs(x, y, count, route, ate):
    global max_ate, max_route

    if count == 3:
        route.append([x,y])
        if ate > max_ate:
            max_route = route
        return

    for k in range(4):
        nx = x + dxp[k]
        ny = y + dyp[k]

        if 0<=nx<4 and 0<=ny<4:
            route.append([nx,ny])
            total = 0
            for m in monsters:
                if m[0] == nx and m[1] == ny and m[2] >= 0:
                    ate += 1
                    total += 1

            dfs(nx, ny, count+1, route, ate)

            if total:
                ate -= total
            route.remove([nx, ny])
    

def packman_move():
    global max_ate, max_route
    max_ate = 0
    max_route = []

    x, y = packman
    count = 0
    route = []
    ate = 0

    dfs(x, y, count, route, ate)

    idxs = []
    for i, (x,y,d) in enumerate(monsters):
        if [x,y] in route:
            idxs.append(i)

    return idxs


for turn in range(1,t+1):
    # print("-----", turn, "-----")
    # 현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제
    # 복제된 몬스터는 아직은 부화되지 않은 상태로 움직이지 못함
    copied = copy.deepcopy(monsters)
    # print("initial state", monsters)
    # 이동
    monster_move()
    # print("after move", monsters)
    idxs = packman_move()
    # print(max_route)
    # print("dead monsters", idxs)
    
    # 시체 정보 저장
    for idx in idxs:
        monsters[idx][2] = -turn
    # print("dead reflect", monsters)

    # 시체 소멸
    indexes = []
    for k, (x,y,d) in enumerate(monsters):
        if d<0 and -d+2 == turn:
            indexes.append(k) 

    for index in reversed(indexes):
        monsters.remove[index]
    # print("after dead", monsters)
    # 복제 완성
    monsters = monsters + copied
    # print("after copy", monsters)
final_count = 0
for x,y,d in monsters:
    if d>=0:
        final_count += 1

print(final_count)