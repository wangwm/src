import commands
import itertools
list1 = [0,1, 3, 4,9]
list2 = list(itertools.permutations(list1, 1))
#print(list2)
cmd = "cat h_bj.txt |grep ^131|grep -v [0,2,5,6,7,8]|awk '{print $1}'"
(state, out) = commands.getstatusoutput(cmd)
print state
sec_lst = out.split()
#print sec_lsta
for sec in  sec_lst:
	for i in itertools.product('1349', repeat = 4):
		last = ''.join(i)
		phone = "%s%s" % (sec,last)
		print  phone 

