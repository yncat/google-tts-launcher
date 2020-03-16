# -*- coding: utf-8 -*-
#Google tts setting tool
#Copyright (C) 2020 Yukio Nozawa <personal@nyanchangames.com>
from consolemenu import *
from consolemenu.items import *
import json
import os

DEFAULT_SETTINGS={
	'speaking_rate': 1.0,
	'pitch': 0,
	'volume_gain_db': 0,
	'effects_profile_id': 'None'
}

PROFILES=[
	('None', 'なし'),
	('wearable-class-device', 'スマートウォッチやその他のウェアラブル（Apple Watch、Wear OS watch など）'),
	('handset-class-device', 'スマートフォン（Google Pixel、Samsung Galaxy、Apple iPhone など）'),
	('headphone-class-device', 'オーディオ再生用のイヤフォンやヘッドフォン（Sennheiser ヘッドフォンなど）'),
	('small-bluetooth-speaker-class-device', '小型の家庭用スピーカー（Google Home Mini など）'),
	('medium-bluetooth-speaker-class-device', '家庭用スマート スピーカー（Google Home など）'),
	('large-home-entertainment-class-device', '家庭用エンターテイメント システムやスマートテレビ（Google Home Max、LG TV など）'),
	('large-automotive-class-device', '車載用スピーカー'),
	('telephony-class-application', 'インタラクティブ音声レスポンス（IVR）システム')
]

SETTINGS_FILE_NAME='settings.json'

def checkValue(val,min,max):
	try:
		val=float(val)
	except ValueError:
		print("数字を入力してください。")
		return False
	#end except
	if val<min or val>max:
		print("%sから%sの間で指定してください。" % (min,max))
		return False
	#end error
	return True
#end checkValue

def inputWithCheck(description_text,default,min,max):
	default=float(default)
	while(True):
		ret=input("%s 現在 %.1f:" % (description_text,default))
		if ret=='':
			ret=default
			break
		#end use default
		if checkValue(ret,min,max): break
	#end while
	return ret

if not os.path.exists('settings.json'):
	print("デフォルト設定を作成中...")
	with open('settings.json', 'w', encoding='UTF-8') as f:
		f.write(json.dumps(DEFAULT_SETTINGS))
	#end open
#end make default settings

print("設定を読み込み中...")
with open('settings.json', 'r', encoding='UTF-8') as f:
	settings=json.load(f)
	#end open

settings['speaking_rate']=inputWithCheck("音声速度の倍率(0.25～4.0)倍",settings['speaking_rate'],0.25,4.0)
settings['pitch']=inputWithCheck("音声の音程(-20.0～20.0)セミトーン",settings['pitch'],-20.0,20.0)
settings['volume_gain_db']=inputWithCheck("音声の音量(-96.0～16.0)dB",settings['volume_gain_db'],-96.0,16.0)

all_profiles=[elem[0] for elem in PROFILES]
selected_profiles=[]
available_profiles=[elem[0] for elem in PROFILES]

while(True):
	if len(available_profiles)==0: break
	menu=SelectionMenu(available_profiles,title="適用する音声プロファイル", show_exit_option=False)
	menu.show()
	selected_str=available_profiles[menu.selected_option]
	selected_profiles.append(selected_str)
	if selected_str!='None':
		if 'None' in available_profiles: available_profiles.remove('None')
	else:
		break
	#end if 
	while(True):
		yn=input("さらにプロファイルを追加しますか? y/n:")
		if yn=='y' or yn=='n': break
	#end while
	if yn=='n': break
	available_profiles.remove(selected_str)
#end while

if 'None' in selected_profiles: selected_profiles=None
settings['effects_profile_id']=selected_profiles
print("")
print("設定を保存中...")
with open('settings.json', 'w', encoding='UTF-8') as f:
	f.write(json.dumps(settings))
#end open
print(settings)
print("OK!")
