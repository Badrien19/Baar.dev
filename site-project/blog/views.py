from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post
from .models import Game
from users.models import Profile
from .forms import GameForm
# Create your views here.


def home(request):
	context = {
        'posts': Post.objects.all()
    }
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
	return render(request, 'blog/about.html')

def fcfw(request):
	users = Profile.objects.order_by('-elo')
	return render(request, 'blog/fcfw.html', {'users' : users})

def history(request):
    context = {
        'games' : reversed(Game.objects.all())
    }
    return render(request, 'blog/history.html', context)

def createGame(request):
    form = GameForm()
    if request.method == 'POST':
        #print ("RESULT: ", request.POST.get('winner'))
        #print ("RESULT: ", request.POST.get('looser'))
        #print ("RESULT: ", request.POST.get('ratio'))
        #print ("RESULT: ", request.POST.get('draw'))
        
        draw = request.POST.get('draw')
        winner = Profile.objects.get(user_id=request.POST.get('winner'))
        looser = Profile.objects.get(user_id=request.POST.get('looser'))


        if draw:
            ratio = 5
            winner.draw += 1
            looser.draw += 1
        else:
            ratio = request.POST.get('ratio')
            winner.victory += 1
            looser.loose += 1

        chance_w = float(int(winner.elo) / (int(winner.elo) + int(looser.elo)))
        chance_l = float(int(looser.elo) / (int(winner.elo) + int(looser.elo)))

        winner.elo = round(float(winner.elo) + float(ratio) * (1 - (float(chance_w))), 2)
        looser.elo = round(float(looser.elo) + float(ratio) * (0 - (float(chance_l))), 2)

        winner.save()
        looser.save()
 
        form = GameForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.stat_winner = round(float(ratio) * (1 - (float(chance_w))), 2)
            instance.stat_looser = round(float(ratio) * (0 - (float(chance_l))), 2)
            instance.save()
            return redirect('/fcfw')

    context = {'form':form}
    return render(request, 'blog/game_form.html', context)