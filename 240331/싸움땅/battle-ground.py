n, m ,k = map(int, input().split())

nums = [list(map(int, input().split())) for _ in range(n)]
guns = [[[] for _ in range(n)] for _ in range(n)]

for i in range(n):
    for j in range(n):
        if nums[i][j] != 0:
            guns[i][j].append(nums[i][j])

players = [list(map(int, input().split())) for _ in range(m)]   #x,y,d,s
players = [[x-1,y-1,d,s] for x,y,d,s in players]
locations = [[x,y] for x,y,d,s in players]
scores = [0] * m
player_guns = [0] * m

dx = [-1,0,1,0]
dy = [0,1,0,-1]

def move(p):
    x,y,d,s = players[i]
    
    # 방향대로 한 칸 이동, 격자를 벗어나는 경우 반대방향으로 바꿔 이동
    nx = x + dx[d]
    ny = y + dy[d]
    
    # 격자 벗어나는 경우 방향 바꿔주기
    flag = False
    if nx == -1:
        nx = 1
        flag = True
    if ny == -1:
        ny = 1
        flag = True
    if nx == n:
        nx = n-2
        flag = True
    if ny == n:
        ny = n-2
        flag = True
    
    if flag:
        d = (d+2) % 4
    
    players[i] = [nx,ny,d,s]
    locations[i] = [nx,ny]


def fight(i, j):
    # global scores
    # 초기 능력치와 총의 공격력의 합을 비교, 더 큰 플레이어가 이김
    # 같은 경우 초기능력치가 높은 플레이어가 승리
    score_i = player_guns[i] + players[i][3]
    score_j = player_guns[j] + players[j][3]

    # 공격력 합의 차이만큼 포인트 획득
    diff = abs(score_i - score_j)
    winner, loser = i, j
    if (score_i < score_j) or (diff == 0 and players[i][3] < players[j][3]):
        winner, loser = j, i


    # 진 플레이어는 총 내려놓고
    x,y,d,s = players[loser]
    guns[x][y].append(player_guns[loser])
    player_guns[loser] = 0

    # 가던 방향으로 한칸 이동, 다른 플레이어가 있거나 범위 밖이면 이동 가능할때까지 90도씩 회전
    for o in range(4):
        nx = x + dx[(d+o)%4]
        ny = y + dy[(d+o)%4]
    
        # 격자 벗어나는 경우 방향 바꿔주기
        if 0<=nx<n and 0<=ny<n:
            if locations.count([nx,ny]) == 0:
                locations[loser] = [nx,ny]
                players[loser] = [nx,ny,d,s]
                break
            
    # 이동했을 때 총이 있다면 공격력이 높은 총 획득
    if guns[nx][ny]:
        player_guns[loser] = max(guns[nx][ny])
        guns[nx][ny].remove(max(guns[nx][ny]))

    # 이긴 플레이어는 점수 획득 및 총 swap
    scores[winner] += diff
    swap_gun(winner)



def swap_gun(l):
    x, y = locations[l]
    
    if guns[x][y]:
        if max(guns[x][y]) > player_guns[l]:
            if player_guns[l] != 0:
                guns[x][y].append(player_guns[l])
            player_guns[l] = max(guns[x][y])

        guns[x][y].remove(max(guns[x][y]))



for r in range(k):
    # print(r)
    for i,p in enumerate(players):
        # 플레이어 이동
        # print(players[i], locations[i])
        move(i)
        # print(players[i], locations[i])
        met = False
        for j,p in enumerate(players):
            if i == j:  # 자기자신은 패스
                continue
            
            if locations[i] == locations[j]:
                met = True
                fight(i,j)

        # 다른 플레이어를 만나지 않았다면 총 바꾸기
        if not met:
            swap_gun(i)

print(*scores)