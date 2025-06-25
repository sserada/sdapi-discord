# sdapi-discord

このプロジェクトは、Stable Diffusion APIを使用してテキストプロンプトから画像を生成するDiscordボットです。

[Click here for the English README](./README.md)

## 機能

-   **画像生成**: `/generate` コマンドを使用して、テキストプロンプトから画像を生成します。
-   **カスタマイズ可能なパラメータ**: ネガティブプロンプト、シード、ステップ数、サンプラーなど、画像生成のためのさまざまなパラメータを調整できます。
-   **ヘルプコマンド**: `/help` コマンドでボットの使い方に関する情報を取得できます。

## 前提条件

-   Python 3.8以上
-   Discordボットトークン
-   Stable Diffusion APIの実行中のインスタンス

## インストール

1.  **リポジトリをクローンします:**

    ```bash
    git clone https://github.com/sserada/sdapi-discord.git
    cd sdapi-discord
    ```

2.  **依存関係をインストールします:**

    このプロジェクトでは、依存関係の管理に [Rye](https://rye-up.com/) を使用しています。

    ```bash
    rye sync
    ```

3.  **環境変数を設定します:**

    サンプルファイルをコピーして `.env` ファイルを作成します:

    ```bash
    cp .env.example .env
    ```

    `.env` ファイルを開き、DiscordボットトークンとStable Diffusion APIインスタンスのURLを追加します:

    ```
    DISCORD_BOT_TOKEN="your-discord-bot-token"
    SD_API_URL="http://127.0.0.1:7860"
    ```

## 使い方

ボットを起動するには、次のコマンドを実行します:

```bash
rye run start
```

### Discordコマンド

-   `/generate <prompt> [options]`: 画像を生成します。
    -   `prompt` (必須): 生成したい画像の主な説明。
    -   `negative_prompt` (任意): 画像で避けたいものの説明。
    -   `seed` (任意): 前の画像を再現するための特定の番号。
    -   `steps` (任意): 生成ステップ数。
    -   `sampler` (任意): 使用するサンプリング方法。
    -   `cfg_scale` (任意): 画像がプロンプトにどれだけ強く準拠するかの度合い。
    -   `width` (任意): 画像の幅。
    -   `height` (任意): 画像の高さ。
-   `/help`: ヘルプ情報を表示します。

## 貢献

貢献を歓迎します！ issueを開いたり、プルリクエストを送信したりしてください。
