from django.contrib.auth.models import Permission


class CanEditPostsPermission(Permission):
    codename = 'can_edit_posts'
    name = 'Can edit posts'
