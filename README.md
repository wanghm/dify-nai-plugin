## dify-nai-plugin

**Author:** huimin  
**Version:** 0.0.1  
**Type:** model  

### Description
`dify-nai-plugin` is a plugin designed for utilizing AI models. It processes prompts and generates responses using the specified model. Users can leverage both customizable and predefined models to suit their needs.

### Features
- **Multilingual Support**: Supports English (`en_US`), Simplified Chinese (`zh_Hans`), and Japanese (`ja_JP`).
- **Model Customization**: Allows users to configure their own models or use predefined ones.
- **Security**: Ensures data is processed within the user's environment and is not transmitted externally.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/dify-nai-plugin.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Import and initialize the plugin:
   ```python
   from dify_nai_plugin import DifyNaiPluginModelProvider

   provider = DifyNaiPluginModelProvider()
   ```

2. Invoke the model:
   ```python
   result = provider.invoke(
       model="your-model-name",
       credentials={"api_key": "your-api-key"},
       prompt_messages=[{"role": "user", "content": "Hello, world!"}],
       model_parameters={"temperature": 0.7}
   )
   print(result)
   ```

### Configuration
Edit the `dify-nai-plugin.yaml` file to configure models and credentials. Example configuration:

```yaml
models:
  - name: example-model
    path: models/llm/example_model/llm.py
model_credential_schema:
  credential_form_schemas:
    - variable: api_key
      label:
        en_US: API Key
      type: secret-input
      required: true
      placeholder:
        en_US: Enter your API Key
```

### License
This project is licensed under the [MIT License](./LICENSE).
