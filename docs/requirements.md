### Stable Diffusion画像生成Discord Bot 要件定義書

#### 1. 概要
本プロジェクトは、Stable Diffusion WebUI (AUTOMATIC1111版) のAPIと連携し、Discord上でテキストから画像を生成するPython製のBotを開発するものである。ユーザーはDiscordのチャットに特定のコマンドとテキスト（プロンプト）を入力することで、手軽に画像生成を行えるようにする。

#### 2. 機能要件
- **画像生成機能**
    - Discordのスラッシュコマンド（例: `/generate`）を使用して画像生成をリクエストできる。
    - 必須パラメータとして、画像の内容を指示する「プロンプト (`prompt`)」を受け付ける。
    - 任意パラメータとして、以下の項目を指定できる。
        - ネガティブプロンプト (`negative_prompt`): 生成したくない要素の指定
        - 生成ステップ数 (`steps`): 画像の品質に影響
        - シード値 (`seed`): 画像の再現性を持たせるための値
        - 画像の幅 (`width`)
        - 画像の高さ (`height`)
        - サンプラー (`sampler`): `Euler a`, `DPM++ 2M Karras` などのサンプリング方法
        - CFGスケール (`cfg_scale`): プロンプトへの忠実度
    - Botはユーザーからのリクエストを受け付け後、「生成中です...」のような中間メッセージを返信する。
    - Stable Diffusion WebUI APIの `/sdapi/v1/txt2img` エンドポイントにリクエストを送信する。
    - APIから画像データを受け取り、生成された画像をDiscordのチャンネルに投稿する。
    - 投稿する際には、生成に使用したパラメータ（プロンプト、シード値など）を併記し、ユーザーが後から確認できるようにする。

- **エラーハンドリング機能**
    - Stable Diffusion WebUI APIサーバーがダウンしている、または応答がない場合に、ユーザーにエラーメッセージを通知する。
    - APIへのリクエストが失敗した場合（無効なパラメータなど）に、エラー内容をユーザーに通知する。

- **ヘルプ機能**
    - Botの基本的な使い方や、利用可能なコマンド、パラメータの一覧を表示するヘルプコマンド（例: `/help`）を実装する。

#### 3. 非機能要件
- **設定管理**
    - Discord Botのトークンや、Stable Diffusion WebUI APIのエンドポイントURLなどの設定値は、コードに直接書き込まず、設定ファイル（例: `.env` ファイル）で管理する。
- **依存ライブラリ**
    - `discord.py` (またはその後継ライブラリ) を使用してDiscord Botを実装する。
    - `requests` または `httpx` を使用してAPIへのHTTPリクエストを行う。
    - `python-dotenv` を使用して設定ファイルを読み込む。
- **ロギング**
    - 実行中のイベント（画像生成リクエスト、エラーなど）をコンソールやログファイルに出力し、デバッグや運用監視を容易にする。

#### 4. 開発環境・使用ライブラリ
- **言語:** Python 3.10以上
- **主要ライブラリ:**
    - `discord.py`
    - `requests` / `httpx`
    - `python-dotenv`
    - `Pillow` (画像のハンドリングが必要な場合)
