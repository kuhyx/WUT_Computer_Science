

section	.data



image_info_address EQU 8  ; First argument passed to our function starts from 8
first_piece_address EQU 12 ; From that point we just add 4 to address of next
; arguments
piece_to_swap_with_address EQU 16
horizontal_divisons_address EQU 20
piece_width_address EQU 24
piece_height_address EQU 28
piece_width_bytes_address EQU 32
piece_height_bytes_address EQU 36
bytes_per_row_address EQU 40
firstPieceStartingByte EQU 44
secondPieceStartingByte EQU 48


pImg_inside_image_info_address EQU 12


image_width		EQU 0
image_height		EQU 4
bytes_per_row_inside_image_info_address	EQU 8
image_pImg		EQU	12
image_pHeaderInfo	EQU 16 ; not really used

; first.X, first.Y, second.X, second.Y



%macro print 2      ;number of arguments this macro takes
  mov	edx, %1       ;message length
  mov	ecx, %2       ;message to write
  mov	ebx,1         ;file descriptor (stdout)
  mov	eax,4         ;system call number (sys_write)
  int	0x80          ;call kernel
%endmacro



section	.text
global inner_loops     ;must be declared for linker (ld)
; extern void hello_world(imageInfo* pInfo, int firstPiece, int pieceToSwapWith,
;												int horizontalDivisions, int pieceWidth,
;												int pieceHeight);

; mov	ecx, [ebp + 8]	; ecx <- address of imgInfo struct, not saved
; mov eax, [ebp + 12]	; eax <- firstPiece, not saved
; mov edx, [ebp + 16] ; edx <- pieceToSwapWith, not saved
; mov esi, [ecx + image_pImg] ; esi <- start of pixels in picture, saved
; mov ebx, [ebp + 20] ; ebx <- horizontalDivisions
; mov edi, [ebp + 24] ; edi <- pieceWidth

inner_loops:	          ;tells linker entry point

  push ebp  ; as per calling convention we need to keep the values of
  ; certain registers
  mov ebp,esp
  push ebx
  push esi
  push edi

  ; what we use:
  ; ecx - firstPieceFirstByteAddress
  ; edx - secondPieceFirstByteAddress
  ; esi
  ; edi

  ; what we have:
  ; eax
  ; ebx

  push ebx
  push eax
  ;mov eax, [ebp + firstPieceStartingByte]
  ;mov eax, [eax + image_pImg]
  mov edi, 0

x_pixels_loop:
    cmp edi, [ebp + piece_width_bytes_address]
    ;cmp edi, 300
    jge x_pixels_loop_end
    mov esi, 0

  ; ecx = secondPieceStartingByte
  ; edx = firstPieceStartingByte
  ; we still have eax and ebx
  ;
  y_pixels_loop:
    cmp esi, [ebp + piece_height_bytes_address]
    ;cmp esi, 96000
    jge y_pixels_loop_end
    mov ecx, [ebp + secondPieceStartingByte]
    mov eax, [ebp + firstPieceStartingByte]
    add ecx, edi
    add ecx, esi
    add eax, edi
    add eax, esi

    mov BYTE bl, [eax]
    mov BYTE dl, [ecx]
    mov BYTE[ecx], bl
    mov BYTE[eax], dl

    mov BYTE bl, [eax + 1]
    mov BYTE dl, [ecx + 1]
    mov BYTE[ecx + 1], bl
    mov BYTE[eax + 1], dl

    mov BYTE bl, [eax + 2]
    mov BYTE dl, [ecx + 2]
    mov BYTE[ecx + 2], bl
    mov BYTE[eax + 2], dl



    add esi, [ebp + bytes_per_row_address]
    jmp y_pixels_loop


  ; 		for(x = 0; x < pieceWidth * 3; x += 3)
  y_pixels_loop_end:
    add edi, 3
    jmp x_pixels_loop

  x_pixels_loop_end:

  pop esi
  pop edi
  pop ebx
  mov esp, ebp
  pop ebp
  ret
