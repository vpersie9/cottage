def sequential_search(a_list,item):
	pos=0
	found=False
	while pos < len(a_list) and not found:
		if a_list[pos] == item:
			found = True
		else:
			pos += 1
	return found

test_list=[1,2,32,8,17,19,42,13,0]
print sequential_search(test_list,3)
print sequential_search(test_list,13)


def binary_search(a_list,item):
	first=0
	last=len(a_list)-1
	found=False
	while first<=last and not found:
		midpoint=(first+last)//2
		if a_list[midpoint]==item:
			found=True
		else:
			if a_list[midpoint]>item:
				last=midpoint-1
			else:
				first=midpoint+1
	return found

test_list=range(10)
print binary_search(test_list,8)
print binary_search(test_list,12)

