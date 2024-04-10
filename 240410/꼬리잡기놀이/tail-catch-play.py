from collections import deque

# input = open("input.txt").readline

n, m, k = map(int, input().split())

dx = [0,-1,0,1]
dy = [1,0,-1,0]

start = [0,0]

space = [list(map(int, input().split())) for _ in range(n)]
heads = []
tails = []
score = 0

for i in range(n):
    for j in range(n):
        if space[i][j] == 1:
            heads.append([i,j])
        elif space[i][j] == 3:
            tails.append([i,j])

# print(heads)
# print(tails)
def move():        
    #머리를 2로 바꾸고 한칸 앞을 1로, 
    for i, head in enumerate(heads):
        hx, hy = head
        space[hx][hy] = 2
        for d in range(4):
            nx = hx + dx[d]
            ny = hy + dy[d]
        
            if 0<=nx<n and 0<=ny<n:
                if space[nx][ny] == 4:
                    space[nx][ny] = 1
                    heads[i] = [nx, ny]

    # 꼬리를 4로 바꾸고 한칸 앞을 3으로
    for j, tail in enumerate(tails):
        tx, ty = tail
        space[tx][ty] = 4
        for d in range(4):
            nx = tx + dx[d]
            ny = ty + dy[d]
        
            if 0<=nx<n and 0<=ny<n:
                if space[nx][ny] == 2:
                    space[nx][ny] = 3
                    tails[j] = [nx, ny]
    

def throw(d):
    sx, sy = start
    
    for i in range(n):
        nx = sx + dx[d]*i
        ny = sy + dy[d]*i

        # if 0<=nx<n and 0<=ny<n:
        if space[nx][ny] in [1,2,3]:
            return [nx, ny]
    
    return False

def scoring(hit):
    global score
    count = 1
    final = 0
    tx, ty = -1, -1
    hx, hy = -1, -1

    # head 찾고 점수 더하기
    if hit in heads:
        hx, hy = hit
        final = count
    else:
        q = deque()
        q.append([hit[0], hit[1], count])

        while q:
            x, y, count = q.popleft()
            
            for i in range(4):
                nx = x + dx[i] 
                ny = y + dy[i]
                
                if 0<=nx<n and 0<=ny<n:
                    if space[nx][ny] == 1:    # 머리인 경우
                        final = count + 1
                        hx, hy = nx, ny
                    elif space[nx][ny] == 2:    # 몸통인 경우 큐에 넣고 계속 진행
                        q.append([nx, ny, count+1])
                    elif space[nx][ny] == 3:    # 꼬리인 경우 큐에 넣지 않고 tail 좌표 기록만 해놓음
                        tx, ty = nx, ny
            
            if tx != -1 and hx != -1:
                break
    
    score += (final**2)

    # head 와 tail 방향 바꾸기
    t = tails.index([tx, ty])
    h = heads.index([hx, hy])

    temp = tails[t]
    tails[t] = heads[h]
    heads[h] = temp

    space[tx][ty] = 1
    space[hx][hy] = 3



for turn in range(k):
    move()
    # for i in range(n):
    #     print(space[i])
    # print()

    d = (turn // n) % 4
    hit = throw(d)

    if hit:
        scoring(hit)

    if d == 0:
        start[0] += 1
    elif d == 1:
        start[1] += 1
    elif d == 2:
        start[2] -= 1
    else:
        start[3] -= 1

print(score)


# 오답노트
# 1. 격자에 일정 부분을 차지하는 영역들을 정의해야한다면 리스트보다는 숫자로 구분해서 map으로 표현할 수 있다.