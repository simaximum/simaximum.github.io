import re
from collections import Counter

symbols = (
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al',
    'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
    'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr',
    'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
    'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm',
    'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W',
    'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
    'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf',
    'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
    'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo'
)


def _is_balanced(formula):
    """Check if all sort of brackets come in pairs."""
    # Very naive check, just here because you always need some input checking
    c = Counter(formula)
    return c['['] == c[']'] and c['{'] == c['}'] and c['('] == c[')']


def parse_formula(molecule):

    if not _is_balanced(molecule):
        raise ValueError('Unbalanced formula')

    full = []
    last = [Counter()]
    multi = 0
    action = ""

    for token in re.findall('[A-Z][a-z]?|\d+|.', molecule):
        if token in symbols:
            last[-1] = last[-1] + Counter({token})
            action = token
        elif token.isdecimal():
            count = int(token)
            if action.isalpha():
                last[-1][action] = last[-1][action] * count
            elif action in ')]}':
                for element in last[multi-1:]:
                    for k in element:
                        element[k] = element[k] * count
                multi -= 1
        elif token in '([{':
            if multi == 0:
                full.append(last)
                last = [Counter()]
            else:
                last.append(Counter())
            multi += 1
        elif token in ')]}':
            action = token

        else:
            raise ValueError(f'Unrecognized element in formula: {token}')

    full.append(last)
    flat_full = [item for sublist in full for item in sublist]
    return sum(flat_full, Counter())
