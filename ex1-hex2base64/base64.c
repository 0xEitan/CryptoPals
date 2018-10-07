#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "base64.h"

#define FIRST_6_BITS(ptr)  (*(ptr) >> 2)
#define SECOND_6_BITS(ptr) (((*(ptr) & 0b00000011) << 4) + (*((ptr) + 1) >> 4))
#define THIRD_6_BITS(ptr)  (((*((ptr) + 1) & 0b00001111) << 2) + (*((ptr) + 2) >> 6))
#define FOURTH_6_BITS(ptr) (*((ptr) + 2) & 0b00111111)

#define ENCODED_BUFFER_LEN(buffer)  (ceil(strlen(buffer) / 3.0) * 4)

#define FILLER_BYTE '='

typedef unsigned char u8;

u8 TABLE[64] = {
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
	'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
	'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
	'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
	'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
	'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
	'w', 'x', 'y', 'z', '0', '1', '2', '3',
	'4', '5', '6', '7', '8', '9', '+', '/'
};

u8 * base64_encode(const u8 * buffer)
{
	int len = ENCODED_BUFFER_LEN(buffer) + 1;
	u8 * encoded = malloc(len);
	if (NULL == encoded) {
		return NULL;
	}

	u8 * tmp;
	for (tmp = encoded; *buffer; buffer += 3)
	{
		*tmp++ = TABLE[FIRST_6_BITS(buffer)];
		*tmp++ = TABLE[SECOND_6_BITS(buffer)];

		// In case the string length isn't divisible by 3:
		if (*(buffer + 1)) {
			*tmp++ = TABLE[THIRD_6_BITS(buffer)];

			if (*(buffer + 2)) {
				*tmp++ = TABLE[FOURTH_6_BITS(buffer)];
			} else {
				*tmp++ = FILLER_BYTE;
				break;
			}
		} else {
			*tmp++ = FILLER_BYTE;
			*tmp++ = FILLER_BYTE;
			break;
		}
	}

	*tmp = '\0';

	return encoded;
}