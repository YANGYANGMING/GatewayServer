import os, django, time, threading, random, json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GatewayServer.settings")
django.setup()
# from emat import calThickness
from GWS import models

datas = models.Waveforms.objects.values('data', 'temperature').filter(network_id='0.0.2.1').order_by('id')[:5]
print(datas)
for data_item in datas:
    data = eval(data_item['data'])
    sum_data = sum(data)
    # print('sum==', sum)
    average = sum_data // len(data)
    # print('average==', average)
    difference = average - 2048
    # print('difference==', difference)
    new_data = data[:161]
    for item2 in data[161:]:
        if item2 - difference > 0:
            new_data.append(item2 - difference)
    # print(new_data)
    # print(len(new_data))

    material_obj = models.Material.objects.values('sound_V', 'temperature_co').get(id=2)
    sound_V = material_obj['sound_V']
    temperature_co = material_obj['temperature_co']
    true_sound_V = float(sound_V - ((float(data_item['temperature']) - 25) * temperature_co))
    print('true_sound_V', true_sound_V)
    # thickness = calThickness(data=new_data, gain_db=60, vel_mps=true_sound_V)


