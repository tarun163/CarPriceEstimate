import os
import random
import pandas as pd

from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse

from .models import CarValueData, EstimatedData
from .utils import check_data, check_input_file
from .tasks import insert_data

# home page
def home(request):
    return render(request, 'front.html')

# upload data
def upload_data(request):
    """_summary_

    upload data only by csv file 
    Async Celery task 
    """
    if request.method == "POST":
        # cheking file
        file = request.FILES['file']
        if file == None or file == '':
            return JsonResponse(data={
                'success': False,
                'message': 'please import file!'
            })
        # checking file type    
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension != '.csv':
            return JsonResponse(data={
                'success': False,
                'message': 'file should be .csv'
            })
            
        # convert file for checking colums    
        try:
            df = pd.read_csv(file)
        except:
            return JsonResponse(data={
                'success': False,
                'message': 'some thing went wrong'
            })
        keys = list(df.keys())
        check_list = check_input_file(keys)

        if len(check_list) > 0:
            return JsonResponse(data={
                'success': False,
                'error': check_list,
            }) 
        
        # upload file into folder, it should be in database
        file_path = 'upload/' + file.name
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk) 
        
        
        insert_data.apply_async(args=[file_path])
        
        print("Task received!")
        return JsonResponse(data={
            'success': True,
            'status': 'Success',
            'message': 'Task received!'
        })
        
    return JsonResponse(data={
        'success': False,
        'messgae': 'request should be POST'
    })
    
    
def estimate_result(request):
    if request.method == "POST":
        
        year = request.POST.get('year', None)
        make = request.POST.get('make', None)
        model = request.POST.get('model', None)
        mileage = request.POST.get('mileage', None)
        # checking data
        message, cleaned_data = check_data(year, make, model, mileage)
        if message:    
            return JsonResponse(data={
                'success': False,
                'final_result': message,
            })
        
        # taking clean data    
        year = cleaned_data.get('year', None)
        make = cleaned_data.get('make', None)
        model = cleaned_data.get('model', None)
        mileage = cleaned_data.get('mileage', None)    
        
        # fetchig data
        data = CarValueData.objects.filter(~Q(listing_price = "nan"), ~Q(listing_mileage = "nan"), ~Q(listing_price = 0), year=year, make=make, model=model).order_by('listing_price')
        
        # if mileage is given then directly take first 100 data inorder to price 
        if mileage != None and mileage != '':
            
            final_result_data = data.filter(listing_mileage=mileage)[:100]
            total_price = 0
            for i in final_result_data:
                total_price += i.listing_price
            
            final_result = round(total_price//(final_result_data.count()), -2)
            
            if mileage == '':
                mileage = 0
            
            # saving results
            EstimatedData.objects.create(
                make=make,
                year=year,
                model=model,
                estimated_price=final_result,
                listing_mileage = mileage
            )
            
            return JsonResponse(data={
                'success': True,
                'final_result': final_result,
                'top_result_data':  list(final_result_data.values()),
                'message': 'data fetched successfully!'
            })
            
            
        # else taking simple random sampling method for top results
        N = data.count()  # length of data
        if N >= 100:
            n = 100    # total top points have to take
            K = int(N//n)
            # take random point to start
            random_number = random.randint(0, K)
           
            result_id_list = []
            count = 0
            for i in range(random_number, N, K):
                result_id_list.append(data[i].pk)
                count += 1
                
                if count == 100:
                    break
            
            # final data used to estimate    
            final_result_data = data.filter(pk__in=result_id_list)    
            total_price = 0
            
            for i in final_result_data:
                total_price += i.listing_price
            
            # round to 100 places    
            final_result = round(total_price//(final_result_data.count()), -2)
            
            if mileage == '':
                mileage = 0
            
            EstimatedData.objects.create(
                make=make,
                year=year,
                model=model,
                estimated_price=final_result,
                listing_mileage = mileage
            )
            
            return JsonResponse(data={
                'success': True,
                'message': 'data fetched successfully!',
                'final_result': final_result,
                'top_result_data':  list(final_result_data.values()),
            })
            
        elif N > 0 and N < 100:   
            final_result_data = data 
            total_price = 0
            for i in final_result_data:
                total_price += i.listing_price
            
            final_result = round(total_price//(final_result_data.count()), -2)
            
            if mileage == '':
                mileage = 0
            
            EstimatedData.objects.create(
                make=make,
                year=year,
                model=model,
                estimated_price=final_result,
                listing_mileage = mileage
            )
            
            return JsonResponse(data={
                'success': True,
                'final_result': final_result,
                'top_result_data':  list(final_result_data.values()),
                'message': 'data fetched successfully!'
            })
            
        else:
            return JsonResponse(data={
                'success': False,
                'message': 'No data found!'
            })
                
        
    return JsonResponse(data={
        'success': False,
    })    
        
            
# celery -A vinaudit worker --loglevel=info
            
        
        
        
