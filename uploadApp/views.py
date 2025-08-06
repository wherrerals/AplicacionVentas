# views.py
from django.shortcuts import render, redirect
from uploadApp.form import ImagenForm
from uploadApp.models.imgdb import ImagenDB

def subir_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ver_imagenes')  # redirige a una lista u otra vista
    else:
        form = ImagenForm()
    
    return render(request, 'upload_img.html', {'form': form})


def ver_imagenes(request):
    imagenes = ImagenDB.objects.all()
    return render(request, 'view_img.html', {'imagenes': imagenes})


def subir_multiples_imagenes(request):
    if request.method == 'POST':
        nombre_base = request.POST.get('nombre', 'Imagen')
        archivos = request.FILES.getlist('archivos')
        
        for archivo in archivos:
            ImagenDB.objects.create(nombre=nombre_base, archivo=archivo)

        return redirect('ver_imagenes')
    
    return render(request, 'upload_all_img.html')