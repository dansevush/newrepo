#!/usr/bin/env python

"""
To invoke, use python 2.7: "python fitblocks.py"
All packages should be available with python 2.7
The test_fit_blocks function should be called with the number of units in the problem, multiplied by ten
So a width of 12 would be 120, and the seams would be located in multiples of 30 or 45

"""
from itertools import combinations
import time
from datetime import timedelta

# enable/disable test function calls here
def main():

    # examples given in problem
    test_fit_blocks(120, 4) # 120 is equivalent to using 12, and 4 rows
    test_fit_blocks(270, 5) # 270 is equivalent to using 27, and 5 rows

    # the one we're solving
    test_fit_blocks(480, 10)    # 480 is the same as 48, and 10 rows

    # just test the permutations we generate
    # test_permutations()


# recursive helper function used by test code
def count_patterns_depth(last_row, row=0, seam_good=None,seams_list=None, seam_good_counts=None):
    """    
    :param last_row: number of rows (0 relative)
    :param row: current row (0 relative)
    :param seam_good: dict used to get lists of possible good seams for any given seam
    :param seams_list: all possible seams that will fit (base candidates)
    :param seam_good_counts: dict cache for memoizing
    :return: None for last_row, otherwise total count for all rows traversed so far
    """

    if seams_list is None or seam_good is None or seam_good_counts is None:
        return None

    if row == last_row:
        return len(seams_list)

    total_count = 0
    if row == 0:
        top_level_progress = 0
        total_progress = len(seams_list)
        program_start_time = time.time()

    for seam in seams_list:
        start_time = time.time()

        if tuple(seam_good[seam]) in seam_good_counts[row]:
            this_count = seam_good_counts[row][tuple(seam_good[seam])]
        else:
            this_count = count_patterns_depth(last_row, row + 1, seam_good=seam_good, 
                seams_list=seam_good[seam], seam_good_counts=seam_good_counts)
            seam_good_counts[row][tuple(seam_good[seam])] = this_count
        total_count += this_count
        if row == 0:
            top_level_progress += 1
            template = 'step {:>5,}  count:{:>17,}  total count:{:>18,}   elapsed {}  total elapsed {}'
            print template.format(top_level_progress, this_count, total_count,
                str(timedelta(seconds=time.time() - start_time))[6:], 
                str(timedelta(seconds=time.time() - program_start_time))[3:] )

    return total_count


def test_fit_blocks(test_width=120, test_rows=2, test_blocks=(30,45)):

    # first generate all perfect fits, using the sizes in test_blocks and test_width
    results = generate_unique_fits(test_width, test_blocks[0], test_blocks[1])
    results_length = len(results)

    # show what we've got
    if results_length == 0:
        print '**oops!** Width of {0} did not line up with lengths of {1}'.format(test_width, test_blocks)
    else:
        seams_list = []
        permutations_list = []
        seam_to_permutations = {}

        print '\nWidth of {0} has {1} unique block pattern{2}'.format(test_width, results_length, 's' if results_length > 1 else '')
        for t in results:
            if t[0] and t[1]:
                print '={0}x{1}w blocks and {2}x{3}w blocks'.format(t[0], test_blocks[0], t[1], test_blocks[1])
            elif t[0]:
                print '={0}*{1} block{2}'.format(t[0], test_blocks[0], 's' if t[0] > 1 else '')
            elif t[1]:
                print '={0}*{1} block{2}'.format(t[1], test_blocks[1], 's' if t[1] > 1 else '')

            if test_width > 480:
               pass
            else:
                print 't:', t
                for permutation in generate_permutations(t, test_blocks):
                    print list(permutation)
                    seams = create_seams(permutation)
                    seams_list.append(seams)
                    permutations_list.append(permutation)
                    seam_to_permutations[seams]=permutation

    print 'seams count:', len(seams_list)
    if len(seams_list) > 65:
        print 'hang on, this will take a few seconds...'

    seam_good = {}
    perms_good = {}
    for seam_outer in seams_list:
        good_list=[]
        perms_good_list=[]
        for seam_inner in seams_list:
            if seam_inner is seam_outer:
                continue
            if seam_outer & seam_inner:
                pass
            else:
                good_list.append(seam_inner)
                perms_good_list.append(seam_to_permutations[seam_inner])
        seam_good[seam_outer]=good_list
        perms_good[seam_outer]=perms_good_list

    for seam in seams_list:
        permutations = seam_to_permutations[seam]
        print '\ncols:', list(permutations)
        print 'seam:', sorted(seam)
        print 'good count:', len(seam_good[seam])
        print 'seams count:', len(seams_list)


    pattern_list = []
    row_counts = []

    seams_dict = {}
    for seam in seams_list:
        seams_dict[seam] = seam_good[seam]

    seam_good_counts = {}
    # init our cache for the depth (row count)
    for i in range(0, test_rows):
        seam_good_counts[i] = {}
    total = count_patterns_depth(test_rows-1, seam_good=seam_good, seams_list=seams_list, seam_good_counts=seam_good_counts)
    print 'total for  ', test_rows, ' rows depth is ', '{:,}'.format(total)

    return


