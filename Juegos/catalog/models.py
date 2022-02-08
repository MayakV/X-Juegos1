from django.db import models
from django.template.defaultfilters import slugify
from Juegos.settings import BASE_DIR, GAMES_DIR
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from os.path import isfile
# Create your models here.


class Category(models.Model):
    """Model representing a game category."""
    name = models.CharField(max_length=200, help_text='Enter category (genre)')
    #full_name = models.CharField(max_length=200, null=True, help_text='Enter full name')
    #img_path = models.CharField(max_length=200, default="img/", help_text='Enter path to the image')
    slug = models.SlugField(null=False, unique=True)

    def get_games(self):
        return Game.objects.filter(category=self.pk)

    def get_absolute_url(self):
        """Get a url for top games in this category"""
        return reverse('all-games-category', kwargs={'slug': self.slug})

#    def get_all_page_url(self, page_number):
#        """Get a url for all games in this category"""
#        return reverse('all-games-category-page', kwargs={'slug': self.slug, 'pg': page_number})

    def get_new_url(self):
        """Get a url for new games in this category"""
        return reverse('new-games-category', kwargs={'slug': self.slug})

    def get_top_url(self):
        """Get a url for top games in this category"""
        return reverse('top-games-category', kwargs={'slug': self.slug})

    def get_image_path(self):
        return 'category_thumbnails/' + self.slug + '.jpg'

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Game(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    #author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the game')
    # isbn = models.CharField('ISBN', max_length=13,
    #                         help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    #thumb_path = models.CharField(max_length=200, default="img/", help_text='Enter path to the thumbnail image')
    slug = models.SlugField(null=slugify(title), unique=True)

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    category = models.ManyToManyField(Category, help_text='Select a category for this game')

    date_published = models.DateField(default='1990-01-01');

    times_played = models.IntegerField(default=0);

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_game_path(self):
        #return os.path.join(BASE_DIR, "catalog/static"),
        return 'games/' + slugify(self.title) + '/'

    def get_full_game_path(self):
        return BASE_DIR + "/catalog/static/games/" + slugify(self.title) + "/"

    def get_thumbnail_path(self):
        #return os.path.join(BASE_DIR, "catalog/static"),
        full_path = self.get_full_game_path()
        file_name = ""
        if isfile(full_path + "thumbnail.jpg"):
            file_name = "thumbnail.jpg"
        elif isfile(full_path + "thumbnail.png"):
            file_name = "thumbnail.png"
        return self.get_game_path() + file_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('game-detail', args=[str(self.slug)])

    def get_fullscreen_url(self):
        return "https://jgs.x-juegos.es/" + self.slug

    def display_category(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(category.name for category in self.category.all()[:3])

    display_category.short_description = 'Category'
