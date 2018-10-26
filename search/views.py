from django.shortcuts import render
from django.http.response import JsonResponse
from .word_search import word_search, update_freq


def home(request):
    return render(request, 'search/search.html')


def search(request):
    results = {}
    if request.method == 'GET':
        word = request.GET.get('word', '')
        if word:
            results = word_search(word)
        if request.is_ajax():
                update_freq.after_response(results, word)
                print(results)
                return JsonResponse(results)
        else:
            words = []
            for result in results.get("hits", {}).get('hits', []):
                words.append(result.get("_source", {}).get("word", ''))
            return render(request, 'search/search.html',
                          {'results': words})





