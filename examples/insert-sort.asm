	jump start
array:
	data 44
	data 36
	data 86
	data 96
	data 63
	data 27
	data 66
	data 10
	data 82
	data 74
zero:
	data 0
arrayptr:
	ref array
nextchar:
	data 33
nextline:
	data 10
start:
	load zero
	stor r0		; r0 = buffer
	load arrayptr
	stor r2		; r2 = pivot pointer
	inc r2
	load zero
	stor r1		; r1 = seek pointer
	;load zero
	;stor r3		; r3 = iteration counter

loop0:
	; loading pivot element
	load r2
	stor r1
	ldi r1
	jmpz outhere
	stor r0

loop1:
	dec r1
	ldi r1

	sub r0
	jmpn next2 ; if [r1] is less then r0
	; else mov [r1] to [r1 + 1]
	ldi r1
	inc r1
	sti r1
	dec r1
	; leave if r1 == arrayptr
	; i.e. first element
	load arrayptr
	sub r1
	jmpz next
	jump loop1
next2: ; [r1] is less than r0
	inc r1
next:
	load r0
	sti r1
	inc r2
	jump loop0

outhere:

	load arrayptr
	stor r1
display:
	ldi r1
	jmpz displayend
	stor dout
	inc r1
	jump display
displayend:
	rset