i=[9,10,11,12]
f=open('9_1.html','r+',encoding="utf-8")
string=f.read()
f.close()

for k in i:
 for j in range(10):
    s="{}_{}.html".format(k,(j+1))
    f=open(s,"w+",encoding="utf-8")
    f.write(string)
    f.close()