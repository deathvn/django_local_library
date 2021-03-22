import datetime

from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.form import RenewBookForm
from catalog.models import Author

# Create your views here.
# @login_required
def index(request):
    """View function for hom page of site"""

    # Generate count of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Challenge yourself
    num_genres_i = Genre.objects.filter(name__contains = 'i')
    # print (num_genres_i)
    num_genres_i = num_genres_i.count()
    num_books_i = Book.objects.filter(title__contains = 'i').count()

    # Number of visits to this view
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    # del request.session['num_visits']

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_genres_i' : num_genres_i,
        'num_books_i' : num_books_i,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects \
            .filter(borrower=self.request.user)  \
            .filter(status__exact='o')  \
            .order_by('due_back')


class AllLoanedBookListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects \
            .filter(status__exact='o')  \
            .order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific Book Instance by Librarian."""
    book_instace = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create  a form instance and populate it with data from the request
        form = RenewBookForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            book_instace.due_back = form.cleaned_data['renewal_date']
            book_instace.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form' : form,
        'book_instance' : book_instace,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')


## Challenge modified Books
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')