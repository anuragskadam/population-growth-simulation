# Population Evolution Simulation  

(This is my attempt at simulating evolution by natural selection.)  
  
In his book Origin of Species, Charles Darwin proposed the idea of evolution of species using natural selection. This was a revolutionary idea in our understanding of origin and evolution of life on this planet. He proposed that species evolve over time due to random mutations in the genetic code of organisms in an ecosystem. These traits are selected for by nature if they have a survival and/or reproductive advantage over the others.  
Now, in order to model this simulated ecosystem we have added random mutations which may give individuals a higher (or lower) chance of survival. Survival advantages include speed of individuals, visibility to the predator (eg. a prey that is better able to camoflage in its environment is less likely to be eaten than the ones more visible), etc.  
  
Predators eating preys, and reproduction of individuals are controlled by random variables. Since population size grows and falls stochastically, this model resembles a random walk in n dimensions (n being the number of species in the ecosystem).  
A random walk in one dimension may be a drunk person taking a step forward or backward with certain probability at each time step. If we run this drunk simulation very many times (yes "very many" is an actual technical term), the distribution of the final position fits a Gaussian curve.  
  
![image](https://user-images.githubusercontent.com/83920669/233838587-97bf53e1-8a76-4f03-885d-67063a172241.png)  
  
What you see above are the resultant plots after running the simulation 6000 times. It's apparent that the distribution of final populations of species closely fits a Gaussian curve like a n-D random walk.  
  
However, we noticed that the genetic changes that occur due to natural selection have not been prominent as they require us to run the simulation over a much longer duration than our computational limitations permit (evolution is a slow process). This can be rectified in the future to observe the desired results.
