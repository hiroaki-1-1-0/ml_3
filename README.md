## URL
https://hiroaki-ito-ml.streamlit.app/

## 概要
* streamlitを用いた映画レコメンドアプリケーション
* 学習データ：movielensの映画データ
* 推薦アルゴリズム：item2vec

## インストール
ライブラリをインストール
```
pip install pandas numpy streamlit gensim
```
または、requirements.txtを用いてインストール
```
pip install -r requirements.txt
```

## アプリの起動
```
# サンプルアプリの起動
streamlit run sample.py

# 映画レコメンドアプリの起動
streamlit run app.py
```