def generate_unique_fits(width, block1, block2):
    """
    Generate the unique list of counts. This will get turned into permutations later
    param width: width for blocks to fit exactly
    param block1, block2: width of the two blocks
    return list of tuples with count for (block1, block2)
    """
    fits_list=[]

    block1_max = int(width/block1)
    block2_max = int(width/block1)
    for block1_count in range(0, block1_max+1):
        for block2_count in range(0, block2_max+1):
            if width == block1_count * block1 + block2_count * block2:
                fits_list.append((block1_count, block2_count))

    return fits_list

def generate_pattern(counts, sizes):
    """
    param counts: tuple with (count1, count2)
    param sizes: tuple with (size1, size2)
    returns list of tuples
    """
    if 0 in counts:
        ix = 0 if counts[0] else 1
        return [tuple(([sizes[ix]]) * counts[ix])]
    width1, width2 = sizes
    return  (([sizes[0]]) * counts[0]) + (([sizes[1]]) * counts[1])

def generate_permutations(counts, sizes):
    """
    param counts: tuple with (count1, count2)
    param sizes: tuple with (size1, size2)
    returns list of tuples
    """
    total_bits = counts[0] + counts[1]
    bits_to_set = counts[1]
    unset_value = sizes[0]
    set_value = sizes[1]
    print 'kbits total bits:', total_bits, ' set bits:', bits_to_set, ' set_value', set_value, 'unset value:', unset_value
    all_patterns = kbits(total_bits, bits_to_set, set_value, unset_value)
    unique = unique_permutations(all_patterns)
    print 'generator count - all:', len(all_patterns), ' unique:', len(unique)
    return sorted(unique)

    # this is not used anymore - using permutations has an ugly factorial slowdown
    base_pattern = generate_pattern(counts, sizes)
    print 'base pattern:', base_pattern

    results = list(perms(base_pattern))
    unique = unique_permutations(results)
    return sorted(unique)

def create_seams(row_data):
    """
    :param row_data: tuple or list containing (relative) widths
    :return: seams: set containing absolute seams
    """
    offset = 0
    seams = set()
    for col in row_data:
        # print 'col:', col, ' type:', type(col)
        offset += col
        seams.add(offset)

    # last seam is actually end of row, don't need it in the set
    seams.discard(offset)
    # easier to hash if it's frozen
    return frozenset(seams)

def unique_permutations(input_list):
    """
    eliminate dupes
    """
    s = set()
    for entry in input_list:
        s.add(tuple(entry))
    l = []
    for entry in s:
        l.append(list(entry))
    return l


# found this code on the interwebs, avoids the n facorial problem
def kbits(width, bits_to_set, set_value=1, unset_value=0):
    result = []
    if bits_to_set == 0:
        result.append([unset_value] * width)

    for bits in combinations(range(width), bits_to_set):
        s = [unset_value] * width
        for bit in bits:
            s[bit] = set_value
            result.append(s)
    return result



