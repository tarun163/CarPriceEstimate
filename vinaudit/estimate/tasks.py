
from celery import shared_task, Celery
from .models import CarValueData
import pandas as pd


import logging

celery = Celery(__name__)
celery.config_from_object(__name__)


# @celery.task
@shared_task
def insert_data(file_path): 
    
    df = pd.read_csv(file_path)
   
    df['listing_price'] = df['listing_price'].fillna(0)
    df['listing_mileage'] = df['listing_mileage'].fillna(0)  
    df['year'] = df['year'].fillna(0) 
    df['trim'] = df['trim'].fillna('') 
    df['make'] = df['make'].str.lower() 
    df['model'] = df['model'].str.lower()  
    df['dealer_vdp_last_seen_date'] = df['dealer_vdp_last_seen_date'].fillna('1000-10-10')
    
    data_dict = df.to_dict('records')
    # check the insertion
    i = 0
    for ins in data_dict:
        try:
            CarValueData.objects.create(**ins)
            print(i)
            i += 1
        except Exception as e:
            print(e)    


# celery -A vinaudit worker -l info --pool=solo