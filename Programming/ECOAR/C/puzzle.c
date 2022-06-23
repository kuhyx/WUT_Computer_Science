// ECOAR x86 PUZZLE Project Krzysztof Rudnicki, 307585
#include <stdio.h> // fopen(); fread(); fwrite(); fclose()
#include <stdlib.h> // printf(); srand();
#include <memory.h> // malloc(); free();
#include <time.h> // time();

const int BMP_HEADER_SIZE = 54;
// as per: https://www.daubnet.com/en/file-format-bmp
const int BMP_SIGNATURE_0x = 0x4D42;
// as per: https://www.daubnet.com/en/file-format-bmp
const int NUMBER_OF_HEADERS = 1; // There is only one header in BMP file
const int BYTE_PER_PIXEL = 24; // as per project description of the bmp file
const int DESIRED_COMPRESSION_VALUE = 0;
// as per project description of the bmp file
const int CANNOT_OPEN_FILE_FOR_WRITING = -1;
const int CANNOT_WRITE_HEADER_OR_IMAGE = -2;
const int BYTES_FOR_SINGLE_PIXEL = 3;  // R byte + G byte + B byte
const int WRONG_BMP_HEADER_SIZE = 1;
const int ERROR_READING_SOURCE_FILE = 2;

const char ENTER_VERTICAL_DIVISON_MESSAGE[]
= "Enter number of vertical divisons: ";

const char ENTER_HORIZONTAL_DIVISON_MESSAGE[]
= "Enter number of horizontal divisons: ";

const char WRONG_BMP_HEADER_SIZE_MESSAGE[]
= "Check compilation options so as bmpHeaderInfo struct size is 54 bytes.\n";

const char READ_AND_BINARY_MODE[] = "rb"; // open file to read and binary mode
const char WRITE_AND_BINARY_MODE[] = "wb"; // open file to write and binary mode
const char SOURCE_IMAGE_NAME[] = "source.bmp"; // as per project description
const char DESTINATION_IMAGE_NAME[] = "dest.bmp"; // as per project description
const char ERROR_READING_SOURCE_FILE_MESSAGE[]
= "Error reading source file (probably).\n";

// "Specifies the packing alignment for structure, union, and class members."
// something like .align in MIPS?
// https://docs.microsoft.com/en-us/cpp/preprocessor/pack?view=msvc-160
#pragma pack(push, 1)
/* push - pushed to stack, n = 1
n - (Optional) Specifies the value, in bytes, to be used for packing.
If the compiler option /Zp isn't set for the module,
the default value for n is 8. Valid values are 1, 2, 4, 8, and 16.
The alignment of a member is on a boundary that's either a
multiple of n, or a multiple of the size of the member,
whichever is smaller. */
// We pack it to "1" to get exactly 54 bytes for bmpHeaderInfo structure
// Changing it to "8" gives us an error, changing it to "2" does not


typedef struct
{
	unsigned short bytesImageType;	// 0x4D42 = "BMP" in Ascii, not used
	unsigned long  bytesFileSize;	// file size in bytes, not used
	unsigned short  bfReservedOne; // reserved bytes from bmp file
	unsigned short  bfReservedTwo; // reserved bytes from bmp file
	unsigned long  bytesPixelDataOffset;	// offset of pixel data, not used
	unsigned long  bytesHeaderSize;
	// header size (bitmap info size), not used
	long  bytesImageWidth;			// image width, USED
	long  bytesImageHeight;			// image height, USED
	short bytesBitmapPlanes;			// bitmap planes (== 1) USED
	short bytesPixelBitCount;
	// bit count of a pixel (== 24) (24 from project description), USED
	unsigned long  bytesImageCompression;
	// should be 0 (no compression), USED
 	unsigned long  bytesImageSize;		// image size (not file size!), USED
	long bytesHorizontalResolution;			// horizontal resolution, not used
	long bytesVerticalResolution;			// vertical resolution, not used
	unsigned long  bytesColorsUsed;
	// not important for RGB images, not used
	unsigned long  bytesColorsImportant;
	// not important for RGB images, not used
} bmpHeaderInfo;
// Struct containing info from header of a RGB type BMP file

