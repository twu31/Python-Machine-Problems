
# coding: utf-8

# # Recursion
# 
# ## Overview

# For this assignment you will explore a handful of problems that are most easily solved using recursive processes.

# ## The Super Digit
# 
# The "super digit" of a (base 10) number *N* is defined as follows:
# - if the number consists of a single digit, it is simply *N*
# - otherwise, it is the super digit of the sum of the digits of *N*
# 
# Examples:
# - the super digit of 7 is 7
# - the super digit of 42 is the super digit of 4+2=6, which is 6
# - the super digit of 9876 is the super digit of 9+8+7+6=30, which is the super digit of 3+0=3, which is 3
# 
# Implement the recursive function `super_digit`, which returns the super digit of its argument.

# In[80]:

def super_digit(n):
    if n < 10:
        return n 
    else:
        superdigit=0
        for x in str(n):
            superdigit = superdigit + int(x)
        if superdigit > 9:
            return super_digit(superdigit)
        elif superdigit < 10:
            return superdigit       


# In[81]:

from unittest import TestCase

tc = TestCase()

tc.assertEqual(super_digit(5), 5)
tc.assertEqual(super_digit(30), 3)
tc.assertEqual(super_digit(9876), 3)
tc.assertEqual(super_digit(11111111111111), 5)
tc.assertEqual(super_digit(12345678901234567890), 9)


# ## Pascal's Triangle
# 
# Pascal's triangle is a triangular arrangement of numbers where the top row contains the single number `1`, and the values in each following (centered) row are the sum of the value(s) in the row above. The following first five rows of Pascal's triangle should help demonstrate the idea:
# 
#               1
#              1 1
#             1 2 1
#            1 3 3 1
#           1 4 6 4 1
#       
# By convention, the rows and columns of Pascal's triangle are numbered starting from 0 — note that the 0th column of every row contains the value 1. To aid in the computation of edge cases (columns in rows that do not have two values above them), it is also convenient to imagine that there are columns in row 0 extending off in both directions that contain 0s. I.e., we might envision the first row of Pascal's triangle as follows:
# 
#     ... 0 0 0 1 0 0 0 ...
#              1 1
#             1 2 1
#            1 3 3 1
#           1 4 6 4 1
# 
# Wolfram Mathworld has a good writeup on the [properties and provenance of Pascal's Triangle](http://mathworld.wolfram.com/PascalsTriangle.html).
# 
# Complete the following function, which returns the value to be found in a given row and column of Pascal's triangle.

# In[82]:

def pascal(row, column):
    if column==0:
        return 1
    elif row == 0:
        return 0
    return (row * pascal(row-1, column-1)) / column
    #return pascal(row, column) + pascal(r,l)


# In[83]:

# generate the first 10 rows of Pascal's Triangle
for row in range(10):
    print('{: ^45}'.format(' '.join(str(pascal(row, col)) for col in range(row+1))))


# In[84]:

from unittest import TestCase

tc = TestCase()

tc.assertEqual(pascal(0, 0), 1)
tc.assertEqual(pascal(1, 0), 1)
tc.assertEqual(pascal(2, 1), 2)
tc.assertEqual(pascal(5, 1), 5)
tc.assertEqual(pascal(5, 2), 10)
tc.assertEqual(pascal(10, 5), 252)


# ## Subset Product
# 
# This next one asks you to employ a common recursive pattern — that of computing all the subsets of a given set of things. In this problem, you are to determine whether or not an integer $P \gt 1$ can be computed as the product of any combination of a provided list of integers (where each factor *f* $> 0$ can only be used once).
# 
# Examples:
# 
# - given $P = 10$, and the list [2, 3, 4, 5], we see that $2 \times 5 = 10$, so the answer is yes
# - given $P = 81$, and the list [2, 2, 3, 3, 4, 9], $3 \times 3 \times 9 = 81$, so the answer is yes
# - given $P = 100$ and the list [3, 4, 5, 8, 10], the answer is no
# 
# Complete the implementation of the recursive `can_make_product`, which returns `True` or False based on whether the argument `p` can be computed as the product of some subset of the list of integers `vals`.

# In[85]:

