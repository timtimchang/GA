##Genetic Algorithms Assignment #1     
	ID:r07921076 Name:張晏誠 Instructor: Tian-Li Yu

1. (a) It could not happen. Assume $$f(00)$$ is the greatest, the deception occur 	**iff** $$ f(1*)>f(0*) ; f(*1)>f(*0) $$, it means: 

	$$
	\begin{cases}
	  f(11) + f(10) > f(01) + f(00) & (1)  \\
	  f(11) + f(01) > f(10) + f(00) & (2)  
	\end{cases}
	$$

	when $$(1) + (2)$$, the $$f(11)>f(00)$$, but the $$f(00)$$ is the greatest, contridiction.      

	(b) Probability of 3-deception is 0.0057. Implemented by python 3.7.
	
	(c) Probability of 4-deception is 0.0026. Implemented by python 3.7.
	
	(d) continue...
	
2. (a)