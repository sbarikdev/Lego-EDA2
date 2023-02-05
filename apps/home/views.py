# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - Lego
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

import pandas as pd
import json
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url="/login/")
def eda2(request):
    data = None
    path = 'apps/data/test5.parquet'
    try:
        df = pd.read_parquet(path, engine='pyarrow')
        df2 = df.head(50)
        json_data = df2.reset_index()
        data = json.loads(json_data.to_json(orient ='records'))
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 10)
    except Exception as e:
        print('error is---->', e)
        return render(request,'home/data/error.html', {'message': 'Error while loading data'})
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {'data': data,'message': 'data loaded successfully.'}
    return render(request, "home/data/eda.html", context)
