from django.shortcuts import redirect, render
from .forms import ReviewForm, CommentForm
from django.contrib import messages
from .models import Review, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews':reviews,
    }
    return render(request, 'reviews/index.html', context)


@login_required
def create(request):
    if request.method == "POST":
        create_form = ReviewForm(request.POST, request.FILES)
        if create_form.is_valid():
            reviews = create_form.save(commit=False)
            reviews.user = request.user
            reviews.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('reviews:index')
    else:
        create_form = ReviewForm()
    context = {
        'create_form': create_form,
    }
    return render(request, 'reviews/create.html', context)

@login_required
def detail(request, review_pk):
    reviews = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    
    context = {
        'reviews': reviews,
        "comments": reviews.comment_set.all(),
        'comment_form': comment_form,
    }
    return render(request,'reviews/detail.html', context)

@login_required
def update(request,review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
            if request.method == "POST":
                update_form = ReviewForm(request.POST, instance=review)
                if update_form.is_valid():
                    update_form.save()
                    messages.success(request, '글이 수정되었습니다.')
                    return redirect('reviews:detail', review.pk)
            else:
                update_form = ReviewForm(instance=review)
            context = {
                'update_form':update_form,
            }
            return render(request, 'reviews/update.html', context)
    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('reviews:detail', review.pk)

@login_required
def delete(request, review_pk):
    reviews = Review.objects.get(pk=review_pk)
    reviews.delete()
    messages.warning(request, '글이 삭제되었습니다.')
    return redirect('reviews:index')


@login_required
def like(request, review_pk):
    reviews = Review.objects.get(pk=review_pk)
    if request.user in reviews.like_user.all():
      reviews.like_user.remove(request.user)
    else:
      reviews.like_user.add(request.user)
    return redirect('reviews:detail', review_pk)


@login_required
def comments(request, review_pk):
    reviews = Review.objects.get(pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.reviews = reviews
      comment.user = request.user
      comment.save()

    return redirect('reviews:detail', reviews.pk)


@login_required
def comments_delete(request, review_pk, comment_pk):
    reviews = Review.objects.get(pk=review_pk)
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', review_pk)

def main(request):
    return render(request, 'reviews/main.html')