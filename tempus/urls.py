"""
URL configuration for tempus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from tempus.views import (
    dashboard_view,
    ficha_config_view,
    fichas_create_view,
    fichas_view,
    login_view,
    logout_view,
    matrix_delete_view,
    matrix_detail_view,
    matrix_list_view,
    matrix_upload_view,
    profile_view,
    sites_ambiences_view,
    users_delete_non_admin_view,
    users_plant_upload_template_view,
    users_plant_upload_view,
    users_panel_view,
    users_upload_template_view,
    users_upload_view,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('perfil/', profile_view, name='profile'),
    path('usuarios/', users_panel_view, name='users-panel'),
    path('usuarios/eliminar-no-admin/', users_delete_non_admin_view, name='users-delete-non-admin'),
    path('usuarios/cargar/', users_upload_view, name='users-upload'),
    path('usuarios/cargar/plantilla/', users_upload_template_view, name='users-upload-template'),
    path('usuarios/cargar/planta/plantilla/', users_plant_upload_template_view, name='users-plant-upload-template'),
    path('usuarios/cargar/planta/', users_plant_upload_view, name='users-upload-plant'),
    path('fichas/', fichas_view, name='fichas-panel'),
    path('fichas/<int:pk>/configurar/', ficha_config_view, name='ficha-config'),
    path('fichas/crear/', fichas_create_view, name='fichas-create'),
    path('sedes-ambientes/', sites_ambiences_view, name='sites-ambiences'),
    path('matriz/cargar/', matrix_upload_view, name='matrix-upload'),
    path('matriz/', matrix_list_view, name='matrix-list'),
    path('matriz/<int:pk>/', matrix_detail_view, name='matrix-detail'),
    path('matriz/<int:pk>/eliminar/', matrix_delete_view, name='matrix-delete'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
