from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.core.validators import MaxValueValidator, MinValueValidator


class FuzzyForm(forms.Form):
    avel_consol = forms.FloatField(required=True, label="Альвеолярная консолидация", initial=0.75,
                                   validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    gipox = forms.FloatField(required=True, label="Гипоксемия", initial=355.8,
                             validators=[MinValueValidator(0.0), MaxValueValidator(400.0)])
    compl = forms.FloatField(required=True, label="Комплаенс респираторной системы (мл\см Н2О)", initial=56.8,
                             validators=[MinValueValidator(0.0), MaxValueValidator(90.0)])
    press = forms.FloatField(required=True, label="Положительное давление в конце выдоха (см Н2О)", initial=19.2,
                             validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            'avel_consol',
            'gipox',
            'compl',
            'press',
            Submit('submit', 'Получить результат', css_class="btn-success")
        )
