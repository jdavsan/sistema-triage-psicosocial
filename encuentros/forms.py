from django import forms
from .models import EncuentroVirtual

class EncuentroForm(forms.ModelForm):
    """Formulario para programar encuentros virtuales"""
    
    class Meta:
        model = EncuentroVirtual
        fields = ['trabajador_social', 'fecha_programada', 'duracion_estimada', 'enlace_meet']
        widgets = {
            'fecha_programada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duracion_estimada': forms.NumberInput(attrs={'min': 15, 'max': 120}),
            'enlace_meet': forms.URLInput(attrs={'placeholder': 'https://meet.google.com/...'})
        }
    
    def clean_fecha_programada(self):
        fecha = self.cleaned_data.get('fecha_programada')
        from django.utils import timezone
        if fecha and fecha < timezone.now():
            raise forms.ValidationError("No puede programar un encuentro en el pasado")
        return fecha