#pragma pack(pop)
// stack popped

typedef struct
{
	unsigned int imageWidth;
	unsigned int imageHeight;  // same as in bmpHeaderInfo
	unsigned int bytesPerRow;
	// Bytes per row, important in MIPS, important here
	unsigned char* pImg;
	// pImg is a pointer to the begining of pixels data of the picture
	bmpHeaderInfo *pHeaderInfo;  // pointer to info from header
} imageInfo; // Stores info about image







// If we want to write something to imageInfo struct first we need to empty it
imageInfo* allocateSpaceForImageInfo()
{
// we allocate as much space as this struct needs
	imageInfo* emptyImageInfo = malloc(sizeof(imageInfo));
// 		Then in this "if" we basically set starting values for
//		everything we care about
	if (emptyImageInfo != NULL)
	{
		emptyImageInfo->imageWidth = 0;
		emptyImageInfo->imageHeight = 0;
		emptyImageInfo->bytesPerRow = 0;
		emptyImageInfo->pImg = NULL;
		emptyImageInfo->pHeaderInfo = NULL;
	}
	return emptyImageInfo; // Then we retun the struct that we will use
}

void* freeImageInfo(imageInfo* toFree)
{
	if (toFree != NULL) // If image info is already empty no need to free it
	{
		if (toFree->pImg != NULL) free(toFree->pImg);
		// pImg is an char* so we need to free it extra
		if (toFree->pHeaderInfo != NULL) free(toFree->pHeaderInfo);
		// pHeaderInfo is a struct so we need to free it extra
		free(toFree);  // Finally we can free the rest of the struct
	}
	return NULL;
	// we return void* since function readBMP calling freeImageInfo returns a
	// pointer
}

// 	We use pFile to read/write to file and struct containing imageInfo in our
//	program, we have to free memory after using these two
void* freeResources(FILE* pFile, imageInfo* toFree)
{
	if (pFile != NULL) fclose(pFile);  // Close file if it isn't already closed
	return freeImageInfo(toFree);
}


imageInfo* readBMP(const char* fileName)
{
	imageInfo* pInfo = 0;
	/* 	https://stackoverflow.com/q/48288191
		Assignment of the constant 0 to a pointer will produce a null pointer
		distinguishable from a pointer to any object. */
	FILE* bmpFile = 0;

	// allocateSpaceForImageInfo returns NULL if something went bad
	pInfo = allocateSpaceForImageInfo();
	if (pInfo == NULL) return NULL;


	// if fopen returns NULL then something bad happened
	bmpFile = fopen(fileName, READ_AND_BINARY_MODE);
	// cannot open file
	if (bmpFile == NULL) return freeResources(bmpFile, pInfo);

	/* 	1. if malloc didn't allocate any memory then something bad happened
		fread arguments: buffer to which we will save data that we read
		size of single data element in bytes
		number of elements that we will read
		stream on which this operation will be done
		We will save data to pHeaderInfo so that's our buffer
		We will get as much data as there is in bmpHeader
		There is just one header so we will read just from one header
		We will read all of that from bmp file
		it returns number of correctly read values, our desired return value is
		1 so if it returns any other then there was a mistake
		NUMBER_OF_HEADERS = 1 */
		pInfo->pHeaderInfo = malloc(sizeof(bmpHeaderInfo));
		size_t returnedElements = fread(	(void*)pInfo->pHeaderInfo,
																			sizeof(bmpHeaderInfo),
																			NUMBER_OF_HEADERS,
																			bmpFile										);

	if	(pInfo->pHeaderInfo == NULL || returnedElements != NUMBER_OF_HEADERS)
		{
			return freeResources(bmpFile, pInfo);
		}

	/* 	We check if image type is different than BMP
		We check if bitmap planes are different than 1
		we check if number of bits in one pixels is differnt than 24
		we check if there is any image compresssion
		those are the project assumptions if any of them are broken then there
		was a mistake
		BMP_SIGNATURE_0x = 0x4D42
		BYTE_PER_PIXEL = 24
		DESIRED_COMPRESSION_VALUE = 0 */
	if(	pInfo->pHeaderInfo->bytesImageType != BMP_SIGNATURE_0x ||
		pInfo->pHeaderInfo->bytesBitmapPlanes != 1 ||
		pInfo->pHeaderInfo->bytesPixelBitCount != BYTE_PER_PIXEL ||
		pInfo->pHeaderInfo->bytesImageCompression != DESIRED_COMPRESSION_VALUE)
		{
			return (imageInfo*) freeResources(bmpFile, pInfo);
		}

	/* 	We check if we allocated any memory to the image
		We check if number of read elements from the file are different than
		image size in bytes if any of this this is true then
		something went wrong
	*/
	pInfo->pImg = malloc(pInfo->pHeaderInfo->bytesImageSize);
	size_t returnedElementsData = fread((void *)pInfo->pImg,
										1,
										pInfo->pHeaderInfo->bytesImageSize,
										bmpFile);
	if(	pInfo->pImg == NULL ||
		returnedElementsData != pInfo->pHeaderInfo->bytesImageSize)
		{
			return (imageInfo*) freeResources(bmpFile, pInfo);
		}


	fclose(bmpFile); // We can close the file

	pInfo->imageWidth = pInfo->pHeaderInfo->bytesImageWidth;
	pInfo->imageHeight = pInfo->pHeaderInfo->bytesImageHeight;

	pInfo->bytesPerRow = pInfo->pHeaderInfo->bytesImageSize /
						 pInfo->pHeaderInfo->bytesImageHeight;

	// bytesPerRow = imageSize / imageHeight
	return pInfo;
}

