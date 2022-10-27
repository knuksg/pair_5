from django.shortcuts import redirect, render
from .forms import ReviewForm
from django.contrib import messages
from .models import Review
# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews':reviews,
    }
    return render(request, 'reviews/index.html', context)

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

def detail(request, review_pk):
    reviews = Review.objects.get(pk=review_pk)
    context = {
        'reviews':reviews,
    }
    return render(request,'reviews/detail.html', context)

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