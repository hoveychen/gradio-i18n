# gradio-i18n

<a href="https://pypi.org/project/gradio-i18n/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio-i18n"></a> <a href="https://github.com/hoveychen/gradio-i18n/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> 

Reactive Multi-language Gradio App with minimal effort. Enables Gradio app displayiing localized UI responding to the browser language settings.

## Installation
    
```bash 
pip install gradio-i18n
```

## Usage

1. Prepare a translation dict like examples below. 
2. Wrap text intended to be localized with `gradio_i18n.gettext()`
3. Invoke `gradio_i18n.translate_blocks()`, within the context of gradio blocks.

```python

import gradio as gr
from gradio_i18n import gettext, translate_blocks


def greet(name):
    return f"Hello {name}!"


lang_store = {
    "en": {
        "Submit": "Submit✅",
        "Name": "Name 📛",
        "Greeting": "Greeting 🎉",
        "Input your name here.": "Input your name here. 📝",
    },
    "zh": {
        "Submit": "提交",
        "Name": "名字",
        "Greeting": "问候",
        "Input your name here.": "在这里输入你的名字。",
    },
}

with gr.Interface(
    fn=greet,
    inputs=gr.Textbox(
        label=gettext("Name"), placeholder=gettext("Input your name here.")
    ),
    outputs=gr.Textbox(label=gettext("Greeting")),
    submit_btn=gettext("Submit"),
) as demo:
    translate_blocks(demo, lang_store)

demo.launch()

```

> [!NOTE]
> Keep in mind that the translate_blocks() function MUST BE called in the gradio block context (`with`)

# Build translation dictionary

To build the transtion dictionary to be passed to `translate_blocks`, we provide a simple helper function to dump all the i18n texts from the gradio blocks object.

This is an example of using yaml to persist the translation.

```python
import gradio_i18n
import yaml

trans_file = "translations.yaml"
if not os.path.exists(trans_file):
    lang_store = {}
else:
    lang_store = yaml.safe_load(open(trans_file))

# define your gradio block here....
# with gr.Blocks() as block:
#     ....
#     gradio_i18n.translate_blocks(block, lang_store)

collected_texts = gradio_i18n.dump_blocks(block, langs=["zh", "en"], include_translations=lang_store)
yaml.safe_dump(collected_texts, open(trans_file, "w"))
```

