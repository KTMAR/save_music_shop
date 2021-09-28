from django.shortcuts import render
from django import views

from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView

from .mixins import CartMixin
from .models import Artist, Album, Customer, ImageGallery, Cart
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login


class BaseView(View):

    def get(self, request, *args, **kwargs):
        album = Album.objects.all()
        artist = Artist.objects.all()
        gallery = ImageGallery.objects.all()

        context = {
            'album': album,
            'artist': artist,
            'gallery': gallery,
        }
        return render(request, 'index.html', context)


# class ArtistDetailView(views.generic.DetailView):
#     model = Artist
#     queryset = Artist.objects.all()
#     template_name = 'artist/artist_detail.html'
#     slug_url_kwarg = 'artist_slug'
#     context_object_name = 'artist'

# views.generic.DetailView

class AlbumDetailView(DetailView,CartMixin):

    CT_MODEL_MODEL_CLASS = {
        'album': Album,
    }

    # def dispatch(self, request, *args, **kwargs):
    #     self.model = self.CT_MODEL_MODEL_CLASS[kwargs['album_detail']]
    #     self.queryset = self.model._base_manager.all()
    #     return super().dispatch(request, *args, **kwargs)
    #
    model = Album
    queryset = Album.objects.all()
    template_name = 'album/album_detail.html'
    slug_url_kwarg = 'album_slug'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class LoginView(views.View):
    """Инстациируем форму"""

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,

        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        # если че то не получилось при авторизации(не валидна)
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,

        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            """Что бы присвоить пассворд,нужно сначала сохранить юзера(new_user),а потом уже задать ему пароль"""
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            """Затем создаем покупателя"""
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            """Залогиним юзера"""
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        print(kwargs.get('artist_slug'))
        print(kwargs.get('album_slug'))

        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        context = {
            'cart': self.cart,
        }
        return render(request, 'cart.html', context)
