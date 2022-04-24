from django.contrib import admin
from .models import *


class ArtistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'repertoire', 'photo')
    list_display_links = ('id', 'name', 'surname')


class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class TracksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_date', 'genre')
    list_display_links = ('id', 'title')


class LyricsAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_id', 'content', 'poet', 'composer')
    list_display_links = ('id', 'track_id',)


class ChartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class TracksArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_id', 'track_id')
    list_display_links = ('artist_id', 'track_id')


admin.site.register(Artists, ArtistsAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Tracks, TracksAdmin)
admin.site.register(Lyrics, LyricsAdmin)
admin.site.register(Charts, ChartsAdmin)
admin.site.register(TracksArtist, TracksArtistAdmin)
