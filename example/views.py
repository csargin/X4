# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, "about.html", {})

def calendar(request):
    return render(request, 'calendar.html' , {})

def search(request):

    if request.method == 'POST':
        ticker = request.POST['ticker']

        try:
            try:
                temp = si.get_quote_table(ticker, dict_result=False).set_index('attribute')
                api= pd.DataFrame(data=temp)
            except:
                ticker = ticker + ".IS"
                temp = si.get_quote_table(ticker, dict_result=False).set_index('attribute')
                api= pd.DataFrame(data=temp)

        except Exception as e:
            api = "Error"
        return render(request, 'search.html',{'api': api, 'ticker': ticker.upper()  })
    else:
        return render(request, 'search.html',{'ticker': "Enter a ticker symbol" })

