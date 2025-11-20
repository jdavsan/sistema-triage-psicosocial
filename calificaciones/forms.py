from django import forms
from .models import CalificacionSQLite

class CalificacionForm(forms.ModelForm):
    # ELIMINAR confirmar_nombre completamente
    
    class Meta:
        model = CalificacionSQLite
        fields = ['nombre', 'calificacion', 'comentario']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tu nombre completo'
            }),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '5',
                'placeholder': '1-5'
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Tu comentario sobre el servicio...'
            }),
        }
        labels = {
            'nombre': 'Tu nombre *',
            'calificacion': 'Calificación (1-5) *',
            'comentario': 'Comentario (opcional)',
        }
    
    def clean_calificacion(self):
        calificacion = self.cleaned_data.get('calificacion')
        if calificacion and (calificacion < 1 or calificacion > 5):
            raise forms.ValidationError("La calificación debe estar entre 1 y 5")
        return calificacion