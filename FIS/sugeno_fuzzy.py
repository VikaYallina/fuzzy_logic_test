from FIS.sugeno import *
from pyswip import Prolog

def create_sugeno_fuzzy():
    # A simple fuzzy inference system for the tipping problem
    # Create a fuzzy system object
    prolog = Prolog()
    FS = FuzzySystem(verbose=True)

    AC_1 = FuzzySet(function=Triangular_MF(0, 0, 0.1), term="none")
    AC_2 = FuzzySet(function=Triangular_MF(0, 0.25, 0.5), term="one_quad")
    AC_3 = FuzzySet(function=Triangular_MF(0.25, 0.5, 0.75), term="two_quad")
    AC_4 = FuzzySet(function=Triangular_MF(0.5, 0.75, 1), term="three_quad")
    AC_5 = FuzzySet(function=Triangular_MF(0.95, 1, 1.05), term="four_quad")
    FS.add_linguistic_variable("avel_consol",
                               LinguisticVariable([AC_1, AC_2, AC_3, AC_4, AC_5], universe_of_discourse=[0, 1.05]))

    G_1 = FuzzySet(function=Pi_MF(-173.5, -40.0, 100.0, 130.0), term="very_low")
    G_2 = FuzzySet(function=Gaussian_MF(137.5, 15.91), term="low")
    G_3 = FuzzySet(function=Pi_MF(160.0, 190.0, 205, 240), term="medium")
    G_4 = FuzzySet(function=Gaussian_MF(262.5, 15.92), term="high")
    G_5 = FuzzySet(function=Pi_MF(265.0, 300.0, 486.3, 843.9), term="very_high")
    FS.add_linguistic_variable("gipox", LinguisticVariable([G_1, G_2, G_3, G_4, G_5], universe_of_discourse=[0, 400]))

    C_1 = FuzzySet(function=Pi_MF(-9, -1, 19, 27.4), term="very_low")
    C_2 = FuzzySet(function=Gaussian_MF(30.0, 5.5), term="low")
    C_3 = FuzzySet(function=Gaussian_MF(50.0, 5.5), term="medium")
    C_4 = FuzzySet(function=Gaussian_MF(70.0, 5.5), term="high")
    C_5 = FuzzySet(function=Pi_MF(70.0, 79.5, 102.3, 120.5), term="very_high")
    FS.add_linguistic_variable("compl", LinguisticVariable([C_1, C_2, C_3, C_4, C_5], universe_of_discourse=[0, 90]))

    P_1 = FuzzySet(function=Pi_MF(-6.75, -0.75, 5, 6.5), term="very_low")
    P_2 = FuzzySet(function=Gaussian_MF(7.0, 0.7), term="low")
    P_3 = FuzzySet(function=Gaussian_MF(10.0, 0.7), term="medium")
    P_4 = FuzzySet(function=Gaussian_MF(13.0, 0.7), term="high")
    P_5 = FuzzySet(function=Pi_MF(13.2, 14.8, 21.5, 26.83), term="very_high")
    FS.add_linguistic_variable("press", LinguisticVariable([P_1, P_2, P_3, P_4, P_5], universe_of_discourse=[0, 20]))

    # # Define fuzzy sets and linguistic variables
    # S_1 = FuzzySet(points=[[0., 1.],  [5., 0.]], term="poor")
    # S_2 = FuzzySet(points=[[0., 0.], [5., 1.], [10., 0.]], term="good")
    # S_3 = FuzzySet(points=[[5., 0.],  [10., 1.]], term="excellent")
    # FS.add_linguistic_variable("Service", LinguisticVariable([S_1, S_2, S_3], concept="Service quality"))
    #
    # F_1 = FuzzySet(points=[[0., 1.],  [10., 0.]], term="rancid")
    # F_2 = FuzzySet(points=[[0., 0.],  [10., 1.]], term="delicious")
    # FS.add_linguistic_variable("Food", LinguisticVariable([F_1, F_2], concept="Food quality"))

    # Define output crisp values
    FS.set_crisp_output_value("small", 0)
    FS.set_crisp_output_value("medium", 2)
    FS.set_crisp_output_value("severe", 4)

    # Define fuzzy rules
    press_values = ["very_low", "low", "medium", "high", "very_high"]
    reg_values = ["none", "one_quad", "two_quad", "three_quad", "four_quad"]
    gep_values = ["very_high", "high", "medium", "low", "very_low"]
    comp_values = ["very_high", "high", "medium", "low", "very_low"]

    prolog.consult("FIS/kb.pl")
    rules = []
    for reg in range(len(reg_values)):
        for gep in range(len(gep_values)):
            for comp in range(len(comp_values)):
                for press in range(len(press_values)):
                    _str = f"result(xray({reg_values[reg]}), gipox({gep_values[gep]}), compliance({comp_values[comp]}), pressure({press_values[press]}), Y)"
                    for s in prolog.query(_str):
                        res = s["Y"]
                        rule = f"IF (avel_consol IS {reg_values[reg]}) AND (gipox IS {gep_values[gep]}) AND (compl IS {comp_values[comp]}) AND (press IS {press_values[press]}) THEN (Result IS {res})"
                        rules.append(rule)

    FS.add_rules(rules)



    # Perform Sugeno inference and print output
    return FS

