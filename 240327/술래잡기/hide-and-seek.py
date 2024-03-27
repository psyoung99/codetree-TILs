#술래잡기
n, m, h, k=map(int, input().split())
runner=[]
rds={2:[(1, 0), (-1, 0)], 1:[(0, 1), (0, -1)]}
rd_info=[]
lose=[0]*m
flag=1
idx=0
for _ in range(m):
    x, y, d=map(int, input().split())
    runner.append((x-1, y-1, 0)) #d=1->lr
    rd_info.append(d)
chaser=[n//2, n//2, (-1, 0)]
trees=[]
for _ in range(h):
    x, y=map(int, input().split())
    trees.append((x-1, y-1))
score=0
inOut=[chaser]
outIn=[]
#outIn=[[0, 0, (1, 0)]]
def cMove_inout(chaser):
    global inOut, flag, outIn
    nx, ny, nd=chaser
    dist=1
    cnt=0
    ds=[(-1, 0), (0, 1), (1, 0), (0, -1)]
    dn=0
    while True:
        for direction in range(dist):
            nx, ny=nx+ds[dn][0], ny+ds[dn][1]
            if (nx, ny)==(0, 0):
                inOut.append((nx, ny, (1, 0)))
                outIn.append((0, 0, (1, 0)))
                cMove_outin()
                return
            inOut.append([nx, ny, ds[dn]])
        cnt+=1
        dn=(dn+1+4)%4
        inOut[-1][2]=ds[dn]
        if cnt==2:
            dist+=1
            cnt=0
def cMove_outin():
    global outIn, flag
    nx, ny=0, 0
    visit=[[0]*n for _ in range(n)]
    visit[0][0]=1
    ds=[(1, 0), (0, 1), (-1, 0), (0, -1)]
    cnt=0
    for i in range(n*n):
        nx, ny=nx+ds[cnt][0], ny+ds[cnt][1]
        visit[nx][ny]=1
        if cnt==0:
            if nx==n-1 or visit[nx+1][ny]>0:
                cnt+=1
        if cnt==1:
            if ny==n-1 or visit[nx][ny+1]>0:
                cnt+=1
        if cnt==2:
            if nx==0 or visit[nx-1][ny]>0:
                cnt+=1
        if cnt==3:
            if ny==0 or visit[nx][ny-1]>0:
                cnt=0
        if (nx, ny)==(n//2, n//2):
            outIn.append((nx, ny, (-1, 0)))
            flag=1
            return
        outIn.append([nx, ny, ds[cnt]])
cMove_inout(chaser)
#print(inOut)
#print(outIn)
def rMove():
    cx, cy, cd=chaser
    for i in range(m):
        if lose[i]==1:
            continue
        rx, ry, rd=runner[i]
        if abs(cx-rx)+abs(cy-ry)>3:
            continue
        xx=rx+rds[rd_info[i]][rd][0]
        yy=ry+rds[rd_info[i]][rd][1]
        if 0<=xx<n and 0<=yy<n:
            if xx==cx and yy==cy:
                continue
            else:
                runner[i]=(xx, yy, rd)
        else:
            rd=1-rd
            xx = rx + rds[rd_info[i]][rd][0]
            yy = ry + rds[rd_info[i]][rd][1]
            if [xx, yy, cd]!=chaser:
                runner[i]=(xx, yy, rd)
def cMove():
    global chaser, route, idx
    if chaser[0]==0 and chaser[1]==0:
        idx=1
      #  print("OOOOOO")
        route=outIn
    elif chaser[0]==n//2 and chaser[1]==n//2:
        idx=1
      #  print("IIIIII")
        route=inOut
    chaser=[route[idx][0], route[idx][1], route[idx][2]]
    idx+=1
route=inOut
for turn in range(1, k+1):
    rMove()
    cMove()
    #print('r',runner)
    rs=[]
    livenum=0
    for i in range(m):
        if lose[i]==0:
            rs.append(runner[i])
            livenum+=1
    cx, cy, cd=chaser
    num=0
    for i in range(3):
        xx=cx+cd[0]*i
        yy=cy+cd[1]*i
        if not (0<=xx<n and 0<=yy<n):
            continue
        for j in range(m):
            if lose[j]==1:
                continue
            if (xx, yy)==(runner[j][0], runner[j][1]):
                if (xx, yy) in trees:
                    continue
                lose[j]=1
                num+=1
    score+=turn*num
print(score)