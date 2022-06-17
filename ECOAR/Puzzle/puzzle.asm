#only 24-bits 320x240 pixels BMP files are supported
# 24 * 320 * 240 = 1843200 bits = 1843200 / 8 bytes = 230400 bytes
# let's round it to 240000 for a good measure
.eqv BMP_FILE_SIZE 230454
.eqv BYTES_PER_ROW 960

.data
	.align 4
	res:	.space 2
	image:	.space BMP_FILE_SIZE
	start_message_vertical: .asciiz "\nEnter number of vertical divisions:\n" # .asciiz stores the string 
	end_message_vertical: .asciiz "You entered this many vertical divisions: " 
	start_message_horizontal: .asciiz "\nEnter number of horizontal divisions:\n"
	end_message_horizontal : .asciiz "You entered this many horizontal divisions: "
	start_message: .asciiz "Enter number of vertical and horizontal divisions:\n"
	buffer: .space 1024
	HEIGHT: .word 240
	WIDTH: .word 320
	newline: .asciiz "\n"
	pieces: .word
	input_file_name: .asciiz "source.bmp"  # name of input file as choosen in the project instruction
	output_file_name: .asciiz "dest.bmp" # name of output file as choosen in the project instruction

.text

_main:
	jal user_input_horizontal_division  # puts number of horizontal divisions to $s5
	jal user_input_vertical_division  # puts number of vertical divisions to $s4
	jal calculate_number_of_pieces # puts number of pieces to $s3
	jal random_number
	jal calculate_piece_WIDTH  # calculates the WIDTH of a single piece based on number of vertical divisons
	jal calculate_piece_HEIGHT # calculates the WIDTH of a single piece based on number of horizontal divisons
	jal read_bmp
	
	li $a0, 8
	jal calculate_piece_position_x
	li $a0, 8
	jal calculate_piece_position_y
	li $a0, 9
	jal calculate_piece_position_y
	li $a0, 5
	jal calculate_piece_position_y
	li $a0, 2
	jal calculate_piece_position_y
	li $a0, 10
	jal calculate_piece_position_y
	 
	#put red pixel in bottom left corner	
	li $a0, 0		#x
	li $a1, 0		#y
	li $a2, 0x00FF0000	#color - 00RRGGBB
	jal put_pixel 
	
	#get pixel from x y
	li	$a0, 0		#x
	li	$a1, 0		#y
	jal     get_pixel_v0
	#get pixel from x y
	li	$a0, 0		#x
	li	$a1, 5		#y
	jal     get_pixel_v1
	
	#put pixel that we got from the previous get pixel to x y position
	li $a0, 0		#x
	li $a1, 1		#y
	move $a2, $v0
	jal put_pixel 
	
	#put pixel that we got from the previous get pixel to x y position
	li $a0, 0		#x
	li $a1, 2	#y
	move $a2, $v1
	jal put_pixel
	
	jal save_bmp
	jal end_program  

.macro print(%text)
	la $a0, %text  
	li $v0, 4
	syscall
.end_macro

.macro print_int(%num)
	li $v0, 1 # If you want to print the integer the code is 1
	move $a0, %num # move the integer stored in %num to $a0
	syscall
.end_macro

.macro println()
      	la $a0, newline                     # New line string stored here
      	li $v0, 4
      	syscall
.end_macro


calculate_piece_position_x: # piece value is taken from $a0
	div $a0, $s4 # number of vertical divisons is stored in $s4
	mfhi $a1
	beq $a1, 0, piece_position_x_mod_zero
	sub $a1, $a1, 1
	println()
	print_int($a1)
	jr $ra

piece_position_x_mod_zero:
	li $a2, 0
	add $a2, $a2, $s5
	println()
	print_int($a2)
	jr $ra

	
calculate_piece_position_y:  #piece value is taken from $a0
	div $a0, $s4
	mfhi $a1
	beq $a1, 0, piece_position_y_mod_zero
	div $a2, $a0, $s4
	move $t0, $s4
	sub $a2, $t0, $a2
	println()
	print_int($a2)
	jr $ra
	

