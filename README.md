# Besiege MOD Save & Load

by Gokiburian 2022.11.17

## 概要
Besiegeのmodの切り替えの簡略化するソフトです。

## 動作条件
Windowsならたぶん動く...？

## ファイル構成
- `savemod.exe` : 本体1
- `loadmod.exe` : 本体2
- `README.md` : 本説明書
- `path.txt` : path設定ファイル
- `Besiege.url` : Besiegeをsteamから起動するいつものやつ。loadmod.exeを使った後に自動作成しBesiegeを立ち上げる
- `vanilla.bms` : modがすべてoffになっている状態が記録されたサンプル.bmsファイル
- `bmsファイルとload.exeの関連付け方法.pdf` : bmsファイルをクリックするだけでloadmod.exeで開く方法の説明
- `source` (興味のあるヒト用)
  - `savemod.py` : savemod.exeの中身
  - `loadmod.py` : loadmod.exeの中身
  - `Besiege_Mod.ico` : アイコン
  - `encode.bat` : pythonファイルをexeに変換する
- `backup`
  - `Modding.xml` : Modding.xmlのバックアップ。loadmod.exeで書き換える直前のものを保持。初回起動前はない

  ※基本的に上記の構成から変更しないでください

## インストール
リポジトリをクローンします
```bash
git clone https://github.com/Gokiburian/Besiege_MOD_Save_Load.git
```

## アンインストール
フォルダーごとそのまま削除して下さい

## 使い方
1. `path.txt`にBesiege\Besiege_Data\Mods\Config\Modding.xmlのフルパスを書いてください。デフォルトでは
```
C:\Program Files (x86)\Steam\steamapps\common\Besiege\Besiege_Data\Mods\Config\Modding.xml
```
となっています。

2. 設定後、`savemod.exe`を実行すると.bmsファイルとして現在のonになっているmodの状況を保存します。好きな場所に配置して下さい。

3. `loadmod.exe`を実行して.bmsファイルを選択、もしくは.bmsファイルに対して「プログラムから開く」->`loadmod.exe` を指定すると保存したmodの状況を再現します。後者は一度設定すると.bmsファイルをダブルクリックするだけで済むようになるのでオススメです。

  ※どちらのexeもゲームを終了してから実行してください

## 免責
Copyright (c) 2021 Gokiburian

## 更新履歴
- **ver2.0** : 専用アイコンの設定、バックアップ機能および自動Besiege起動機能、その他エラー防止機能の追加
- **ver2.1** : 自動Besiege起動方法改良
- **ver2.2** : コンソールへの表示の調整し、操作しやすく
- **ver2.3** : すべてのModがON、Modが一つもインストールされていない状態時に発生する不具合修正

## 連絡先
- **Discord**: gokigoukin5
- **E-mail**: moto.allergyholder@gmail.com
