file = open('32_bit.asm')
lines = file.readlines()
stri=""
for li in lines:
	l=li.split("\n")
	if l[0]=="mov eax, 4":
		stri= stri+"mov rax, 1\n"
	elif l[0]=="mov eax, 1":
		stri=stri+"mov rax, 60\n"
	elif l[0]=="int 0x80":
		stri=stri+"syscall\n"
	else:
		words=l[0].split()
		for word in words:
			if word=="eax,":
				stri= stri+"rax,"
			elif word=="ebx,":
				stri=stri+"rdi,"
			elif word=="ecx,":
				stri=stri+"rsi,"
			elif word=="edx,":
				stri=stri+"rdx,"
			elif word=="esp,":
				stri=stri+"rsp,"
			elif word=="eax":
				stri=stri+"rax"
			elif word=="ebx":
				stri=stri+"rdi"
			elif word=="ecx":
				stri=stri+"rsi"
			elif word=="edx":
				stri=stri+"rdx"
			elif word=="esp":
				stri=stri+"rsp"
			else:
				stri=stri+str(word)
			stri=stri+" "
	stri=stri+"\n"
file.close()
f =open("64_bit.asm",'w')
f.write(stri)
f.close()
