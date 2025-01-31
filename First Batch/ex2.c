#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

int main()
{

	int fd;
	if ((fd = open("dummy", O_RDONLY)) < 0)
	{
		fprintf(stderr, "Error opening file: %s\n", strerror(errno));
		exit(1);
	}

	void *ptr;
	if ((ptr = mmap(NULL, 0x4A, PROT_EXEC, MAP_PRIVATE, fd, 0x1000)) == MAP_FAILED)
	{
		fprintf(stderr, "Error calling mmap: %s\n", strerror(errno));
		exit(1);
	}
	printf("%p\n", ptr);
	close(fd);

	(*(void (*)())ptr + 0x0106)();

	exit(0);
}