int saveBMP(const imageInfo* pInfo, const char* fileName)
{
	FILE *bmpFile = fopen(fileName, WRITE_AND_BINARY_MODE);

	// fopen returns NULL if something went bad
	// WRITE_AND_BINARY_MODE = "wb"
	// cannot open file for writing
	if (bmpFile == NULL) return CANNOT_OPEN_FILE_FOR_WRITING;

	/* 	if we wrote more or less than one header then there is something wrong
		if we wrote more or less bytes to the image than there are bytes in the
		image then there is something wrong
		CANNOT_WRITE_HEADER_OR_IMAGE = -2 */
	size_t returnedHeaders = fwrite(pInfo->pHeaderInfo, sizeof(bmpHeaderInfo),
									NUMBER_OF_HEADERS, bmpFile);
	size_t returnedData = fwrite(pInfo->pImg, 1,
								 pInfo->pHeaderInfo->bytesImageSize, bmpFile);

	if (returnedHeaders != NUMBER_OF_HEADERS ||
		returnedData != pInfo->pHeaderInfo->bytesImageSize)
	{
		fclose(bmpFile);  // cannot write header or image
		return CANNOT_WRITE_HEADER_OR_IMAGE;
	}

	fclose(bmpFile);
	return 0;
}

void set_pixel(unsigned char * pPix, unsigned int color)
{
	/* 	pImg -> pImg returns the starting addres of pixels
		then we calculate byte position of a pixel we want to change by:
		bytesPerRow * y_coordinate + x * 3 (3 bytes for RGB)
		BYTES_FOR_SINGLE_PIXEL = 3 */

	// if x and y are inside the image then we can commence forward

	*pPix = (color >> 16) & 0xFF; // R color of the pixel
	*(pPix + 1) = (color >> 8) & 0xFF; // G color of the pixel
	*(pPix + 2) =  color & 0xFF; // B color of the pixel
}

unsigned int getColor(unsigned char * pPix)
{
	char R, G, B; // change to unsigned char
	R = *pPix;
	G = *(pPix + 1);
	B = *(pPix + 2);
	unsigned int color = 0;
	color = ( ((R & 0xFF) << 16) | (( G & 0xFF) << 8) | (B & 0xFF));
	return color;
}

int calculateStartingPixelX(int pieceNumber, int horizontalDivisons,
							int pieceWidth)
{
	int temp = pieceNumber % horizontalDivisons;
	if(temp == 0) temp = horizontalDivisons;
	return (temp - 1) * pieceWidth;
}

