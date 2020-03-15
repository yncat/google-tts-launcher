# -*- coding: utf-8 -*-
#Google tts setting tool
#Copyright (C) 2020 Yukio Nozawa <personal@nyanchangames.com>

from getch import getch
import json
import platform
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

KEY_UP=0
KEY_DOWN=1
KEY_RETURN=2
IS_WINDOWS=platform.system()=='Windows'

def getConsoleArrowInput():
	return _getConsoleArrowInput_win() if IS_WINDOWS else _getConsoleArrowInput_nonWin()

def _getConsoleArrowInput_win():
	key=ord(getch())
	if key==13: return KEY_RETURN
	if key==224:
		key=ord(getch())
		if key==80: return KEY_DOWN
		if key==72: return KEY_UP
	#end 224
	return -1
#end _getConsoleArrowInput_win

def _getConsoleArrowInput_nonWin():
	key=ord(getch())
	if key==13: return KEY_RETURN
	if key==0x1b:
		key=ord(getch())
		if key==0x5b:
			key=ord(getch())
			if key==0x41: return KEY_UP
			if key==0x42: return KEY_DOWN
	return -1

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

def _printChoice(tup,first=False):
	s=", ".join(tup)
	if len(s)>80: s=s[0:80]
	if len(s)<80:
		l=[' '] * (90-len(s))
		s+=(''.join(l))
	#end padding
	if first:
		print("%s" % (s), end="",flush=True)
	else:
		print("\r%s" % (s), end="",flush=True)
	#end print
#end _printChoice

def showMenu(description_text,selection_tuple,default):
	print("%s 上下矢印で選択:" % description_text)
	i=0
	for elem in selection_tuple:
		if default==elem[0]:
			cursor=i
			break
		#end if
		i+=1
	#end while

	_printChoice(selection_tuple[cursor],first=True)
	while(True):
		k=getConsoleArrowInput()
		if k==KEY_RETURN: break
		if k==KEY_UP:
			if cursor==0: continue
			cursor-=1
		#end up
		if k==KEY_DOWN:
			if cursor==len(selection_tuple)-1: continue
			cursor+=1
		#end down
		_printChoice(selection_tuple[cursor])
	#end while
	return selection_tuple[cursor][0]

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
#音声プロファイルは作ってる途中。矢印で選択させたいけどできない。
#settings['effects_profile_id']=showMenu("適用する音声プロファイル",PROFILES,settings['effects_profile_id'])
print("")
print("設定を保存中...")
with open('settings.json', 'w', encoding='UTF-8') as f:
	f.write(json.dumps(settings))
#end open
print(settings)
print("OK!")
