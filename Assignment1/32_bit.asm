global _start
_start:
mov eax, 5
mov ebx, 5
add eax, ebx
sub esp, 16
mov ecx, 10
mov ebx, 16
.L1:
xor edx, edx
div ecx
or dl, 0x30
sub ebx, 1
mov [ esp + ebx ], dl
test eax, eax
jnz .L1
mov eax, 4
lea ecx, [ esp + ebx ]
mov edx, 16
sub edx, ebx
mov ebx, 1
int 0x80
add esp, 16
mov eax, 1
xor ebx, ebx
int 0x80