from django.shortcuts import render
from newsapi import NewsApiClient
from django.http import JsonResponse

# Create your views here.

def get_news_data(selectedTopic):
    newsapi = NewsApiClient(api_key='fe651200121e4ca6afffb7d0edad9dd5')
    try:
        topnews = newsapi.get_top_headlines(category=selectedTopic) # catch information from dropdown box
        return topnews
    except Exception as e:
        # Handle the exception (e.g., log the error)
        print(f"An error occurred while fetching news data: {str(e)}")
        return None

def home(request):
    selectedTopic = request.GET.get('selectedTopic', 'general')  # Default to 'general' if no topic is selected
    news_data = get_news_data(selectedTopic)

    if news_data is not None and 'articles' in news_data:
        topnews = news_data['articles']
        title = []
        desc = []
        url = []
        author = []
        date = []

        for i in range(len(topnews)):
            news = topnews[i]
            title.append(news['title'])
            desc.append(news['description'])
            url.append(news['url'])
            author.append(news['author'])
            date.append(news['publishedAt'])
        all_news = zip(title, desc, url, author, date)

        # Render the HTML template with the data
        return render(request, 'home.html', {'all_news': all_news})
    else:
        # Handle the case where news data is not available or an error occurred
        return JsonResponse({'error': 'No data found'})


