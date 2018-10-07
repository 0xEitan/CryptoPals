#include <stdio.h>

#include "base64.h"


int main()
{
	u8 * res = base64_encode("Hello, my name is Eitan.");
	printf("Result: %s\n", res);
	free(res);

	return 0;
}