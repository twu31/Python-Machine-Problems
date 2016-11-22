
# coding: utf-8

# # Hashtable
# 
# ## Overview
# 
# For this assignment you will complete the implementation of a hashtable data structure, which exposes an API mirroring that of the built-in Python `dict`.
# 
# A hashtable is conceptually a two-tiered data structure, where keys are initially mapped — via their hash values — to slots in a "buckets" array, each of which in turn contain singly-linked (non-circular) lists of key/value pairs (known as "chains"). The hope is that by keeping the number of collisions — i.e., instances where keys map to the same bucket — low, key-based lookups can be performed very quickly. The essential operations on a hashtable `h` are listed alongside their behavior/mechanics below:
# 
# | Operation | Description |
# |-----------|-------------|
# | `h[k]`&nbsp;`=`&nbsp;`v` | The key `k`'s hash value is used to locate the appropriate slot in the array of buckets. If the bucket entry is `None`, a new linked list is created with `k` & `v` as the first entry and the head of the list is placed in the bucket. Otherwise, the list is searched for a node containing key `k`; if found the node's value will be updated with `v`, else a new node containing key `k` & value `v` is appended to the list. Note that this implies a given key has a unique mapping in a hashtable. |
# | `h[k]`    | The key `k`'s hash value is used to locate the appropriate slot in the array of buckets. If the bucket entry is not `None`, the linked list at that location is searched for a node containing `k`; if found, the corresponding value is returned. If the bucket is empty or the list does not contain a node with key `k`, a `KeyError` is raised. |
# | `del`&nbsp;`h[k]` | The key `k`'s hash value is used to locate the appropriate slot in the array of buckets. If the bucket entry is not `None`, the linked list in the bucket is searched for a node with key `k`; if found, it is deleted. If either the bucket is empty or the list doesn't contain key `k`, a `KeyError` is raised. |
# | `k`&nbsp;`in`&nbsp;`h` | Returns `True` if key `k` is found in a list in the appropriate bucket. |
# | `len(h)` | Returns the number of keys stored across all buckets. |
# | `iter(h)` | Returns an iterator over all the keys in the hashtable. |
# | `h.keys()` | Returns an iterator over all the keys in the hashtable (the same as above). |
# | `h.values()` | Returns an iterator over all the values in the hashtable. |
# | `h.items()` | Returns an iterator over all the key/value pairs (as tuples) in the hashtable. |
# | `h.setdefault(key, default)` | If `key` is in the dictionary, return its value. If not, insert key with a value of `default` and return `default`. `default` defaults to `None`. |
# 
# Your hashtable will be provided with the initial number of buckets on creation (i.e., in `__init__`), which will be used to create an array with that size (where each slot contains `None`). Because the hash value of a given key can exceed the number of buckets, hash values will be mapped to buckets using the modulus operator; i.e., `hash(k) % len(self.buckets)` will return the index of the appropriate bucket for key `k`.
# 
# For testing purposes, the `avg_chain_length` method is provided, which returns the average length of the chains stored across all non-empty buckets. You may want to look over its implementation to get a sense of how the buckets and lists they contain might be navigated.

# In[3]:

