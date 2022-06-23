CC=gcc
ASMBIN=nasm

all : asm cc link
asm :
	$(ASMBIN) -o asm_part.o -f  elf32 -g -l asm_part.lst asm_part.asm
cc :
	$(CC) -m32 -c -g -O0 puzzle.c
link :
	$(CC) -m32 -g -o puzzle.out -g puzzle.o asm_part.o -no-pie
clean :
	rm *.o
	rm setcol_test
	rm asm_part.lst
