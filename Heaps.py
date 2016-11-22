
# coding: utf-8

# # Heaps

# ## Overview
# 
# For this assignment you will update the heap data structure implemented in class so that it accepts a `key` function in its initializer, which will allow the contents of the heap to be maintained using an arbitrary priority (as dictated by the key extracted by said function).
# 
# See the naive implementation of a priority queue in the [lecture notes](https://braeburn.cs.iit.edu/jupyter/user/lee/notebooks/cs331/source/Lectures/priority-queues.ipynb#2.-Naive-implementation) (and the following examples) for details on how such a `key` function might be used. Your changes to the `Heap` class will need to be more extensive, however, than those found in the naive priority queue, as we are not using a built-in `sort` (which already takes a `key` function). 
# 
# Just as with the naive priority queue, the default `key` function should simply sort on the value of the elements themselves — such a default value has already been inserted for you into the `__init__` parameter list. You will, at the very least, need to update the `_heapify` and `add` methods, below, to complete this assignment.

# In[37]:

class Heap:
    def __init__(self, key=lambda x:x):
        self.data = []
        self.key  = key

    @staticmethod
    def _parent(idx):
        return (idx-1)//2
        
    @staticmethod
    def _left(idx):
        return idx*2+1

    @staticmethod
    def _right(idx):
        return idx*2+2
    
    def _heapify(self, idx=0):
        while True:
            l = Heap._left(idx)
            r = Heap._right(idx)
            maxidx = idx
            if l < len(self) and self.key(self.data[l]) > self.key(self.data[idx]):
                maxidx = l
            if r < len(self) and self.key(self.data[r]) > self.key(self.data[maxidx]):
                maxidx = r
            if maxidx != idx:
                self.data[idx], self.data[maxidx] = self.data[maxidx], self.data[idx]
                idx = maxidx
            else:
                break
            
    def add(self, x):
        self.data.append(x)
        i = len(self.data) - 1
        p = Heap._parent(i)
        while i > 0 and self.key(self.data[p]) < self.key(self.data[i]):
            self.data[p], self.data[i] = self.data[i], self.data[p]
            i = p
            p = Heap._parent(i)
        
    def max(self):
        return self.data[0]

    def pop_max(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data)-1]
        del self.data[len(self.data)-1]
        self._heapify()
        return ret
    
    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)


# In[38]:

from unittest import TestCase
import random

tc = TestCase()
h = Heap()

random.seed(0)
for _ in range(10):
    h.add(random.randrange(100))

tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])


# In[39]:

from unittest import TestCase
import random

tc = TestCase()
h = Heap(lambda x:-x)

random.seed(0)
for _ in range(10):
    h.add(random.randrange(100))

tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])


# In[40]:

from unittest import TestCase
import random

tc = TestCase()
h = Heap(lambda s:len(s))

h.add('hello')
h.add('hi')
h.add('abracadabra')
h.add('supercalifragilisticexpialidocious')
h.add('0')

tc.assertEqual(h.data,
              ['supercalifragilisticexpialidocious', 'abracadabra', 'hello', 'hi', '0'])


# In[41]:

from unittest import TestCase
import random

tc = TestCase()
h = Heap()

random.seed(0)
lst = list(range(-1000, 1000))
random.shuffle(lst)

for x in lst:
    h.add(x)

for x in range(999, -1000, -1):
    tc.assertEqual(x, h.pop_max())


# In[42]:

from unittest import TestCase
import random

tc = TestCase()
h = Heap(key=lambda x:abs(x))

random.seed(0)
lst = list(range(-1000, 1000, 3))
random.shuffle(lst)

for x in lst:
    h.add(x)

for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x:abs(x))):
    tc.assertEqual(x, h.pop_max())

