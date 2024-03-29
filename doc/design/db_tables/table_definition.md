# テーブル定義

sqlalchemyを用いて生成するため、基本は/src/gbf/models/内のテーブル定義に従う。

## テーブルの役割について

テーブルごとに３種類の役割があり、さらに２種類のスコープに分かれる。

### テーブルの役割詳細

テーブルに対応するクラスの__tabletype__属性に設定する。

#### reference

頻繁には変更せず、参照が中心のテーブル。
エンジニア用語で言えば「マスターテーブル」と呼ばれたりする。
全体用のスプレッドシート、またはサーバー毎のスプレッドシートからデータを読み込み、データベースへと反映する機能を持つ。

#### transaction

現在進行中または未来の情報。
例えばマルチバトル募集や将来のスケジュールなど。
内部の値の確認ができるよう、スプレッドシートへ反映する。

#### history

履歴に関する情報。
例えばスプレッドシート最終読込日時など。
内部の値の確認ができるよう、スプレッドシートへ反映する。

### テーブルのスコープについて

テーブルに対応するクラスの__tablescope__属性に設定する。

#### グローバルスコープ

全サーバー共通のテーブル。

#### サーバー（ギルド）スコープ

各サーバー固有のテーブル。
グローバルスコープとキーが同じものについてはサーバースコープを優先する。
