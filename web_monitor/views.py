import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from benchmark.logic.BenchmarkRunner import LogicModule
from benchmark.models import Result
from .utils import get_plot
import threading
import datetime

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

        run_arguments = {
            "urls": [url],
            "amount_of_rounds": rounds,
            "seconds_between_rounds": int(interval),

        }
        report = Result()

        report.save()
        id = report.pk
        threading.Thread(target=run_thread, args=[run_arguments, id]).start()
        print("ID to ", id)
        return render(request, 'benchmark.html', {"id":id})

    if request.method == "GET":
        return render(request, 'base.html')


def check_finish(request):
    print("got check request")
    if is_ajax(request) and request.method == "GET":
        try:
            id = request.GET.get("id", None)
            print("good request ", request.GET,  id)
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
    return JsonResponse(data_json, status=200)
    #chart = get_plot(x, y, z)
    #return render(request, 'plot.html', {'chart': None})