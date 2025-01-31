#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <elf.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

void print_section_info(const char *filename, Elf64_Ehdr *ehdr) {
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        perror("Error opening file");
        exit(1);
    }

    // Read the section headers
    Elf64_Shdr *shdr = (Elf64_Shdr *) malloc(ehdr->e_shnum * sizeof(Elf64_Shdr));
    if (shdr == NULL) {
        perror("Error allocating memory for section headers");
        close(fd);
        exit(1);
    }

    // Move file pointer to the section header table
    if (lseek(fd, ehdr->e_shoff, SEEK_SET) == -1) {
        perror("Error seeking to section header table");
        free(shdr);
        close(fd);
        exit(1);
    }

    // Read the section header table into memory
    if (read(fd, shdr, ehdr->e_shnum * sizeof(Elf64_Shdr)) != ehdr->e_shnum * sizeof(Elf64_Shdr)) {
        perror("Error reading section header table");
        free(shdr);
        close(fd);
        exit(1);
    }

    // Get the section header string table index
    Elf64_Shdr *shstrtab = &shdr[ehdr->e_shstrndx];

    // Read section header string table
    char *strtab = (char *) malloc(shstrtab->sh_size);
    if (strtab == NULL) {
        perror("Error allocating memory for string table");
        free(shdr);
        close(fd);
        exit(1);
    }

    if (lseek(fd, shstrtab->sh_offset, SEEK_SET) == -1) {
        perror("Error seeking to string table");
        free(strtab);
        free(shdr);
        close(fd);
        exit(1);
    }

    if (read(fd, strtab, shstrtab->sh_size) != shstrtab->sh_size) {
        perror("Error reading string table");
        free(strtab);
        free(shdr);
        close(fd);
        exit(1);
    }

    // Print out section header info
    printf("Section Headers:\n");
    printf("  [Nr] Name              Type            Addr   Offset   Size   EntSize\n");
    for (int i = 0; i < ehdr->e_shnum; i++) {
        Elf64_Shdr *sec = &shdr[i];
        printf("  [%2d] %-17s %-15x %08lx %08lx %08lx %08lx\n", i,
               &strtab[sec->sh_name], sec->sh_type, sec->sh_addr,
               sec->sh_offset, sec->sh_size, sec->sh_entsize);
    }

    // Cleanup
    free(strtab);
    free(shdr);
    close(fd);
}

void parse_elf_header(const char *filename) {
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        perror("Error opening ELF file");
        exit(1);
    }

    // Read ELF header
    Elf64_Ehdr ehdr;
    if (read(fd, &ehdr, sizeof(Elf64_Ehdr)) != sizeof(Elf64_Ehdr)) {
        perror("Error reading ELF header");
        close(fd);
        exit(1);
    }

    // Check for valid ELF magic number
    if (memcmp(ehdr.e_ident, ELFMAG, SELFMAG) != 0) {
        printf("Not a valid ELF file\n");
        close(fd);
        exit(1);
    }

    // Print ELF Header information
    printf("ELF Header:\n");
    printf("  Magic:   ");
    for (int i = 0; i < EI_NIDENT; i++) {
        printf("%02x ", ehdr.e_ident[i]);
    }
    printf("\n");

    printf("  Class:                             ");
    switch (ehdr.e_ident[EI_CLASS]) {
        case ELFCLASS32:
            printf("ELF32\n");
            break;
        case ELFCLASS64:
            printf("ELF64\n");
            break;
        default:
            printf("Unknown\n");
            break;
    }

    printf("  Data:                              ");
    switch (ehdr.e_ident[EI_DATA]) {
        case ELFDATA2LSB:
            printf("Little Endian\n");
            break;
        case ELFDATA2MSB:
            printf("Big Endian\n");
            break;
        default:
            printf("Unknown\n");
            break;
    }

    printf("  Version:                           %d\n", ehdr.e_ident[EI_VERSION]);
    printf("  OS/ABI:                            %d\n", ehdr.e_ident[EI_OSABI]);
    printf("  ABI Version:                       %d\n", ehdr.e_ident[EI_ABIVERSION]);
    printf("  Type:                              %x\n", ehdr.e_type);
    printf("  Machine:                           %x\n", ehdr.e_machine);
    printf("  Version:                           %x\n", ehdr.e_version);
    printf("  Entry point address:               %lx\n", ehdr.e_entry);
    printf("  Start of program headers:          %lx\n", ehdr.e_phoff);
    printf("  Start of section headers:          %lx\n", ehdr.e_shoff);
    printf("  Flags:                             %x\n", ehdr.e_flags);
    printf("  Size of this header:               %d\n", ehdr.e_ehsize);
    printf("  Size of program headers:           %d\n", ehdr.e_phentsize);
    printf("  Number of program headers:         %d\n", ehdr.e_phnum);
    printf("  Size of section headers:           %d\n", ehdr.e_shentsize);
    printf("  Number of section headers:         %d\n", ehdr.e_shnum);
    printf("  Section header string table index: %d\n", ehdr.e_shstrndx);

    // Parse section information
    print_section_info(filename, &ehdr);

    close(fd);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <ELF file>\n", argv[0]);
        return 1;
    }

    parse_elf_header(argv[1]);
    return 0;
}
