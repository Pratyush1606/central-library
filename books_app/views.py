from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect

from .models import Book
from .serializers import BookSerializer

class AddBook(APIView):

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(template_name="book_add.html", status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            "name": request.data.get("name"),
            "published": request.data.get("published"),
            "author": request.data.get("author"),
            "domain": request.data.get("domain"),
            "is_available": request.data.get("is_available", False),
        }

        serializer = BookSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return redirect("books_app:book_list")
        
        error = {
            "error": "Invalid data"
        }
        return Response(data=error, template_name="book_add.html", status=status.HTTP_400_BAD_REQUEST)

class BookList(APIView):

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        query_author = request.query_params.get("author")
        query_published = request.query_params.get("published")
        query_domain = request.query_params.get("domain")

        queried = False
        if(query_author):
            queried = True
            books = Book.objects.filter(author=query_author)
        else:
            books = Book.objects.all()
        
        if(query_published):
            queried = True
            books = books.filter(published=query_published)
        
        if(query_domain):
            queried = True
            books = books.filter(domain=query_domain)

        serializers = BookSerializer(books, many=True)
        data = {
            "results": serializers.data,
            "query": {
                "author": query_author if query_author else "",
                "published": query_published if query_published else "",
                "domain": query_domain if query_domain else ""
            },
            "queried": queried
        }
        return Response(data=data, template_name="book_list.html", status=status.HTTP_200_OK)

class BookUpdate(APIView):

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, id):
        try:
            book = Book.objects.get(book_id=id)
        except Book.DoesNotExist:
            return Response(template_name="book_list.html", status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book)
        return Response(data={"book": serializer.data}, template_name="book_edit.html", status=status.HTTP_200_OK)
    
    def post(self, request, id):
        try:
            book = Book.objects.get(book_id=id)
        except Book.DoesNotExist:
            return Response(template_name="book_list.html", status=status.HTTP_404_NOT_FOUND)

        data = {
            "name": request.data.get("name"),
            "published": request.data.get("published"),
            "author": request.data.get("author"),
            "domain": request.data.get("domain"),
            "is_available": request.data.get("is_available", False),
        }

        serializer = BookSerializer(book, data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
        
        return redirect("books_app:book_list")
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(book_id=id)
        except Book.DoesNotExist:
            return Response(template_name="book_list.html", status=status.HTTP_404_NOT_FOUND)
        
        book.delete()
        return Response(template_name="book_list.html", status=status.HTTP_200_OK)
        