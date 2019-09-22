from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import generic

from .models import Term, Category, Definition, Sport


def get_page_range_to_display_for_pagination(page_obj):
    display_left = display_right = 5

    current_page = page_obj.number
    last_page = page_obj.paginator.page_range.stop - 1

    if current_page <= display_left:
        display_left = current_page - 1
        display_right = display_right + (display_right - display_left)
    if current_page + display_right > last_page:
        left_over = display_right - (last_page - current_page)
        display_right = display_right - left_over

        pages_from_display_left_to_start = current_page - display_left - 1
        if pages_from_display_left_to_start >= left_over:
            display_left += left_over
        else:
            display_left += pages_from_display_left_to_start

    return range(current_page - display_left, current_page + display_right + 1)


class IndexView(generic.ListView):
    context_object_name = 'terms'
    template_name = 'dictionary/index.html'
    paginate_by = 20
    queryset = Term.approved_terms.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_obj = context['page_obj']
        page_range_to_display = get_page_range_to_display_for_pagination(page_obj)
        context['page_range_to_display'] = page_range_to_display

        context['all_sports'] = Sport.active_sports.all()

        return context


class SearchResultsView(generic.ListView):
    context_object_name = 'terms'
    template_name = 'dictionary/search.html'
    paginate_by = 20

    def get_queryset(self):
        search_key = self.request.GET.get('term')
        terms = Term.approved_terms.filter(text__icontains=search_key)
        return terms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('term')
        context['results_count'] = context['paginator'].count

        page_obj = context['page_obj']
        page_range_to_display = get_page_range_to_display_for_pagination(page_obj)
        context['page_range_to_display'] = page_range_to_display
        context['is_search_pagination'] = True

        return context


class SportIndexView(generic.ListView):
    context_object_name = 'terms'
    template_name = 'dictionary/sport_index.html'
    paginate_by = 20

    def get_queryset(self):
        sport_slug = self.kwargs['sport_slug']
        sport = get_object_or_404(Sport, slug=sport_slug)
        category_name = self.request.GET.get('category')
        category = get_object_or_404(Category, name=category_name) if category_name else None
        sport = get_object_or_404(Sport, slug=sport_slug)

        if category:
            return Term.approved_terms.filter(sport=sport).filter(categories__in=(category,))
        else:
            return Term.approved_terms.filter(sport=sport)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sport_slug = self.kwargs['sport_slug']
        sport = get_object_or_404(Sport, slug=sport_slug)
        context['sport'] = sport
        context['categories'] = sport.categories.all()

        page_obj = context['page_obj']
        page_range_to_display = get_page_range_to_display_for_pagination(page_obj)
        context['page_range_to_display'] = page_range_to_display

        context['all_sports'] = Sport.active_sports.all()

        return context


class TermDetailView(generic.DetailView):
    context_object_name = 'term'
    slug_url_kwarg = 'term_slug'
    template_name = 'dictionary/term_detail.html'

    def get_object(self):
        sport_slug = self.kwargs['sport_slug']
        term_slug = self.kwargs.get(self.slug_url_kwarg)

        sport = get_object_or_404(Sport, slug=sport_slug)
        term = get_object_or_404(Term, sport=sport, slug=term_slug)

        return term

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        definitions = Definition.approved_definitions.filter(term=self.object)
        context['definitions'] = definitions

        return context


def random_term(request):
    term = Term.approved_terms.random()
    return redirect(term)
