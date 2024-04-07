from collections import deque

# input = open("input.txt").readline

n, m, k = map(int, input().split())

space = [list(map(int, input().split())) for _ in range(n)] #0은 부서진포탑
space = [[[space[i][j], 0, -(i+j), -j] for j in range(m)] for i in range(n)]

# 공격력이 0 이하가 되며 ㄴ부서지며 더 이상 공격할 수 없음.abs

# 우하좌상
dx = [0,1,0,-1, -1,1,1,-1]
dy = [1,0,-1,0, 1,1,-1,-1]

def weakest():
    # 공격력이 가장 낮은 포탑 - 가장최근에 공격한 포탑 - 행열합이 큰 포탑 - 열이 큰포탑
    mx, my = -1,-1
    min_attack = [5001, 1, 1, 1]

    for i in range(n):
        for j in range(m):
            if space[i][j][0] > 0:
                if space[i][j] < min_attack:
                    min_attack = space[i][j]
                    mx, my = i, j
    
    return mx, my
    

def strongest(wx, wy):
    # 공격력이 가장 높은 포탑 - 공격이 가장 오래된 포탑 - 행열합이 작은 포탑 - 열이 작은 포탑
    mx, my = -1,-1
    max_attack = [-1, -1000, -10, -10]

    for i in range(n):
        for j in range(m):
            if space[i][j][0] > 0 and i != wx and j != wy:    # 부서진 포탑이거나 공격자가 아닌 경우만 체크
                if space[i][j] > max_attack:
                    min_attack = space[i][j]
                    mx, my = i, j
    
    return mx, my


# def dfs(x, y, sx, sy, route, visited):
#     if x == sx and y == sy:
#         return route, True
    
#     for i in range(4):
#         nx = x+dx[i]
#         ny = y+dy[i]

#         if 0<=nx<n and 0<=ny<y:
#             if space[nx][ny] != 0 and visited[nx][ny] == False:
#                 visited[nx][ny] = True
#                 route.append([nx, ny])
#                 new_route, found = dfs(nx, ny, sx, sy, route, visited)
#                 visited[nx][ny] = False
        
#         if found:
#             break

#     return new_route, found


# def laser_attack(wx, wy, sx, sy):
#     # dfs로 다 가보면서 route가 제일 짧게 나온 경우를 리턴
#     route = [[k] for k in range(n*m)]
#     visited = [[False]*m for _ in range(n)]

#     for i in range(4):
#         new_route = []

#         nx = wx+dx[i]
#         ny = wy+dy[i]

#         if 0<=nx<n and 0<ny<m:
#             if space[nx][ny] != 0:
#                 new_route.append([nx, ny])
#                 visited[nx][ny] = True
                
#                 new_route, found = dfs(nx, ny, sx, sy, new_route, visited)
#                 if found:
#                     if len(route) > len(new_route)
#                     route = new_route

#                 visited[nx][ny] = False
    
#     return route


def laser_attack(wx, wy, sx, sy):
    # bfs로 가면서 어디서 왔는지 기록해놓기. found이면 경로 역추척해서 append
    history = [[[] for _ in range(m)] for _ in range(n)]
    # -1,0,1    0,0,2   1,0,3   1,1,3
         
    found = False

    # 레이저 루트 찾기.
    q = deque()
    q.append([-1, wx, wy])

    while q:
        direction, x, y = q.popleft()   # -1,0,1    0,0,2

        for i in range(4):
            nx = (x + dx[i] + n) % n
            ny = (y + dy[i] + n) % n

            if nx == sx and ny == sy:
                found = True
                history[nx][ny].append([direction, x, y])
                break

            if space[nx][ny][0] > 0:
                history[nx][ny].append([direction, x, y])
                q.append([i, nx, ny])

        if found:
            break
    
    # for i in range(n):
    #     print(history[i])

    # 경로 역추적하기
    route = []
    cx, cy = sx, sy
    if not history[cx][cy]: # 목적지에 history가 없으면 길이 없다는 뜻이므로 빈 루트 리턴
        return route
        
    while True:
        d, ox, oy = history[cx][cy][0]
        # print(d, ox, oy)
        if d == -1:
            break
        route.append([ox, oy])  # 1,3
        
        bx, by = ox - dx[d], oy - dy[d]

        if len(history[ox][oy]) > 1:
            for d, hx, hy in history[ox][oy]:
                if hx == bx and hy == by:
                    history[ox][oy] = [[d, hx, hy]]
                    break

        cx, cy = ox, oy

    # 공격
    if route:
        power = space[wx][wy][0]
        for rx, ry in route:
            space[rx][ry][0] -= power//2
        space[sx][sy][0] -= power
        
    return route


def bomb_attack(wx, wy, sx, sy):
    power = space[wx][wy][0]
    space[sx][sy][0] -= power
    route = []

    for i in range(8):
        nx = (sx + dx[i] + n) % n
        ny = (sy + dy[i] + n) % n
    
        if nx != wx and ny != wy:
            space[nx][ny][0] -= power//2
            route.append([nx, ny])

    return route



for turn in range(k):
    # 가장 약한 포탑을 공격자로 선정
    wx, wy = weakest()

    # for z in range(n):
    #     print(space[z])
    # breakpoint()
    space[wx][wy][0] += (n+m)
    space[wx][wy][1] = -turn # 최근 공격 타이밍 표시

    # for z in range(n):
    #     print(space[z])
    # breakpoint()

    sx, sy = strongest(wx, wy)
    
    route = laser_attack(wx, wy, sx, sy)
    # print(route)
    # for z in range(n):
    #     print(space[z])
    # breakpoint()
    
    if not route: # 루트가 비어있으면 포탄 어택
        route = bomb_attack(wx, wy, sx, sy)

    route.append([sx, sy])
    route.append([wx, wy])

    count = 0
    for i in range(n):
        for j in range(m):
            if space[i][j][0] > 0:
                count += 1
                if [i,j] not in route:
                    space[i][j][0] += 1

    # 부서지지 않은 포탑이 1개가 되면 즉시 중지됨
    if count <= 1:
        break

    # for z in range(n):
    #     print(space[z])
    # breakpoint()

# 남아있는 가장 강한 포탑의 공격력
max_potop = 0

for i in range(n):
    for j in range(m):
        if space[i][j][0] > max_potop:
            max_potop = space[i][j][0]

print(max_potop)

# 오답노트
# 1. 최단거리 문제는 bfs로 풀자... dfs는 머리터져