from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm
from django.utils.text import slugify

from .models import Post, Comment, FavouritePost
from .forms import CommentForm


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual blog post and its comments.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    # ✅ Check if current user has favourited this post
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = post.favourites.filter(user=request.user).exists()

    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Comment submitted and awaiting approval"
            )
            # Return early so old comment.save() below isn't hit
            return render(
                request,
                "blog/post_detail.html",
                {
                    "post": post,
                    "comments": comments,
                    "comment_count": comment_count,
                    "comment_form": CommentForm(),  # reset form
                    "is_favourite": is_favourite,
                },
            )
        # Invalid form — fall through to re-render with errors
    else:
        comment_form = CommentForm()

    # NOTE: your original comment.save() line is left in place but unreachable

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "is_favourite": is_favourite,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    View to edit comments
    """
    if request.method == "POST":
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, "Comment Updated!")
        else:
            messages.add_message(request, messages.ERROR, "Error updating comment!")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    View to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, "Comment deleted!")
    else:
        messages.add_message(
            request, messages.ERROR, "You can only delete your own comments!"
        )

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been updated!")
            return redirect("post_detail", slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, "blog/edit_comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_slug = comment.post.slug

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
        return redirect("post_detail", slug=post_slug)

    return render(request, "blog/delete_comment.html", {"comment": comment})


# ✅ Toggle favourite functionality
@login_required
def toggle_favourite(request, post_id):
    """
    Add or remove a post from the user's favourites.
    """
    post = get_object_or_404(Post, id=post_id, status=1)
    fav, created = FavouritePost.objects.get_or_create(post=post, user=request.user)

    if created:
        messages.success(request, "Added to favourites.")
    else:
        fav.delete()
        messages.info(request, "Removed from favourites.")

    next_url = (
        request.POST.get("next")
        or request.META.get("HTTP_REFERER")
        or reverse("home")
    )
    return redirect(next_url)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created!")
            return redirect("home")  # change to a post detail URL if you have one
    else:
        form = PostForm()
    return render(request, "blog/post_create.html", {"form": form})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 1             # ✅ publish it
            if hasattr(post, "slug") and not post.slug:
                post.slug = slugify(post.title)
            post.save()
            messages.success(request, "Post created and published!")
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "blog/post_create.html", {"form": form})