from django.shortcuts import render
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Rejestracja nowego użytkownika"""
    if request.method != "POST":
        #Wyświetlanie pustego formularza rejestracji
        form = UserCreationForm()
    else:
        #Przetworzenie wypełnionego formularza
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            #Zalogowanie użytkownika, a następnie przekierowanie na strone główną
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('leaarning_logs:index'))
            
    context = {'form': form}
    return render(request, 'users/register.html', context)

# Create your views here.
