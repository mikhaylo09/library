from django.urls import path
from . import views
from rest_framework import routers
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='API')

urlpatterns = [
    path('swag/', schema_view),
    path('', views.index, name='index'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.delete_book, name='book-delete'),
    path('register/', views.register, name='register'),
]


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'bookall', views.BookallViewSet)
router.register(r'bookdestroyed', views.BookDestroyedViewSet)
router.register(r'authorall', views.AuthorallViewSet)
router.register(r'reviews', views.ReviewViewSet)


urlpatterns += [
    path('loan/<str:id>/update', views.BookInstanceUpdate.as_view(), name='loan'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reviews/create', views.reviews_list, name='rlist'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('booklook/<int:pk>', views.BookDetailView.as_view(), name='book-lookup'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authorlook/<int:pk>', views.AuthorDetailView.as_view(), name='author-lookup'),
]