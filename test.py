
# def convertToCNF(fomula):

#     if len(formula)==1:
#         return formula

#     A=""
#     B=""

#     # if formula is of the form A & B


from sympy import *

a = 10
b = 2
c = 3
tmp = True
tmp = tmp & (symbols(str(b)) >> ~symbols(str(a)))
tmp = tmp & (symbols(str(a)) >> symbols(str(b)))
print(to_cnf((tmp)))

cnf = to_cnf((tmp))
cnf = str(cnf)
clauses = []
temp = []
sign = 1
cnf = cnf.split(' & ')
# for l in cnf:
#     if l == ' ' or l == '|' or l == '(' or l == ')':
#         continue
#     elif l == '&':
#         clauses.append(temp[:])
#         temp.clear()
#     elif l == '~':
#         sign = -1
#     else:
#         temp.append(sign*int(l))
#         sign = 1

for l in cnf:
    l = l.strip('(')
    l = l.strip(')')
    l = l.split(' | ')
    for lit in l:
        if lit[0] == '~':
            temp.append(-int(lit[1:]))
        else:
            temp.append(int(lit))
    clauses.append(temp[:])
    temp.clear()


print(clauses)
