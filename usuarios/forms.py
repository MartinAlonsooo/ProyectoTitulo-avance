# usuarios/forms.py
from allauth.socialaccount.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from .models import (
    Comerciante, Post, Comentario,
    RELACION_NEGOCIO_CHOICES, TIPO_NEGOCIO_CHOICES,
    CATEGORIA_POST_CHOICES, INTERESTS_CHOICES
)

# Opciones de región
REGIONES_CHILE = [
    ('', 'Selecciona tu región'),
    ('RM', 'Región Metropolitana'),
    ('I', 'Región de Tarapacá'),
    ('II', 'Región de Antofagasta'),
    ('III', 'Región de Atacama'),
    ('IV', 'Región de Coquimbo'),
    ('V', 'Región de Valparaíso'),
    ('VI', 'Región del Libertador General Bernardo O’Higgins'),
    ('VII', 'Región del Maule'),
    ('VIII', 'Región del Biobío'),
    ('IX', 'Región de La Araucanía'),
    ('X', 'Región de Los Lagos'),
    ('XI', 'Región Aysén del General Carlos Ibáñez del Campo'),
    ('XII', 'Región de Magallanes y de la Antártica Chilena'),
    ('XIII', 'Región de Ñuble'),
    ('XIV', 'Región de Los Ríos'),
]

# -------------------------------------------
# FORMULARIO DE REGISTRO DE COMERCIANTE
# -------------------------------------------
class RegistroComercianteForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mínimo 8 caracteres',
            'id': 'password',
            'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
        }),
        max_length=255
    )
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repite la contraseña',
            'id': 'confirm-password',
            'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
        }),
        max_length=255
    )

    relacion_negocio = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + list(RELACION_NEGOCIO_CHOICES),
        label='Relación con el negocio',
        required=True,
        widget=forms.Select(attrs={
            'id': 'id_relacion_negocio',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d171b] dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary border border-[#cfdfe7] dark:border-gray-600 bg-background-light dark:bg-gray-800 focus:border-primary h-12 p-[15px] text-base font-normal leading-normal appearance-none cursor-pointer'
        })
    )

    tipo_negocio = forms.ChoiceField(
        choices=[('', 'Selecciona un tipo')] + list(TIPO_NEGOCIO_CHOICES),
        label='Tipo de negocio',
        required=True,
        widget=forms.Select(attrs={
            'id': 'id_tipo_negocio',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d171b] dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary border border-[#cfdfe7] dark:border-gray-600 bg-background-light dark:bg-gray-800 focus:border-primary h-12 p-[15px] text-base font-normal leading-normal appearance-none cursor-pointer'
        })
    )


    region_select = forms.ChoiceField(
        choices=REGIONES_CHILE,
        label='Región',
        required=True,
        widget=forms.Select(attrs={
            'id': 'id_region_select',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d171b] dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary border border-[#cfdfe7] dark:border-gray-600 bg-background-light dark:bg-gray-800 focus:border-primary h-12 p-[15px] text-base font-normal leading-normal appearance-none cursor-pointer'
        })
    )

    class Meta:
        model = Comerciante
        fields = (
            'nombre_apellido', 'email', 'whatsapp',
        )
        widgets = {
            'nombre_apellido': forms.TextInput(attrs={
                'placeholder': 'Ej: Juan Pérez',
                'id': 'fullname',
                'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'tucorreo@ejemplo.com',
                'id': 'email',
                'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
            }),
            'whatsapp': forms.TextInput(attrs={
                'placeholder': '+56912345678',
                'id': 'whatsapp',
                'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Comerciante.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email.lower()

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if not whatsapp:
            raise ValidationError('El número de WhatsApp es obligatorio.')
        if not whatsapp.startswith('+569'):
            raise ValidationError('El WhatsApp debe comenzar con +569 seguido de 8 dígitos.')
        if len(whatsapp) != 12:
            raise ValidationError('El formato debe ser +569XXXXXXXX (12 caracteres).')
        return whatsapp

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Las contraseñas no coinciden.')
            elif len(password) < 8:
                self.add_error('password', 'La contraseña debe tener al menos 8 caracteres.')

        # Mapear comuna_select a comuna
        comuna = cleaned_data.get('comuna_select')
        if comuna:
            cleaned_data['comuna'] = comuna

        # Mapear region_select a region
        region = cleaned_data.get('region_select')
        if region:
            cleaned_data['region'] = region

        return cleaned_data

# -------------------------------------------
# FORMULARIO DE LOGIN
# -------------------------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none',
            'placeholder': 'tucorreo@ejemplo.com'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none',
            'placeholder': '••••••••'
        })
    )

