from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class ArtistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'repertoire', 'get_html_photo')
    list_display_links = ('id', 'name', 'surname')
    fields = ('name', 'surname', 'repertoire', 'photo', 'get_html_photo')
    readonly_fields = ('id', 'get_html_photo')
    save_on_top = True
    save_as = True


    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src = '{object.photo.url}' width = 50>")

    get_html_photo.short_description = "Miniature"


class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    fields = ('title', 'photo')
    readonly_fields = ('id',)
    save_as = True


class TracksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_date', 'genre')
    list_display_links = ('id', 'title')
    fields = ('title', 'artist', 'file', 'genre','published_date')
    readonly_fields = ('id',)
    save_as = True


class LyricsAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_id', 'content', 'poet', 'composer')
    list_display_links = ('id', 'track_id',)
    fields = ('track_id','content', 'poet', 'composer', 'photo')
    readonly_fields = ('id',)
    save_as = True
    save_on_top = True


class ChartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    fields = ('title', 'photo')
    readonly_fields = ('id',)
    save_as = True


class TracksArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_id', 'track_id')
    list_display_links = ('artist_id', 'track_id')
    fields = ('artist_id', 'track_id')
    save_as = True


admin.site.register(Artists, ArtistsAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Tracks, TracksAdmin)
admin.site.register(Lyrics, LyricsAdmin)
admin.site.register(Charts, ChartsAdmin)
admin.site.register(TracksArtist, TracksArtistAdmin)

admin.site.site_title = 'Admin-panel of Qazmusic'
