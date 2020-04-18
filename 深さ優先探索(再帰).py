

#a = int(input())
#b,c = map(int,input().split())
#s = input()
#list_s = list(input())
#list_int = list(map(int,input().split()))

#list = [0 for i in range(n)]
#dp = [[0 for i in range(A)] for j in range(B)]

#print (' '.join(list)))

import sys

sys.setrecursionlimit(10000000)

H,W = map(int, input().split())
maze = []

for i in range(H):
	maze.append(list(input()))

flag = 0
	
def search(x,y):
	global maze
	
	if 0 <= x < W and 0 <= y < H:
		if maze[y][x] == "g" :
			print ("Yes")
			sys.exit()
		elif maze[y][x] == "#":
			return
		elif maze[y][x] == 1:
			return
		maze[y][x] = 1
		
		search(x+1, y)
		search(x-1, y)
		search(x, y+1)
		search(x, y-1)
	else:
		return

		
for y in range(H):
	for x in range(W):
		if maze[y][x] == "s":
			search(x,y)
			print ("No")
			sys.exit()





































