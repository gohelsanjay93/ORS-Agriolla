from django import forms

from .models import MachineReports


class MachinereportForm(forms.ModelForm):
    class Meta:
        model = MachineReports
        fields = '__all__'