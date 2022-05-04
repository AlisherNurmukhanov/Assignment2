from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *
from .utils import *


class QazmusicHome(DataMixin, ListView):
    model = Tracks
    template_name = 'qazmusic/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowArtists(DataMixin, ListView):
    model = Artists
    template_name = 'qazmusic/artists.html'
    context_object_name = 'artists_list'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic - Artists')

        return dict(list(context.items()) + list(c_def.items()))


class ArtistView(DataMixin, DetailView):
    model = Artists
    template_name = 'qazmusic/artist-view.html'
    pk_url_kwarg = 'artist_id'
    slug_url_kwarg = 'fullname'
    context_object_name = 'artist'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str('qazmusic - ' + str(context['artist'])))
        return dict(list(context.items()) + list(c_def.items()))


class ShowGenres(DataMixin, ListView):
    model = Genres
    template_name = 'qazmusic/show_genres.html'
    context_object_name = 'genres'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic - Genres')
        return dict(list(context.items()) + list(c_def.items()))


class GenreView(DataMixin, DetailView):
    model = Genres
    template_name = 'qazmusic/genre_view.html'
    pk_url_kwarg = 'genre_id'
    slug_url_kwarg = 'title'
    context_object_name = 'genre'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str('qazmusic - ' + str(context['genre'])))
        return dict(list(context.items()) + list(c_def.items()))


class ShowCharts(DataMixin, ListView):
    model = Charts
    template_name = 'qazmusic/show_charts.html'
    context_object_name = 'charts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic - Charts')
        return dict(list(context.items()) + list(c_def.items()))


class ChartView(DataMixin, DetailView):
    model = Charts
    template_name = 'qazmusic/chart_view.html'
    pk_url_kwarg = 'chart_id'
    context_object_name = 'chart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str('qazmusic - ' + str(context['chart'])))
        context['tracks_in_chart'] = get_charts_tracks(self.kwargs.get('chart_id'))
        return dict(list(context.items()) + list(c_def.items()))


class ShowLyrics(DataMixin, ListView):
    model = Lyrics
    template_name = 'qazmusic/show_lyrics.html'
    context_object_name = 'lyrics'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic - Lyrics')
        return dict(list(context.items()) + list(c_def.items()))


class LyricView(DataMixin, DetailView):
    model = Lyrics
    template_name = 'qazmusic/lyric_view.html'
    pk_url_kwarg = 'lyric_id'
    slug_url_kwarg = 'track_title'
    context_object_name = 'lyric'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str('qazmusic' + str(context['lyric'])))
        context['track_title'] = get_tracks().get(pk=context['lyric'].track_id_id)
        context['artist'] = get_artists().get(pk=context['track_title'].artist_id)
        return dict(list(context.items()) + list(c_def.items()))


# регистрация
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'qazmusic/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic - Register')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        mail = EmailMessage(
             'Verify email',
             'Please, verify the your account',
             settings.EMAIL_HOST_USER,
             to=[form.cleaned_data.get('email')]
        )
        mail.fail_silently = False
        mail.send()

        if mail:
            user = form.save()
            login(self.request, user)
            return redirect('home')
        else:
            return redirect('register')


# логин (авторизация)
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'qazmusic/auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='qazmusic - Login')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# выйти из профиля
def logout_user(request):
    logout(request)
    return redirect('login')


def show_archive(request):
    current_genre = Genres.objects.get(pk=3)
    context = {
        'title': 'Golden fund',
        'header_menu': header_menu,
        'tracks': get_tracks(),
        'artists': get_artists(),
        'genre': current_genre
    }
    return render(request, 'qazmusic/genre_view.html', context=context)


def upload(request):
    succesful = False
    if request.method == 'POST':
        form = UploadMusic(request.POST, request.FILES)
        if form.is_valid():
            succesful = True
            form.save()

    else:
        form = UploadMusic()

    context = {
        'title': 'qazmusic - Upload',
        'header_menu': header_menu,
        'form': form,
        'genres': get_genres(),
        'artists': get_artists(),
        'upload_message': succesful
    }
    return render(request, 'qazmusic/upload.html', context=context)


def update_track(request, pk):
    succesful = False
    track = Tracks.objects.get(pk=pk)
    form = UploadMusic(instance=track)
    if request.method == 'POST':
        form = UploadMusic(request.POST, instance=track)
        if form.is_valid():
            succesful = True
            form.save()

    context = {
        'title': 'qazmusic - Upload',
        'header_menu': header_menu,
        'form': form,
        'genres': get_genres(),
        'artists': get_artists(),
        'upload_message': succesful
    }

    return render(request, 'qazmusic/upload.html', context=context)


def delete_track(request, pk):
    track = Tracks.objects.get(pk=pk)
    form = UploadMusic(instance=track)
    if request.method == 'POST':
        track.delete()
        return redirect('/artists')

    context = {
        'title': 'qazmusic - Upload',
        'header_menu': header_menu,
        'form': form,
        'item': track
    }
    return render(request, 'qazmusic/delete_track.html', context=context)


def show_contacts_page(request):
    is_send_message = False
    is_exists_error = False

    if request.method == 'POST':
        contact_form = ContactsForm(request.POST, request.FILES)

        if contact_form.is_valid():
            subject = contact_form.cleaned_data['subject']
            content = contact_form.cleaned_data['content']
            email = contact_form.cleaned_data['email']
            photo = request.FILES['photo']

            mail = EmailMessage(subject, content, settings.EMAIL_HOST_USER, to=[email])
            mail.attach(photo.name, photo.read())
            mail.send()

            if mail:
                is_send_message = True
            else:
                is_exists_error = True
    else:
        contact_form = ContactsForm()

    context = {
        'form': contact_form,
        'is_send_message': is_send_message,
        'header_menu': header_menu,
        'is_exists_error': is_exists_error,
        'title': 'Contacts'
    }

    return render(request, 'qazmusic/contacts.html', context=context)
