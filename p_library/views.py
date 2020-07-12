from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import redirect
from p_library.models import Book
from p_library.models import Publisher
from p_library.models import Friend
from p_library.models import UserProfile
from django.http import HttpResponse
from django.template import loader
from p_library.models import Author  
from p_library.forms import AuthorForm, BookForm, FriendForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import formset_factory  
from django.http.response import HttpResponseRedirect
from django.shortcuts import render  
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib import auth  
from django.http.response import HttpResponseRedirect  
from django.urls import reverse_lazy
from django.views.generic import FormView  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, authenticate  
from p_library.forms import ProfileCreationForm
from allauth.socialaccount.models import SocialAccount
 

def index1(request):  
    context = {}  
    if request.user.is_authenticated:  
        context['username'] = request.user.username
        context['github_url'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']     
    return render(request, 'index1.html', context)

class RegisterView(FormView):  
  
    form_class = UserCreationForm  
  
    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(RegisterView, self).form_valid(form)  
  
  
class CreateUserProfile(FormView):  
  
    form_class = ProfileCreationForm  
    template_name = 'profile-create.html'  
    success_url = reverse_lazy('p_library:index1')  
  
    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('p_library:login'))  
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)  
  
    def form_valid(self, form):  
        instance = form.save(commit=False)  
        instance.user = self.request.user  
        instance.save()  
        return super(CreateUserProfile, self).form_valid(form)    
  
  
def login(request):  
    if request.method == 'POST':  
        form = AuthenticationForm(request=request, data=request.POST)  
        if form.is_valid():  
            auth.login(request, form.get_user())  
            return HttpResponseRedirect(reverse_lazy('p_library:index1'))  
    else:  
        context = {'form': AuthenticationForm()}  
        return render(request, 'login.html', context)  
  
  
def logout(request):  
    auth.logout(request)  
    return HttpResponseRedirect(reverse_lazy('p_library:index1'))

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    list_100 = range(1,101)
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "list_100": list_100,
    }
    return HttpResponse(template.render(biblio_data, request))
    
def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def publisher_list(request):  
    context = {}
    pubs = Publisher.objects.all()
    context['pubs'] = pubs
    if request.user.is_authenticated:  
        context['username'] = request.user.username
        #context['github_url'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']     
    return render(request, 'publishers.html', context)

def publisher_list1(request):
    template = loader.get_template('publishers.html')
    pubs = Publisher.objects.all()
    biblio_data = {      
        "pubs": pubs,
    }
    return HttpResponse(template.render(biblio_data, request))
    
def friend_list(request):
    template = loader.get_template('friend_list.html')
    friends = Friend.objects.all()
    biblio_data = {      
        "friends": friends,
    }
    return HttpResponse(template.render(biblio_data, request))
    
def authors_list(request):
    template = loader.get_template('authors_list.html')
    pubs = Author.objects.all()
    biblio_data = {      
        "object_list": pubs,
    }
    return HttpResponse(template.render(biblio_data, request))
    
class AuthorEdit(CreateView):  
    model = Author  
    form_class = AuthorForm  
    #success_url = reverse_lazy('p_library:author_list')
    success_url = '/authors'    
    template_name = 'author_edit.html'  
  
  
class AuthorList(ListView):  
    model = Author  
    template_name = 'authors_list.html'
    
class AuthorUpdate(UpdateView):
    model = Author
    success_url = reverse_lazy('p_library:author_list')
    fields = ["full_name", "birth_year", "country"]
    template_name = 'author_edit.html'
    
class AuthorDelete(DeleteView):
    model = Author
    form_class = AuthorForm
    fields = ["full_name", "birth_year", "country"]
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_delete.html'

class BookEdit(CreateView):  
    model = Book  
    form_class = BookForm  
    #success_url = reverse_lazy('p_library:book_list')
    success_url = '/books'    
    template_name = 'book_edit.html'  
  
  
class BookList(ListView):  
    model = Book  
    template_name = 'books_list.html'
    
class BookUpdate(UpdateView):
    model = Book
    success_url = reverse_lazy('p_library:friend_list')
    fields = ["friend"]
    template_name = 'book_edit.html'
    
class BookDelete(DeleteView):
    model = Book
    form_class = BookForm
    fields = ["friend"]
    success_url = reverse_lazy('p_library:book_list')
    template_name = 'book_delete.html'

    
def author_create_many(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  #  Первым делом, получим класс, который будет создавать наши формы. Обратите внимание на параметр `extra`, в данном случае он равен двум, это значит, что на странице с несколькими формами изначально будет появляться 2 формы создания авторов.
    if request.method == 'POST':  #  Наш обработчик будет обрабатывать и GET и POST запросы. POST запрос будет содержать в себе уже заполненные данные формы
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  #  Здесь мы заполняем формы формсета теми данными, которые пришли в запросе. Обратите внимание на параметр `prefix`. Мы можем иметь на странице не только несколько форм, но и разных формсетов, этот параметр позволяет их отличать в запросе.
        if author_formset.is_valid():  #  Проверяем, валидны ли данные формы
            for author_form in author_formset:  
                author_form.save()  #  Сохраним каждую форму в формсете
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))  #  После чего, переадресуем браузер на список всех авторов.
    else:  #  Если обработчик получил GET запрос, значит в ответ нужно просто "нарисовать" формы.
        author_formset = AuthorFormSet(prefix='authors')  #  Инициализируем формсет и ниже передаём его в контекст шаблона.
    return render(request, 'manage_authors.html', {'author_formset': author_formset})
    
def books_authors_create_many(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  
    BookFormSet = formset_factory(BookForm, extra=2)  
    if request.method == 'POST':  
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')  
        if author_formset.is_valid() and book_formset.is_valid():  
            for author_form in author_formset:  
                author_form.save()  
            for book_form in book_formset:  
                book_form.save()  
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))  
    else:  
        author_formset = AuthorFormSet(prefix='authors')  
        book_formset = BookFormSet(prefix='books')  
    return render(
	    request,  
		'manage_books_authors.html',  
		{  
	        'author_formset': author_formset,  
			'book_formset': book_formset,  
		}  
	)
    
class FriendEdit(CreateView):  
    model = Friend  
    form_class = FriendForm  
    success_url = reverse_lazy('p_library:friend_list')  
    template_name = 'friend_edit.html'  
  
  
class FriendList(ListView):  
    model = Friend  
    template_name = 'friend_list.html'