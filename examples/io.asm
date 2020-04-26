    jump main
newline:
    data 10
dst:
    data 0 0 0 0 0 0
; puts subroutine
puts:
    push r0
    stor r0
puts1:
    ldi r0
    jmpz puts2
    stor cout
    inc r0
    jump puts1
puts2:
    pop r0
    ret
; main subroutine
main:
    set dst
    stor r1
    set 5
    stor r2
loop:
    load cout
    ; store and inc
    sti r1
    inc r1
    dec r2
    ; check if newline
    stor r0
    load newline
    sub r0
    jmpz end
    ; check count
    load r2
    jmpz end
    jump loop
end:
    set dst
    call puts
    rset 0
