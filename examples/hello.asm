    set hello
    stor r9
loop:
    ldi r9
    jmpz end
    stor cout
    inc r9
    jump loop
end:
    rset
hello:
    char H
    char e
    char l
    char l
    char o
    char ,
    data 32
    char w
    char o
    char r
    char l
    char d
    char !
    data 10
    data 0