def test_permutations():

    element_values = (30, 45)
    counts=((3,0), (2,1), (1,2))
    counts=((1,2), (4,0), (3,4), (6,2), (9,0), (1,10), (4,8), (7,6), (10,4), (13,2))
    # Width of 120 has 2 unique block patterns
    # 1x30w blocks and 2x45w blocks  (1, 2)
    # 4x30 blocks                    (4, 0)

    # Width of 270 has 4 unique block patterns
    # 6x45w blocks
    # 3x30w blocks and 4x45w blocks   (3, 4)
    # 6x30w blocks and 2x45w blocks   (6, 2)
    # 9x30 blocks                     (9, 0)

    # Width of 480 has 6 unique block patterns
    #  1x30w  10x45w blocks           (1, 10)  
    #  4x30w   8x45w blocks           (4, 8)
    #  7x30w   6x45w blocks           (7, 6)
    # 10x30w   4x45w blocks           (10, 4)
    # 13x30w   2x45w blocks           (13, 2)
    # 16x30w

    # element_values=(0,1)

    for count in counts:
        total_bits = count[0] + count[1]
        bits_to_set = count[1]
        unset_value = element_values[0]
        set_value = element_values[1]
        all_patterns = kbits(total_bits, bits_to_set, set_value, unset_value)
        unique = unique_permutations(all_patterns)
        print 'generator count - all:', len(all_patterns), ' unique:', len(unique)
        for perm in unique:
            print perm
# we place this dead last because python does not care about forward declarations
main()




# please ignore this code, not used anymore
# experimented with bitfields instead of sets. 
# memory was not the issue once I used depth first traversal

#
# from http://code.activestate.com/recipes/113799/
# added ability to init with a string or array
class bitfield(object):
    def __getitem__(self, index):
        return (self._d >> index) & 1 

    def __init__(self,value=0):
        if type(value) == list and value:
            if type(value[0]) == int:
                value = ''.join(map(str, value))
            value = ''.join(value)
        if type(value) == str:
            value = int(value, 2)
        self._d = value

    def __setitem__(self,index,value):
        value    = (value&1L)<<index
        mask     = (1L)<<index
        self._d  = (self._d & ~mask) | value

    def __getslice__(self, start, end):
        mask = 2L**(end - start) -1
        return (self._d >> start) & mask

    def __setslice__(self, start, end, value):
        mask = 2L**(end - start) -1
        value = (value & mask) << start
        mask = mask << start
        self._d = (self._d & ~mask) | value
        return (self._d >> start) & mask

    def __int__(self):
        return self._d

    def __str__(self):
        return bin(self._d)

# we'll subclass bitfield to get our features
# granularity defines the linear scale to use for each bit
# our default is convienently 15
class bitmap(bitfield):
    def __init__(self, value=0, granularity=15):
        print 'init bitmap value:', value
        super(bitmap, self).__init__(value)
        self.set_granularity(granularity)

    def clear(self):
        self._d = 0

    def set_granularity(self, granularity):
        self._granularity = granularity

    # absolute col positioning
    def set_abs(self, cols):
        self.clear()
        for col in cols:
            # print 'col:', col, type(col)
            # print 'granularity:', self._granularity, type(self._granularity)
            if col % self._granularity: # ignore cols that are not on granular boundries
                continue
            bit_position = (col / self._granularity)-1
            self.__setitem__(bit_position, 1)
    def set_rel(self, cols):
        abs_col = 0
        abs_list = []
        for col in cols:
            if col % self._granularity: # ignore cols that are not on granular boundries
                continue
            abs_col += col
            abs_list.append(abs_col)
        self.set_abs(abs_list)

    def get_abs(self):
        bits = self._d
        abs_list = []
        bit_value = self._granularity
        while bits:
            if bits & 1:
                abs_list.append(bit_value)
            bits >>= 1
            bit_value += self._granularity
        return abs_list

    def get_rel(self):
        rel_list = []
        last_abs_value = 0
        for col in self.get_abs():
            rel_list.append(col - last_abs_value)
            last_abs_value += col - last_abs_value
        return rel_list


def test_bitfield():
    t = bitmap(0b101010, granularity=1)
    print t

    t = bitmap([1,0,1,0,1,0])
    print t
    print t.get_rel()
    print t.get_abs()
    print t

    t= bitmap()

    t.set_abs([30,75,120])
    # t.set_rel((30, 45, 45))
    # print t
    print t.get_abs()
    print t.get_rel()