# -------------------------------------------
# FORMULARIO PARA POSTS
# -------------------------------------------
class PostForm(forms.ModelForm):
    uploaded_file = forms.FileField(
        required=False,
        label='Subir Archivo (Imagen/Documento)',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-input-file block w-full text-sm text-text-light file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary/10 file:text-primary hover:file:bg-primary/20 dark:file:bg-primary dark:file:text-white',
        })
    )

    url_link = forms.URLField(
        required=False,
        label='Link URL',
        widget=forms.URLInput(attrs={
            'placeholder': 'Opcional: URL de una imagen externa o link',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-light dark:text-text-dark focus:outline-0 focus:ring-2 focus:ring-primary border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary h-12 placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark p-[10px] text-base font-normal leading-normal'
        })
    )

    etiquetas_input = forms.CharField(
        required=False,
        label='Etiquetas',
        help_text='Etiqueta a otros usuarios o agrega hashtags, separados por coma (ej: @JuanPerez, #Marketing)',
        widget=forms.TextInput(attrs={
            'placeholder': '@usuario, #hashtag',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-light dark:text-text-dark focus:outline-0 focus:ring-2 focus:ring-primary border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary h-12 placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark p-[10px] text-base font-normal leading-normal'
        })
    )

    class Meta:
        model = Post
        fields = ('titulo', 'contenido', 'categoria') 
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Titulo',
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-light dark:text-text-dark focus:outline-0 focus:ring-2 focus:ring-primary border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary h-12 placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark p-[10px] text-base font-normal leading-normal'
            }),
            'contenido': forms.Textarea(attrs={
                'placeholder': 'Escribe aquí el contenido de tu publicación...',
                'rows': 5,
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-light dark:text-text-dark focus:outline-0 focus:ring-2 focus:ring-primary border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark p-[10px] text-base font-normal leading-normal'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select flex w-full min-w-0 flex-1 rounded-lg text-text-light dark:text-text-dark focus:outline-0 focus:ring-2 focus:ring-primary border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary h-12 placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark p-[10px] text-base font-normal leading-normal'
            }, choices=CATEGORIA_POST_CHOICES),
        }

    def clean(self):
        cleaned_data = super().clean()
        url_link = self.cleaned_data.get('url_link')
        uploaded_file = self.cleaned_data.get('uploaded_file')
        etiquetas_input = self.cleaned_data.pop('etiquetas_input', None)

        if uploaded_file and url_link:
            self.add_error(None, "Solo puedes subir un archivo O proporcionar un link URL, no ambos.")
        if url_link:
            cleaned_data['imagen_url'] = url_link
        if etiquetas_input:
            cleaned_data['etiquetas'] = etiquetas_input
        return cleaned_data

# -------------------------------------------
# FORMULARIOS VARIOS
# -------------------------------------------
class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Comerciante
        fields = ['foto_perfil']

class BusinessDataForm(forms.ModelForm):
    class Meta:
        model = Comerciante
        fields = ['relacion_negocio', 'tipo_negocio', 'region', 'nombre_negocio']
        widgets = {
            'relacion_negocio': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            }),
            'tipo_negocio': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            }),
            'region': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            }),
            'nombre_negocio': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white',
                'placeholder': 'Ej: Minimarket El Sol'
            }),
        }


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = Comerciante
        fields = ['email', 'whatsapp']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white', 'placeholder': 'tu@correo.cl'}),
            'whatsapp': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white', 'placeholder': '+569XXXXXXXX'}),
        }

class InterestsForm(forms.Form):
    intereses = forms.MultipleChoiceField(
        choices=INTERESTS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Selecciona tus intereses"
    )

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'placeholder': 'Escribe tu comentario...',
                'rows': 3,
                'class': 'w-full resize-none rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-primary focus:border-primary p-[10px] text-base'
            }),
        }
        labels = {'contenido': 'Tu Comentario'}

# -------------------------------------------
# FORMULARIO DE REGISTRO SOCIAL
# -------------------------------------------
class SocialSignupForm(SignupForm):
    nombre_apellido = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Juan Pérez',
            'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
        })
    )

    whatsapp = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '+56912345678',
            'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'
        })
    )

    relacion_negocio = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + list(RELACION_NEGOCIO_CHOICES),
        required=True,
        widget=forms.Select(attrs={'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'})
    )

    tipo_negocio = forms.ChoiceField(
        choices=[('', 'Selecciona un tipo')] + list(TIPO_NEGOCIO_CHOICES),
        required=True,
        widget=forms.Select(attrs={'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'})
    )


    region_select = forms.ChoiceField(
        choices=REGIONES_CHILE,
        required=True,
        widget=forms.Select(attrs={'class': 'w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none'})
    )

    def save(self, request):
        user = super().save(request)
        comerciante, created = Comerciante.objects.get_or_create(
            email=user.email,
            defaults={
                'nombre_apellido': self.cleaned_data['nombre_apellido'],
                'whatsapp': self.cleaned_data['whatsapp'],
                'relacion_negocio': self.cleaned_data['relacion_negocio'],
                'tipo_negocio': self.cleaned_data['tipo_negocio'],
                'region': self.cleaned_data['region_select'],
            }
        )
        return user
