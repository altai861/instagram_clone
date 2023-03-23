from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_image = models.ImageField(blank=True)
    bio = models.CharField(max_length=250, blank=True)


    def __str__(self):
        return f"{self.user.username}"

    def liked_post(self, post):
        likes = Like.objects.all()
        for like in likes:
            if like.post == post and like.user == self.user:
                return True
        return False
    def my_posts(self):
        count = 0
        posts = Post.objects.all()
        for post in posts:
            if post.user == self.user:
                count += 1
        return count
    def who_I_followed(self):
        all_the_people_I_followed = []
        for follow in Follow.objects.all():
            if follow.user == self.user:
                all_the_people_I_followed.append(follow.followed_person)
        return all_the_people_I_followed


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    activity_name = models.TextField(blank=False)

    def __str__(self):
        return f"{self.activity_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=False, upload_to='post_pictures')
    post_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} + {self.activity.activity_name}"

    def likes_count(self):
        count = 0
        likes = Like.objects.all()
        for like in likes:
            if like.post == self:
                count += 1
        return count
    def who_liked(self):
        liked_people = []
        likes = Like.objects.all()
        for like in likes:
            if like.post == self:
                liked_people.append(like.user)
        return liked_people
    def all_the_comments(self):
        comments = Comment.objects.all()
        my_comments = []
        for comment in comments:
            if comment.post == self:
                my_comments.append(comment)
        return my_comments
    def comments_len(self):
        count = 0
        comments = Comment.objects.all()
        for comment in comments:
            if comment.post == self:
                count += 1
        return count
    def who_saved(self):
        saved_people = []
        savings = Saved.objects.all()
        for save in savings:
            if save.post == self:
                saved_people.append(save.user)
        return saved_people
    



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment}"


class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} save {self.post}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_person = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="following_person")

    def __str__(self):
        return f"{self.user} followed {self.followed_person}"