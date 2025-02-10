from django.contrib import admin

from .models import Author, Category, Post, Book, Tag, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Book)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin) :
    list_display = ('id' , 'name' , 'created_at')
admin.site.register(Comment)
