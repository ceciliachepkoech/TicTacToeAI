import random as rnd
import copy
from functools import reduce
import pickle
import time
import numpy as np


class Evo:
    def __init__(self):
        self.pop = {}  # ((ob1, eval1), (obj2, eval2), ...) ==> solution
        self.fitness = {}  # name -> objective func
        self.agents = {}  # name -> (agent operator, # input solutions)

    def size(self):
        """ The size of the solution population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f):
        """ Registering an objective with the Evo framework
        name - The name of the objective (string)
        f    - The objective function:   f(solution)--> a number """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Registering an agent with the Evo framework
        name - The name of the agent
        op   - The operator - the function carried out by the agent  op(*solutions)-> new solution
        k    - the number of input solutions (usually 1) """
        self.agents[name] = (op, k)

    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population as a list of solutions
            We are returning DEEP copies of these solutions as a list """
        if self.size() == 0:  # No solutions in the populations
            return []
        else:
            popvals = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(popvals)) for _ in range(k)]

    def add_solution(self, sol):
        """Add a new solution to the population """
        eval = tuple(
            [(name, f(sol, self.pop.values())) for name, f in self.fitness.items()]
        )
        # print(eval)
        self.pop[eval] = sol

    def run_agent(self, name):
        """ Invoke an agent against the current population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    def evolve(self, n=1, dom=100, status=100, sync=1000, timeout=600):
        """ To run n random agents against the population
        n - # of agent invocations
        dom - # of iterations between discarding the dominated solutions
        status - # iterations between printing current population to the screen
        sync - # iternations between saving population to disk """
        start_time = time.time()

        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rnd.choice(agent_names)  # pick an agent to run
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:  # print the population
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population Size: ", self.size())
                print(self)
                print(f"Time elapsed: {time.time()-start_time}s")

            if i % sync == 0:
                # try:
                #     with open("solutions.dat", "rb") as file:

                #         # load saved population into a dictionary object
                #         loaded = pickle.load(file)

                #         # merge loaded solutions into my population
                #         for eval, sol in loaded.items():
                #             self.pop[eval] = sol
                # except Exception as e:
                #     print(e)

                # remove the dominated solutions
                self.remove_dominated()

                # resave the non-dominated solutions back to the file
                with open(f"solutions-{i}.dat", "wb") as file:
                    pickle.dump(self.pop, file)

            if (timeout and time.time() - start_time) > timeout:
                print(f"Hit time out after {i} iterations")
                break

        # Clean up population
        self.remove_dominated()

    @staticmethod
    def _dominates(p, q):
        # pscores = [score for _, score in p]
        # qscores = [score for _, score in q]
        # score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        # min_diff = min(score_diffs)
        # max_diff = max(score_diffs)
        # return min_diff >= 0.0 and max_diff > 0.0
        return p < q

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        # nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        nds = sorted(self.pop.keys())[:10]
        old_pop = {k: self.pop[k] for k in nds}
        self.pop = {}
        for sol in old_pop.values():
            self.add_solution(sol)

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""

        scores = [x[0][1] for x in self.pop.keys()]
        best = min(scores)
        worst = max(scores)
        rslt += f"best:\t{best}\n"
        rslt += f"worst:\t{worst}\n"

        return rslt
