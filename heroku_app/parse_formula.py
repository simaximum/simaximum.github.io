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

brackets_map = {
    '(': ')',
    '[': ']',
    '{': '}',
}


def _is_balanced(formula):
    """Check if brackets are well balanced."""
    stack = []
    opening = brackets_map.keys()
    closing = brackets_map.values()
    for i in formula:
        if i in opening:
            stack.append(i)
        elif i in closing:
            if (len(stack) > 0) and (i == brackets_map[stack[-1]]):
                stack.pop()
            else:
                return "Unbalanced"
    if len(stack) == 0:
        return "Balanced"
    else:
        return "Unbalanced"


def parse_formula(formula):
    """Parse the formula."""

    if not _is_balanced(formula):
        raise ValueError('Unbalanced brackets')

    # Final list of parsed atoms
    final_list = []
    # Currently parsed list of atoms
    current_list = [Counter()]
    # Number of multiplications to perform
    nb_multiplications = 0
    # Action switch
    action = ""

    # Divide formula into its tokens
    formula_tokens = re.findall('[A-Z][a-z]?|\d+|.', formula)

    for token in formula_tokens:
        if token in symbols:
            # Add atom to the currently parsed list, switch 'action' to atom symbol
            current_list[-1] = current_list[-1] + Counter({token})
            action = token

        elif token.isdecimal():
            count = int(token)
            if action in symbols:
                # Multiply count of last seen atom
                current_list[-1][action] = current_list[-1][action] * count
            elif action in ')]}':
                # Multiply count of all atom groups between last seen brackets
                for group in current_list[nb_multiplications-1:]:
                    for atom in group:
                        group[atom] = group[atom] * count
                nb_multiplications -= 1
            else:
                raise ValueError('Formula cannot start with a number')

        elif token in '([{':
            if nb_multiplications == 0:
                # Non-nested opening bracket: add currently parsed list to final list, and start a new one
                final_list.append(current_list)
                current_list = [Counter()]
            else:
                # Nested opening bracket: add a new atom group to currently parsed list
                current_list.append(Counter())
            nb_multiplications += 1

        elif token in ')]}':
            # Switch 'action' to closing brackets
            action = token

        else:
            raise ValueError(f'Unrecognized element in formula: {token}')

    # Finalize final list, flatten it, return aggregated counters
    final_list.append(current_list)
    flat_final_list = [item for sublist in final_list for item in sublist]
    return sum(flat_final_list, Counter())
