from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Game, Category
from Juegos.settings import BASE_DIR, GAMES_DIR
from django.template.defaultfilters import slugify
from os import listdir
from shutil import copytree
from datetime import datetime
from ftplib import FTP
#from modeltranslation.admin import TranslationAdmin
import logging

# Register your models here.

'''
# Define the admin class
class GameAdmin(admin.ModelAdmin):
    change_list_template = "templates/games_changelist.html"
    list_display = ('title', 'description', 'display_category', 'date_published', 'times_played')
    list_filter = ('date_published',)
    #   logger = logging.getLogger("django")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            #path('add-games/', self.add_games),
        ]
        return my_urls + urls

    def add_games(self, request):
        games_added = 0
        self.get_server_game_list()
        for directory in self.get_server_game_list():
            game_name = directory.rsplit('/', 1)[-1]
            if game_name not in (".", "..", "mj") and not Game.objects.filter(slug=slugify(game_name)).exists():
                game = Game(title=game_name,
                            description="",
                            slug=slugify(game_name),
                            date_published=datetime.date(datetime.now()))
                game.save()
                games_added += 1
        #self.message_user(request, games_added + " Games added")
        return HttpResponseRedirect("../")

    def get_server_game_list(self):
        server = FTP()
        server.connect('da1.v.fozzy.com')
        server.login('adminos1@x-juegos.es', 'h7J)aT9B14Sp')
        # You don't have to print this, because this command itself prints dir contents

        return server.nlst("public_html/jgs")
'''

# Register the admin class with the associated model
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    #exclude = ('name', )
    prepopulated_fields = {"slug": ("title",)}
    change_list_template = "games_changelist.html"
    list_display = ('title', 'description', 'display_category', 'date_published', 'times_played')
    list_filter = ('date_published',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add-games/', self.add_games),
        ]
        return my_urls + urls

    def add_games(self, request):
        games_added = 0
        #self.get_server_game_list()
        for directory in self.get_server_game_list():
            game_name = directory.rsplit('/', 1)[-1]
            if game_name not in (".", "..", "mj") and not Game.objects.filter(slug=slugify(game_name)).exists():
                game = Game(title=game_name,
                            description="",
                            slug=slugify(game_name),
                            date_published=datetime.date(datetime.now()))
                game.save()
                games_added += 1
        self.message_user(request, str(games_added) + " Games added")
        return HttpResponseRedirect("../")

    def get_server_game_list(self):
        server = FTP()
        server.connect('da1.v.fozzy.com')
        server.login('adminos1@x-juegos.es', 'h7J)aT9B14Sp')
        # You don't have to print this, because this command itself prints dir contents

        return server.nlst("public_html/jgs")

    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): #admin.ModelAdmin, #TranslationAdmin
    #exclude = ('name', )
    prepopulated_fields = {"slug": ("name",)}
    pass
