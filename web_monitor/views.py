import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from numpy import mean

from benchmark.logic.BenchmarkRunner import LogicModule
from benchmark.models import Result
import threading
import datetime
import numpy as np
import matplotlib.pyplot as plt
from .utils import get_plot


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def run_thread(args, id):
    lm = LogicModule(args)
    lm.run()
    r = Result.objects.get(pk=id)
    r.data_json = json.dumps(lm.data)
    r.finished = True
    r.save()
    print("Function finished")


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

        urls = url.split()

        run_arguments = {
            "urls": urls,
            "amount_of_rounds": rounds,
            "seconds_between_rounds": int(interval),

        }
        report = Result()

        report.save()
        id = report.pk
        threading.Thread(target=run_thread, args=[run_arguments, id]).start()
        print("ID to ", id)
        return render(request, 'benchmark.html', {"id": id})

    if request.method == "GET":
        return render(request, 'base.html')


def check_finish(request):
    print("got check request")
    if is_ajax(request) and request.method == "GET":
        try:
            id = request.GET.get("id", None)
            print("good request ", request.GET, id)
            r = Result.objects.get(pk=id)
            print("got object")
            return JsonResponse({"finished": r.finished}, status=200)
        except:
            return JsonResponse({}, status=400)
    return JsonResponse({}, status=400)


def results(request, id):
    history = Result.objects.get(pk=id)
    print(history.data_json)
    data_json = json.loads(history.data_json)
    a = range(9)

    labels = [f"URL{i}" for i in range(1, len(data_json) + 1)]
    sis = [round(mean(val["sis"])) for val in data_json.values()]
    lcps = [round(mean(val["lcps"])) for val in data_json.values()]
    urls = list(data_json.keys())

    chart = get_plot(labels, sis, lcps)

    data = [{"url": urls[i],
             "sis": sis[i],
             "lcps": lcps[i],
             "label": labels[i],
             }
            for i in range(len(urls))
            ]

    context = {
        'chart': chart,
        'data': data,
    }
    return render(request, 'plot.html', context)
