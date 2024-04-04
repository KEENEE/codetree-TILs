from collections import deque

# input = open("input.txt").readline
n, m = map(int, input().split())

space = [list(map(int, input().split())) for _ in range(n)] # 0은 빈공간, 1은 베이스캠프
stores = [list(map(int, input().split())) for _ in range(m)]
stores = [[i-1,j-1] for i,j in stores]
cur = []

dx = [-1,0,0,1]
dy = [0,-1,1,0]


def move():
    # 편의점 방향을 향해 1칸 움직임
    # 최단거리로 움직여야함. 도달하기까지 거쳐야하는 칸의 수가 최소가 되도록.

    for k, person in enumerate(cur):
        if person == -1:
            continue
        # print(k, cur[k], stores[k])
        px, py = person

        ### 최단거리 경로 판단할때 이렇게 다 가보고 결정하는게 맞나?
        min_direction = -1
        distances = [n*2] * 4

        # 4방향 각각에 대해 bfs 실행
        for d in range(4):
            nx = px + dx[d]
            ny = py + dy[d]
            # print(nx, ny)

             # 편의점에 도달하면 멈추기
            if stores[k] == [nx,ny]:
                distances[d] = 0
                break

            if 0<=nx<n and 0<=ny<n:
                if space[nx][ny] != -1:
                    # 해당 칸에서 편의점까지 얼마나 걸리는지 판단
                    q = deque()
                    q.append([0, nx, ny])
                    
                    visited = [[False]*n for _ in range(n)]
                    found = False
                    while q:
                        turn, x, y = q.popleft()
                        visited[x][y] = True

                        for j in range(4):
                            tx = x + dx[j]
                            ty = y + dy[j]

                            if [tx,ty] == stores[k]:
                                found = True
                                break
                            
                            if 0<=tx<n and 0<=ty<n:
                                if space[tx][ty] != -1 and visited[tx][ty] == False:
                                    visited[tx][ty] = True
                                    q.append([turn+1, tx, ty])
                        
                        if found:
                            distances[d] = turn + 1
                            break

        
        # 4방향 다 탐색한 후 편의점까지 도달한 거리가 가장 짧았던 방향의 인덱스 추출해서 그 방향으로 이동
        # print(distances)
        min_idx = distances.index(min(distances))
        fx, fy = px+dx[min_idx], py+dy[min_idx]
        # print(cur, fx, fy)
        cur[k] = [fx, fy]
        # print(cur, fx, fy)
        # 이동이 끝나면 다른 사람은 해당 편의점 칸을 지나갈 수 없게 됨. -1처리
        if [fx, fy] == stores[k]:
            space[fx][fy] = -1
            # print(fx, fy)
            cur[k] = -1
            stores[k] = [-1,-1]

                    


def nearest(store):
    # bfs로 돌면서 편의점에서 가까운 곳 찾기
    q = deque()

    q.append([0, store[0], store[1]])
    cur_turn = 0
    candidate = []
    visited = [[False]*n for _ in range(n)]
    

    while q:
        turn, x, y = q.popleft()
        visited[x][y] = True

        if turn > cur_turn:
            # print(candidate)
            # 다음 거리 진행하기 전에 2개 이상이면 행열이 작은것 고르기
            if candidate:   ### 여러개 중 우선순위에 따라 하나 선정하는 방법 보기
                candidate.sort()
                return candidate[0]
                    
            cur_turn += 1

        for j in range(4):
            nx = x + dx[j]
            ny = y + dy[j]
            # print(nx, ny)

            if 0<=nx<n and 0<=ny<n:
                if space[nx][ny] != -1 and visited[nx][ny] == False:
                    if space[nx][ny] == 1:
                        candidate.append([nx,ny])
                    q.append([turn+1, nx, ny])
                    
    return candidate[0]
             


def basecamp(i):
    # t분일때 t번 사람은 가고싶은 편의점과 가장 가까운 베이스캠프에 들어감
    # 여러개이면 행이 작은, 같다면 열이 작은 캠프로 들어감, 모두 이동한 뒤 -1처리
    bx,by = nearest(stores[i])
    cur.append([bx, by])
    space[bx][by] = -1


time = 0
while True:
    # print()
    # print("-----",time,"-----")
    
    if cur:
        move()
        
    if stores.count([-1,-1]) == len(stores):
        break

    if time < m:
        basecamp(time)

    # for z in range(n):
    #     print(space[z])
    # print(cur)
    # print(stores)
    time += 1

    # breakpoint()

print(time+1)