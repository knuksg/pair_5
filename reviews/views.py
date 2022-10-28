from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm, CommentForm
from django.contrib import messages
from .models import Review, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    reviews = Review.objects.order_by('-pk')
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
        "comments": reviews.comment_set.order_by('-pk'),
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

    review = get_object_or_404(Review, pk=review_pk)

    if request.user in review.like_user.all():
      # 좋아요 삭제
      review.like_user.remove(request.user)
      is_liked = False
    else:
      # 좋아요 추가
      review.like_user.add(request.user)
      is_liked = True
    #  리다이렉트

    context = {
      'isLiked': is_liked,
      'likeCount': review.like_user.count(),
    }
    return JsonResponse(context)

    # reviews = Review.objects.get(pk=review_pk)
    # if request.user in reviews.like_user.all():
    #   reviews.like_user.remove(request.user)
    # else:
    #   reviews.like_user.add(request.user)
    # return redirect('reviews:detail', review_pk)


@login_required
def comments(request, review_pk):
    reviews = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.reviews = reviews
      comment.user = request.user
      comment.save()
      context = {
          'content': comment.content,
          'username': comment.user.username,
      }

    return JsonResponse(context)


@login_required
def comments_delete(request, review_pk, comment_pk):
    reviews = Review.objects.get(pk=review_pk)
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', review_pk)

def main(request):
    return render(request, 'reviews/main.html')