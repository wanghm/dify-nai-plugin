## dify-nai-plugin

**作者:** huimin  
**バージョン:** 0.0.1  
**タイプ:** モデル  

### 説明
`dify-nai-plugin`は、AIモデルを利用するためのプラグインです。このプラグインは、プロンプトを処理し、指定されたモデルを使用して応答を生成します。ユーザーは、カスタマイズ可能なモデルや事前定義されたモデルを利用できます。

### 特徴
- **多言語対応**: 英語（`en_US`）、簡体字中国語（`zh_Hans`）、日本語（`ja_JP`）をサポート。
- **モデルのカスタマイズ**: ユーザーが独自のモデルを設定可能。
- **セキュリティ**: データはユーザーの環境内で処理され、外部に送信されません。

### インストール
1. このリポジトリをクローンします:
   ```bash
   git clone https://github.com/your-repo/dify-nai-plugin.git
   ```

2. 必要な依存関係をインストールします:
   ```bash
   pip install -r requirements.txt
   ```

### 使用方法
1. プラグインをインポートして初期化します:
   ```python
   from dify_nai_plugin import DifyNaiPluginModelProvider

   provider = DifyNaiPluginModelProvider()
   ```

2. モデルを呼び出します:
   ```python
   result = provider.invoke(
       model="your-model-name",
       credentials={"api_key": "your-api-key"},
       prompt_messages=[{"role": "user", "content": "こんにちは、世界！"}],
       model_parameters={"temperature": 0.7}
   )
   print(result)
   ```

### 設定
`dify-nai-plugin.yaml`ファイルを編集して、モデルや認証情報を設定します。設定例:

```yaml
models:
  - name: example-model
    path: models/llm/example_model/llm.py
model_credential_schema:
  credential_form_schemas:
    - variable: api_key
      label:
        ja_JP: APIキー
      type: secret-input
      required: true
      placeholder:
        ja_JP: APIキーを入力してください
```

### ライセンス
このプロジェクトは [MIT License](./LICENSE) の下でライセンスされています。

### お問い合わせ
質問や問題がある場合は、[support@example.com](mailto:support@example.com)までご連絡ください。
