from pysat.solvers import Glucose3
import copy

g = Glucose3()
# clauses corresponding to (~a or b) and (~a or c) and (a or b or d) and ~d and ~b
# The above sentence is not satisfiable. If you remove ~b, then it becomes satisfiable.
p = [[-16, 4, 1], [-4, 16], [-1, 16],  [-16]]
l = copy.deepcopy(p)

# g.add_clause([-16, 4, 1])
# g.add_clause([-4, 16])
# g.add_clause([-1, 16])
# g.add_clause([-16])
# g.add_clause([4])

for c in l:
    g.add_clause(c)
print(g.solve())
print(g.get_model())
