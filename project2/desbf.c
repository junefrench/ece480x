#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <openssl/des.h>
#include <pthread.h>
#ifdef __APPLE__
#define bswap_8(x) ((x) & 0xff)
#define bswap_16(x) ((bswap_8(x)<<8)|(bswap_8((x)>>8)))
#define bswap_32(x) ((bswap_16(x)<<16)|(bswap_16((x)>>16)))
#define bswap_64(x) ((bswap_32(x)<<32)|(bswap_32((x)>>32)))
#else
#include <byteswap.h>
#endif

#define SEARCH_BLOCK_SIZE (0xffff)

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

uint64_t ksp_max(keyspace_t *ksp)
{
	uint32_t *maskp = (uint32_t *) &ksp->mask;
	size_t popcount = __builtin_popcount(maskp[0]) + __builtin_popcount(maskp[1]);
	if(popcount == 64) {
		return ~0ULL;
	} else {
		return (1ULL<<popcount) - 1;
	}
}

uint64_t ksp_get(keyspace_t *ksp, uint64_t i)
{
	uint64_t key = ksp->key;
	for(size_t j = 0; j < ksp->blockc; j++) {
		size_t start = ksp->blocks[j * 2];
		size_t end = ksp->blocks[j * 2 + 1];
		key |= (i & ((1ULL << (end - start)) - 1ULL)) << start;
		i >>= (end - start);
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

uint64_t ntoh64(uint64_t h)
{
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	return bswap_64(h);
#else
	return h;
#endif
}

uint64_t hton64(uint64_t h)
{
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	return bswap_64(h);
#else
	return h;
#endif
}

typedef struct {
	pthread_mutex_t mtx;
	uint64_t nblk;
	uint64_t pt;
	uint64_t ct;
	keyspace_t *ksp;
} checkargs_t;

void *check_thread(void *arg)
{
	checkargs_t *args = (checkargs_t *) arg;
	while(1) {
		uint64_t gct = 0, pt = hton64(args->pt), ct = hton64(args->ct);

		size_t start, end;
		pthread_mutex_lock(&args->mtx);
		size_t max = ksp_max(args->ksp);
		if(args->nblk == max) {
			pthread_mutex_unlock(&args->mtx);
			return NULL;
		}
		start = args->nblk;
		if(max - start <= SEARCH_BLOCK_SIZE) {
			printf("Last block\n");
			end = max;
		} else {
			end = start + SEARCH_BLOCK_SIZE;
		}
		args->nblk = end;
//		printf("Starting task from %lu to %lu\n", start, end);
		pthread_mutex_unlock(&args->mtx);
		
		keyspace_t *ksp = args->ksp;
		DES_cblock *ptb = (DES_cblock *) &pt;
		DES_cblock *gctb = (DES_cblock *) &gct;
		DES_cblock *ctb = (DES_cblock *) &ct;
		for(uint64_t i = start; i <= end; i++) {
			uint64_t kg = hton64(ksp_get(ksp, i));
	//		printf("kg: %016llx\n", kg);

			DES_cblock *kb = (DES_cblock *) &kg;

			DES_key_schedule keysched;
			DES_set_key(kb, &keysched);
			DES_ecb_encrypt(ptb, gctb, &keysched, DES_ENCRYPT);

	//		printf("gct:%016llx\n", gct);

			if(ct == gct){
				printf("%016llx\n", ntoh64(kg));
				exit(0);
			}
		}
	}
	return NULL;
}

int main(int argc, char **argv)
{
	uint64_t pt, ct, k, m;
	size_t nt;
	if(argc == 3 || argc == 4) {
		pt = parsehex(argv[1]);
		ct = parsehex(argv[2]);
		k  = 0x0000000000000000ULL;
		m  = 0xffffffffffffffffULL;
		if(argc == 4) {
			nt = atoi(argv[3]);
		} else {
			nt = 1;
		}
	} else if(argc == 5 || argc == 6) {
		pt = parsehex(argv[1]);
		ct = parsehex(argv[2]);
		k  = parsehex(argv[3]);
	        m  = parsehex(argv[4]);	
		if(argc == 6) {
			nt = atoi(argv[5]);
		} else {
			nt = 1;
		}
	} else {
		fprintf(stderr, "Usage: %s plaintext cyphertext [key mask] [jobs], where all arguments except jobs are hex-encoded 64-bit values\n", argv[0]);
		fprintf(stderr, "	plaintext: plaintext of a known plain/cyphertext pairing\n");
		fprintf(stderr, "	cyphertext: cyphertext of a known plain/cyphertext pairing\n");
		fprintf(stderr, "	key: (optional) the partially-known key\n");
		fprintf(stderr, "	key: (optional, must accompany key) mask in which the unknown bits in key are 1\n");
		fprintf(stderr, "	jobs: (optional) number of worker threads to spawn\n");

		return 1;
	}

	m &= ~0x0101010101010101ULL;

//	printf("pt: %016llx\n", pt);
//	printf("ct: %016llx\n", ct);
//	printf("k:  %016llx\n", k);
//	printf("m:  %016llx\n", m);
	keyspace_t *ksp = ksp_init(k, m);

	uint64_t max = ksp_max(ksp);

	pthread_t threads[nt];
	checkargs_t args;
	args.pt = pt;
	args.ct = ct;
	args.ksp = ksp;
	pthread_mutex_init(&args.mtx, NULL);
	for(int i = 0; i < nt; i++) {
		pthread_create(&threads[i], NULL, check_thread, &args);
	}
	for(int i = 0; i < nt; i++) {
		pthread_join(threads[i], NULL);
	}
	fprintf(stderr, "No solution");
	return 1;
}

