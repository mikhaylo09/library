from django.shortcuts import render
from .models import Book, Author, BookInstance, Review
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from .forms import RenewBookForm, UserRegistrationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import BookSerializer, AuthorSerializer, ReviewSerializer, UserSerializer, BookDestroyedSerializer
import datetime


def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )
  

class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.filter(state='2')
    paginate_by = 10
        

class BookDetailView(generic.DetailView):
    model = Book

    
class AuthorListView(generic.ListView):
    model = Author

    
class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial={'date_of_death':'12/10/2016',}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
    

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    kwarg = 'id'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', 'image']
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_create = datetime.date.today()
        form.instance.state = '2'
        return super(BookCreate, self).form_valid(form)


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        obj = Book.objects.get(id=kwargs['pk'])
        obj.id = None
        obj.user = str(self.request.user)
        obj.date_update = datetime.date.today()
        obj.state = '3'
        obj.save()
        for x in obj.genre.all():
            obj.genre.create(x)
            print (x)
        return super(BookUpdate, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = str(self.request.user)
        form.instance.date_update = datetime.date.today()
        form.instance.state = '2'
        return super(BookUpdate, self).form_valid(form)

    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', 'image']
    permission_required = 'catalog.can_mark_returned'

        # Arguments from form
        #title = form.instance.title
        #author = form.instance.author
        #summary = form.instance.summary
        #isbn = form.instance.isbn
        #language = form.instance.language
        #rating = form.instance.rating
        #state = '2'
        #user = str(self.request.user)
        #date_destroy = form.instance.date_destroy
        #date_create = form.instance.date_create
        #date_update = form.instance.date_update
        #book=Book.objects.create(title=title, author=author, summary=summary, isbn=isbn,
        #language=language, rating=rating, state=state, user=user,
        #date_destroy=date_destroy, date_create=date_create, date_update=date_update)
        #for x in form.instance.genre.all():
            #book.genre.add(x)
            #print (x)


def delete_book(request, pk):
        box = Book.objects.filter(id=pk)
        date_destroy = datetime.date.today()
        user_destroy = request.user.username
        box.update(state='0', user=user_destroy, date_destroy=date_destroy)
        return HttpResponseRedirect(reverse('books') )
    

class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    pk_url_kwarg = 'id'
    fields = ['id', 'book', 'status', 'imprint', 'due_back', 'status', 'borrower']
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('books')
    

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewCreate(PermissionRequiredMixin, CreateView):
    model = Review
    fields = ['rate', 'book', 'content']
    permission_required = 'catalog.can_mark_returned'


class BookallViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(state='2')
    serializer_class = BookSerializer


class BookDestroyedViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(state='0')
    serializer_class = BookDestroyedSerializer


class AuthorallViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@csrf_exempt
def books_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete
        return HttpResponse(status=204)


@csrf_exempt
def reviews_list(request):
    if request.method == 'GET':
        books = Review.objects.all()
        serializer = ReviewSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
