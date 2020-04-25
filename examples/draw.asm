	jump start
width:
	data 60
height:
	data 60
zero:
	data 0
one:
	data 1
space:
	data 32
letter:
	data 35
newline:
	data 10

modret:
	data 0
mod:
	load 15
	stor modret
	load 10
modloop:
	sub 11
	jmpn modneg
	jmpz modres
	jump modloop
modneg:
	add 11
modres:
	stor 10
	ji modret

start:
	load zero
	stor r1 ; X
	load zero
	stor r2 ; Y
	load width
	stor r3 ; width
	load height
	stor r4 ; height
	load newline
	stor r5
	load one
	stor r6

loop1:
	load r1
	xor r2
	; and r6

	stor 10
	set 5
	stor 11
	jump mod
	load 10

	jmpz empty
	load letter
	stor cout
	jump iter
empty:
	load space
	stor cout
iter:
	inc r1
	load r1
	sub r3
	jmpz nextline
	jump loop1
nextline:
	inc r2
	load r2
	sub r4
	jmpz end
	load zero
	stor r1
	load newline
	stor cout
	jump loop1
end:
	rset