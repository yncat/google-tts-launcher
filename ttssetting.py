# -*- coding: utf-8 -*-
#Google tts setting tool
#Copyright (C) 2020 Yukio Nozawa <personal@nyanchangames.com>
from consolemenu import *
from consolemenu.items import *
from google.cloud import texttospeech
from google.cloud.texttospeech import enums
from copy import copy
import json
import os
import re

SETTING_FILE_NAME_PATTERN=re.compile(r"\A[a-zA-Z0-9_\-]+\Z")
key_file_name="speech_key.json"
settings={
	'protocol_version': 2,
	'speaking_rate': 1.0,
	'pitch': 0,
	'volume_gain_db': 0,
	'effects_profile_id': 'None',
	'language_code': 'ja-JP',
	'name': 'ja-JP-Wavenet-A'
}

languages={
	'ar-XA': 'アラビア語',
	'cs-CZ': 'チェコ語',
	'da-DK': 'デンマーク語',
	'nl-NL': 'オランダ語',
	'en-AU': '英語（オーストラリア）',
	'en-IN': '英語（インド）',
	'en-GB': '英語（イギリス）',
	'en-US': '英語（アメリカ）',
	'fil-PH': 'フィリピン語',
	'fi-FI': 'フィンランド語',
	'fr-CA': 'フランス語（カナダ）',
	'fr-FR': 'フランス語（フランス）',
	'de-DE': 'ドイツ語',
	'el-GR': 'ギリシャ語',
	'hi-IN': 'ヒンディー語',
	'hu-HU': 'ハンガリー語',
	'id-ID': 'インドネシア語',
	'it-IT': 'イタリア語',
	'ja-JP': '日本語',
	'ko-KR': '韓国語',
	'cmn-CN': '標準中国語',
	'nb-NO': 'ノルウェー語',
	'pl-PL': 'ポーランド語',
	'pt-BR': 'ポルトガル語（ブラジル）',
	'pt-PT': 'ポルトガル語（ポルトガル）',
	'ru-RU': 'ロシア語',
	'sk-SK': 'スロバキア語',
	'es-ES': 'スペイン語',
	'sv-SE': 'スウェーデン語',
	'tr-TR': 'トルコ語',
	'uk-UA': 'ウクライナ語',
	'vi-VN': 'ベトナム語'
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

def voiceSetting():
	print("音声エンジンを取得中...")
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(key_file_name)
	client = texttospeech.TextToSpeechClient()
	voices = client.list_voices()
	voices_list=[]
	for voice in voices.voices:
		name=voice.name
		lc=[]
		for language_code in voice.language_codes:
			lc.append(language_code)
		#end language
		ssml_gender=enums.SsmlVoiceGender(voice.ssml_gender)
		gender=ssml_gender.name
		voices_list.append((name,lc,gender))
	#
	language_code_dict={}
	for elem in voices_list:
		for elem2 in elem[1]:
			if not elem2 in language_code_dict: language_code_dict[elem2]=1
		#end for
	#end for
	language_code_list=list(language_code_dict)
	language_code_list.sort()
	sel=[]
	for elem in language_code_list:
		s="%s(%s)" % (elem,languages[elem]) if elem in languages else elem
		sel.append(s)
	#end append
	menu=SelectionMenu(sel,title="言語コード", show_exit_option=False)
	menu.show()
	l=language_code_list[menu.selected_option]
	sel=[]
	sel2=[]
	for elem in voices_list:
		if l in elem[1]:
			sel.append("%s %s" % (elem[0], elem[2]))
			sel2.append(elem[0])
	#end append
	menu=SelectionMenu(sel,title="使用する音声", show_exit_option=False)
	menu.show()
	v=sel2[menu.selected_option]
	global settings
	settings['language_code']=l
	settings['name']=v

def rewriteSettings():
	global settings
	print("設定をアップデート中...")
	d=copy(DEFAULT_SETTINGS)
	d['speaking_rate']=settings['speaking_rate']
	d['pitch']=settings['pitch']
	d['volume_gain_db']=settings['volume_gain_db']
	d['effects_profile_id']=settings['effects_profile_id']
	settings=d
#end rewriteSettings

if not os.path.isdir("settings"):
	print("設定フォルダを作成中...")
	os.mkdir("settings")

if not 'protocol_version' in settings: rewriteSettings()

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
if os.path.exists(key_file_name):
	voiceSetting()
else:
	print("認証情報がないため、音声設定をスキップします。")
#end voice setting
print("")
while(True):
	n=input("この設定につける名前:")
	if re.match(SETTING_FILE_NAME_PATTERN,n): break
	print("設定の名前には、半角アルファベット、数字、アンダースコア、ハイフン以外を使えません。")

print("設定 %s を保存中..." % n)
with open("settings/%s.json" % (n), 'w', encoding='UTF-8') as f:
	f.write(json.dumps(settings))
#end open
print(settings)
print("OK!")
