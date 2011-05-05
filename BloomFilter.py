from array import array

class BloomFilter:
    # http://en.wikipedia.org/wiki/Bloom_filter
    # http://bit.ly/bloom_filter
    # http://code.activestate.com/recipes/577686/

    def __init__(self, num_bits, num_probes, probe_func):
        self.num_bits= num_bits
        num_words = (num_bits + 31) // 32
        self.arr = array('L', [0]) * num_words
        self.num_probes = num_probes
        self.probe_func = get_probes

    def add(self, key):
        for i, mask in self.probe_func(self, key):
            self.arr[i] |= mask

    def match_template(self, bfilter):
        return (self.num_bits == bfilter.num_bits \
            and self.num_probes == bfilter.num_probes \
            and self.probe_func == bfilter.probe_func)

    def union(self, bfilter):
        if self.match_template(bfilter):
            self.arr = [a | b for a, b in zip(self.arr, bfilter.arr)]
        else:
            # Union b/w two unrelated bloom filter raises this
            raise ValueError("Mismatched bloom filters")

    def intersection(self, bfilter):
        if self.match_template(bfilter):
            self.arr = [a & b for a, b in zip(self.arr, bfilter.arr)]
        else:
            # Intersection b/w two unrelated bloom filter raises this
            raise ValueError("Mismatched bloom filters")

    def __contains__(self, key):
        return all(self.arr[i] & mask for i, mask in self.probe_func(self, key))

