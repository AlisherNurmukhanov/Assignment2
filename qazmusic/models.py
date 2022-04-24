from django.db import models
from django.urls import reverse


class Artists(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    surname = models.CharField(max_length=255, db_index=True, null=True)
    repertoire = models.IntegerField(verbose_name='repertoire', null=True)
    photo = models.ImageField(upload_to='photo/', null=True)

    def get_absolute_url(self):
        return reverse('artist-view', kwargs={
            'artist_id': self.pk,
            'fullname': self.name + '-' + self.surname
        })

    def __str__(self):
        return self.name + ' ' + self.surname

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'


class Genres(models.Model):
    title = models.CharField(max_length=50, db_index=True)

    def get_absolute_url(self):
        return reverse('genre-view', kwargs={
            'genre_id': self.pk,
            'title': self.title.replace(' ', '-')
        })

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Tracks(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    file = models.FileField(verbose_name='file', upload_to='tracks/')
    published_date = models.DateField(auto_now=False)
    genre = models.ForeignKey(Genres, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'


class Lyrics(models.Model):
    track_id = models.ForeignKey(Tracks, on_delete=models.PROTECT)
    poet = models.CharField(max_length=255, db_index=True, null=True)
    composer = models.CharField(max_length=255, db_index=True, null=True)
    content = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('lyric-view', kwargs={
            'lyric_id': self.pk,
            'track_title': self.track_id.title.replace(' ', '-')
        })

    def __str__(self):
        return self.track_id.title

    class Meta:
        verbose_name = 'Lyric'
        verbose_name_plural = 'Lyrics'


class Charts(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    number_of_tracks = models.ManyToManyField(Tracks, blank=True)

    def get_absolute_url(self):
        return reverse('chart_view', kwargs={
            'chart_id': self.pk,
        })

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Chart'
        verbose_name_plural = 'Charts'


class TracksArtist(models.Model):
    artist_id = models.ForeignKey(Artists, on_delete=models.CASCADE)
    track_id = models.ForeignKey(Tracks, on_delete=models.CASCADE)
