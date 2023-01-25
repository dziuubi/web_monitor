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
from .utils import get_plot, get_other_plot


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
        tries = int(request.POST.get('Tries'))
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
            "amount_of_tries": tries,
        }
        report = Result()
        report.args = json.dumps(run_arguments)
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
    args = json.loads(history.args)

    print(args)
    data_json = json.loads(history.data_json)
    print(data_json)
    data_formatted = {"sis": {},
                      "lcps": {}}
    # URL/TYPE/ROUND/RESULTS
    ##for every url, we need to make round list
    #TYPE/URL/Round/Results
    for url, types in data_json.items():
        for type, rounds in types.items():
            print(rounds)
            for number, round_ in rounds.items():
                print(f"number: {number}, round: {round_}")
                if url not in data_formatted[type]:
                    data_formatted[type][url] = []
                data_formatted[type][url].append(round(mean(round_)))

    print("Formatted", data_formatted)
    labels = [f"Round {i}" for i in range(1, args["amount_of_rounds"] + 1)]
    #sis = [round(mean(val["sis"])) for val in data_json.values()]
    #lcps = [round(mean(val["lcps"])) for val in data_json.values()]
    urls = args["urls"]

    chart_siss = get_other_plot(labels, data_formatted["sis"], 'Chart of average SI times for given URLs')
    chart_lcps = get_other_plot(labels, data_formatted["lcps"], 'Chart of average LCP times for given URLs')

    data = [{"url": url,
             "sis": round(mean([item for sublist in types["sis"].values() for item in sublist])),
             "lcps": round(mean([item for sublist in types["lcps"].values() for item in sublist])),
             }
            for url, types in data_json.items()]

    context = {
        'chart_siss': chart_siss,
        'chart_lcps': chart_lcps,
        'data': data
    }
    return render(request, 'plot.html', context)
