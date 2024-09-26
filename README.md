# SUUMO Crawler And Notify Tool

## 特徴

- 条件に合った新しい家を通知
- お気に入りの家をリストアップ
  - 特定のアイコンで反応すると、ボットがメッセージをピン留めします。
  - 反応した物件はスプレッドシートでハイライトされます。（リアクションを外すとハイライトは削除されます）

## 使用方法

このプロジェクトはDevContainerを使用しています。
VSCodeの拡張機能にDevContainerを入れ、docker上で起動すると、cdkをローカルに入れる必要もなく楽です。
またSpreadSheetのテンプレートは `docs/` 配下にxlsxファイルで置いてあります。

※ aws-cliで設定されているアカウント、リージョンにデプロイされます

docs配下に格納されている `process1` 〜 `process3` までをご参照ください。
全て完了したら、以下でデプロイできます。

コンテナ起動時、初回だけ

```shell
poetry shell
```

```shell
cd cdk/
cdk deploy --all
```

デプロイ完了後、 `process4` を実施し設定を完了してください。

## 全て削除する場合

```shell
cd cdk/
cdk destroy --all
```
