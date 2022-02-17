array = [1,2,3,4,5,6,7,8,9,10,11]
array.sort()

out_idx = []

ranges = [(0,len(array)-1)]

while len(out_idx)<len(array):
  rtemp = []
  for r in ranges:
    length = (r[1]-r[0])+1
    if length == 1:
      out_idx.append(r[0])
    elif length == 2:
      out_idx.append(r[0])
      out_idx.append(r[1])
    else:
      i = (int)(r[0]+(length/2))
      out_idx.append(i)
      rtemp.append((r[0], i-1))
      rtemp.append((i+1, r[1]))
  ranges = rtemp

out = []
for i in out_idx:
  out.append(array[i])

print(out)