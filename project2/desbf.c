#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct {
	uint64_t key; // data of partial key
	uint64_t mask; // mask for bits which are unknown in key
	size_t blockc; // number of blocks of 1s in mask
	size_t *blocks; // for each block of 1s in mask, contains the index of the start and end of the block
} keyspace_t;

keyspace_t *ksp_init(uint64_t key, uint64_t mask)
{
	// Allocate keyspace struct
	keyspace_t *ksp = malloc(sizeof(keyspace_t));

	// Initialize key and mask
	ksp->key = key & ~mask; // masked bits of key should be 0
	ksp->mask = mask;

	// Determine number of contiguous blocks of '1' bits in mask
	size_t blkc = 0;
	int inblk = 0;
	for(size_t i = 0; i <= 64; i++) {
		uint64_t curbit = (i != 64) && (mask & (1ULL << i));
		if(curbit && !inblk) {
			blkc++;
			inblk = 1;
		} else if(!curbit && inblk) {
			inblk = 0;
		}
	}

	// Store blkc
	ksp->blockc = blkc;

	// Construct block buffer
	size_t *blk = malloc(sizeof(size_t) * blkc * 2);
	ksp->blocks = blk;
	inblk = 0;
       	size_t start = 0;
	for(size_t i = 0; i <= 64; i++) {
		uint64_t curbit = (i != 64) && (mask & (1ULL << i));
		if(curbit && !inblk) {
			start = i;
			inblk = 1;
		} else if(!curbit && inblk) {
			*blk++ = start;
			*blk++ = i;
			inblk = 0;
		}
	}

	return ksp;
}

void ksp_free(keyspace_t *ksp)
{
	free(ksp->blocks);
	free(ksp);
}

size_t ksp_len(keyspace_t *ksp)
{
	uint32_t *maskp = (uint32_t *) &ksp->mask;
	size_t popcount = __builtin_popcount(maskp[0]) + __builtin_popcount(maskp[1]);
	return 1ULL<<popcount;
}

uint64_t ksp_get(keyspace_t *ksp, size_t i)
{
	uint64_t key = ksp->key;
	for(int j = 0; j < ksp->blockc; j++) {
		size_t start = ksp->blocks[j * 2];
		size_t end = ksp->blocks[j * 2 + 1];
		key |= (i & ((1ULL << end) - 1ULL)) << start;
		i >>= end - start;
	}
	return key;
}

uint64_t parsehex(char *str)
{
	uint64_t v = 0ULL;
	for(int i = 0; i < 16 && str[i] != '\0'; i++) {
		uint64_t b;
		if(str[i] >= '0' && str[i] <= '9') {
			b = str[i] - '0';
		} else if(str[i] >= 'a' && str[i] <= 'f') {
			b = str[i] - 'a' + 10;
		} else if(str[i] >= 'A' && str[i] <= 'F') {
			b = str[i] - 'A' + 10;
		}

		v |= b << ((15 - i) * 4);
	}
	return v;
}

int main(int argc, char **argv) {
	printf("%llx\n", parsehex(argv[1]));
}

