#ifndef __EX1_HEX_H__
#define __EX1_HEX_H__

typedef unsigned char u8;

/**
*	Encodes the given buffer using base 64 encoding
*	and returns a pointer to the encoded string
*
*	@note User should free the encoded buffer
*/
u8 * base64_encode(const u8 * buffer);

#endif  /* __EX1_HEX_H__ */

