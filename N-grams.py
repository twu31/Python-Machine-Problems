

ROMEO_SOLILOQUY = """
        But, soft! what light through yonder window breaks?
        It is the east, and Juliet is the sun.
        Arise, fair sun, and kill the envious moon,
        who is already sick and pale with grief, 
        That thou her maid art far more fair than she:
        be not her maid, since she is envious;
        her vestal livery is but sick and green
        and none but fools do wear it; cast it off.
        It is my lady, O, it is my love! 
        O, that she knew she were!
        She speaks yet she says nothing: what of that?
        Her eye discourses; I will answer it.
        I am too bold, 'tis not to me she speaks:
        two of the fairest stars in all the heaven, 
        having some business, do entreat her eyes
        to twinkle in their spheres till they return.
        What if her eyes were there, they in her head?
        The brightness of her cheek would shame those stars,
        as daylight doth a lamp; her eyes in heaven 
        would through the airy region stream so bright
        that birds would sing and think it were not night.
        See, how she leans her cheek upon her hand!
        O, that I were a glove upon that hand,
        that I might touch that cheek!"""


# Using the string's built-in `split` method --- previously mentioned in class --- along with `lower`, we can derive from the passage a list of tokens.

# In[2]:

toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]

toks[:8]


# In[3]:

n=4
for i in range(0, n-2):
    print('ha')


# In[4]:

grams={}
grams[toks[0]]=(toks[1],)
grams[toks[4]]


# We could do more interesting things (such as separating out punctuation), but we'll keep our parser simple. For the sake of consistency, we'll rely on this fairly straighttforward approach to parsing. Onwards!
# 
# ### `compute_ngrams`
# 
# Your first task is to write `compute_ngrams`, which will take a list of tokens, a value `n` indicating the n-gram length (e.g., 3 for 3-grams), and return an n-gram dictionary. The keys in the returned dictionary should all be strings, whose values will be lists of one or more tuples. Note that even in the case of `n`=2 (which would be the minimum value) the dictionary should map strings to lists of 1-tuples (i.e., instead of to lists of individual tokens).

# In[5]:

def compute_ngrams(toks, n=2):
    """Returns an n-gram dictionary based on the provided list of tokens."""
    ngrams={}
    tup=()
    t=len(toks)
    y=1
    m=n
    
    for x in range(0,t-n+1):
        tup=(toks[x+1],)
        y=x
        for i in range(0, m-2):
            y+=1
            tup= tup + (toks[y+1],)
            
        ngrams.setdefault(toks[x], [])
        ngrams[toks[x]].append(tup)
      
    #print(ngrams)
    return ngrams
    


# And now for some simple tests:

# In[6]:

from unittest import TestCase
tc = TestCase()

simple_toks = [t.lower() for t in 'I really really like cake.'.split()]

compute_ngrams(simple_toks)
tc.assertEqual(compute_ngrams(simple_toks), 
               {'i': [('really',)], 'like': [('cake.',)], 'really': [('really',), ('like',)]})
tc.assertEqual(compute_ngrams(simple_toks, n=3), 
               {'i': [('really', 'really')],
                'really': [('really', 'like'), ('like', 'cake.')]})

romeo_toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]

dct = compute_ngrams(romeo_toks, n=4)
tc.assertEqual(dct['but'], [('sick', 'and', 'green'), ('fools', 'do', 'wear')])
tc.assertEqual(dct['it'], 
              [('is', 'the', 'east,'),
               ('off.', 'it', 'is'),
               ('is', 'my', 'lady,'),
               ('is', 'my', 'love!'),
               ('were', 'not', 'night.')])


# I've also placed the entire text of Peter Pan (courtesy of [Project Gutenberg][]) on the server, to be used to stress test your function just a bit. The following code reads the passage of the file (if you're not working on the course server this won't work for you):
# 
# [Project Gutenberg]: http://gutenberg.org

# In[7]:

PETER_PAN_FILENAME = '/srv/cs331/peterpan.txt'

with open(PETER_PAN_FILENAME) as infile:
    pp_text = infile.read()
    
print(pp_text[1361:1949])


# Time for some larger test cases!

# In[8]:

tc = TestCase()