piece_position_y_mod_zero:
	div $a2, $a0, $s4
	li $t0, 0
	add $t0, $s4, 1
	sub $a2, $t0, $a2
	println()
	print_int($a2) 
	jr $ra

calculate_number_of_pieces:
	mul $s3, $s4, $s5
	jr $ra

random_number:
	move $a1, $s3  #Here you set $a1 to the max bound.
    	li $v0, 42  #generates the random number.
    	syscall
    	#add $a0, $a0, 100  #Here you add the lowest bound
    	#li $v0, 1   #1 print integer
    	syscall
    	jr $ra

	
	
close_file:
	li $v0, 16
	move $a0, $s6
	syscall
	jr $ra

calculate_piece_WIDTH:
	lw $a0, HEIGHT
	div $s1, $a0, $s4 # number of vertical divisons is kept in $s1
	jr $ra
	
calculate_piece_HEIGHT:
	lw $a0, WIDTH
	div $s2, $a0, $s5 # number of vertical divisons is kept in $s2
	jr $ra

display_start_message:
	print(start_message)


user_input_vertical_division: # puts number of vertical divisions to $s4
	print(start_message_vertical)
	li $v0, 5 # we want to get the integer from the keyboard
	syscall # this will allow us to enter the number which will be stored in $v0
	# Store the result in $t0
	move $s4, $v0 # $t0 = $v0
	print(end_message_vertical)
	print_int($s4)
	jr $ra
	
enter_int:
	li $v0, 5 # we want to get the integer from the keyboard
	syscall # this will allow us to enter the number which will be stored in $v0
	# Store the result in $t0
	move $t0, $v0 # $t0 = $v0
	jr $ra


	
user_input_horizontal_division: # puts number of vertical divisions to $s5
	print(start_message_horizontal)
	li $v0, 5 # we want to get the integer from the keyboard
	syscall # this will allow us to enter the number which will be stored in $v0
	# Store the result in $t0
	move $s5, $v0 # $t0 = $v0
	print(end_message_horizontal)
	print_int($s5)
	jr $ra

calculate_picture_area:
	lw $t0, HEIGHT
	lw $t1, WIDTH
	mul $t2, $t0, $t1
	jr $ra
	
read_bmp:
#description: 
#	reads the contents of a bmp file into memory
#arguments:
#	none
#return value: none
	sub $sp, $sp, 4		#push $ra to the stack
	sw $ra,($sp)
	sub $sp, $sp, 4		#push $s1
	sw $s1, ($sp)
#open file
	li $v0, 13
        la $a0, input_file_name		#file name 
        li $a1, 0		#flags: 0-read file
        li $a2, 0		#mode: ignored
        syscall
	move $s1, $v0      # save the file descriptor
	
#check for errors - if the file was opened
#...

#read file
	li $v0, 14
	move $a0, $s1
	la $a1, image
	li $a2, BMP_FILE_SIZE
	syscall

#close file
	li $v0, 16
	move $a0, $s1
        syscall
	
	lw $s1, ($sp)		#restore (pop) $s1
	add $sp, $sp, 4
	lw $ra, ($sp)		#restore (pop) $ra
	add $sp, $sp, 4
	jr $ra
	
put_pixel:
#description: 
#	sets the color of specified pixel
#arguments:
#	$a0 - x coordinate
#	$a1 - y coordinate - (0,0) - bottom left corner
#	$a2 - 0RGB - pixel color
#return value: none

	sub $sp, $sp, 4		#push $ra to the stack
	sw $ra,($sp)

	la $t1, image + 10	#adress of file offset to pixel array
	lw $t2, ($t1)		#file offset to pixel array in $t2
	la $t1, image		#adress of bitmap
	add $t2, $t1, $t2	#adress of pixel array in $t2
	
	#pixel address calculation
	mul $t1, $a1, BYTES_PER_ROW #t1= y*BYTES_PER_ROW
	move $t3, $a0		
	sll $a0, $a0, 1
	add $t3, $t3, $a0	#$t3= 3*x
	add $t1, $t1, $t3	#$t1 = 3x + y*BYTES_PER_ROW
	add $t2, $t2, $t1	#pixel address 
	
	#set new color
	sb $a2,($t2)		#store B
	srl $a2,$a2,8
	sb $a2,1($t2)		#store G
	srl $a2,$a2,8
	sb $a2,2($t2)		#store R

	lw $ra, ($sp)		#restore (pop) $ra
	add $sp, $sp, 4
	jr $ra
	
	
