from django import forms
from .models import CalificacionSQLite

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = CalificacionSQLite
        fields = ['nombre', 'comentario', 'calificacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'minlength': '3',  # Mínimo 3 caracteres
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí...',
                'rows': 4,
            }),
            'calificacion': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
    
    def clean_nombre(self):
        """Validar que el nombre tenga al menos 3 caracteres"""
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        return nombre
    
    def clean_calificacion(self):
        """Validar que la calificación esté en el rango correcto"""
        calificacion = self.cleaned_data.get('calificacion')
        if calificacion < 1 or calificacion > 5:
            raise forms.ValidationError('La calificación debe estar entre 1 y 5')
        return calificacion