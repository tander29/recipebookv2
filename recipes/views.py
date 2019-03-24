from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponseRedirect, reverse
from recipes.models import Recipe, Author, User
from recipes.forms import Add_Recipe, Add_Author, SignupForm, LoginForm, EditRecipe
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    recipes = Recipe.objects.all()
    recipebook = {'recipes': recipes}
    return render(request, 'index.html', recipebook)


def recipe_view(request, recipe_id):
    """Original func, changed var of the page options to reflect data"""
    page_options = {}
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    page_options.update({'recipe': recipe})
    page_options.update(edit_page_options(request, recipe))
    if request.method == 'POST':
        update_recipe(request, recipe)
        return HttpResponseRedirect(reverse('recipe', kwargs={"recipe_id": recipe_id}))
    return render(request, 'recipe.html', page_options)


def update_recipe(request, recipe):
    form = EditRecipe(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        recipe.title = data['title']
        recipe.description = data['description']
        recipe.instructions = data['instructions']
        recipe.time_required = data['time_required']
        recipe.save()
    return


@login_required()
def myfavorites(request):
    """User can see self favorited recipes"""
    html = 'myfavorites.html'
    page_options = {}
    if request.user.author:
        recipes = request.user.author.favorites.all()
        page_options.update({"recipes": recipes})
    return render(request, html, page_options)


def favorite(request, recipe_id):
    """To favorite a recipe """
    user = request.user.author
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe not in user.favorites.all():
        user.favorites.add(recipe)
    elif recipe in user.favorites.all():
        user.favorites.remove(recipe)
    return HttpResponseRedirect(reverse('recipe',
                                        kwargs={"recipe_id": recipe_id}))


def edit_page_options(request, recipe):
    """Page options for logged in users and forms Recipe page"""
    page_options = {}
    if request.user.is_anonymous:
        return page_options
    if request.user.is_staff or request.user.author == recipe.author:
        form = EditRecipe(initial={"title": recipe.title,
                                   "description": recipe.description,
                                   "instructions": recipe.instructions,
                                   "time_required": recipe.time_required,
                                   })
        page_options.update({"form": form})
    favorited = False
    try:
        if recipe in request.user.author.favorites.all():
            favorited = True
    except:
        pass
    page_options.update({"favorited": favorited})
    return page_options


def author_view(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.filter(author=author)
    recipebook = {'recipes': recipes, 'author': author}
    return render(request, 'author.html', recipebook)


@login_required()
def add_recipe(request):
    form = None
    if request.method == 'POST':
        form = Add_Recipe(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                instructions=data['instructions'],
                author=data['author'],
                time_required=data['time_required']
            )
            return render(request, 'updated.html')
    else:
        form = Add_Recipe()
        if not request.user.is_staff:
            form.fields['author'].queryset = Author.objects.filter(
                user=request.user)
    return render(request, 'add_recipe.html', {'form': form})


@login_required()
@staff_member_required(login_url='error')
def add_author(request):
    form = None
    if request.method == 'POST':
        form = Add_Author(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data['name'])
            Author.objects.create(
                name=data['name'],
                bio=data['bio'],
                user=new_user
            )
            return render(request, 'updated.html')
    else:
        form = Add_Author()

    return render(request, 'add_author.html', {'form': form})


def signup_view(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])
            login(request, user)
            Author.objects.create(
                name=data['name'],
                user=user
            )
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SignupForm()
    return render(request, 'generic_form.html', {"form": form})


def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})


def logout_view(request):

    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def error_view(request):
    return render(request, 'error.html')
