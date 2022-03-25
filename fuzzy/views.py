from django.shortcuts import render
from .forms import FuzzyForm
from FIS.mamdani_fuzzy import create_mamdani_system
from FIS.sugeno_fuzzy import create_sugeno_fuzzy

# Create your views here.
global mamdani_system
mamdani_system = create_mamdani_system()
global sugeno_system
sugeno_system = create_sugeno_fuzzy()

def show_result(request):
    output_mamdani = None
    output_sugeno = None
    if request.method == "POST":
        form = FuzzyForm(request.POST)
        if form.is_valid():
            avel_consol = form.cleaned_data['avel_consol']
            gipox = form.cleaned_data['gipox']
            compl = form.cleaned_data['compl']
            press = form.cleaned_data['press']

            output_mamdani = mamdani_system.evaluate_output({
                'avel_consol': avel_consol,
                'gipox': gipox,
                'compl': compl,
                'press': press
            })

            # Set antecedents values
            sugeno_system.set_variable("avel_consol", avel_consol)
            sugeno_system.set_variable("gipox", gipox)
            sugeno_system.set_variable("compl", compl)
            sugeno_system.set_variable("press", press)
            output_sugeno = sugeno_system.Sugeno_inference()
    else:
        form = FuzzyForm()

    return render(request, "form.html", {'form': form, 'output_mamdani':output_mamdani, 'output_sugeno':output_sugeno})
