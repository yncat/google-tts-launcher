﻿# Google tts launcher

初回のインストール時には、 pip install -r requirements.txt を実行して、必要なライブラリを入れます。

speech_key.json に、認証情報のJSONを保存して、このプログラムと同じフォルダに置きます。

その後、

python ttssetting.py

を実行して、音声の設定をします。設定の最後に、名前を付けます。

設定が完了したら、

python ttslauncher.py ファイル名.txt 設定名

とします。

ファイル名.txt には、しゃべらせたい言葉を改行で句切って書いたテキストファイルを指定します。

1行で1ファイルになります。

ttslauncher.py の引数に、設定の名前を追加しておくと、選択画面をスキップして、その設定ファイルを読み込もうとします。見つからなければ、選択画面を表示します。

出力される音声ファイルのファイル名は、使用した設定の名前と、行の最初の20文字をとって、適当につけられます。

出力される音声ファイルは、 out フォルダの中に作られます。
## 設定

python ttssetting.py

とすることで、設定を行えます。

## 設定値について

- 音声の速度: 音声の速度です。

- 音程: 声の高さです。

- 音量: 音量を増幅させたり、減らしたりできます。

- 音声プロファイル: モバイルデバイスや家庭用スピーカー向けに、音声の波形を最適化してくれる機能です。複数のプロファイルを順番に通すこともできます。

- 言語コード: 使用する音声の言語を選択します。

- 音声エンジン: 言語コードで選んだ言語に対応する音声エンジンが表示されます。ここで選択した音声が利用されます。

- 設定の名前: この設定につける名前です。名前をべつにすることで、複数の音声設定を管理することができます。
