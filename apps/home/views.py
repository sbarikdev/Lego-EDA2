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
def eda_flow(request):
    data = None
    path = '/home/satyajit/Desktop/opensource/data/us_amz.csv'
    try:
        import os
        if os.path.exists(path):
            df = pd.read_csv(path, low_memory=False)
            adls_client = None
        else:
            adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')
            path = '/Unilever/satyajit/us_amz.csv'
            mode = 'rb'
            with adls_client.open(path, mode) as f:
                df = pd.read_csv(f, low_memory=False)
            # output_str = data.to_csv(mode = 'w', index=False)
            # with adls_client.open('/home/satyajit/Videos/lego.csv', 'wb') as o:
            #     o.write(str.encode(output_str))
            #     o.close()
    except Exception as e:
        print('error is---->', e)
        return render(request,'home/index.html', {'message': 'Error while loading data'})
    df2 = df.head(100)
    df3 = df.head(3500)
    data2 = df3.to_dict()
    json_data = df2.reset_index()
    data = json.loads(json_data.to_json(orient ='records'))
    context = {'data': data, 'message': 'data loaded successfully.'}
    if request.method == 'POST':
        id_col = request.POST.get('id_col')
        target_col = request.POST.get('target_col')
        time_index_col = request.POST.get('time_index_col')
        file_name = request.POST.get('file_name')
        #download_path = request.POST.get('download_path')
        static_cat_col_list = request.POST.getlist('static_cat_col_list')
        temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
        temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
        sort_col_list = request.POST.getlist('sort_col_list')
        amz_columns_dict = {'id_col': id_col,
                        'target_col': target_col,
                        'time_index_col': time_index_col,
                        'static_num_col_list': [],
                        'static_cat_col_list': static_cat_col_list,
                        'temporal_known_num_col_list':  temporal_known_num_col_list,
                        'temporal_unknown_num_col_list': [],
                        'temporal_known_cat_col_list': temporal_known_cat_col_list,
                        'temporal_unknown_cat_col_list': [],
                        'strata_col_list': [],
                        'sort_col_list': sort_col_list,
                        'wt_col': None,
                        }
        import os
        try:   
            user = request.user
            username = user.username
            try:
                status = async_task.delay(amz_columns_dict,file_name,username,data2)
            except Exception as e:
                print('task delay error is---->', e)
                return render(request,'home/index.html', {'message': 'Task delay Error while generating EDA'})
            print('status--------------->', status)
            user = request.user
            # if user.email:
            #     from_email = settings.FROM_EMAIL
            #     recipient_email = user.email
            #     subject = 'EDA file generated'
            #     message = 'Your EDA file is generated successfully.'
            #     try:
            #         from django.core.mail import send_mail
            #         status = send_mail(subject, message, from_email, [recipient_email, ], fail_silently=False)
            #     except Exception as e:
            #         print('email error is ------>', e)
            #         return render(request,'home/index.html', {'message': 'email error'})
            # else:
            #     recipient_email = None 
            return render(request,'home/index.html', {'message': 'Save Complete'})
        except Exception as e:
            print('error is---->', e)
            return render(request,'home/index.html', {'message': 'Error while generating EDA'})
    return render(request, "home/data/eda-flow.html", context)

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
        print('error is------>', e)
        return render(request,'home/data/error.html', {'message': 'Error while loading data'})
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {'data': data,'message': 'data loaded successfully.'}

    if request.method == 'POST':
        Key = request.POST.get('Key')
        target_col = request.POST.get('target_col')
        year_week_col = request.POST.get('year_week_col')
        curr_week = request.POST.get('curr_week')
        #download_path = request.POST.get('download_path')
        forecast_end_week = request.POST.getlist('forecast_end_week')
        promo_indicator_col = request.POST.getlist('promo_indicator_col')
        customer_col = request.POST.getlist('customer_col')
        category_col = request.POST.getlist('category_col')
        region = request.POST.getlist('region')
        country = request.POST.getlist('country')
        amz_columns_dict = {'Key': Key,
                        'target_col': target_col,
                        'year_week_col': year_week_col,
                        'curr_week': curr_week,
                        'forecast_end_week': forecast_end_week,
                        'promo_indicator_col':  promo_indicator_col,
                        'customer_col': customer_col,
                        'category_col': category_col,
                        'region': region,
                        'country': country,
                        }
        # import os
        # try:   
        #     user = request.user
        #     username = user.username
        #     try:
        #         status = async_task.delay(amz_columns_dict,file_name,username,data2)
        #     except Exception as e:
        #         print('task delay error is---->', e)
        #         return render(request,'home/index.html', {'message': 'Task delay Error while generating EDA'})
        #     print('status--------------->', status)
        #     return render(request,'home/index.html', {'message': 'Save Complete'})
        # except Exception as e:
        #     print('error is---->', e)
        #     return render(request,'home/index.html', {'message': 'Error while generating EDA'})
    return render(request, "home/data/eda.html", context)
