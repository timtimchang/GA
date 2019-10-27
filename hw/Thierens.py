from GA import GA 
import random
import math

class T_model(GA):
    def __init__(self, length = 3, population = 10, ell = 0):
        GA().__init__( length)
        self.length = length
        self.max = 2 ** length 
        self.min = 0
        self.ell = ell

        # for the population and chromosome
        self.population = population
        self.pop_float = float(population)
        self.chromosome = []
        for i in range( int(self.population) ):
            chrom = self.d2b( random.randint(0, self.max - 1) )
            self.chromosome.append(chrom)

    def one_max(self, bin):
        fitness = 0
        
        for i in range(len(bin) ):
            if bin[i] == '1' or bin[i] == 1 : fitness += 1

        return fitness


    def XO(self, display = False ):
        idx = random.randint(0, self.length - 1)
        if display :
            print("select idx:", idx)
            print(self.chromosome)
        
        idx_bit_list = []
        for i in range( int(self.population)):
            idx_bit_list.append(self.chromosome[i][idx])
        
        random.shuffle(idx_bit_list)
        for i in range( int(self.population) ):
            self.chromosome[i][idx] = idx_bit_list[i]
 
        if display: print(self.chromosome)

    def selection(self, s = 2):
        iter = int(self.pop_float // s)

        sel_idx =  [ i for i in range(int(self.population))] 
        random.shuffle(sel_idx )

        sel_chrom = []
        for i in range(0,iter):
            chrom1 = self.chromosome[sel_idx[i * 2]]
            chrom2 = self.chromosome[sel_idx[i * 2 + 1]]

            fit1 = self.one_max(chrom1)
            fit2 = self.one_max(chrom2)

            if chrom1 > chrom2 :
                sel_chrom.append(chrom1)
            else:
                sel_chrom.append(chrom2)

        chromosome = sel_chrom + sel_chrom
        if len(self.chromosome) % 2 == 1 : chromosome.append( self.chromosome[ sel_idx[-1] ] )

        self.chromosome = chromosome

        #print(self.chromosome      ) 

    def problem_size(self):
        count = 0
        if len(self.chromosome) != self.population : print(len(self.chromosome), self.population) 

        for i in range( self.population ):
            if self.chromosome[i] == ['1']*self.length or self.chromosome[i] == [1]*self.length :
                count += 1

        return count

    def run(self, iter = 30):
        ps_list = []
        for i in range(iter):
            self.XO()
            self.selection()
            ps_list.append( self.problem_size() )

        print "ell ", int(self.ell) 
        print "  problem size list ", list(ps_list)


if __name__ == "__main__" :
    print("Run Thierens...")

    for i in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500] :
        GA_ = T_model(population = int(4 * i * math.log(i)), ell = i ) # 4 * ell * log(ell)
        GA_.run()