def can_make_product(p, vals):
    if p==1:
        return True
    elif not vals:
        return False
    elif p % vals[-1]==0:
        last = vals[-1]
        vals.pop()
        return can_make_product(p//last, vals) #recursion of the function or the function where it iterates through vals and p
    else:
        vals.pop()
        return can_make_product(p, vals)


# In[86]:

from unittest import TestCase

tc = TestCase()

tc.assertTrue(can_make_product(10, [2, 5]))
tc.assertTrue(can_make_product(10, [2, 3, 4, 5]))
tc.assertTrue(can_make_product(10, [3, 4, 2, 5]))
tc.assertTrue(can_make_product(10, [10]))
tc.assertTrue(can_make_product(81, [2, 2, 3, 3, 4, 9]))
tc.assertTrue(can_make_product(66402, [2, 4, 5, 12, 17, 25, 31, 63]))
tc.assertFalse(can_make_product(10, [2, 2, 2, 4]))
tc.assertFalse(can_make_product(243, [2, 2, 3, 3, 3, 4, 4, 4]))
tc.assertFalse(can_make_product(81, [2, 3, 5, 9, 11]))
tc.assertFalse(can_make_product(100, [3, 4, 5, 8, 10]))
tc.assertFalse(can_make_product(12369, [3, 4, 5, 8, 19, 20, 31]))


# ## Block Voting Systems

# In voting systems such as the United States' electoral college, voters are assigned different weights which we'll refer to as voting "blocks". This makes it so that a given voter may have a greater or lesser impact on the  outcome of a vote.
# 
# There are a few different ways of measuring the effectiveness of a block voting system. You'll write a couple of recursion functions to help do this.
# 
# To start, it's interesting to determine the number of ways in which a block voting system can be tied. Consider a system of 3 voting blocks: block A = 3 votes, block B = 2 votes, block C = 1 vote. The following are tie situations where each block can vote either *for* or *against* some measure:
# 
# - A *for* vs. B + C *against* (3 vs. 2 + 1)
# - B + C *for* vs. A *against* (2 + 1 vs. 3)
# 
# With the list of voting blocks [1, 1, 2, 3, 5], on the other hand, there are a total of 4 possible tied scenarios (you should be able to enumerate them).
# 
# Complete the implementation of the function `number_ties`, which returns the number of tie situations arising from the provided list of voting blocks. Note that we've also include two default arguments that you may find useful in your implementation — feel free to change their names and/or initial values (or add additional arguments with default values). 

# In[87]:

def number_ties(blocks, for_votes=0, against_votes=0):
    if not blocks and for_votes==against_votes:
        return 1
    elif not blocks:
        return 0
    else:
        num = blocks[0]
        return number_ties(blocks[1:],for_votes+num,against_votes) + number_ties(blocks[1:],for_votes,against_votes+num)


# In[88]:

from unittest import TestCase

tc = TestCase()

tc.assertEqual(number_ties([1, 2, 3]), 2)
tc.assertEqual(number_ties([1, 1, 2, 3, 5]), 4)
tc.assertEqual(number_ties([4, 5, 6, 7, 8, 9]), 0)
tc.assertEqual(number_ties([10, 15, 9, 4, 4, 8, 12, 8]), 10)
tc.assertEqual(number_ties([17, 10, 9, 9, 10, 10, 7, 12, 17, 13, 14, 9, 16, 16, 5]), 554)
tc.assertEqual(number_ties([16, 17, 17, 30, 15, 27, 22, 20, 33, 33, 26, 22, 27, 19, 15, 16, 25, 25, 19, 18]), 8040)


# More importantly, we can compute how many situations arise in which a given block can cast the *deciding vote*.
# 
# E.g., given voting blocks [1, 2, 3, 4], to determine the number of times the last block casts the deciding vote, we observe that:
# - there are a total of eight ways in which blocks 1, 2, and 3 can vote:
#     1. 1 + 2 + 3 (for) vs. 0 (against)
#     2. 1 + 2 (for) vs. 3 (against)
#     3. 1 + 3 (for) vs. 2 (against)
#     4. 1 (for) vs. 2 + 3 (against)
#     5. 2 + 3 (for) vs. 1 (against)
#     6. 2 (for) vs. 1 + 3 (against)
#     7. 3 (for) vs. 1 + 2 (against)
#     8. 0 (for) vs. 1 + 2 + 3 (against)
# - in cases 2-7, the last voter (with a block of 4 votes) can cause the result to swing one way or the other (or end in a tie); we therefore say that the last block has the deciding vote in *6* cases
# 
# If you repeat the analysis for blocks 1, 2, and 3, you'll find that they are the deciding voters in 2, 4, and 4 cases, respectively (meaning that the blocks with 2 and 3 votes are equally important!).
# 
# You are to implement the function `deciding_votes_per_block`, which will take a list of voting blocks and return a list of times that each block is the deciding vote. You should define a separate recursive function (in the same cell) that computes the number of deciding votes given a particular block.

# In[89]:

def deciding_votes_per_block(blocks):
    to_return=[]
    for i in range(len(blocks)):
        tocheck=blocks.pop()
        to_return.append(deciding_count(blocks,tocheck))
        blocks.insert(0, tocheck)
    to_return.reverse()
    return to_return
        

def deciding_count(blocks1,tocheck, for_votes=0, against_votes=0):
    if not blocks1 and ((tocheck + for_votes) < against_votes or (tocheck+against_votes) < for_votes):
        return 0
    elif not blocks1:
        if ((tocheck+for_votes) >= against_votes ) or ((tocheck+against_votes) >= for_votes):
            return 1
    else:
        num=blocks1[0]
        return deciding_count(blocks1[1:],tocheck,for_votes+num,against_votes) + deciding_count(blocks1[1:],tocheck,for_votes,against_votes+num)


# In[90]:

from unittest import TestCase

tc = TestCase()

tc.assertEqual(deciding_votes_per_block([1, 1, 2]), [2, 2, 4])
tc.assertEqual(deciding_votes_per_block([1, 2, 3, 4]), [2, 4, 4, 6])
tc.assertEqual(deciding_votes_per_block([4, 5, 6, 7, 8, 9]), [4, 8, 8, 12, 12, 16])
tc.assertEqual(deciding_votes_per_block([10, 15, 9, 4, 4, 8, 12, 8]), [40, 70, 40, 20, 20, 34, 50, 34])
tc.assertEqual(deciding_votes_per_block([17, 10, 9, 9, 10, 10, 7, 12, 17, 13, 14, 9, 16, 16, 5]), 
               [5112, 3040, 2750, 2750, 3040, 3040, 2172, 3578, 5112, 3886, 4200, 2750, 4792, 4792, 1626])

