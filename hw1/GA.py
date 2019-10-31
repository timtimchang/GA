import numpy as np 
import random 
from itertools import chain, combinations
import copy

class GA:
    def __init__(self, length = 3, rank = False):
        self.length = length
        self.max = 2 ** length 
        self.min = 0

        self.fit = []
        self.best_fit = 0
        self.arg_best_fit = []
        if rank == True : self.rank_fit()

    def rank_fit(self):
        self.fit = list(range( self.max))
        random.shuffle(self.fit)
        self.best_fit = max(self.fit)
        self.arg_best_fit = int( max(range(len(self.fit)), key= self.fit.__getitem__ ))

    def f(self, x):
        if x < self.min or x > self.max :
            return nan

        return self.fit[x]

    def printf(self):
        print("fitness:")
        for i in range(self.max ):
            print("  f{} = {}".format(self.d2b(i), self.fit[i]) ) 
            #print("  f({:0>4b}) = {:5.0f}".format(i, self.fit[i]) )

    def d2b(self, dec):
        #print("  d2b:",dec)
        if not type(dec) == int :
            dec = int(dec)

        bin_format = '{:0>' + str(self.length) +'b}'
        bin = [int(i) for i in list( bin_format.format(dec ))]
        
        return bin

    def b2d(self, bin):
        length = len(bin)
        dec = 0
        for i in range(len(bin)):
            if bin[i] == 1:
                dec += 2 ** (length - i - 1)
            if bin[i] == '1':
                dec += 2 ** (length - i - 1)

        return int(dec)

    def powerset(self, iterable):
        """
        ps = []
        x = len(s)
        for i in range(1 << x):
            ps.append( [int(s[j]) for j in range(x) if (i & (1 << j))] )
        return ps 
        """
        s = list(iterable)
        ps =  [i for i in chain.from_iterable(combinations(s, r) for r in range(len(s)+1))] 
        #print("ps",ps)

        return ps 


    def all_set(self, chrom):
        #print("chrom",chrom)
        idx = [ i for i in range(len(chrom)) if chrom[i] == '*' ]
        if len(idx) > 1 :
            enum = [ self.d2b(i)[len(chrom) - len(idx):] for i in range(len(idx)**2) ]
            iter = len(enum)
        else:
            enum = [[0], [1]]
            iter = 2
        #print(enum)
        #print(idx)

        set = []
        for i in range(iter):
            count = 0
            temp = []
            for j in range(len(chrom)) :
                if j in idx : 
                    temp.append(str(enum[i][count]))
                    count += 1
                else:
                    temp.append(chrom[j])
            set.append(temp)

        #print(set)
        return set

    def refit(self):
        self.fit = list(range( self.max))
        random.shuffle(self.fit)
        self.best_fit = max(self.fit)
        self.arg_best_fit = int( max(range(len(self.fit)), key= self.fit.__getitem__ ))


if __name__ == "__main__" :
    print("this is the main of GA")

