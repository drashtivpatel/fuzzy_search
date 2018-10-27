from django.shortcuts import render
from django.http.response import JsonResponse
from .word_search import word_search, update_freq


def home(request):
    """
    View for rendering index page
    :param request:
    :return: Renders home page
    """
    return render(request, 'search/search.html')


def search(request):
    """
    Search API endpoint for providing autocomplete which renders template and return list of words as well
    :param request:
    :return: Template Rendering/JSON Array Response
    """
    words = []
    if request.method == 'GET':
        word = request.GET.get('word', '')
        if word:
            results = word_search(word)
            for result in results.get("hits", {}).get('hits', []):
                words.append(result.get("_source", {}).get("word", ''))
            update_freq.after_response(results, word)
        if request.is_ajax():
                return JsonResponse(words, safe=False)
        else:
            if request.GET.get('submit'):
                return render(request, 'search/search.html',
                              {'results': words})
            return JsonResponse(words, safe=False)





