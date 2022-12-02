from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Item
from .forms import ReviewForm


class ItemList(generic.ListView):
    model = Item
    queryset = Item.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class ItemDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Item.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        reviews = item.reviews.filter(approved=True).order_by('created_on')
        liked = False
        if item.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'item_detail.html',
            {
                'item': item,
                'reviews': reviews,
                'reviewed': False,
                'liked': liked,
                'review_form': ReviewForm(),
            }
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Item.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        reviews = item.reviews.filter(approved=True).order_by('created_on')
        liked = False
        if item.likes.filter(id=self.request.user.id).exists():
            liked = True

        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.name = request.user.username
            review_form.instance.item = item
            review_post = review_form.save(commit=False)
            review_post.save()
        else:
            review_form = ReviewForm()

        return render(
            request,
            'item_detail.html',
            {
                'item': item,
                'reviews': reviews,
                'reviewed': True,
                'liked': liked,
                'review_form': review_form,
            }
        )
