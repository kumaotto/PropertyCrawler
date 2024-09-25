# Slackの設定

1. **`.env.example`をコピーする:**

```shell
   cp .env.example .env
```

1. **Slackでトークンを作成する**

手順:

1. Slack APIにログイン: [Slack API](https://api.slack.com/)にアクセスし、アプリを選択します。
![Slack API](docs/images/slack-api-top.png)
2. OAuth & Permissionsページ: 左側のメニューから「OAuth & Permissions」を選択します。
![OAuth & Permissions](docs/images/oauth-permissions.png)
3. Bot Token Scopes: 「Bot Token Scopes」セクションで、アプリに必要なスコープを追加します。このプロジェクトで必要な権限は以下です。

- chat:write (メッセージの投稿)
- channels:read (チャンネル情報の読み取り)
- channels:history
- groups:history
- im:history
- mpim:history
- incoming-webhook
- pins:write
- reactions:read

4. OAuthトークンの再生成: スコープを追加した後、「OAuth Tokens for Your Workspace」セクションで「Reinstall App」ボタンをクリックして新しいトークンを生成します。
![oauth-token](docs/images/oauth-tokens.png)

5. Incoming Webhooksからwebhook URLを払い出す
※後ほどURLは使うので控えておく
![webhooks](docs/images/webhooks.png)

6. 通知したいSlackのチャンネルをLambdaの環境変数に設定する
`cdk/crawling_batch_stack.py` の `TARGET_SLACK_CHANNEL` に値を入れる。
