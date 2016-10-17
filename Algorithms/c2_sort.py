def short_bubble_sort(a_list):
	exchanges=True
	pass_num=len(a_list) - 1
	while pass_num > 0 and exchanges:
		exchanges=False
		for i in range(pass_num):
			if a_list[i] > a_list[i+1]:
				exchanges=True
				a_list[i],a_list[i+1]=a_list[i+1],a_list[i]
		pass_num -= 1

a_list=[20,40,30,90,110,30,40,70,10]

short_bubble_sort(a_list)	
print a_list

def selection_sort(a_list):
	for fill_slot in range(len(a_list)-1,0,-1):
		post_max=0
		for action in range(1,fill_slot+1):
			if a_list[action] > a_list[post_max]:
				post_max=action
		a_list[fill_slot],a_list[post_max]=a_list[post_max],a_list[fill_slot]
				
a_list=[20,40,30,90,110,30,40,70,10]

selection_sort(a_list)	
print a_list


class HashTable(object):
	def __init__(self):
		self.size=11
		self.slots=[None] * self.size
		self.data=[None] * self.size
	
	#put data in slot
	def put_data_in_slot(self,key,data,slot):
		if self.slots[slot] == None:
			self.slots[slot] = key
			self.data[slot] = data
			return True
		else:
			if self.slots[slot] == key:
				self.data[slot] = data #replace
				return True
			else: #collision
				return False
		
	#execute put_data_in_slot and plus slot
	def put(self,key,data):
		slot=self.hash_function(key,self.size)
		result=self.put_data_in_slot(key,data,slot)
		while not result:
			slot=self.rehash(slot,self.size)
			result=self.put_data_in_slot(key,data,slot)

	#reminder method
	def hash_function(self,key,size):
		return key % size
	
	#plus 1
	def rehash(self,old_hash,size):
		return (old_hash + 1) % size

	def get(self,key):
		start_slot=self.hash_function(key,len(self.slots))
		data=None
		stop=False
		found=False
		position = start_slot
		while self.slots[position] != None and not found and not stop:
			if self.slots[position] == key:
				found=True
				data=self.data[position]
			else:
				position=self.rehash(position,len(self.slots))
				if position == start_slot:
					stop=True
		return data

	def __getitem__(self,key):
		return self.get(key)

	def __setitem__(self,key,data):
		self.put(key,data)


if __name__=="__main__":
	table=HashTable()
	table[54]='cat'
	table[26]='dog'
	table[93]='lion'
	table[17]='tiger'
	table[77]='bird'
	table[44]='goat'
	table[55]='pig'
	table[20]='chicken'
	print table.slots
	print table.data
