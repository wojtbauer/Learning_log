from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Strona główna dla aplikacji learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Wyświetnie wszystkich tematów"""
    topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Wyświetla pojedynczy temat i wszystkie powiązane z nim wpisy"""
    topic = Topic.objects.get(id=topic_id)
    #Upewniamy sie że temat należy do zalogowanego użytkownika
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != "POST":
        """Nie przekazano żadnych danych, należy utowrzyc pusty formularz"""
        form = TopicForm()
    else:
        """Przekazano dane za pomocą żądania POST, należy je powtórzyć"""
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))        
            
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required    
def new_entry(request, topic_id):
    """Dodawanie nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        #Nie przekazano żadnych danych, należy utworzyć nowy formularz
        form = EntryForm()
    else:
        #Przekazano dane za pomocą żadania POST, należy je przetworzyć
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
            args=[topic_id]))
            
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        #Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu
        form = EntryForm(instance=entry)
    else:
        #Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', 
            args=[topic.id]))
            
    context = {'entry': entry,'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


# Create your views here.
