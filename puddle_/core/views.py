from django.shortcuts import render
from item.models import Item, category
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import login 
from .forms import SignUpForm
from django.contrib.messages.views import SuccessMessageMixin
from instagram.views import get_instagram_feed



def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = category.objects.all()
    image_urls = get_instagram_feed() # llama a la función get_instagram_feed() de tus vistas de instagram para obtener los enlaces de las imágenes
   
    return render(request, "core/index.html", {
        "items": items,
        "categories": categories,
        "image_urls": image_urls, # agrega los enlaces de las imágenes a los argumentos de la plantilla
    })

def contact(request):
    return render(request, "core/contact.html")


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    next_page = reverse_lazy('index')


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('index')
    success_message = 'La cuenta se ha creado con éxito.'

    def form_valid(self, form):
        print("form_valid() called")
        valid = super().form_valid(form)
        login(self.request, self.object)
        print("User logged in")
        return valid

    def form_invalid(self, form):
        print(form.errors)  # Añadir esta línea para imprimir los errores del formulario
        messages.error(self.request, 'Error al crear la cuenta. Por favor, verifica tus datos e inténtalo de nuevo.')
        return super().form_invalid(form)