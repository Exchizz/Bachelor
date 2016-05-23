#include "xxhash.h"
#include <iostream>

#define CAN_UUID	0x1FFFF7E8
int main(){
	int *data;
	*data = 0x1FFFF7E8;

	std::cout << "hash: " <<  XXH32((void * )data, 3*4, 0) << std::endl;
	return 0;
}
