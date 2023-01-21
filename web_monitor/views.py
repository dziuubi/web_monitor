import json

from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect

from benchmark.logic.BenchmarkRunner import LogicModule
from web_monitor.models import Result
from .utils import get_plot
import threading
import datetime

def run_thread(args, ID = "id_test"):
    r = Result()
    r.ID=ID
    r.created_on=datetime.datetime.now()
    r.save()
    lm = LogicModule(args)
    lm.run()

    r.data_json = json.dumps(lm.data)
    r.finished = True

    r.save()

def home(request):
    if request.method == "POST":
        url = request.POST.get('URL')
        rounds = int(request.POST.get('Rounds'))
        interval = request.POST.get('Interval')
        submitbutton = request.POST.get('Submit')

        context = {'URL': url,
                   'rounds': rounds,
                   'interval': interval,
                   'submitbutton': submitbutton
                   }
        print(context)

        run_arguments = {
            "urls": [url],
            "amount_of_rounds": rounds,
            "seconds_between_rounds": int(interval),

        }
        threading.Thread(target=run_thread, args=[run_arguments]).start()

        return HttpResponse("Hello, BENCHMARK")


        #

    if request.method == "GET":
        return render(request, 'base.html')

def results(request):
    url = request.data.id
    history = Result.objects.filter(URL=url).order_by("created_on").all()
    x = [r.created_on for r in history]
    y = [r.sis for r in history]
    z = [r.lcps for r in history]
    chart = get_plot(x, y, z)
    return render(request, 'plot.html', {'chart': chart})