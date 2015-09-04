global _start 
_start: 
mov rax, 5 
mov rdi, 5 
add rax, rdi 
sub rsp, 16 
mov rsi, 10 
mov rdi, 16 
.L1: 
xor rdx, rdx 
div rsi 
or dl, 0x30 
sub rdi, 1 
mov [ rsp + rdi ], dl 
test rax, rax 
jnz .L1 
mov rax, 1

lea rsi, [ rsp + rdi ] 
mov rdx, 16 
sub rdx, rdi 
mov rdi, 1 
syscall

add rsp, 16 
mov rax, 60

xor rdi, rdi 
syscall

