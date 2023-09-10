import streamlit as st
import pandas as pd
import numpy as np
import gensim

st.title('映画レコメンド')

# 映画情報の読み込み
movies = pd.read_csv("data/movies.tsv", sep="\t")

# 学習済みのitem2vecモデルの読み込み
model = gensim.models.word2vec.Word2Vec.load("data/item2vec.model")

# 映画IDとタイトルを辞書型に変換
movie_ids = movies["movie_id"].tolist()
movie_titles = movies["title"].tolist()
movie_genres = movies["genre"].tolist()
movie_tags = movies["tag"].tolist()
movie_id_to_title = dict(zip(movie_ids, movie_titles))
movie_title_to_id = dict(zip(movie_titles, movie_ids))
movie_id_to_genre = dict(zip(movie_ids, movie_genres))
movie_id_to_tag = dict(zip(movie_ids, movie_tags))

st.markdown("## 1本の映画に対して似ている映画を表示する")
selected_movie = st.selectbox("映画を選んでください", movie_titles)
selected_movie_id = movie_title_to_id[selected_movie]
selected_count_1 = st.slider("結果の出力件数の上限を指定してください", value = 5, min_value = 1, max_value = 30) # add: 検索件数の上限の指定
selected_score_1 = st.number_input("スコアの下限を指定してください", value = 0.3, min_value = 0.0, max_value = 0.99) # add: スコア下限の指定
st.write(f"あなたが選択した映画は{selected_movie}(id={selected_movie_id})です")
st.write(f"あなたが指定した検索件数の上限は{selected_count_1}です") # add: 指定した検索件数の上限の表示
st.write(f"あなたが指定したスコア下限は{selected_score_1}です") # add: 指定したスコア下限の表示

# 似ている映画を表示
st.markdown(f"### {selected_movie}に似ている映画")
results = []
for movie_id, score in model.wv.most_similar(selected_movie_id, topn = selected_count_1): # add: 検索件数の制限
    if score < selected_score_1: # add: スコアの制限
        break
    title = movie_id_to_title[movie_id]
    genre = movie_id_to_genre[movie_id] # add: genreの追加
    tag = movie_id_to_tag[movie_id] # add: tagの追加
    results.append({"movie_id":movie_id, "title": title, "genre": genre, "tag": tag, "score": score})
results = pd.DataFrame(results)
st.write(results)


st.markdown("## 複数の映画を選んでおすすめの映画を表示する")

selected_movies = st.multiselect("映画を複数選んでください", movie_titles)
selected_count_2 = st.slider("結果の出力件数の上限を指定してください", value = 10, min_value = 1, max_value = 30) # add: 検索件数の指定
selected_score_2 = st.number_input("スコアの下限を指定してください", value = 0.2, min_value = 0.0, max_value = 0.99) # add: スコア下限の指定
selected_movie_ids = [movie_title_to_id[movie] for movie in selected_movies]
vectors = [model.wv.get_vector(movie_id) for movie_id in selected_movie_ids]
count_1 = 0
if len(selected_movies) > 0:
    for selected_movie in selected_movies:
        st.write(f"あなたが選択した映画の1つは{selected_movie}(id={movie_title_to_id[selected_movie]})です")
        count_1 += 1
st.write(f"あなたが指定した検索件数の上限は{selected_count_2}です") # add: 指定した検索件数の上限の表示
st.write(f"あなたが指定したスコア下限は{selected_score_2}です") # add: 指定したスコア下限の表示
if len(selected_movies) > 0:
    count_2 = 0
    user_vector = np.mean(vectors, axis=0)
    st.markdown(f"### おすすめの映画")
    recommend_results = []
    for movie_id, score in model.wv.most_similar(user_vector, topn = selected_count_2): # add: 検索件数の上限の制限
        if score < selected_score_2: # add: スコアの制限
            break
        title = movie_id_to_title[movie_id]
        genre = movie_id_to_genre[movie_id] # add: genreの追加
        tag = movie_id_to_tag[movie_id] # add: tagの追加
        if not (count_2 < count_1): # add: 選択した映画の非表示
            recommend_results.append({"movie_id":movie_id, "title": title, "genre": genre, "tag": tag, "score": score})
        count_2 += 1
    recommend_results = pd.DataFrame(recommend_results)
    st.write(recommend_results)