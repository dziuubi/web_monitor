from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import asyncio
import threading

from benchmark.logic.BenchmarkRunner import LogicModule


def index(request):
    return HttpResponse("Hello, INDEX")


async def benchmark(args=None):
    if args is None:
        args = {}
    threading.Thread(target=LogicModule(args).run(), args={}).start()
    return HttpResponse("Hello, BENCHMARK")
