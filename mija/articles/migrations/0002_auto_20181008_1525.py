from django.db import migrations
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from articles.models import Category, Article


def get_permission(codename, ct):
    return Permission.objects.get(
        codename=codename,
        content_type=ct,
    )


def change_permissions(group, codename, ct, apply_migration=False):
    permission_articles = get_permission(
        codename, ct
    )
    if apply_migration:
        group.permissions.add(permission_articles.id)
    else:
        group.permissions.remove(permission_articles.id)


def prepare_custom_permissions(apps, schema_editor, apply_mig):
    Group = apps.get_model('auth', 'Group')
    publisher_group, publisher_group_created = Group.objects.get_or_create(
        name='publisher'
    )
    editor_group, editor_group_created = Group.objects.get_or_create(
        name='editor'
    )
    ct_article = ContentType.objects.get_for_model(Article)
    ct_category = ContentType.objects.get_for_model(Category)
    permissions_configuration = (
        (publisher_group, 'add_category', ct_category, apply_mig),
        (publisher_group, 'change_category', ct_category, apply_mig),
        (editor_group, 'add_article', ct_article, apply_mig),
        (editor_group, 'change_article', ct_article, apply_mig),
        (publisher_group, 'change_article', ct_article, apply_mig),
        (publisher_group, 'view_article', ct_article, apply_mig),
        (editor_group, 'view_article', ct_article, apply_migration),
        (publisher_group, 'can_publish_unpublish', ct_article, apply_mig),
    )
    for perm in permissions_configuration:
        change_permissions(*perm)


def apply_migration(apps, schema_editor):
    prepare_custom_permissions(apps, schema_editor, True)


def revert_migration(apps, schema_editor):
    prepare_custom_permissions(apps, schema_editor, False)


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            apply_migration, revert_migration
        ),
    ]
