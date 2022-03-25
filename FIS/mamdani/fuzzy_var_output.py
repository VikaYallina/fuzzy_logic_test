from .fuzzy_variable import FuzzyVariable
from .fuzzy_set import FuzzySet
import matplotlib.pyplot as plt

class FuzzyOutputVariable(FuzzyVariable):

    def __init__(self, name, min_val, max_val, res):
        super().__init__(name, min_val, max_val, res)
        self._output_distribution = FuzzySet(name, min_val, max_val, res)

    def clear_output_distribution(self):
        self._output_distribution.clear_set()

    def add_rule_contribution(self, rule_consequence):
        self._output_distribution = self._output_distribution.union(rule_consequence)

    def get_crisp_output(self):
        fig, axs = plt.subplots(1, 1)

        self._output_distribution.plot_set(axs)

        plt.show()
        return self._output_distribution.cog_defuzzify()


    def get_crisp_output_info(self):
        return self._output_distribution.cog_defuzzify(), self._output_distribution


if __name__ == "__main__":
    pass