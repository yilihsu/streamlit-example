import re
from collections import Counter
import pandas as pd
from tqdm import tqdm
def words(text): return re.findall(r'\w+', text.lower())
df = pd.read_csv("unigram_freq.csv")

WORDS = word_count = Counter(words(open('big.txt').read())) + Counter(words(open('all_words.txt').read()))
N = sum(word_count.values())

letters    = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    dup = [word.replace("r","rr"), word.replace("d","dd"), word.replace("s","ss"), word.replace("r","rr").replace("s","ss") , word.replace("s","ss").replace("d", "dd")]
    return set(deletes + transposes + replaces + inserts + dup)# + inserts2 + inserts3)#, word) #transposes2 + transposes3 + transposes4 + transposes5+ transposes6 + replaces + inserts), word)


def correction(word): 
    return max(candidates(word), key=P)


def candidates(word): 
    if len(known(edits1(word)))>0:
        return known(edits1(word))
    elif len(known(edits2(word)))>0:
        return known(edits2(word))
    else:
        return [word]

def in_unigramdf(word):
    if word in df['word'].unique():
        return [word]
    else:
        return []
    
def known(words): 
    return set(w for w in words if w in word_count)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correct_text(text):
    "Correct all the words within a text, returning the corrected text."
    return re.sub('[a-zA-Z]+', correct_match, text)

def correct_match(match):
    "Spell-correct word in match, and preserve proper upper/lower/title case."
    word = match.group()
    return case_of(word)(correction(word.lower()))

def case_of(text):
    "Return the case-function appropriate for text: upper, lower, title, or just str."
    return (str.upper if text.isupper() else
            str.lower if text.islower() else
            str.title if text.istitle() else
            str)

print('Speling -->', correct_text('Speling'))
# speling spelling
    
    
def P(word): 
    try:
        return 0.8*(word_count[word] / N) + 0.2*int(df[df['word'] == word]['count'])/df['count'].sum() # float
    except:
        return (word_count[word] / N) # float

def spelltest(tests, verbose=True):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.time()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tqdm(tests):
        w = correct_text(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w.lower()], right, WORDS[right.lower()]))
                #print(candidates(wrong))
    dt = time.time() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

#print(unit_tests())
spelltest(Testset(open('spell-testset2.txt'))) # Development set

