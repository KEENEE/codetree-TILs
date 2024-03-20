n, m, k, c = list(map(int, input().split()))

space = [list(map(int, input().split())) for _ in range(n)]
ing = [[[]]*n for _ in range(n)]

for i in range(n):
    for j in range(n):
        ing[i][j] = [space[i][j], 0, 0]    # 최종값, 제초제여부, grown

dx = [0,1,0,-1]
dy = [1,0,-1,0]
dw = [-1,1,1,-1]
dz = [1,1,-1,-1]

def grow():
    for i in range(n):
        for j in range(n):
            ing
            if ing[i][j][0] > 0:
                for d in range(4):
                    nx = i+dx[d]
                    ny = j+dy[d]

                    if 0<=nx<n and 0<=ny<n:
                        if ing[nx][ny][0] > 0:
                            ing[i][j][0] += 1


def spread():
    for i in range(n):
        for j in range(n):
            candidate = []
            if ing[i][j][0] > 0:
                for d in range(4):
                    nx = i+dx[d]
                    ny = j+dy[d]

                    if 0<=nx<n and 0<=ny<n:
                        if ing[nx][ny][0] == 0 and ing[nx][ny][1] == 0:
                            candidate.append((nx,ny))
                            
            if candidate:
                for cx,cy in candidate:
                    ing[cx][cy][2] += ing[i][j][0]//len(candidate)

    # 없앨 수 없을까?
    for i in range(n):
        for j in range(n):
            ing[i][j][0] += ing[i][j][2]
            ing[i][j][2] = 0



def find_kill(x,y,remaining, direction=None, kill = False):
    global killed

    if remaining == 0:
        if ing[x][y][0] > 0:
            killed += ing[x][y][0]
        if kill:
            ing[x][y][0] = 0    # 나무 실제로 죽이고
            ing[x][y][1] = c    # 그 자리에 제초제 남은 연수 표시
        return killed

    if ing[x][y][0] > 0:    # 나무가 있는 칸일 때만 제초제를 뿌림
        if direction != None:
            killed += ing[x][y][0]
            if kill:
                ing[x][y][0] = 0    # 나무 실제로 죽이고
                ing[x][y][1] = c    # 그 자리에 제초제 남은 연수 표시
            
            nx = x+dw[direction]
            ny = y+dz[direction]
            
            if 0<=nx<n and 0<=ny<n:
                if ing[nx][ny][0] > 0: # 한번더 대각선으로 갔을때 나무임
                    find_kill(nx, ny, remaining-1, direction, kill)
                elif ing[nx][ny][0] == 0 and kill:   # 대각선이 빈자리이면
                    ing[nx][ny][1] = c    # 그 자리에 제초제 남은 연수 표시

        else:   # 최초에만 모든 방향 탐색
            killed += ing[x][y][0]  # 시작한 위치부터 죽이고 시작
            if kill:
                ing[x][y][0] = 0    # 나무 죽이고
                ing[x][y][1] = c    # 제초제 남은 연수 표시

            for d in range(4):
                nx = x+dw[d]
                ny = y+dz[d]
                
                if 0<=nx<n and 0<=ny<n:
                    if ing[nx][ny][0] > 0: # 대각선이 나무이면
                        find_kill(nx, ny, remaining-1, d, kill)  # 그 자리에서 한번더 찾음, 가던 방향명시
                    elif ing[nx][ny][0] == 0 and kill:   # 대각선이 빈자리이면
                        ing[nx][ny][1] = c    # 그 자리에 제초제 남은 연수만 표시하고 끝남

    return killed
    

total_killed = 0
for years in range(m):
    grow()

    spread()

    max_killed = 0
    idx = None
    for i in range(n):
        for j in range(n):
            ing[i][j][1] -= 1   # 나무 성장 끝났으니까 여기서 제초제 남은연수 1년씩 줄여도 됨
            killed = 0
            round_killed = find_kill(i, j, k, None, killed)
            if round_killed > max_killed:
                max_killed = round_killed
                idx = (i, j)

    if idx:
        kx, ky = idx    # 제초제를 뿌릴 좌표
        find_kill(kx, ky, k, kill = True)
        total_killed += max_killed

print(total_killed)