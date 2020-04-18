


aa = inpl()

b = 1
for a in aa:
	b |= b << a

'''
aaの部分和が，左からi番目のbのbitが
・1ならiが作れる
・0ならiは作れない
'''
