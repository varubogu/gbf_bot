# テーブル定義

sqlalchemyを用いて生成するため、基本は/src/gbf/models/内のテーブル定義に従う。

## テーブルの役割（分類）について

テーブルごとに３種類の役割があり、さらに全サーバー共通用・サーバー毎用に分かれる。

### reference

頻繁には変更せず、参照が中心のテーブル
エンジニア用語で言えば「マスターテーブル」と呼ばれたりする
全体用のスプレッドシート、またはサーバー毎のスプレッドシートからデータを読み込み、データベースへと反映する機能を持つ。

### transaction

現在進行中または未来の情報
例えばマルチバトル募集や将来のスケジュールなど
内部の値の確認ができるよう、スプレッドシートへ反映する

### history

履歴に関する情報
例えばスプレッドシート最終読込日時など
内部の値の確認ができるよう、スプレッドシートへ反映する