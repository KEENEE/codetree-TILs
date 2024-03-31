# input = open("input.txt").readline
n, m, k = map(int, input().split())

# 좌상단이 1,1
dx = [-1,1,0,0]
dy = [0,0,-1,1]

space = [list(map(int, input().split())) for _ in range(n)]
participants = [list(map(int, input().split())) for _ in range(m)]
out = list(map(int, input().split()))

participants = [[i-1,j-1] for i,j in participants]
out = [out[0]-1, out[1]-1]


# 0 빈칸, 1~9 내구도 회전할때 1씩 깎임
# 출구에 도달하면 탈출


def move(p):
    moved = False
    x, y = participants[p]
    ox,oy = out

    dist = abs(x-ox)+abs(y-oy)
    
    for d in range(4):
        nx = x+dx[d]
        ny = y+dy[d]
        # print(nx,ny)
        if 0<=nx<n and 0<=ny<n:
            if space[nx][ny] == 0:
                if abs(nx-ox)+abs(ny-oy) < dist:
                    participants[p] = [nx,ny]
                    dist = abs(nx-ox)+abs(ny-oy)
                    moved = True
                    break
    
    return dist, moved



def find_smallest(p):
    x,y = participants[p]
    ox,oy = out
    d = max(abs(x-ox), abs(y-oy))    # 정사각형의 한 변의 길이 구하기

    max_x = max(ox, x)
    max_y = max(oy, y)

    left_x = max(0, max_x-d)
    left_y = max(0, max_y-d)

    return left_x, left_y, left_x+d, left_y+d


def rotate(r, x1,y1,x2,y2): #1,0,2,1
    global out
    d = x2-x1     #2
    diff = x1-y1    #1

    temp = [[0]*n for _ in range(n)]

    for i in range(x1,x2+1):    #1,2
        for j in range(y1,y2+1):    #0,1
            temp[x1+j-y1][y1+x2-i] = space[i][j]

    out = [x1+out[1]-y1, y1-out[0]+x2]

    for i in range(x1,x2+1):
        for j in range(y1,y2+1):
            space[i][j] = max(0, temp[i][j]-1)

    for i in range(len(participants)):
        if x1<=participants[i][0]<=x2 and y1<=participants[i][1]<=y2:
            # print("change", i)
            participants[i] = [x1+participants[i][1]-y1, y1-participants[i][0]+x2]
            


move_sum = 0

for i in range(k):
    min_dist = n
    min_part = 0
    
    # 참가자 이동
    for p in range(len(participants)):
        # print(i, p)
        dist, moved = move(p)
        # print(moved)
        if moved:   # 이동횟수 카운트
            move_sum += 1
            
        flag = False
        if dist < min_dist: # 최소거리인지 검사 
            flag = True
        elif dist == min_dist:
            if participants[min_part][0] > participants[p][0]:
                flag = True
            elif participants[min_part][0] == participants[p][0]:
                if participants[min_part][1] > participants[p][1]:
                    flag = True
        
        if flag:    # 더 최단거리인 경우 min_dist 바꿔주기
            if dist != 0: # 출구에 없는 경우에만(출구에 있으면 나가야하니까)
                min_dist = dist
                min_part = p


    for k in range(len(participants)-1,-1,-1):
        if participants[k] == out:
            del participants[k]
            if k < min_part:
                min_part -= 1
    
    if len(participants) == 0:
        break

    # 정사각형 찾기
    x1,y1,x2,y2 = find_smallest(min_part)

    # 회전, 내구도 감소
    rotate(i, x1,y1,x2,y2)



print(move_sum)
print(out[0]+1, out[1]+1)