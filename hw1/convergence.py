from GA import GA 
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class T_model(GA):
    def __init__(self, ell = 30):
        GA().__init__(ell)
        self.length = ell
        self.ell = ell
        self.max = 2 ** ell - 1
        
        # for the population and chromosome
        self.population = int( 4 * ell * math.log(ell) )
        self.chromosome = []
        self.re_new()

    def re_new(self):
        self.chromosome = []
        for i in range( self.population ):
            chrom = self.d2b( random.randint(0, self.max) )
            self.chromosome.append(chrom)

    def one_max(self, bin):
        fitness = 0
        
        for i in range(len(bin) ):
            if bin[i] == '1' or bin[i] == 1 : fitness += 1

        return fitness

    def op_XO(self, display = False):
        chromosome = [ i[:] for i in self.chromosome ]

        sel_idx =  [ i for i in range(len(chromosome))] 
        random.shuffle(sel_idx )
        
        for i in range(0,len(chromosome) - 1,2):
            #print(i, self.population)
            chrom1 = chromosome[sel_idx[i]]
            chrom2 = chromosome[sel_idx[i + 1]]

            idx = random.randint(1, self.length - 1)
            temp = chrom1[idx:]
            chrom1 = chrom1[:idx] + chrom2[idx:]
            chrom2 = chrom2[:idx] + temp

            chromosome[sel_idx[i]] = chrom1
            chromosome[sel_idx[i+1]] = chrom2

        self.chromosome = chromosome[:]
        #if display : print(chromosome)

    def u_XO(self, display = False):
        chromosome = [ i[:] for i in self.chromosome ]

        sel_idx =  [ i for i in range(len(chromosome))] 
        random.shuffle(sel_idx )

        for i in range(0,len(chromosome) - 1,2):
            #print(i, self.population)
            chrom1 = chromosome[sel_idx[i]]
            chrom2 = chromosome[sel_idx[i + 1]]

            num = random.randint(1, self.length - 1)
            idx = random.sample(range(self.length), num)
            for i in idx:
                temp = chrom1[i]
                chrom1[i] = chrom2[i]
                chrom2[i] = temp

            chromosome[sel_idx[i]] = chrom1[:]
            chromosome[sel_idx[i+1]] = chrom2[:]

        self.chromosome = chromosome[:]
        #if display : print(chromosome)

    def pw_XO(self, display = False ):
        #idx = random.randint(0, self.length - 1)
        idx_set = [ i for i in range(self.length)]
        chromosome = [ i[:] for i in self.chromosome ]

        for idx in idx_set:

            idx_bit_list = []
            for i in range( int(self.population)):
                idx_bit_list.append(chromosome[i][idx])

            random.shuffle(idx_bit_list)
            for i in range( int(self.population) ):
                chromosome[i][idx] = idx_bit_list[i]
                #chromosome[i][idx] = i 
                #print chromosome
        
        self.chromosome = chromosome[:]

    def tour_select(self, s = 2):
        chromosome = self.chromosome[:]
        sel_chrom = []

        for j in range(0,s):
            sel_idx =  [ i for i in range(len(chromosome))] 
            random.shuffle(sel_idx )

            for i in range(0,len(chromosome)-1,s):
                #print(i, self.population)
                chrom1 = chromosome[sel_idx[i]]
                chrom2 = chromosome[sel_idx[i + 1]]

                fit1 = self.one_max(chrom1)
                fit2 = self.one_max(chrom2)

                if fit1 > fit2 :
                    sel_chrom.append(chrom1)
                else:
                    sel_chrom.append(chrom2)
            
            if len(chromosome) % len(sel_chrom) != 0 : chromosome.append(chromosome[sel_idx[-1]]) 
    
        self.chromosome = sel_chrom[:]
        #print(self.chromosome)

    def trun_select(self, s = 2):
        iter = self.population

        fit_list = []
        for i in range(iter):
            fit = self.one_max( self.chromosome[i])
            fit_list.append(fit)
        
        fit_arr = np.array(fit_list)
        sort_list = np.argsort(fit_arr)[::-1]
        chromosome = [ self.chromosome[i] for i in sort_list]

        self.chromosome = chromosome[0: len(chromosome)//2] * 2
        if self.population != len(self.chromosome) : self.chromosome.append( chromosome[len(chromosome)//2 + 1])


    def convergence_rate(self):
        count = 0

        if len(self.chromosome) != self.population : print("chromosome size:",len(self.chromosome),"population size:", self.population) 
        for i in range( self.population ):
            #print self.chromosome[i]
            if self.chromosome[i] == ['1']*self.length or self.chromosome[i] == [1]*self.length :
                count += 1

        #print count
        #print self.population

        return count/float(self.population)

    def run(self, iter = int(1e6), display = False, XO = 'op'):
        print "ell ", int(self.ell) 
        print "population:", self.population
        print "cross over:", XO
        cr_iter = []
        test_num = 30
        
        for j in range(test_num):
            self.re_new()
            for i in range(iter):
                self.tour_select()
                if XO == 'op' :self.op_XO(display = display)
                if XO == 'u' :self.u_XO(display = display)
                if XO == 'pw' :self.pw_XO(display = display)
                
                cr = self.convergence_rate()
                if display : print "  iter",i,"convergence rate {:.4f}".format(cr)
                if cr == 1 : 
                    cr_iter.append(i)
                    break

        #print cr_iter
        a_cr_iter = sum(cr_iter)/ float(test_num)
        print "avg. convergence iter: {:.4f}".format( a_cr_iter)

        return a_cr_iter


if __name__ == "__main__" :
    print("Run convergence...")

    ell_set = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500] 

    print ""
    op_list = []
    for i in ell_set : 
        GA_ = T_model(ell = i ) # population size =  4 * ell * log(ell)
        cr = GA_.run(display = False, XO = 'op')
        op_list.append(cr)
        print ""

    print ""
    u_list = []
    for i in ell_set : 
        GA_ = T_model(ell = i ) # population size =  4 * ell * log(ell)
        cr = GA_.run(display = False, XO = 'u')
        u_list.append(cr)
        print ""

    print ""
    pw_list = []
    for i in ell_set : 
        GA_ = T_model(ell = i ) # population size =  4 * ell * log(ell)
        cr = GA_.run(display = False, XO = 'pw')
        pw_list.append(cr)
        print ""

    # for ploting
    plt.xlabel('ell')
    plt.ylabel('convergence time')
    plt.title('Experiment of three XO with a SGA on the OneMplt problem')
    plt.xlim((ell_set[0], ell_set[-1]))
    plt.ylim((0,500))

    plt.plot(ell_set, op_list, label='one point XO')
    plt.plot(ell_set, u_list, label='uniform XO')
    plt.plot(ell_set, pw_list, label='population wise XO')

    plt.legend()
    plt.savefig("./result/convergence.png")
    plt.show()
