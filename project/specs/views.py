from django.shortcuts import render
from .serializers import *
from rest_framework.generics import ListAPIView
from django.http import HttpResponse
import json
from .models import PhoneName, Product
from Specs_scrap import *



def get_specs_and_save(phone_name_str):
    data = getSpecs(phone_name_str)
    if not data:
        return False

    
    others_data = []
    if 'BODY' in data and ' ' in data['BODY']:
        others_data.append(data['BODY'][' '])
    if 'MEMORY' in data and ' ' in data['MEMORY']:
        others_data.append(data['MEMORY'][' '])
    if 'FEATURES' in data and ' ' in data['FEATURES']:
        others_data.append(data['FEATURES'][' '])

    others = "\n".join(others_data)

    
    phone_name_obj, created = PhoneName.objects.get_or_create(phone_name=phone_name_str)

    
    if Product.objects.filter(phone_name=phone_name_obj).exists():
        print(f"Data for {phone_name_str} already exists. Skipping.")
        return False

    
    if data:
        try:
        
            main_camera = next((data['MAIN CAMERA'][key] for key in data.get('MAIN CAMERA', {}) if key in ['Single', 'Dual', 'Triple', 'Quad', 'Penta']), '')
            selfie_camera = next((data['SELFIE CAMERA'][key] for key in data.get('SELFIE CAMERA', {}) if key in ['Single', 'Dual', 'Triple', 'Quad', 'Penta']), '')

            product = Product.objects.create(
                phone_name=phone_name_obj,
                technology=data.get('NETWORK', {}).get('Technology', ''),
                announced=data.get('LAUNCH', {}).get('Announced', ''),
                status=data.get('LAUNCH', {}).get('Status', ''),
                dimensions=data.get('BODY', {}).get('Dimensions', ''),
                weight=data.get('BODY', {}).get('Weight', ''),
                build=data.get('BODY', {}).get('Build', ''),
                sim=data.get('BODY', {}).get('SIM', ''),
                display_type=data.get('DISPLAY', {}).get('Type', ''),
                display_size=data.get('DISPLAY', {}).get('Size', ''),
                resolution=data.get('DISPLAY', {}).get('Resolution', ''),
                protection=data.get('DISPLAY', {}).get('Protection', ''),
                os=data.get('PLATFORM', {}).get('OS', ''),
                chipset=data.get('PLATFORM', {}).get('Chipset', ''),
                cpu=data.get('PLATFORM', {}).get('CPU', ''),
                gpu=data.get('PLATFORM', {}).get('GPU', ''),
                card_slot=data.get('MEMORY', {}).get('Card slot', ''),
                internal=data.get('MEMORY', {}).get('Internal', ''),
                main_camera=main_camera,
                main_camera_features=data.get('MAIN CAMERA', {}).get('Features', ''),
                main_camera_video=data.get('MAIN CAMERA', {}).get('Video', ''),
                selfie_camera=selfie_camera,
                selfie_camera_features=data.get('SELFIE CAMERA', {}).get('Features', ''),
                selfie_camera_video=data.get('SELFIE CAMERA', {}).get('Video', ''),
                loudspeaker=data.get('SOUND', {}).get('Loudspeaker', ''),
                headphone_jack=data.get('SOUND', {}).get('3.5mm jack', ''),
                wlan=data.get('COMMS', {}).get('WLAN', ''),
                bluetooth=data.get('COMMS', {}).get('Bluetooth', ''),
                positioning=data.get('COMMS', {}).get('Positioning', ''),
                nfc=data.get('COMMS', {}).get('NFC', ''),
                radio=data.get('COMMS', {}).get('Radio', ''),
                usb=data.get('COMMS', {}).get('USB', ''),
                sensors=data.get('FEATURES', {}).get('Sensors', ''),
                battery_type=data.get('BATTERY', {}).get('Type', ''),
                charging=data.get('BATTERY', {}).get('Charging', ''),
                colors=data.get('MISC', {}).get('Colors', ''),
                model_name=data.get('MISC', {}).get('Models', ''),
                sar=data.get('MISC', {}).get('SAR', ''),
                sar_eu=data.get('MISC', {}).get('SAR EU', ''),
                price=data.get('MISC', {}).get('Price', ''),
                performance=data.get('TESTS', {}).get('Performance', ''),
                display=data.get('TESTS', {}).get('Display', ''),
                camera=data.get('TESTS', {}).get('Camera', ''),
                loudness=data.get('TESTS', {}).get('Loudspeaker', ''),
                battery=data.get('TESTS', {}).get('Battery (old)', ''),
                battery_new=data.get('TESTS', {}).get('Battery (new)', ''),
                others=others
            )
            product.save()
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False


def fetch_and_save_product_data(request):
    try:
        
        phone_names = PhoneName.objects.all()[1118:]

        for phone_name_obj in phone_names:
            phone_name = phone_name_obj.phone_name

            
            if get_specs_and_save(phone_name):
                print(f"Data fetched and saved successfully for {phone_name}")
            else:
                print(f"Failed to fetch or save data for {phone_name}")

        return HttpResponse("Process completed successfully for all phones")

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    

###Data from database

class PhoneList(ListAPIView):
    queryset = PhoneName.objects.all()
    serializer_class = PhoneNameSerializer
    
    
    
class Product(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





##to save phone names in the database
# def extract_phones(json_file_path):

#     with open(json_file_path) as json_file:
#         temp = json.load(json_file)
    
#     d = dict(temp)
#     phone_list = []
#     for i in d.keys():
#         for j in d[i]:
#             phone_list.append(i + " " + j)
    
#     return phone_list

# def save_phones(phone_list):

#     for phone in phone_list:
#         PhoneName.objects.create(phone_name=phone)
        


# def load_phones(request):

#     json_file_path = 'specs/phone_models_list.json'
#     try:
#         phone_list = extract_phones(json_file_path)
#         save_phones(phone_list)
#         return HttpResponse("Phones loaded and saved successfully.")
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}")
