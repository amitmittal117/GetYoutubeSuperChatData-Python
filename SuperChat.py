import pytchat
import time
import json
from currency_converter import CurrencyConverter
import pafy
from pytube import Playlist

playlist_url = 'https://www.youtube.com/playlist?list=PLTzg_af9oEx5c87G0KuA13qyezlw9o5Pn'

p = Playlist(playlist_url)
for url in p.video_urls:
    print(url)
    video = pafy.new(url)
    video_id = video.videoid
    chat = pytchat.create(video_id=video_id)
    currency = {}
    video_length = video.length
    while chat.is_alive():
        all_data = chat.get().json()
        flag = True
        for data in json.loads(all_data):
            if data.get('type') == 'superChat':
                if data.get('currency') in currency:
                    temp = currency[data.get('currency')] + data.get('amountValue')
                    currency[data.get('currency')] = temp
                else:
                    currency[data.get('currency')] = data.get('amountValue')
            elif data.get('type') == 'newSponsor':
                if data.get('message') in currency:
                    currency[data.get('message')] = currency[data.get('message')] + 1
                else:
                    currency[data.get('message')] = 1
            elif data.get('type') == 'superSticker':
                print('superSticker ---------------------------------------' + str(data))
            if flag:
                print(currency)
                if '-' not in data.get('elapsedTime'):
                    time_elap = data.get('elapsedTime').split(':')
                    time_elap = int(time_elap[0])*60 + int(time_elap[1])
                    print(str((time_elap * 100)//int(video_length)) + "% Completed.")
                flag = False
                print(data.get('elapsedTime'))

    total = 0
    converter = CurrencyConverter()

    for every in currency.keys():
        try:
            total += converter.convert(currency[every], every[:3], 'INR')   
        except Exception as e:
            print (every[:3] + " " + str(currency[every]))
            print (e)
            
    print ("INR " + str(total//1))
