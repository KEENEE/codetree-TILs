import copy
# input = open("input.txt").readline
m, t = map(int, input().split())

packman = list(map(int, input().split()))
packman = [packman[0]-1, packman[1]-1]

monsters = [list(map(int, input().split())) for _ in range(m)]
monsters = [[x-1,y-1,d-1] for x,y,d in monsters]
dead = []

dx = [-1,-1,0,1,1,1,0,-1]
dy = [0,-1,-1,-1,0,1,1,1]

max_ate = 0
max_route = []

def available(nx, ny):
    return 0<=nx<4 and 0<=ny<4 and [nx,ny] != packman


def monster_move():
    for i, monster in enumerate(monsters):
        x, y, d = monster
        
        if d < 0:
            continue
        # print(i, x,y,d)
        nx = x+dx[d]
        ny = y+dy[d]

        # print(nx, ny)
        # print(available(nx, ny))
        cur_d = d
        while not available(nx, ny):
            cur_d = (cur_d+1) % 8
            nx = x+dx[cur_d]
            ny = y+dy[cur_d]
            # print(nx, ny, cur_d)
            if cur_d == d:
                break

        if available(nx, ny):
            # print(nx, ny, cur_d)
            monsters[i] = [nx, ny, cur_d]



dxp = [-1,0,1,0]
dyp = [0,-1,0,1]

def dfs(x, y, count, route, ate, visited):
    global max_ate, max_route
    
    if count == 3:
        # print(x, y, count, route, ate)
        if ate > max_ate:
            
            max_route = copy.deepcopy(route)
            max_ate = ate
        return

    for k in range(4):
        nx = x + dxp[k]
        ny = y + dyp[k]

        if 0<=nx<4 and 0<=ny<4:
            route.append([nx,ny])
            visit = []
            for i, m in enumerate(monsters):
                if m[0] == nx and m[1] == ny and m[2] >= 0:
                    if not visited[i]:
                        visited[i] = True
                        visit.append(i)
            
            dfs(nx, ny, count+1, route, ate+len(visit), visited)
            
            for v in visit:
                visited[v] = False
            del route[-1]
    

def packman_move():
    global max_ate, max_route, packman
    max_ate = 0
    
    x, y = packman
    count = 0
    route = []
    ate = 0
    visited = [False] * len(monsters)

    dfs(x, y, count, route, ate, visited)
    packman = max_route[-1]

    idxs = []
    for i, (x,y,d) in enumerate(monsters):
        if d >= 0:
            if [x,y] in max_route:
                idxs.append(i)

    return idxs


for turn in range(1,t+1):
    # print("-----", turn, "-----")
    # 현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제
    # 복제된 몬스터는 아직은 부화되지 않은 상태로 움직이지 못함
    copied = []
    for m in monsters:
        if m[2] >= 0:
            copied.append(m)

    # print("initial state", monsters)
    # 이동
    monster_move()
    # print("after move", monsters)
    # print(packman)
    idxs = packman_move()
    # print("max_route", max_route)
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
        del monsters[index]
        
    # print("after dead", monsters)
    # 복제 완성
    monsters = monsters + copied
    # print("after copy", monsters)
    # breakpoint()

final_count = 0
for x,y,d in monsters:
    if d>=0:
        final_count += 1

print(final_count)