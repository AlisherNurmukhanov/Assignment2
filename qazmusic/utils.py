from .models import *

header_menu = {
    'Artists': 'artists',
    'Genres': 'genres',
    'Charts': 'charts',
    'Lyrics': 'lyrics',
    'Golden fund': 'archive',
    'Upload': 'upload',
    'Contacts': 'contacts',
}


# mixins
class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['header_menu'] = header_menu
        context['tracks'] = get_tracks()
        return context


# useful objects
def get_tracks():
    get_tracks = Tracks.objects.all()
    return get_tracks


def get_artists():
    get_artists = Artists.objects.all()
    return get_artists


def get_genres():
    get_genres = Genres.objects.all()
    return get_genres


def get_charts():
    get_charts = Charts.objects.all()
    return get_charts


def get_lyrics():
    get_lyrics = Lyrics.objects.all()
    return get_lyrics


# utils
def get_tracks_artists(id):
    tracks_artists = TracksArtist.objects.filter(artist_id=id)
    return tracks_artists


def get_charts_tracks(chart_id):
    tracks_in_chart = Tracks.objects.filter(charts__exact=chart_id)
    return tracks_in_chart
