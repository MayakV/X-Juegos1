from django.urls import path
from django_distill import distill_path
from . import views
from .models import Game, Category
from math import ceil
from Juegos.settings import GAMES_ON_PAGE
from django.utils.translation import gettext



def get_index():
    # The index URI path, '', contains no parameters, named or otherwise.
    # You can simply just return nothing here.
    return None


def get_games_pages():
    # This function needs to return an iterable of dictionaries. Dictionaries
    # are required as the URL this distill function is for has named parameters.
    # You can just export a small subset of values here if you wish to
    # limit what pages will be generated.
    num_pages = ceil(Game.objects.count() / GAMES_ON_PAGE)
    for pg in range(1, num_pages + 1):
        yield {'page': pg}


def get_games_pages_in_categories():
    # This function needs to return an iterable of dictionaries. Dictionaries
    # are required as the URL this distill function is for has named parameters.
    # You can just export a small subset of values here if you wish to
    # limit what pages will be generated.
    for cat in Category.objects.all():
        num_pages = ceil(Game.objects.filter(pk=cat.pk).count() / GAMES_ON_PAGE)
        for pg in range(1, num_pages + 1):
            yield {'slug': cat.slug, 'page': pg}


def get_all_games():
    # This function needs to return an iterable of dictionaries. Dictionaries
    # are required as the URL this distill function is for has named parameters.
    # You can just export a small subset of values here if you wish to
    # limit what pages will be generated.
    for game in Game.objects.all():
        yield {'slug': game.slug}


def get_all_categories():
    # This function needs to return an iterable of dictionaries. Dictionaries
    # are required as the URL this distill function is for has named parameters.
    # You can just export a small subset of values here if you wish to
    # limit what pages will be generated.
    for cat in Category.objects.all():
        yield {'slug': cat.slug}


urlpatterns = [
    #path('', views.index, name='index'),
    path('static/', views.static_home, name='shome'),
    #path('home/', views.HomeView.as_view(), name='home'),
    distill_path('',
                 views.HomeView.as_view(),
                 name='home',
                 distill_func=get_index),

    ## Game views
    distill_path(gettext('all-games/'),
                 views.AllGamesView.as_view(),
                 name='all-games',
                 distill_func=get_index),
    distill_path(gettext('all-games/page/<int:page>/'),
                 views.AllGamesView.as_view(),
                 name='all-games-page',
                 distill_func=get_games_pages),
    distill_path(gettext('new-games/'),
                 views.NewGamesView.as_view(),
                 name='new-games',
                 distill_func=get_index),
    distill_path(gettext('new-games/page/<int:page>/'),
                 views.NewGamesView.as_view(),
                 name='new-games-page',
                 distill_func=get_games_pages),
    distill_path(gettext('top-games/'),
                 views.TopGamesView.as_view(),
                 name='top-games',
                 distill_func=get_index),
    distill_path(gettext('top-games/page/<int:page>/'),
                 views.TopGamesView.as_view(),
                 name='top-games-page',
                 distill_func=get_games_pages),

    ## Game views by category
    distill_path(gettext('all-games/<slug:slug>/'),
                 views.AllGamesCategoryView.as_view(),
                 name='all-games-category',
                 distill_func=get_all_categories),
    distill_path(gettext('all-games/<slug:slug>/page/<int:page>/'),
                 views.AllGamesCategoryView.as_view(),
                 name='all-games-category-page',
                 distill_func=get_games_pages_in_categories),
    distill_path(gettext('new-games/<slug:slug>/'),
                 views.NewGamesCategoryView.as_view(),
                 name='new-games-category',
                 distill_func=get_all_categories),
    distill_path(gettext('new-games/<slug:slug>/page/<int:page>/'),
                 views.NewGamesCategoryView.as_view(),
                 name='new-games-category-page',
                 distill_func=get_games_pages_in_categories),
    distill_path(gettext('top-games/<slug:slug>/'),
                 views.TopGamesCategoryView.as_view(),
                 name='top-games-category',
                 distill_func=get_all_categories),
    distill_path(gettext('top-games/<slug:slug>/page/<int:page>/'),
                 views.TopGamesCategoryView.as_view(),
                 name='top-games-category-page',
                 distill_func=get_games_pages_in_categories),

    distill_path(gettext('game/<slug:slug>/'),
                 views.GameView.as_view(),
                 name='game-detail',
                 distill_func=get_all_games),

    #distill_path('game/fs/<slug:slug>/',
    #             views.load_game,
    #             name='game-detail-fullscreen',
    #             distill_func=get_all_games),
]


