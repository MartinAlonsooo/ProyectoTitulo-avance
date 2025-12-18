# administrador/forms.py

from django import forms
from django.contrib.auth.hashers import make_password
from usuarios.models import Comerciante, Beneficio, Post, CATEGORIA_POST_CHOICES # Importar CATEGORIA_POST_CHOICES

ADMIN_CATEGORIES_TUPLES = [
    ('NOTICIAS_CA', 'Noticias Club Almacén'),
    ('DESPACHOS', 'Despachos realizados'),
    ('NUEVOS_SOCIOS', 'Nuevos socios'),
    ('ACTIVIDADES', 'Actividades en curso'),
]

class ComercianteAdminForm(forms.ModelForm):
    raw_password = forms.CharField(
        required=False,
        label="Contraseña nueva",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Comerciante
        fields = [
            'nombre_apellido',
            'email',
            'whatsapp',
            'relacion_negocio',
            'tipo_negocio',
            'nombre_negocio',
            'rol',
            'es_proveedor',      # 👈 importante para el flujo proveedor
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        password = self.cleaned_data.get('raw_password')
        if password:
            instance.password_hash = make_password(password)

        if commit:
            instance.save()

        return instance


# 🔹 FORMULARIO PARA BENEFICIOS
class BeneficioAdminForm(forms.ModelForm):
    class Meta:
        model = Beneficio
        fields = [
            'titulo',
            'descripcion',
            'foto',
            'vence',
            'categoria',
            'estado',
        ]


# 🔹 FORMULARIO PARA POSTS
class PostAdminForm(forms.ModelForm):
    
    # Campo de categoría con opciones limitadas solo a Admin
    categoria = forms.ChoiceField(
        choices=ADMIN_CATEGORIES_TUPLES,
        label='Categoría',
        widget=forms.Select(attrs={
            # Puede agregar estilos aquí si es necesario
        })
    )
    
    class Meta:
        model = Post
        fields = [
            'titulo',
            'contenido',
            'categoria', # Usamos el campo localmente definido arriba
            'imagen_url',
        ]