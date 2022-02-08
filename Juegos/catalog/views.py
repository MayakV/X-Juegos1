from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse
import math

# Create your views here.

from .models import Game, Category
from Juegos.settings import GAMES_ON_PAGE, BASE_DIR, GAMES_DIR
#class BookListView(generic.ListView):
#    model = Game


class HomeView(generic.ListView):
    model = Category
    context_object_name = 'home'   # your own name for the list as a template variable
    #queryset = Game.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    queryset = Category.objects.all()
    #paginate_by = 3
    template_name = 'catalog/home.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = self.queryset
        context['new_games'] = Game.objects.order_by("-date_published")[:3]
        context['top_games'] = Game.objects.order_by("-times_played")[:3]
        return context


class GamesView(generic.ListView):
    #context_object_name = 'game-detail'
    #context_object_name = 'all_games_list'
    model = Game
    page = 1
    queryset = Game.objects.all()
    page_view_url = ''
    template_name = 'catalog/category.html'

    def get(self, request, *args, **kwargs):
        self.page = kwargs.get("page", 1)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GamesView, self).get_context_data(**kwargs)

        paginator = Paginator(self.queryset, GAMES_ON_PAGE)
        context["is_paginated"] = True

        context['games'] = paginator.get_page(self.page)
        context['categories'] = Category.objects.all() #self.queryset

        min_page = max(self.page - 5, 1)
        max_page = min(min_page + 10, paginator.num_pages) + 1
        context["pages_to_display"] = range(min_page, max_page)
        context["any_page"] = reverse(self.page_view_url, kwargs={'page': 1})[:-2]
        context["first_page"] = context["any_page"] + '1/'
        context["prev_page"] = context["any_page"] + str(max(self.page - 1, 1)) + '/'
        context["next_page"] = context["any_page"] + str(min(self.page + 1, paginator.num_pages)) + '/'
        context["last_page"] = context["any_page"] + str(paginator.num_pages)

        return context


class AllGamesView(GamesView):
    queryset = Game.objects.order_by("title")
    page_view_url = 'all-games-page'

    def get_context_data(self, **kwargs):

        context = super(AllGamesView, self).get_context_data(**kwargs)
        context['page_type'] = 'all'
        context['new_games'] = Game.objects.order_by("-date_published")[:7]
        context['top_games'] = Game.objects.order_by("-times_played")[:7]
        return context


class NewGamesView(GamesView):
    queryset = Game.objects.order_by("-date_published")
    page_view_url = 'new-games-page'

    def get_context_data(self, **kwargs):
        context = super(NewGamesView, self).get_context_data(**kwargs)
        context['page_type'] = 'new'
        context['all_games'] = True
        context['top_games'] = Game.objects.order_by("-times_played")[:14]
        return context


class TopGamesView(GamesView):
    queryset = Game.objects.order_by("-times_played")
    page_view_url = 'top-games-page'
    print(BASE_DIR)

    def get_context_data(self, **kwargs):
        context = super(TopGamesView, self).get_context_data(**kwargs)
        context['page_type'] = 'top'
        context['all_games'] = True
        context['new_games'] = Game.objects.order_by("-date_published")[:14]
        return context


class GamesCategoryView(generic.DetailView):
    context_object_name = 'category'
    model = Category
    page = 1
    page_view_url = ''
    order_by = ''
    template_name = 'catalog/category.html'

    def get(self, request, *args, **kwargs):
        self.page = kwargs.get("page", 1)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GamesCategoryView, self).get_context_data(**kwargs)

        paginator = Paginator(Game.objects.filter(category=self.object.pk).order_by(self.order_by), GAMES_ON_PAGE)
        context["is_paginated"] = True

        context['games'] = paginator.get_page(self.page)
        context['categories'] = Category.objects.all() #self.queryset

        min_page = max(self.page - 5, 1)
        max_page = min(min_page + 10, paginator.num_pages) + 1
        context["pages_to_display"] = range(min_page, max_page)
        context["any_page"] = reverse(self.page_view_url, kwargs={'slug': self.object.slug, 'page': 1})[:-2]
        context["first_page"] = context["any_page"] + '1/'
        context["prev_page"] = context["any_page"] + str(max(self.page - 1, 1)) + '/'
        context["next_page"] = context["any_page"] + str(min(self.page + 1, paginator.num_pages)) + '/'
        context["last_page"] = context["any_page"] + str(paginator.num_pages)

        return context


class AllGamesCategoryView(GamesCategoryView):
    order_by = 'title'
    page_view_url = 'all-games-category-page'

    def get_context_data(self, **kwargs):
        context = super(AllGamesCategoryView, self).get_context_data(**kwargs)
        context['page_type'] = 'all'
        context['new_games'] = Game.objects.filter(category=self.object.pk).order_by("-date_published")[:7]
        context['top_games'] = Game.objects.filter(category=self.object.pk).order_by("-times_played")[:7]
        return context


class NewGamesCategoryView(GamesCategoryView):
    order_by = '-date_published'
    page_view_url = 'new-games-category-page'

    def get_context_data(self, **kwargs):
        context = super(NewGamesCategoryView, self).get_context_data(**kwargs)
        context['page_type'] = 'new'
        context['all_games'] = True
        context['top_games'] = Game.objects.filter(category=self.object.pk).order_by("-times_played")[:7]
        return context


class TopGamesCategoryView(GamesCategoryView):
    order_by = '-times_played'
    page_view_url = 'top-games-category-page'

    def get_context_data(self, **kwargs):
        context = super(TopGamesCategoryView, self).get_context_data(**kwargs)
        context['page_type'] = 'top'
        context['all_games'] = True
        context['new_games'] = Game.objects.filter(category=self.object.pk).order_by("-date_published")[:7]
        return context


class GameView(generic.DetailView):
    context_object_name = 'game_object'
    model = Game
    template_name = 'catalog/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # self.queryset
        # Entry.objects.order_by('headline')[0]
        # Entry.objects.order_by('headline')[0:1].get()
        context['category'] = self.object.category.all()[0]  # self.queryset
        cats = [cat.pk for cat in self.object.category.all()]
        # TODO This is a bad way of searching related games. I should check ho many shared tags each game has and order based on that
        context['related_games'] = Game.objects.filter(category__pk__in=cats).exclude(pk=self.object.pk).order_by("-date_published").distinct()[:5]
        context['new_games'] = Game.objects.filter(category__pk=context['category'].pk).exclude(pk=self.object.pk).order_by("-date_published")[:5]
        context['top_games'] = Game.objects.filter(category__pk=context['category'].pk).exclude(pk=self.object.pk).order_by("-times_played")[:5]
        return context


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_games = Game.objects.all().count()
    #num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    categories_start_with_a = Category.objects.filter(name__startswith='A').count()

    # The 'all()' is implied by default.
    #num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_games': num_games,
        'categories_start_with_a': categories_start_with_a,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def static_home(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'static_home.html')


def load_game(request, slug):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, slug + '/index.html')
