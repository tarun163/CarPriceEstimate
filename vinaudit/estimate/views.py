import pandas as pd
from django.shortcuts import render
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from django.http import JsonResponse
from .models import CarValueData, EstimatedData
from .utils import check_data, check_input_file
import random
import os

# from .serializer import CarValueDataSerializer


def home(request):
    return render(request, 'front.html')

def upload_data(request):
    print("get call")
    if request.method == "POST":
        
        # txt_file = "cardata.txt"  
        txt_file = request.FILES['file']
        file_extension = os.path.splitext(txt_file.name)[1].lower()
        if file_extension != '.txt':
            return JsonResponse(data={
                'success': False,
                'message': 'file type should be text'
            })
            
        print(txt_file)

        # Read the text file using pandas with '|' delimiter
        try:
            df = pd.read_csv(txt_file, delimiter='|')
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
            
            
        df['listing_price'] = df['listing_price'].fillna(0)
        df['listing_mileage'] = df['listing_mileage'].fillna(0)  
        df['year'] = df['year'].fillna(0) 
        df['trim'] = df['trim'].fillna('') 
        df['make'] = df['make'].str.lower() 
        df['model'] = df['model'].str.lower()  
        
        data_dict = df.to_dict('records')
        # CarValueData.objects.bulk_create(data_dict)
        i = 0
        for ins in data_dict:
            try:
                CarValueData.objects.create(**ins)
                print(i)
                i += 1
            except Exception as e:
                print(e)    

        print("Conversion successful!")
        return JsonResponse(data={
            'success': True,
            'status': 'Success',
            'message': 'Conversion successful!'
        })
        
    return JsonResponse(data={
        'success': False,
    })
    
    
def estimate_result(request):
    print("get request")
    if request.method == "POST":
        year = request.POST.get('year', None)
        make = request.POST.get('make', None)
        model = request.POST.get('model', None)
        mileage = request.POST.get('mileage', None)
        
        message, cleaned_data = check_data(year, make, model, mileage)
        if message:    
            return JsonResponse(data={
                'success': False,
                'final_result': message,
            })
            
        # year = cleaned_data.get('year', None)
        # make = cleaned_data.get('make', None)
        # model = cleaned_data.get('model', None)
        # mileage = cleaned_data.get('mileage', None)    
        
            
        data = CarValueData.objects.filter(~Q(listing_price = "nan"), ~Q(listing_mileage = "nan"), ~Q(listing_price = 0), year=year, make=make, model=model).order_by('listing_price')
        
        if mileage != None and mileage != '':
            
            final_result_data = data.filter(listing_mileage=mileage)[:100]
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
            
            
        # taking simple random sampling method for top results
        N = data.count()  # length of data
        
        if N > 0:
            n = 100    # total top points have to take
            K = int(N//n)
            
            random_number = random.randint(0, K)
        
            result_id_list = []
            count = 0
            for i in range(random_number, N, K):
                result_id_list.append(data[i].pk)
                count += 1
                
                if count == 100:
                    break
                
            final_result_data = data.filter(pk__in=result_id_list)    
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
                'message': 'data fetched successfully!',
                'final_result': final_result,
                'top_result_data':  list(final_result_data.values()),
            })
        else:
            return JsonResponse(data={
                'success': False,
                'message': 'No data found!'
            })
                
        
    return JsonResponse(data={
        'success': False,
    })    
        
            
        
        
        