get_pixel_v0:
#description: 
#	returns color of specified pixel
#arguments:
#	$a0 - x coordinate
#	$a1 - y coordinate - (0,0) - bottom left corner
#return value:
#	$v0 - 0RGB - pixel color

	sub $sp, $sp, 4		#push $ra to the stack
	sw $ra,($sp)

	la $t1, image + 10	#adress of file offset to pixel array
	lw $t2, ($t1)		#file offset to pixel array in $t2
	la $t1, image		#adress of bitmap
	add $t2, $t1, $t2	#adress of pixel array in $t2
	
	#pixel address calculation
	mul $t1, $a1, BYTES_PER_ROW #t1= y*BYTES_PER_ROW
	move $t3, $a0		
	sll $a0, $a0, 1
	add $t3, $t3, $a0	#$t3= 3*x
	add $t1, $t1, $t3	#$t1 = 3x + y*BYTES_PER_ROW
	add $t2, $t2, $t1	#pixel address 
	
	#get color
	lbu $v0,($t2)		#load B
	lbu $t1,1($t2)		#load G
	sll $t1,$t1,8
	or $v0, $v0, $t1
	lbu $t1,2($t2)		#load R
        sll $t1,$t1,16
	or $v0, $v0, $t1
					
	lw $ra, ($sp)		#restore (pop) $ra
	add $sp, $sp, 4
	jr $ra
	
get_pixel_v1:
#description: 
#	returns color of specified pixel
#arguments:
#	$a0 - x coordinate
#	$a1 - y coordinate - (0,0) - bottom left corner
#return value:
#	$v1 - 0RGB - pixel color

	sub $sp, $sp, 4		#push $ra to the stack
	sw $ra,($sp)

	la $t1, image + 10	#adress of file offset to pixel array
	lw $t2, ($t1)		#file offset to pixel array in $t2
	la $t1, image		#adress of bitmap
	add $t2, $t1, $t2	#adress of pixel array in $t2
	
	#pixel address calculation
	mul $t1, $a1, BYTES_PER_ROW #t1= y*BYTES_PER_ROW
	move $t3, $a0		
	sll $a0, $a0, 1
	add $t3, $t3, $a0	#$t3= 3*x
	add $t1, $t1, $t3	#$t1 = 3x + y*BYTES_PER_ROW
	add $t2, $t2, $t1	#pixel address 
	
	#get color
	lbu $v1,($t2)		#load B
	lbu $t1,1($t2)		#load G
	sll $t1,$t1,8
	or $v1 $v1, $t1
	lbu $t1,2($t2)		#load R
        sll $t1,$t1,16
	or $v1, $v1, $t1
					
	lw $ra, ($sp)		#restore (pop) $ra
	add $sp, $sp, 4
	jr $ra

	save_bmp:
#description: 
#	saves bmp file stored in memory to a file
#arguments:
#	none
#return value: none
	sub $sp, $sp, 4		#push $ra to the stack
	sw $ra,($sp)
	sub $sp, $sp, 4		#push $s1
	sw $s1, ($sp)
#open file
	li $v0, 13
        la $a0, output_file_name		#file name 
        li $a1, 1		#flags: 1-write file
        li $a2, 0		#mode: ignored
        syscall
	move $s1, $v0      # save the file descriptor
	
#check for errors - if the file was opened
#...

#save file
	li $v0, 15
	move $a0, $s1
	la $a1, image
	li $a2, BMP_FILE_SIZE
	syscall

#close file
	li $v0, 16
	move $a0, $s1
        syscall
	
	lw $s1, ($sp)		#restore (pop) $s1
	add $sp, $sp, 4
	lw $ra, ($sp)		#restore (pop) $ra
	add $sp, $sp, 4
	jr $ra
	
	

end_program:
	li $v0, 10
	syscall
	


	
	
	
