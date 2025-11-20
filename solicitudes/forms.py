from django import forms
from .models import SolicitudAyuda

class SolicitudAyudaForm(forms.ModelForm):
    # Campo adicional para confirmar correo
    confirmar_correo = forms.EmailField(
        label="Confirmar correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Confirme su correo electrónico',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = SolicitudAyuda
        fields = [
            'nombre_completo',
            'cedula',
            'edad',
            'celular',
            'genero',
            'correo_electronico',
            'direccion',
            'grupo_raizal',
            'discapacidad',
            'descripcion_discapacidad',
            'urgencia',
            'descripcion_problema',
            'acepta_terminos',
            'acepta_tratamiento_datos',
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'placeholder': 'Ej: María González Pérez',
                'class': 'form-control'
            }),
            'cedula': forms.TextInput(attrs={
                'placeholder': 'Ej: 12345678',
                'class': 'form-control'
            }),
            'edad': forms.NumberInput(attrs={
                'placeholder': 'Ej: 25',
                'min': 1,
                'max': 120,
                'class': 'form-control'
            }),
            'celular': forms.TextInput(attrs={
                'placeholder': 'Ej: 3001234567',
                'class': 'form-control'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'ejemplo@correo.com',
                'class': 'form-control'
            }),
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Dirección completa incluyendo ciudad y barrio',
                'class': 'form-control'
            }),
            'descripcion_discapacidad': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describa brevemente su discapacidad si aplica',
                'class': 'form-control'
            }),
            'descripcion_problema': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describa detalladamente su situación...',
                'class': 'form-control'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo_electronico')
        confirmar_correo = cleaned_data.get('confirmar_correo')
        acepta_terminos = cleaned_data.get('acepta_terminos')
        acepta_tratamiento = cleaned_data.get('acepta_tratamiento_datos')
        
        # Validar que los correos coincidan
        if correo and confirmar_correo:
            if correo != confirmar_correo:
                raise forms.ValidationError({
                    'confirmar_correo': 'Los correos electrónicos no coinciden'
                })
        
        # Validar que acepte términos y condiciones
        if not acepta_terminos:
            raise forms.ValidationError({
                'acepta_terminos': 'Debe aceptar los términos y condiciones para continuar'
            })
        
        # Validar que acepte tratamiento de datos
        if not acepta_tratamiento:
            raise forms.ValidationError({
                'acepta_tratamiento_datos': 'Debe aceptar el tratamiento de datos personales para continuar'
            })
        
        return cleaned_data