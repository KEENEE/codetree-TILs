from collections import deque

input = open("input.txt").readline
n, m, p, c, d = map(int, input().split())

rdf = list(map(int, input().split()))
rdf = [rdf[0]-1 , rdf[1]-1]
rdf_direction = -1
santas = [list(map(int, input().split())) for _ in range(p)]
santas.sort()
santas = [[x-1,y-1] for _,x,y in santas]
santas_directions = [-1]*p

scores = [0] * p
failed = [] # 탈락한 산타
hit = [] # 기절한 산타
hit_time = []   # 기절한 타이밍

dx = [-1,0,1,0,-1,1,1,-1]#상우하좌
dy = [0,1,0,-1,1,1,-1,-1]


def move_rdf():
    global rdf
    global rdf_direction
    # 가까운 산타를 향해 1칸 돌진
    # 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 선택
    x,y = rdf
    min_idx = -1
    min_dist = -1

    for i, (sx, sy) in enumerate(santas):
        if i not in failed:
            distance = (x-sx)**2 + (y-sy)**2
            if min_idx == -1:
                min_idx = i
                min_dist = distance
            else:
                if distance < min_dist:
                    min_idx = i
                    min_dist = distance
                elif distance == min_dist:
                    if sx > santas[min_idx][0]:
                        min_idx = i
                        min_dist = distance
                    elif sx == santas[min_idx][0]:
                        if sy > santas[min_idx][1]:
                            min_idx = i
                            min_dist = distance

    near_dist = -1
    sx, sy = santas[min_idx]

    for j in range(8):
        nx = x+dx[j]
        ny = y+dy[j]

        if 0 <= nx < n and 0 <= ny < n:
            distance = (nx-sx)**2 + (ny-sy)**2
            if near_dist == -1:
                rdf = [nx, ny]
                rdf_direction = j
                near_dist = distance
            elif near_dist > distance:
                rdf = [nx, ny]
                rdf_direction = j
                near_dist = distance


def move_santas(k):
    # 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동합니다.
    near_dist = -1
    rx, ry = rdf
    sx, sy = santas[k]
    cur_distance = (sx-rx)**2 + (sy-ry)**2

    for j in range(4):
        nx = sx+dx[j]
        ny = sy+dy[j]

        if 0 <= nx < n and 0 <= ny < n:
            if [nx, ny] not in santas: # 산타는 다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.
                distance = (nx-rx)**2 + (ny-ry)**2
                if distance < cur_distance:
                    santas[k] = [nx, ny]
                    santas_directions[k] = j
                    cur_distance = distance


def collision(which, idx):
    if which == "rdf":
        # 산타는 자신이 이동해온 반대 방향으로 D 칸 만큼 밀려나게 됩니다.
        direction = (santas_directions[idx]+2) % 4
        power = d
    else: 
        # 산타는 루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.
        direction = rdf_direction
        power = c

    x, y = santas[idx]
    nx = x + dx[direction] * power
    ny = y + dy[direction] * power

    if 0 <= nx < n and 0 <= ny < n:
        waitlist = []
        if [nx, ny] in santas:
            waitlist.append(santas.index([nx,ny]))
            
        santas[idx] = [nx, ny]
        
        while waitlist:
            cur = waitlist[0]
            cx, cy = santas[cur]
            del waitlist[0]

            nx = cx+dx[direction]
            ny = cy+dy[direction]

            if 0 <= nx < n and 0 <= ny < n:
                if [nx, ny] in santas:
                    waitlist.append[santas.index(cur)]
            
                santas[cur] = [nx, ny]
            else:
                santas[cur] = [-1,-1]
                failed.append(cur)
                break
        
    else:   # 만약 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락됩니다.
        failed.append(idx)
        santas[idx] = [-1,-1]



for turn in range(m):
    # t+2 time이 되면 기절한 산타 살리기
    if hit_time:
        while hit_time[0] + 1 < turn:
            del hit[0]
            del hit_time[0]
            if not hit_time:
                break

    # 루돌프 이동
    move_rdf()

    # 루돌프가 움직여서 충졸이 일어난 경우
    if rdf in santas:
        idx = santas.index(rdf)
        scores[idx] += c
        hit.append(idx)
        hit_time.append(turn)
        collision("santa", idx)


    # 산타 이동
    for k in range(len(santas)):
        # 기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없습니다.
        if k not in failed and k not in hit:
            # print(santas[k])
            move_santas(k)
            # print(santas[k])
            
            # 산타가 움직여서 충돌이 발생한 경우
            if santas[k] == rdf:
                scores[k] += d
                hit.append(k)
                hit_time.append(turn)
                collision("rdf", k)

    if len(failed) == len(santas):
        break

    # 매 턴 이후 아직 탈락하지 않은 산타들에게는 1점씩을 추가로 부여합니다.
    for l in range(len(santas)):
        if l not in failed:
            scores[l] += 1

print(*scores)


# 오답노트
# 1. 당연히 산타가 순서대로 주어질 것이라 가정함. 불필요하게 번호를 주지는 않으니 고려하기!
# 2. 변수에 새로운 값을 할당할때 global 처리해주기.