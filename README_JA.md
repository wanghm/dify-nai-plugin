## dify-nai-plugin

**Author:** huimin  
**Version:** 0.0.1  
**Type:** model  

### Description
`dify-nai-plugin`は、AIモデルを利用するためのプラグインです。このプラグインは、プロンプトを処理し、指定されたモデルを使用して応答を生成します。ユーザーは、カスタマイズ可能なモデルや事前定義されたモデルを利用できます。

### Features
- **多言語対応**: 英語（`en_US`）、簡体字中国語（`zh_Hans`）、日本語（`ja_JP`）をサポート。
- **モデルのカスタマイズ**: ユーザーが独自のモデルを設定可能。
- **セキュリティ**: データはユーザーの環境内で処理され、外部に送信されません。

### Installation
1. このリポジトリをクローンします:
   ```bash
   git clone https://github.com/your-repo/dify-nai-plugin.git
   ```
2. 必要な依存関係をインストールします:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
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

### Configuration
`dify-nai-plugin.yaml`ファイルを編集して、モデルや認証情報を設定します。

### License
このプロジェクトは [MIT License](./LICENSE) の下でライセンスされています。
