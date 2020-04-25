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

; swap routine
; r1 - addr 1
; r2 - addr 2
swapt:
	data 0
swap:
	ldi r1
	stor swapt
	ldi r2
	sti r1
	load swapt
	sti r2
	ji 15

start:
	load arrayptr
	stor r1
	stor r2
	inc r1
	load zero
	stor r4
; swapping all the way
loop1:
	ldi r1
	jmpz loop1e ; out of loop if zero/sentinel

	; compare
	ldi r1
	stor r3
	ldi r2
	sub r3
	jmpn noswap

	; swap
	jump swap
	; do not step back
	; if first element
	load r4
	jmpz loop1
	; step back
	dec r1
	dec r2
	dec r4
	jump loop1
noswap:
	; step forward
	inc r1
	inc r2
	inc r4
	jump loop1
loop1e:

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