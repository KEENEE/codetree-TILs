# input = open("input.txt").readline
n, m, h, k = map(int, input().split())

runners = [list(map(int, input().split())) for _ in range(m)]
runners_directions = [d for x,y,d in runners]
runners = [[x-1,y-1] for x,y,d in runners]

trees = [list(map(int, input().split())) for _ in range(h)]
trees = [[x-1, y-1] for x, y in trees]


catcher = [n//2, n//2]
catcher_count = 0
cur_direction = 1

score = 0

dx = [-1,0,1,0]
dy = [0,1,0,-1]


# 5x5 map이면 1,1,2,2,3,3,4,4,4 리스트를 만듬
catcher_dir = []
d = 0
for b in range(1, n+1):
    if b < n:
        catcher_dir.extend([d]*b)
        d = (d+1) % 4
        catcher_dir.extend([d]*b)
        d = (d+1) % 4
    else:
        catcher_dir.extend([0]*(n-1))    #마지막엔 무조건 위 방향으로 n-1칸 전진

for c in reversed(catcher_dir):
    catcher_dir.append((c+2)%4)

catcher_directions = catcher_dir * (100//((n**2-1)*2) + 1)  # directions 이어붙이기


def move_runners():
    # 좌우로만 움직이는 유형은 오른쪽, 상하로만 움직이는 유형은 아래쪽 보고 시작
    # 현재 술래와의 거리가 3 이하인 도망자만 움직입니다. 
    # 두 사람간의 거리는 |x1 - x2| + |y1 - y2|로 정의됩니다.
    global catcher
    cx, cy = catcher
    for i, runner in enumerate(runners):
        rx, ry = runner
        d = runners_directions[i]
        # print(rx, ry, d)
        distance = abs(rx-cx) + abs(ry-cy)
        # print(cx, cy)
        # print(rx, ry, d, distance)
        if distance <= 3:
            nx = rx + dx[d]
            ny = ry + dy[d]

            # 격자 넘어가면 방향 바꿔주기
            if nx == -1:
                runners_directions[i] = (runners_directions[i] + 2) % 4
                nx = 1
            elif nx == n:
                runners_directions[i] = (runners_directions[i] + 2) % 4
                nx = n-2
            if ny == -1:
                runners_directions[i] = (runners_directions[i] + 2) % 4
                ny = 1
            elif ny == n:
                runners_directions[i] = (runners_directions[i] + 2) % 4
                ny = n-2
            
            if nx != cx or ny != cy:   
                runners[i] = [nx, ny]




def move_catcher():
    global catcher_count, catcher

    catch = 0
    cx, cy = catcher
    
    d = catcher_directions[catcher_count]
    nx = cx + dx[d]
    ny = cy + dy[d]
    
    # catcher 위치 옮겨줌
    catcher = [nx, ny]

    # 방향을 바로 틀어줘야함
    d = catcher_directions[catcher_count+1]

    while ([nx, ny] in runners and [nx, ny] not in trees):
        catch += 1
        idx = runners.index([nx, ny])
        del runners[idx]
        del runners_directions[idx]

    for _ in range(2):
        tx = nx + dx[d]
        ty = ny + dy[d]
       
        if 0<=tx<n and 0<=ty<n:
            while ([tx, ty] in runners and [tx,ty] not in trees):
                catch += 1
                idx = runners.index([tx, ty])
                del runners[idx]
                del runners_directions[idx]
        else:
            break

        nx, ny = tx, ty

    catcher_count += 1
    # print(catch)
    return catch


# print(catcher)
# print(runners)

for turn in range(k):
    # print("-----", turn, "-----")
    move_runners()
    # print("runner moved", runners)
    # print("directions", runners_directions)
    catch = move_catcher()
    # print("catcher moved", catcher)
    # print("trees", trees)
    # print("catcher catched", runners)
    # print("directions", runners_directions)
    
    # if catch > 0:
    #     print(turn, catch)
    score += (turn + 1) * catch
    # print(score)
    # breakpoint()


# k번의 턴 동안 얻게되는 총 점수 출력
print(score)


# 오답노트
# 한 위치에 여러명 있을수 있으면 다 잡아야함!!!!!!!!!!