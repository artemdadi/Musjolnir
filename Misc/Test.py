import os
from ctypes import *
from _ctypes import CFuncPtr
class inf(Structure):
	_fields_ = [("dli_fname", c_char_p),
	("dli_fbase", c_void_p),
	("dli_sname", c_char_p),
	('dli_saddr', c_void_p)] 
a = CDLL("libc.so")
b = CDLL("libdl.so")
dl = b.dlopen(b"libc.so", 0)
print(dl)
fun = c_char_p(b"free")
dl_p = c_void_p(dl)
print(dl_p)
print(b.dlsym(dl_p, fun))
er = c_char_p(b.dlerror())
print(er.value)
#x=0
#while er[x]!=0:
#	print(er[x])
#	x+=1
print(b.dlclose(dl_p))
myinf = inf()
print(b.dladdr(dl_p, byref(myinf)))
print(myinf.dli_fname)
