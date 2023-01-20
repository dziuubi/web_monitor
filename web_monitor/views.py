import json

from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect

from benchmark.logic.BenchmarkRunner import LogicModule
from web_monitor.models import Result
from .utils import get_plot


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

        args = {
            "urls": [url],
            "amount_of_rounds": rounds,
            "seconds_between_rounds": int(interval),

        }
        lm = LogicModule(args)
        lm.run()

        for url, results in lm.data.items():
            for i in range(rounds):
                for y in range(2):
                    r = Result()
                    r.URL = url
                    r.sis = results["sis"][i][y]
                    r.lcps = results["lcps"][i][y]
                    r.save()

        history = Result.objects.filter(URL=url).order_by("created_on").all()
        x = [r.created_on for r in history]
        y = [r.sis for r in history]
        z = [r.lcps for r in history]
        chart = get_plot(x, y, z)
        return render(request, 'plot.html', {'chart': chart})

        # json_str = json.dumps(lm.data)

    if request.method == "GET":
        return render(request, 'base.html')
