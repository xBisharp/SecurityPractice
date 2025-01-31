import struct
import sys

class ELFParser:
    def _init_(self, filename):
        self.filename = filename
        self.file = None
        self.header = {}
        self.section_headers = []

    def parse(self):
        with open(self.filename, 'rb') as self.file:
            self._parse_elf_header()
            self._parse_section_headers()

    def _parse_elf_header(self):
        self.file.seek(0)
        elf_header_fmt = '16sHHIQQQIHHHHHH'
        elf_header_size = struct.calcsize(elf_header_fmt)
        elf_header_data = self.file.read(elf_header_size)

        (e_ident, e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, 
         e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, 
         e_shstrndx) = struct.unpack(elf_header_fmt, elf_header_data)

        self.header = {
            'e_ident': e_ident,
            'e_type': e_type,
            'e_machine': e_machine,
            'e_version': e_version,
            'e_entry': e_entry,
            'e_phoff': e_phoff,
            'e_shoff': e_shoff,
            'e_flags': e_flags,
            'e_ehsize': e_ehsize,
            'e_phentsize': e_phentsize,
            'e_phnum': e_phnum,
            'e_shentsize': e_shentsize,
            'e_shnum': e_shnum,
            'e_shstrndx': e_shstrndx,
        }

    def _parse_section_headers(self):
        self.file.seek(self.header['e_shoff'])
        section_header_fmt = 'IIQQQQIIQQ'
        section_header_size = struct.calcsize(section_header_fmt)

        for i in range(self.header['e_shnum']):
            section_header_data = self.file.read(section_header_size)
            (sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size,
             sh_link, sh_info, sh_addralign, sh_entsize) = struct.unpack(
                section_header_fmt, section_header_data)

            section_header = {
                'sh_name': sh_name,
                'sh_type': sh_type,
                'sh_flags': sh_flags,
                'sh_addr': sh_addr,
                'sh_offset': sh_offset,
                'sh_size': sh_size,
                'sh_link': sh_link,
                'sh_info': sh_info,
                'sh_addralign': sh_addralign,
                'sh_entsize': sh_entsize,
            }

            self.section_headers.append(section_header)

    def display_header(self):
        print("ELF Header:")
        for key, value in self.header.items():
            print(f"  {key}: {value}")

    def display_sections(self):
        print("Section Headers:")
        for i, section in enumerate(self.section_headers):
            print(f"Section {i}: ")
            for key, value in section.items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python elf_parser.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    parser = ELFParser(filename)
    parser.parse()
    parser.display_header()
    parser.display_sections()
