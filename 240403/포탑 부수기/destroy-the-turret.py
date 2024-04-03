from collections import deque
n, m, k=map(int, input().split())
board=[[0]*m for _ in range(n)]
for i in range(n):
    inp=list(map(int, input().split()))
    for j in range(m):
        board[i][j]=inp[j]
attack_time=[[0]*m for _ in range(n)]
def decide():
    al=[]
    for i in range(n):
        for j in range(m):
            if board[i][j]<=0:
                continue
            al.append((board[i][j], attack_time[i][j], i, j))
    al.sort(key=lambda x:(x[0], -x[1], -(x[2]+x[3]), -x[3]))
    attacker=(al[0][2], al[0][3])
    strong=(al[-1][2], al[-1][3])
    return attacker, strong
def laser(at, st):
    dx=[0, 1, 0, -1]
    dy=[1, 0, -1, 0]
    r_dx=[-1, 0, 1, 0]
    r_dy=[0, -1, 0, 1]
    dq=deque()
    dq.append((at[0], at[1]))
    visit=[[0]*m for _ in range(n)]
    visit[at[0]][at[1]]=1
    while dq:
        nx, ny=dq.popleft()
        if nx==st[0] and ny==st[1]:
            break
        for i in range(4):
            xx, yy=(nx+dx[i])%n, (ny+dy[i])%m
            if board[xx][yy]<=0:
                continue
            if visit[xx][yy]==0:
                dq.append((xx, yy))
                visit[xx][yy]=visit[nx][ny]+1
    if visit[st[0]][st[1]]>1:
        route=[]
        ax, ay=st[0], st[1]
        for _ in range(visit[st[0]][st[1]]-1):
            amin=5001
            for i in range(4):
                xx, yy = (ax + r_dx[i]) % n, (ay + r_dy[i]) % m
                if 0<visit[xx][yy]<amin:
                    amin=visit[xx][yy]
                    x, y=xx, yy
            route.append((x, y))
            ax, ay=x, y
        for i, j in route:
            if (i, j)==at:
                continue
            board[i][j]-=board[at[0]][at[1]]//2
            related[i][j]=1
        board[st[0]][st[1]]-=board[at[0]][at[1]]
        return True
    else:
        return False
def bomb(at, st):
    dx=[0, -1, -1, -1, 0, 1, 1, 1]
    dy=[-1, -1, 0, 1, 1, 1, 0, -1]
    board[st[0]][st[1]]-=board[at[0]][at[1]]
    for i in range(8):
        x, y=(st[0]+dx[i])%n, (st[1]+dy[i])%m
        if x==at[0] and y==at[1]:
            continue
        if board[x][y]<=0:
            continue
        related[x][y]=1
        board[x][y]-=board[at[0]][at[1]]//2
for turn in range(1, k+1):
    cnt=0
    related=[[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if board[i][j]!=0:
                cnt+=1
    if cnt==1:
        break
    at, st=decide()
    attack_time[at[0]][at[1]]=turn
    related[at[0]][at[1]]=1
    related[st[0]][st[1]]=1
    board[at[0]][at[1]]+=(n+m)
    if not laser(at, st):
        bomb(at, st)
    for i in range(n):
        for j in range(m):
            if board[i][j]<=0:
                board[i][j]=0
    for i in range(n):
        for j in range(m):
            if board[i][j]<=0:
                continue
            if not related[i][j]:
                board[i][j]+=1
res=-1
for i in range(n):
    for j in range(m):
        if res<board[i][j]:
            res=board[i][j]
print(res)