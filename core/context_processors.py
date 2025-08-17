from .forms import SearchForm


def form(request):
    return {"search_form": SearchForm()}
