from django.views.generic import DetailView, ListView, CreateView
from django_filters import FilterSet, ChoiceFilter
from django.utils import timezone
import datetime
from .models import Post

POSTS_PER_PAGE = 10

ORDER_CHOICES = (
    ('1','normal'),
    ('0','reverse'),
)

DATE_CHOICES = (
    ('0.0417','hour'),
    ('0.125','3 hours'),
    ('0.5','12 hours'),
    ('1','24 hours'),
    ('3','3 days'),
    ('7','week'),
    ('30.5','month'),
)
 
    
class PostsFilterSet(FilterSet):
    date_order = ChoiceFilter(field_name='date', choices=ORDER_CHOICES, label='  Order ',
                                initial='1', method='custom_order_filter')
    date_limit = ChoiceFilter(field_name='date', choices=DATE_CHOICES, 
                        label='  Publication limit time ', method='custom_date_filter')
                        
    class Meta:
        model = Post
        fields = ['author']
    
    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', 'added')
        super().__init__(data, *args, **kwargs)
    
    def custom_order_filter(self, queryset, name, value):
        return queryset.filter().order_by(int(value)*'-' + str(name))
    
    def custom_date_filter(self, queryset, name, value):
        lookup = '__'.join([name, 'gte'])
        time_bound = timezone.now() - datetime.timedelta(days=float(value))
        return queryset.filter(**{lookup: time_bound})


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super(FilteredListView, self).get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(FilteredListView, self).get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
        
        
class PostsListView(FilteredListView):
    model = Post
    template_name = 'posts.html'
    queryset = Post.objects.all().order_by('-date')
    filterset_class = PostsFilterSet
    paginate_by = POSTS_PER_PAGE
    

class PostView(DetailView): 
    model = Post
    template_name = 'post.html'
    
    
class PostCreateView(CreateView):
    model = Post
    fields = ['title','body', 'image']
    template_name = 'create.html'
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
