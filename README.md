# Mimatto (みまっと): Tokyo Region-based Minor Offense Crime Heatmap

![crime_analysis](https://img.shields.io/badge/crime_analysis-3B4CC0)
![tokyo](https://img.shields.io/badge/tokyo-648FFF)
![heatmap](https://img.shields.io/badge/heatmap-FD8264)
![flask_api](https://img.shields.io/badge/flask_api-B40426)

![image_from_website](https://lh3.googleusercontent.com/d/1vFw7bat2Jcg4K31fPdLo9wRmXQXEosuj)

This project was submitted to the service development category (サービス開発部門) of the Tokyo Open Data Hackathon 2024, under the team name hinyari mapping (ひんやりまっぴんぐ). View the project page [here](https://odhackathon.metro.tokyo.lg.jp/collection/85/).

The crime heatmap works by representing the arrangement of regions (区市町村の町丁) as computational graph with edges between regions denoting that they share a border. Minor offenses reporting in a precinct don't necessarily have to originate in that precinct, and the public safety of a region can depend on its surrounding regions. Take the example of the Sumida River fireworks and it's influence on not only the regions where people view the fireworks but in the surrounding areas that people may use to park their cars, bicycles or as nodes for public transit. We observe this phenomena in detail in the regions of Shinjuku 4th district (新宿４丁目) and Kabukicho 2nd district (歌舞伎町２丁目).

We use the following datasets (links in Japanese):
1. [Bounding (shapely) polygons for reigons in Japan, by Ministry of Land, Infrastructure, Transport and Tourism (MLITT)](https://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi)
2. [2022 Statistics Report, published by the Tokyo Metropolitan Police Department](https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/tokei/k_tokei04.html)
3. [2024 Region-based Crime Type Dataset by the Tokyo Metropolitan Police Department](https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/jokyo/ninchikensu.html)

Formatted versions of these datasets (retrieved August 2024) as available in the `data/` directory.
