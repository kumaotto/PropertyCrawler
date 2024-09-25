# SUUMO Crawler And Notify Tool

## 特徴

- 条件に合った新しい家を通知
- お気に入りの家をリストアップ
  - 特定のアイコンで反応すると、ボットがメッセージをピン留めします。
  - 反応した物件はスプレッドシートでハイライトされます。（リアクションを外すとハイライトは削除されます）

## 使用方法

docs配下に格納されている `process1` 〜 `process3` までをご参照ください。
全て完了したら、以下でデプロイできます。

```shell
cd cdk/
cdk deploy --all
```

## 全て削除する場合

```shell
cd cdk/
cdk destroy --all
```
