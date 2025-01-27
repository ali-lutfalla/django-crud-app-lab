from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog
from .forms import FeedingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def dog_index(request):
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html',{'dogs': dogs})

@login_required
def dog_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', {'dog': dog, 'feeding_form': feeding_form})

class DogCreate(LoginRequiredMixin, CreateView):
    model = Dog
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class DogUpdate(LoginRequiredMixin, UpdateView):
    model = Dog
    fields = ['breed', 'description', 'age']

class DogDelete(LoginRequiredMixin, DeleteView):
    model = Dog
    success_url = '/dogs/'

@login_required
def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():

        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('dog-detail', dog_id=dog_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)




