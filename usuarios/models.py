# usuarios/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static
from proveedor.models import Proveedor

# --- Opciones de Selección Múltiple ---
RELACION_NEGOCIO_CHOICES = [
    ('DUEÑO', 'Dueño/a'),
    ('ADMIN', 'Administrador/a'),
    ('EMPLEADO', 'Empleado/a clave'),
    ('FAMILIAR', 'Familiar a cargo'),
]

TIPO_NEGOCIO_CHOICES = [
    ('ALMACEN', 'Almacén de Barrio'),
    ('MINIMARKET', 'Minimarket'),
    ('BOTILLERIA', 'Botillería'),
    ('PANADERIA', 'Panadería/Pastelería'),
    ('FERIA', 'Feria Libre'),
    ('KIOSCO', 'Kiosco'),
    ('FOODTRUCK', 'Food Truck/Carro de Comida'),
]

INTERESTS_CHOICES = [
    ('MARKETING', 'Marketing Digital'),
    ('INVENTARIO', 'Gestión de Inventario'),
    ('PROVEEDORES', 'Proveedores Locales'),
    ('FINANZAS', 'Finanzas y Contabilidad'),
    ('CLIENTES', 'Atención al Cliente'),
    ('LEYES', 'Normativa y Leyes'),
    ('TECNOLOGIA', 'Uso de Tecnología y Apps'),
    ('REDES_SOCIALES', 'Redes Sociales para Negocios'),
    ('VENTAS', 'Técnicas de Ventas'),
    ('CREDITOS', 'Créditos y Préstamos Pyme'),
    ('IMPUESTOS', 'Impuestos y Contabilidad Básica'),
    ('DECORACION', 'Decoración y Merchandising'),
    ('SOSTENIBILIDAD', 'Sostenibilidad y Reciclaje'),
    ('SEGURIDAD', 'Seguridad del Negocio'),
    ('LOGISTICA', 'Logística y Reparto'),
    ('INNOVACION', 'Innovación en Productos'),
    ('EMPRENDIMIENTO', 'Modelos de Emprendimiento'),
    ('SEGUROS', 'Seguros para Negocios'),
]

CATEGORIA_POST_CHOICES = [
    ('DUDA', 'Duda / Pregunta'),
    ('OPINION', 'Opinión / Debate'),
    ('RECOMENDACION', 'Recomendación'),
    ('NOTICIA', 'Noticia del Sector'),
    ('GENERAL', 'General'),
    ('NOTICIAS_CA', 'Noticias Club Almacén'),
    ('DESPACHOS', 'Despachos realizados'),
    ('NUEVOS_SOCIOS', 'Nuevos socios'),
    ('ACTIVIDADES', 'Actividades en curso'),
]

CATEGORIAS = [
    ('DESCUENTO', 'Descuento y Ofertas'),
    ('SORTEO', 'Sorteos y Rifas'),
    ('CAPACITACION', 'Capacitación y Cursos'),
    ('ACCESO', 'Acceso Exclusivo'),
    ('EVENTO', 'Eventos Especiales'),
]

ESTADO_BENEFICIO = [
    ('ACTIVO', 'Activo'),
    ('TERMINADO', 'Terminado'),
    ('BENEFICIO_ACTIVO', 'Beneficio Reclamado'),
]

RUBROS_CHOICES = [
    ('ABARROTES', 'Abarrotes'),
    ('CARNES', 'Carnes'),
    ('LACTEOS', 'Lácteos'),
    ('FRUTAS', 'Frutas y Verduras'),
    ('LIMPIEZA', 'Limpieza'),
    ('PANADERIA', 'Panadería'),
    ('VARIOS', 'Varios'),
]

REGIONES_CHILE = [
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


class Comerciante(models.Model):
    ROLES_CHOICES = [
        ('COMERCIANTE', 'Comerciante'),
        ('ADMIN', 'Administrador'),
        ('PROVEEDOR', 'Proveedor'),
        ('TECNICO', 'Técnico de soporte'),
    ]

    nombre_apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='COMERCIANTE')

    whatsapp_validator = RegexValidator(
        regex=r'^\+569\d{8}$',
        message="El formato debe ser '+569XXXXXXXX'."
    )
    whatsapp = models.CharField(validators=[whatsapp_validator], max_length=12, blank=True, null=True)

    relacion_negocio = models.CharField(max_length=10, choices=RELACION_NEGOCIO_CHOICES)
    tipo_negocio = models.CharField(max_length=20, choices=TIPO_NEGOCIO_CHOICES)

    nombre_negocio = models.CharField(max_length=255, blank=True, null=True)

    region = models.CharField(
        max_length=50,
        choices=REGIONES_CHILE,
        default='RM',
        blank=False,
        help_text="Seleccione su región"
    )

    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        default='usuarios/img/default_profile.png',
        blank=True,
        null=True
    )

    intereses = models.CharField(max_length=512, default='', blank=True, help_text="Códigos de intereses separados por coma.")
    es_proveedor = models.BooleanField(default=False)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_conexion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Comerciante'
        verbose_name_plural = 'Comerciantes'

    def __str__(self):
        return f"{self.nombre_apellido} ({self.email})"

    def get_profile_picture_url(self):
        DEFAULT_IMAGE_PATH = 'usuarios/img/default_profile.png'
        if self.foto_perfil and self.foto_perfil.name != DEFAULT_IMAGE_PATH:
            return self.foto_perfil.url
        return static('img/default_profile.png')


class Post(models.Model):
    comerciante = models.ForeignKey(Comerciante, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_POST_CHOICES, default='GENERAL')
    imagen_url = models.URLField(max_length=200, blank=True, null=True)
    etiquetas = models.CharField(max_length=255, blank=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Publicación de Foro'
        verbose_name_plural = 'Publicaciones de Foro'
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return f"[{self.get_categoria_display()}] {self.titulo} por {self.comerciante.nombre_apellido}"


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    comerciante = models.ForeignKey(Comerciante, on_delete=models.CASCADE, related_name='comentarios_dados')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Comentario de {self.comerciante.nombre_apellido} en {self.post.titulo[:20]}"


class Beneficio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='beneficios_fotos/', null=True, blank=True)
    vence = models.DateField(null=True, blank=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='DESCUENTO')
    estado = models.CharField(max_length=30, choices=ESTADO_BENEFICIO, default='ACTIVO')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Beneficio y Promoción'
        verbose_name_plural = 'Beneficios y Promociones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"[{self.get_categoria_display()}] {self.titulo}"


class Propuesta(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='propuestas')
    titulo = models.CharField(max_length=100)
    rubros_ofertados = models.CharField(max_length=255, help_text='Separados por coma')
    zona_geografica = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Propuesta de Proveedor"
        verbose_name_plural = "Propuestas de Proveedores"

    def __str__(self):
        return f"{self.titulo} - {self.proveedor.nombre}"
