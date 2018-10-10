from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    fields = [
        "category", "author", "article_title", "article_body", "published",
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        if (request.user.is_superuser or
                request.user.has_perm('articles.view_article')):
            return qs

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if (request.user.has_perm('articles.can_publish_unpublish') and
                request.user.has_perm('articles.add_article')):
            self.readonly_fields = ["author"]
            return True
        if request.user.has_perm('articles.can_publish_unpublish'):
            self.readonly_fields = [
                "category", "author", "article_title",
                "article_body", "history"
            ]
            return True
        if ((obj.author.id == request.user.id and not obj.published) or
                request.user.is_superuser):
            self.readonly_fields = ["author", "published"]
            return True
        return False


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Permission)
