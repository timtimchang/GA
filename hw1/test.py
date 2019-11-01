import math

s = 2
I = ( 2 * ( math.log(s) - math.log( (4.14*math.log(s))**(1/2) )) )**(1/2)
print  "theoretical value of selection intensity:", I

print "three deception"
for x in range(5,25):
    three_deception = (1 - 0.0057)**( x*(x - 1)*(x-2) / 6)
    print x, three_deception

print "four deception"
for x in range(5,25):
    four_deception = ( 1 - 0.00026 ) ** ( x*(x-1)*(x-2)*(x-3)/24 )
    print x, four_deception

print "intersection"
for x in range(80,100):
    three_deception = (1 - 0.0057)**( x*(x - 1)*(x-2) / 6)
    four_deception = ( 1 - 0.00026 ) ** ( x*(x-1)*(x-2)*(x-3)/24 )
    if three_deception > four_deception : print "intersection !!!!" 

    print x, three_deception - four_deception
