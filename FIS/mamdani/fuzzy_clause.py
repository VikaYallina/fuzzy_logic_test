'''
Fuzzy Clause class. Used in Fuzzy rule
'''


class FuzzyClause():
    '''
	A fuzzy clause of the type 'variable is set'
	used in fuzzy IF ... THEN ... rules
	clauses can be antecedent (if part) or consequent
	(then part)
	'''

    def __init__(self, variable, f_set, degree=1):
        if f_set is None:
            raise Exception('set none')

        if f_set.name == '':
            raise Exception(str(f_set), 'no set name')

        self._variable = variable
        self._set = f_set

    def __str__(self):
        return f'{self._variable.name} is {self._set.name}'

    @property
    def variable_name(self):
        return self._variable.name

    @property
    def set_name(self):
        return self._set.name

    def evaluate_antecedent(self):
        print(self._set.last_dom_value)
        return self._set.last_dom_value

    def evaluate_consequent(self, dom):
        self._variable.add_rule_contribution(self._set.min_scalar(dom))

