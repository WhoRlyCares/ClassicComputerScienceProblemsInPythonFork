from __future__ import annotations

import random

"""
    ACTG -> bits:
        A:00 C:01
        G:10 T:11
    8bit char -> 2 bits
"""


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self.nuc2bits = {
            'A':0b00,
            'C':0b01,
            'G':0b10,
            'T':0b11
        }
        self.bits2nuc = {self.nuc2bits.get(k):k for k in self.nuc2bits.keys()} #having 2 dicts is hashfaster then
        # looking for items
        # in lookup

        self.bit_str = 1
        self.compress(gene)

    def compress(self, gene: str) -> None:
        # self.bit_str = 1
        for n in gene.upper():
            self.bit_str <<= 2  # leftshift
            if n == 'A':
                self.bit_str |= 0b00  # 2 last bit swith to 00
            elif n == 'C':
                self.bit_str |= 0b01  # bitwise ior is works like union for iterable
            elif n == 'G':
                self.bit_str |= 0b10  # since we left shift it always plain add decided bits
            elif n == 'T':
                self.bit_str |= 0b11
            else:
                raise ValueError(f"Invalid Nucleotide: {n}")

    def decompress(self) -> str:
        gene = ""
        for i in range(0, self.bit_str.bit_length() - 1, 2):
            # we set init bit_str=1 => we need (len-1) to ignore it
            bits = self.bit_str >> i & 0b11  # rightshift i then get 2 bits
            if bits == 0b00:
                gene += 'A'
            elif bits == 0b01:
                gene += 'C'
            elif bits == 0b10:
                gene += 'G'
            elif bits == 0b11:
                gene += 'T'
            else:
                raise ValueError(f'Invalide bits {bits} at pos {i}')
        return gene[::-1]  # inverse slice

    def comp_mapped(self, gene) -> None:
        for n in gene.upper():
            self.bit_str <<= 2  # leftshift
            if n in self.nuc2bits.keys():
                self.bit_str |= self.nuc2bits.get(n)
            else:
                raise ValueError(f"Invalid Nucleotide: {n}")
    def decop_mapped(self) -> str:
        gene = ""
        for i in range(0, self.bit_str.bit_length() - 1, 2):
            bits = self.bit_str >> i & 0b11  # rightshift i then get 2 bits
            if bits in self.bits2nuc.keys():
                gene += self.bits2nuc.get(bits)
            else:
                raise ValueError(f'Invalide bits {bits} at pos {i}')
        return gene[::-1]  # inverse slice

    def __str__(self) -> str:
        return self.decompress()

    @staticmethod
    def random_gene_of_len(n):
        return "".join(random.choice(['A', 'C', 'G', 'T']) for _ in range(n))


def run_size_tests(orig=None, gen_len=0) -> None:
    from sys import getsizeof
    original = "TAGGATCATATCCCGTCATCGTAC" * 100
    if not orig:
        if gen_len <= 0:
            orig = original
        else:
            orig = CompressedGene.random_gene_of_len(gen_len)
    print(f"Original {orig[:10]}... is {getsizeof(orig)} bytes")
    compressed = CompressedGene(orig)
    print(f"Compressed {compressed.decompress()[:10]}... is {getsizeof(compressed.bit_str)} bytes ")
    print(f"Orig and compressed are the same: {orig == compressed.decompress()}")

def run_speed_test(gen_len=100, passes=10):
    from functools import partial
    from timeit import Timer
    rnd_seq = CompressedGene.random_gene_of_len(gen_len)
    cg = CompressedGene(rnd_seq)
    cg_map = CompressedGene(rnd_seq)
    print(f"Creating genes from {rnd_seq[:10]}... of len {len(rnd_seq)} {passes} times" )
    t1 = Timer(partial(cg.compress, rnd_seq))
    t2 = Timer(partial(cg_map.comp_mapped, rnd_seq))
    print(f"If/else: {t1.timeit(passes)}  Map {t2.timeit(passes)}")
    print(f"Decoding the same...")
    t1 = Timer(partial(cg.decompress))
    t2 = Timer(partial(cg_map.decop_mapped))
    print(f"If/else: {t1.timeit(passes)}  Map {t2.timeit(passes)}")
    print("Mapping is slower, but more readable...")

if __name__ == "__main__":
    run_size_tests()
    run_speed_test()
    ...
