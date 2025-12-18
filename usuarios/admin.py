from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import (
    Comerciante,
    Post,
    Comentario,
    Beneficio,
    Proveedor,
    Propuesta,
)


# =========================================================
# ADMIN COMERCIANTE
# =========================================================
@admin.register(Comerciante)
class ComercianteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_apellido',
        'email',
        'rol',
        'nombre_negocio',
        'es_proveedor',
        'fecha_registro',
        'ultima_conexion',
        'region',
    )

    list_filter = (
        'rol',
        'region',
        'es_proveedor',
        'relacion_negocio',
        'tipo_negocio',
    )

    search_fields = (
        'nombre_apellido',
        'email',
        'nombre_negocio',
        'whatsapp',
    )

    readonly_fields = (
        'fecha_registro',
        'ultima_conexion',
    )

    fieldsets = (
        ('Datos personales', {
            'fields': (
                'nombre_apellido',
                'email',
                'password_hash',
                'rol',
            )
        }),
        ('Contacto', {
            'fields': (
                'whatsapp',
            )
        }),
        ('Negocio', {
            'fields': (
                'nombre_negocio',
                'region',
                'relacion_negocio',
                'tipo_negocio',
                'es_proveedor',
            )
        }),
        ('Perfil', {
            'fields': (
                'foto_perfil',
                'intereses',
            )
        }),
        ('Auditoría', {
            'fields': (
                'fecha_registro',
                'ultima_conexion',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        🔐 Asegura que la contraseña SIEMPRE quede hasheada
        (admin crea usuarios funcionales para login)
        """
        if obj.password_hash and not str(obj.password_hash).startswith('pbkdf2_'):
            obj.password_hash = make_password(obj.password_hash)

        super().save_model(request, obj, form, change)


# =========================================================
# ADMIN POST
# =========================================================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'comerciante',
        'categoria',
        'fecha_publicacion',
    )

    list_filter = (
        'categoria',
        'fecha_publicacion',
    )

    search_fields = (
        'titulo',
        'contenido',
        'comerciante__nombre_apellido',
        'comerciante__email',
    )


# =========================================================
# ADMIN COMENTARIO
# =========================================================
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'comerciante',
        'fecha_creacion',
    )

    list_filter = (
        'fecha_creacion',
    )

    search_fields = (
        'contenido',
        'comerciante__nombre_apellido',
        'comerciante__email',
        'post__titulo',
    )


# =========================================================
# ADMIN BENEFICIO
# =========================================================
@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'categoria',
        'estado',
        'vence',
        'fecha_creacion',
    )

    list_filter = (
        'categoria',
        'estado',
    )

    search_fields = (
        'titulo',
        'descripcion',
    )


# =========================================================
# ADMIN PROVEEDOR
# =========================================================
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_empresa',
        'email',
        'whatsapp',
        'activo',
        'verificado',
        'fecha_registro',
    )

    list_filter = (
        'activo',
        'verificado',
        'destacado',
        'cobertura',
    )

    search_fields = (
        'nombre_empresa',
        'email',
        'nombre_contacto',
        'descripcion',
    )

    ordering = (
        '-fecha_registro',
    )


# =========================================================
# ADMIN PROPUESTA
# =========================================================
@admin.register(Propuesta)
class PropuestaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'proveedor',
        'zona_geografica',
    )

    list_filter = (
        'zona_geografica',
    )

    search_fields = (
        'titulo',
        'proveedor__nombre_empresa',
        'rubros_ofertados',
    )