pp_toks = [t.lower() for t in pp_text.split()]
dct = compute_ngrams(pp_toks, n=3)
tc.assertEqual(dct['crocodile'], 
               [('passes,', 'but'),
                ('that', 'happened'),
                ('would', 'have'),
                ('was', 'in'),
                ('passed', 'him,'),
                ('is', 'about'),
                ('climbing', 'it.'),
                ('that', 'was'),
                ('pass', 'by'),
                ('and', 'let'),
                ('was', 'among'),
                ('was', 'waiting')])
tc.assertEqual(len(dct['wendy']), 202)
tc.assertEqual(len(dct['peter']), 243)


# ### Random selection

# One more thing before you start work on generating passages from an n-gram dictionary: we need a way to choose a random item from a sequence.
# 
# The [`random.choice` function](https://docs.python.org/3/library/random.html#random.choice) provides just this functionality. Consider (and feel free to play with) the following examples --- you should, at the very least, evaluate the cell a few separate times to see the results:

# In[97]:

import random
print(random.choice(['lions', 'tigers', 'bears']))
print(random.choice(range(100)))
print(random.choice([('really', 'like'), ('like', 'cake')]))


# Note that a separate tutorial on random number generators (and other [`random` module](https://docs.python.org/3/library/random.html) APIs) will be posted separately, but for now just understanding how to use `random.choice` should be sufficient for this assignment.

# ### `gen_passage`
# 
# Finally, you're ready to implement `gen_passage`, which will take an n-gram dictionary and a length for the passage to generate (as a token count). 
# 
# As described earlier, it will work as follows:
# 
# 1. Select a random key from the dictionary and use it as the start token of the passage. It will also serve as the current token for the next step.
# 2. Select a random tuple from the list associated with the current token and append the sequence to the passage. The last token of the selected sequence will be the new current token.
# 3. If the current token is a key in the dictionary then simply repeat step 2, otherwise select another random key from the map as the current token and append it to the passage before repeating step 2.
# 
# You will use `random.choice` whenever a random selection needs to be made. In order for your results to be reproduceable, be sure to sort the dictionary's keys (which, recall, are in no discernible order) before selecting a random one, like this (assuming `ngram_dict` is the dictionary):
# 
#     random.choice(sorted(ngram_dict.keys()))

# In[119]:

def gen_passage(ngram_dict, length=100):
    passage=''
    
    tok1=random.choice(sorted(ngram_dict.keys()))
    tok2=random.choice(ngram_dict.get(tok1))
    passage=''.join(tok1)+' '+''.join(tok2)
    tok3=''.join(tok2[len(tok2)-1])
    #tok4=random.choice(ngram_dict.get(tok3))
    #print(ngram_dict)
    while len(passage.split()) < length:
        if tok3 in ngram_dict:
            #tok4=ngram_dict.get(tok3)
            tok3=random.choice(ngram_dict.get(tok3))
            tok3=''.join(tok3)
            #tok3=random.choice(ngram_dict.get(tok3))
            #print(tok3)
            #if len(tok4)>1:
                #tuplelist=''
                #for _ in range(0, len(tok4)):
                    #tuplelist=tuplelist+''.join(tok4[_])
                #passage=passage+' '+''.join(tok3)+' '+tuplelist
                #tok3=''.join(tok4[len(tok4)-1])
            #else:
            passage=passage+' '+''.join(tok3)
                #tok3=''.join(tok4[len(tok4)-1])
        else:
            tok3 = random.choice(sorted(ngram_dict.keys()))
            passage=passage+' '+''.join(tok3)
    return passage


# For the following test cases to work, it is *critical* that you do not invoke `random.choice` more than is absolutely necessary, and only as prescribed in the steps described above!
# 
# Note that in addition to the automated test cases, we'll also be manually grading your code above.

# In[120]:

tc = TestCase()

random.seed(1234)
simple_toks = [t.lower() for t in 'I really really like cake.'.split()]
tc.assertEqual(gen_passage(compute_ngrams(simple_toks), 10),
               'like cake. i really really really really like cake. i')

random.seed(1234)
romeo_toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]
tc.assertEqual(gen_passage(compute_ngrams(romeo_toks), 10),
               'too bold, \'tis not night. see, how she leans her')