int calculateStartingPixelY(int pieceNumber, int horizontalDivisons,
							int pieceHeight)
{
	return (((pieceNumber - 1) / horizontalDivisons) * pieceHeight);
}

 extern void inner_loops(imageInfo* pInfo, int firstPiece, int pieceToSwapWith,
												int horizontalDivisions, int pieceWidth,
												int pieceHeight, int pieceWidthBytes, int bieceHeightBytes,
												unsigned int bytesPerRow,
												unsigned char *firstPieceStartingByte,
												unsigned char *secondPieceStartingByte); // Incomplete x86 solution

int main(/*int argc, char* argv[]*/) // argc and argv[] are not used anywhere
{

	imageInfo* pInfo; // imageInfo holds all header data from image
	unsigned int columnIndex = 0;
	// bmp header and info header should be 54 bytes as per BMP documentation
	// https://www.daubnet.com/en/file-format-bmp
	if (sizeof(bmpHeaderInfo) != BMP_HEADER_SIZE)
	{
		printf(WRONG_BMP_HEADER_SIZE_MESSAGE);
		return WRONG_BMP_HEADER_SIZE;
	}
	if ((pInfo = readBMP(SOURCE_IMAGE_NAME)) == NULL)
	{
		printf(ERROR_READING_SOURCE_FILE_MESSAGE);
		return ERROR_READING_SOURCE_FILE;
	}

	int verticalDivisions, horizontalDivisions;
	printf(ENTER_VERTICAL_DIVISON_MESSAGE);
	scanf("%d", &verticalDivisions);
	printf(ENTER_HORIZONTAL_DIVISON_MESSAGE);
	scanf("%d", &horizontalDivisions);

	int numberOfPieces = verticalDivisions * horizontalDivisions;
	int pieceWidth = (pInfo -> imageWidth) / horizontalDivisions;
	int pieceHeight = (pInfo -> imageHeight) /  verticalDivisions;
	int pieceWidthBytes = pieceWidth * 3;
	int bieceHeightBytes = pieceHeight * (pInfo -> bytesPerRow);
	srand(time(NULL));
	int firstPiece;
	for(firstPiece = 1; firstPiece <= numberOfPieces; firstPiece++)
	{
		int pieceToSwapWith = rand() % numberOfPieces;
	//	hello_world(pInfo, firstPiece, pieceToSwapWith, horizontalDivisions,
	//							pieceWidth, pieceHeight, pieceWidthBytes, bieceHeightBytes, pInfo -> bytesPerRow); // Incomplete x86 solution



		int firstPieceStartingX = calculateStartingPixelX(firstPiece, horizontalDivisions, pieceWidth);
		int firstPieceStartingY = calculateStartingPixelY(firstPiece, horizontalDivisions, pieceHeight);
		unsigned char *firstPieceStartingByte = firstPieceStartingX * 3 + firstPieceStartingY * pInfo -> bytesPerRow + pInfo -> pImg;

		int secondPieceStartingX = calculateStartingPixelX(pieceToSwapWith, horizontalDivisions, pieceWidth);
		int secondPieceStartingY = calculateStartingPixelY(pieceToSwapWith, horizontalDivisions, pieceHeight);
		unsigned char *secondPieceStartingByte = secondPieceStartingX * 3 + secondPieceStartingY * pInfo -> bytesPerRow + pInfo -> pImg;

		inner_loops(pInfo, firstPiece, pieceToSwapWith, horizontalDivisions,
								pieceWidth, pieceHeight, pieceWidthBytes, bieceHeightBytes, pInfo -> bytesPerRow, firstPieceStartingByte, secondPieceStartingByte);
		/* int x = 0;
		for(x = 0; x < pieceWidth * 3; x += 3)
		{
			int y = 0;
			for(y = 0; y < pieceHeight * pInfo -> bytesPerRow; y += pInfo -> bytesPerRow)
			{
				unsigned int colorOne = getColor(secondPieceStartingByte + x + y);
				unsigned int colorTwo = getColor(firstPieceStartingByte + x + y);
				set_pixel(firstPieceStartingByte + x + y, colorOne);
				set_pixel(secondPieceStartingByte + x + y, colorTwo);
			}
		} */
	}

	saveBMP(pInfo, DESTINATION_IMAGE_NAME);
	freeResources(NULL, pInfo);
		//							printf("Operation failed succesfully\n");
	return 0;
}
