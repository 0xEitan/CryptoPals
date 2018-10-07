#pragma once

typedef unsigned char u8;

/**
*	Encodes the given buffer using base 64 encoding
*	and returns a pointer to the encoded string
*
*	@note User should free the encoded buffer
*/
u8 * base64_encode(const u8 * buffer);
