import numpy as np 
import random 
from itertools import chain, combinations
import copy

class GA:
    def __init__(self, length = 3):
        self.length = length
        self.max = 2 ** length 
        self.min = 0

        # for fit
        self.fit = self.uniform_fit()
        #self.fit = list(range( self.max))
        #random.shuffle(self.fit)
        self.best_fit = max(self.fit)
        self.arg_best_fit = int( max(range(len(self.fit)), key= self.fit.__getitem__ ))
        
    def uniform_fit(self):
        fit_list = []
        for i in range( self.max ):
            fit = random.uniform(0,1)
            fit_list.append(fit)
        
        return fit_list

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

    def deception(self, display = False):
        #print("  abf",self.arg_best_fit)
        best_x = self.d2b( self.arg_best_fit ) 
        best_x = [ 1 - i for i in best_x ] # here best x is the complement of best x 

        s = list(range(self.length))
        idx = self.powerset(s)[1:-1:] # except the [] and [all] 
        #print "idx", idx

        for i in range(len(idx)):
            x_pow = []
            cx_pow = []
            for j in range(self.length):
                if j in idx[i]:
                    x_pow.append(str(best_x[j]))
                    cx_pow.append('#')
                else:
                    x_pow.append('*')
                    cx_pow.append('*')

            x_list = self.all_set(x_pow)            
            cx_pow_ = self.all_set(cx_pow,sym = '#')
            cx_pow_.remove(x_pow)
            cx_list = [ self.all_set(x) for x in cx_pow_ ]                
      
            #print "x_pow", x_pow
            #print "cx_pow", cx_pow_
            #print ""

            x_sum = 0
            cx_sum = [0] * len(cx_list)
            for j in range(len(x_list)):
                x_score = self.f( self.b2d( x_list[j] ))
                x_sum += x_score
                for k in range(len(cx_list)):
                    cx_score = self.f( self.b2d( cx_list[k][j]  ))
                    cx_sum[k] += cx_score
            cx_sum_max = max(cx_sum)

            if cx_sum_max > x_sum : 
                return False
            else:
                if display :
                    print("  x pow", x_pow)
                    print("  cx pow", cx_pow)
                    print("  x list", x_list)
                    print("  cx list", cx_list)
                    print("  x:",x_sum,"cd", cx_sum_max)
                    print()

        return True

    def all_set(self, chrom, sym = "*"):
        #print("chrom",chrom)
        idx = [ i for i in range(len(chrom)) if chrom[i] == sym ]
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

    def deception_test(self, iter = 10e6, display = True): 
        count = 0.0
        
        for i in range(0,int(iter)):
            if display : self.printf()
            if self.deception(display = display) == True : count += 1.0
            self.refit()
            if i % 1e5 == 0 and i != 0: print "complete: {} and the prob is {:.5f}".format(i , count / i)

        return count / iter
    
    def refit(self):
        self.fit = self.uniform_fit()
        self.best_fit = max(self.fit)
        self.arg_best_fit = int( max(range(len(self.fit)), key= self.fit.__getitem__ ))


if __name__ == "__main__" :
    print "Run deception..."

    print "3 genes:"
    GA_thr = GA(3)
    prob = GA_thr.deception_test(iter = 1e6,display=False)
    print("3 deception prob:{:.8f}".format(prob))

    print "4 genes:"
    GA_four = GA(4)
    prob = GA_four.deception_test(iter = 1e6, display=False)
    print("4 deception prob:{:.8f}".format(prob))

