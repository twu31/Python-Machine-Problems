
# coding: utf-8

# # Circular, Array-backed Queue

# ## Overview
# 
# For this assignment you will implement a circular, array-backed queue data structure.
# 
# In the following class, which you are to complete, the backing array will be created and populated with `None`s in the `__init__` method, and the `head` and `tail` indexes set to sentinel values (you shouldn't need to modify `__init__`). Enqueueing and Dequeueing items will take place at the tail and head, with `tail` and `head` tracking the position of the most recently enqueued item and that of the next item to dequeue, respectively. To simplify testing, your implementation should make sure that when dequeuing an item its slot in the array is reset to `None`, and when the queue is emptied its `head` and `tail` attributes should be set to `-1`.
# 
# Because of the fixed size backing array, the `enqueue` operation is defined to raise a `RuntimeError` when the queue is full — the same exception should be raised when `dequeue` is called on an empty queue.
# 
# Finally, the `resize` method will allow the array underlying the queue to be increased in size. It is up to you how to implement this (you can either leave the elements in their current positions, though this may require "unwrapping" elements, or you can simply move all elements towards the front of the array). You may assume that `resize` will only be called with a value greater than the current length of the underlying array.

# In[383]:

class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1
        
        
    def enqueue(self, val):
        if self.tail == -1 and self.head ==-1:
            self.tail = 0
            self.head = 0
            self.data[self.tail] = val
        elif self.head == (self.tail + 1)%len(self.data):
            raise RuntimeError
        else:
            self.tail = (self.tail + 1) % len(self.data)
            self.data[self.tail] = val
        
    def dequeue(self):
        if self.head == -1 and self.tail == -1:
            raise RuntimeError
        
        else:
            x = self.data[self.head]
            if self.head == self.tail:
                self.head =-1
                self.tail =-1
            else:
                self.data[self.head]=None
                self.head = (self.head + 1 ) % len(self.data)
            return x
    
    def resize(self, newsize):
        assert(len(self.data) < newsize)
        newarray =[None]*newsize 
        x = len(self.data)
        for i in range(len(self.data)):
            newarray[i]=self.dequeue()
        self.data = newarray
        self.head = 0
        self.tail = x+newsize-1
    
    def empty(self):
        if self.head == -1 and self.tail==-1:
            return True
        else:
            return False
    
    def __bool__(self):
        return not self.empty()
    
    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        count = 0
        while not self.tail:
            yield self.data[count]
            count+=1


# In[384]:

from unittest import TestCase
tc = TestCase()

q = Queue(5)
tc.assertEqual(q.data, [None] * 5)

for i in range(5):
    q.enqueue(i)
    
with tc.assertRaises(RuntimeError):
    q.enqueue(5)

for i in range(5):
    tc.assertEqual(q.dequeue(), i)
    
tc.assertTrue(q.empty())


# In[385]:

from unittest import TestCase
tc = TestCase()

q = Queue(10)

for i in range(6):
    q.enqueue(i)
    
tc.assertEqual(q.data.count(None), 4)

for i in range(5):
    q.dequeue()
    
tc.assertFalse(q.empty())
tc.assertEqual(q.data.count(None), 9)
tc.assertEqual(q.head, q.tail)
tc.assertEqual(q.head, 5)

for i in range(9):
    q.enqueue(i)

with tc.assertRaises(RuntimeError):
    q.enqueue(10)

for x, y in zip(q, [5] + list(range(9))):
    tc.assertEqual(x, y)
    
tc.assertEqual(q.dequeue(), 5)
for i in range(9):
    tc.assertEqual(q.dequeue(), i)

tc.assertTrue(q.empty())


# In[386]:

from unittest import TestCase
tc = TestCase()

q = Queue(5)
for i in range(5):
    q.enqueue(i)
for i in range(4):
    q.dequeue()
for i in range(5, 9):
    q.enqueue(i)
    
with tc.assertRaises(RuntimeError):
    q.enqueue(10)

q.resize(10)

for x, y in zip(q, range(4, 9)):
    tc.assertEqual(x, y)
    
for i in range(9, 14):
    q.enqueue(i)

for i in range(4, 14):
    tc.assertEqual(q.dequeue(), i)
    
tc.assertTrue(q.empty())
tc.assertEqual(q.head, -1)