class Hashtable:
    class Node:
        """Instances of this class will be used to construct the linked lists (chains)
        found in non-empty hashtable buckets."""
        def __init__(self, key, val, next=None):
            self.key = key
            self.val = val
            self.next = next

    def __init__(self, n_buckets=1000):
        self.buckets = [None] * n_buckets # initially empty buckets array
        self.count = 0
    
    def __getitem__(self, key):
        bucket_idx = hash(key) % len(self.buckets)
        n = self.buckets[bucket_idx]
        while n:
            if n.key == key:
                return n.val
            n = n.next
        raise KeyError
    
    def __setitem__(self, key, val):
        bucket_idx = hash(key) % len(self.buckets)
        self.buckets[bucket_idx] = Hashtable.Node(key, val, next = self.buckets[bucket_idx])
        self.count +=1
    
    def __delitem__(self, key):
        bucket_idx = hash(key) % len(self.buckets)
        n= self.buckets[bucket_idx]
        counter=0
        if n.key==key:
            self.buckets[bucket_idx]=n.next
            counter=counter+1
        if n !=None:
            while n:
                if n.next==None:
                    if n.key==key:
                        n=None
                        counter=counter+1
                    break
                if n.next.key==key:
                    n.next=n.next.next
                    counter=counter+1
                n=n.next
        self.count -=1
        if counter==0: 
            raise KeyError
                
    def __contains__(self, key):
        try:
            _ = key
            return True
            
        except:
            return False
        
        """bucket_idx = hash(key) % len(self.buckets)
        n = self.buckets[bucket_idx]
        while n:
            if n.key == key:
                return True
            n = n.next
        return False"""
        
    def __len__(self):
        return self.count
    
    def __iter__(self):
        for b in self.buckets:
            if not b:
                b.next
            else:
                while b:
                    yield (b.key, b.val)
                    b = b.next
                    
    def keys(self):
        return iter(self)

    def values(self):
        for b in self.buckets:
            if not b:
                next
            else:
                while b:
                    yield( b.val)
                    b = b.next

    def items(self):
        for b in self.buckets:
            if not b:
                next
            else: 
                while b:
                    yield(b.key, b.val)
                    b = b.next
        
    def setdefault(self, key, default=None):
        bucket_idx = hash(key) % len(self.buckets)
        n = self.buckets[bucket_idx]
        while n:
            if n.key == key:
                return n.val
            n=n.next
        self.buckets[bucket_idx] = Hashtable.Node(key, default, self.buckets[bucket_idx])
        self.count = self.count + 1 
        return default


# In[4]:

from unittest import TestCase
import random

tc = TestCase()

class MyInt(int):
    def __hash__(self):
        """MyInts hash to themselves — already current Python default, 
        but just to ensure consistency."""
        return self
    
def ll_len(l):
    """Returns the length of a linked list with head `l` (assuming no sentinel)"""
    c = 0
    while l:
        c += 1
        l = l.next
    return c
    
ht = Hashtable(10)
for i in range(25):
    ht[MyInt(i)] = i*2

tc.assertEqual(len(ht), 25)

for i in range(5):
    tc.assertEqual(ll_len(ht.buckets[i]), 3)
    
for i in range(5, 10):
    tc.assertEqual(ll_len(ht.buckets[i]), 2)

for i in range(25):
    tc.assertTrue(MyInt(i) in ht)
    tc.assertEqual(ht[MyInt(i)], i*2)


# In[5]:

# iterator testing
from unittest import TestCase
import random

tc = TestCase()

ht = Hashtable(100)
d = {}

for i in range(100):
    k, v = str(i), str(random.randrange(10000000, 99999999))
    d[k] = v
    ht[k] = v
    
keys = set(ht.keys())
tc.assertEqual(len(keys), 100)
for k in keys:
    tc.assertTrue(k in ht)
    tc.assertEqual(ht[k], d[k])

tc.assertEqual(sorted(ht.values()), sorted(d.values()))

for k,v in ht.items():
    tc.assertEqual(d[k], v)


# In[6]:

# deletion testing
from unittest import TestCase
import random

tc = TestCase()

ht = Hashtable(100)
d = {}

for i in range(100):
    k, v = str(i), str(random.randrange(10000000, 99999999))
    d[k] = v
    ht[k] = v

for _ in range(50):
    k = str(random.randrange(100))
    if k in d:
        del d[k]
        del ht[k]

tc.assertEqual(len(ht), len(d))

for k,v in ht.items():
    tc.assertEqual(d[k], v)


# In[7]:

# setdefault testing
from unittest import TestCase
import random

tc = TestCase()

ht = Hashtable(100)
d = {}

tc.assertEqual(ht.setdefault('1', '2'), '2')
ht['3'] = '4'
tc.assertEqual(ht.setdefault('3', '5'), '4')
del ht['3']
tc.assertEqual(ht.setdefault('3', '6'), '6')
tc.assertEqual(ht.setdefault('7'), None)
ht['7'] = '8'
tc.assertEqual(ht.setdefault('7'), '8')


# In[8]:

# stress testing

from unittest import TestCase
import random

tc = TestCase()

ht = Hashtable(100000)
d = {}

for _ in range(100000):
    k, v = str(random.randrange(100000)), str(random.randrange(10000000, 99999999))
    d[k] = v
    ht[k] = v
    
for k,v in d.items():
    tc.assertTrue(k in ht)
    tc.assertEqual(d[k], ht[k])

