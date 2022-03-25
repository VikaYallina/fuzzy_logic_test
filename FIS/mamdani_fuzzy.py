from .mamdani.fuzzy_var_output import FuzzyOutputVariable
from .mamdani.fuzzy_var_input import FuzzyInputVariable
from pyswip import Prolog

from .mamdani.fuzzy_system import FuzzySystem


def create_mamdani_system():
    prolog = Prolog()
    x1 = FuzzyInputVariable('avel_consol', 0, 1, 100)
    x1.add_triangular('none', 0, 0, 0.1)
    x1.add_triangular('one_quad', 0, 0.25, 0.5)
    x1.add_triangular('two_quad', 0.25, 0.5, 0.75)
    x1.add_triangular('three_quad', 0.5, 0.75, 1)
    x1.add_triangular('four_quad', 0.95, 1, 1.05)

    x2 = FuzzyInputVariable('gipox', 0, 400, 400)
    x2.add_pi('very_low', -173.5, -40.0, 100.0, 130.0)
    x2.add_gauss('low', 15.91, 137.5)
    x2.add_pi('medium', 160, 190, 205, 240)
    x2.add_gauss('high', 15.92, 262.5)
    x2.add_pi('very_high', 265, 300, 486.3, 843.9)

    x3 = FuzzyInputVariable('compl', 0, 90, 90)
    x3.add_pi('very_low', -9, -1, 19, 27.4)
    x3.add_gauss('low', 5.5, 30.0)
    x3.add_gauss('medium', 5.5, 50.0)
    x3.add_gauss('high', 5.5, 70.0)
    x3.add_pi('very_high', 70.0, 79.5, 102.3, 120.5)

    x4 = FuzzyInputVariable('press', 0, 20, 100)
    x4.add_pi('very_low', -6.75, -0.75, 5, 6.5)
    x4.add_gauss('low', 0.7, 7.0)
    x4.add_gauss('medium', 0.7, 10.0)
    x4.add_gauss('high', 0.7, 13.0)
    x4.add_pi('very_high', 13.2, 14.8, 21.5, 26.83)

    y = FuzzyOutputVariable('result', 0, 4, 50)
    y.add_z('small', 0.0, 2.0)
    y.add_pi('medium', 0.5, 1.8, 2.16, 3.5)
    y.add_s('severe', 2.0, 4.0)

    system = FuzzySystem()
    system.add_input_variable(x1)
    system.add_input_variable(x2)
    system.add_input_variable(x3)
    system.add_input_variable(x4)
    system.add_output_variable(y)

    press_values = ["very_low", "low", "medium", "high", "very_high"]
    reg_values = ["none", "one_quad", "two_quad", "three_quad", "four_quad"]
    gep_values = ["very_high", "high", "medium", "low", "very_low"]
    comp_values = ["very_high", "high", "medium", "low", "very_low"]

    prolog.consult("FIS/kb.pl")

    for reg in range(len(reg_values)):
        for gep in range(len(gep_values)):
            for comp in range(len(comp_values)):
                for press in range(len(press_values)):
                    _str = f"result(xray({reg_values[reg]}), gipox({gep_values[gep]}), compliance({comp_values[comp]}), pressure({press_values[press]}), Y)"
                    for s in prolog.query(_str):
                        system.add_rule(
                            {'avel_consol': reg_values[reg],
                             'gipox': gep_values[gep],
                             'compl': comp_values[comp],
                             'press': press_values[press]},
                            {'result': s["Y"]}
                        )

    return system
    # output = system.evaluate_output({
    #     'avel_consol': 0.75,
    #     'gipox': 360.0,
    #     'compl': 12.0,
    #     'press': 19.0
    # })
