# gradio-i18n

![GitHub License](https://img.shields.io/github/license/hoveychen/gradio-i18n)
![PyPI - Version](https://img.shields.io/pypi/v/gradio-i18n)
[![Huggingface](https://img.shields.io/badge/🤗%20-online%20demo-yellow.svg)](https://huggingface.co/spaces/hoveyc/gradio-i18n)


Reactive Multi-language Gradio App with minimal effort. Enables Gradio app displayiing localized UI responding to the browser language settings.

## Changelog
* v0.2.0: Support persistant language setting in the browser. Support language variants like `zh-Hant`.

## Installation
    
```bash 
pip install gradio-i18n
```

## Basic Example

If you want localized UI based on user's browser language, simply wrap your block definition with `gradio_i18n.Translate()`.
* Wrap all your texts to localize with `gradio_i18n.gettext()`, refer to the example.
* `Translate()` returns the user's language to pass to function inputs.
* `Translate()` accepts a filepath or dict as the translation dict.
* Optional argument `placeholder_langs` will fill key not translated as placeholder back to the disk file.

```python
import gradio as gr

from gradio_i18n import Translate, gettext as _

def greet(name, gender, lang):
    return _("Greeting") + f"! Hello {name} {gender} in {lang}!"

with gr.Blocks() as demo:
    with Translate("translation.yaml", placeholder_langs=["en", "zh", "zh-Hant", "ja", "ko", "es", "fr", "de"]) as lang:
        name = gr.Textbox(
            label=_("Name"), placeholder=_("Input your name here.")
        )
        gender = gr.Radio(choices=[_("Male"), _("Female"), _("Unknown")])
        output = gr.Textbox(label=_("Greeting"))
        submit_btn = gr.Button(value=_("Submit"))

    submit_btn.click(greet, inputs=[name, gender, lang], outputs=output)

demo.launch()

```

## Change UI language Example

You may want user to choose their expected language, pass the component controlling the language value to `gradion_i18n.Translate()`.
If you want to save the language settings after user has chosen the language, pass `persistent=True` in `Translate()` or `translate_blocks()`(Note: gradio >= 5.6.0 is required).

```python
def greet(name, gender, lang):
    return _("Greeting") + _("Hello {name} {gender} in {lang}").format(
        name=name, gender=gender, lang=lang
    )


with gr.Blocks() as demo:
    lang = gr.Radio(
        choices=[
            ("English", "en"),
            ("简体中文", "zh"),
            ("繁體中文", "zh-Hant"),
            ("日本語", "ja"),
            ("한국인", "ko"),
            ("español", "es"),
            ("française", "fr"),
            ("Deutsch", "de"),
        ],
        label=_("Language"),
        render=False,  # You may define the choices ahead before passing to Translate blocks.
    )
    with Translate(
        "translation.yaml",
        lang,
        placeholder_langs=["en", "zh", "zh-Hant", "ja", "ko", "es", "fr", "de"],
        persistant=False,  # True to save the language setting in the browser. Requires gradio >= 5.6.0
    ):
        lang.render()
        name = gr.Textbox(label=_("Name"), placeholder=_("Input your name here."))
        gender = gr.Radio(choices=[_("Male"), _("Female"), _("Unknown")])
        output = gr.Textbox(label=_("Greeting"))
        submit_btn = gr.Button(value=_("Submit"))

    submit_btn.click(greet, inputs=[name, gender, lang], outputs=output)

demo.launch()

```

## Advanced Usage for better control

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
    translate_blocks(translation=lang_store)

demo.launch()

```

> [!NOTE]
> Keep in mind that the translate_blocks() function MUST BE called in the gradio block context (`with`)

## Get/Set current language
Except for automatically translated text value in Gradio components, user may expect to get the current language of the user for localizing contents. To get the current language, simply pass in any component into argument `lang` of `translate_blocks()`, and you will get the language value in the object.

Also, if you change the value of the passed in object, the overall UI will update accordingly.

Example:
```python
import gradio as gr
import gradio_i18n

def get_lang(lang):
    return f"You are using language: {lang}"


with gr.Blocks() as block:
    lang = gr.Dropdown(choices=["zh", "en", "ja"])
    display_lang = gr.Text()
    btn = gr.Button()
    btn.click(get_lang, inputs=[lang], outputs=[display_lang])
    gradio_i18n.translate_blocks(lang=lang)

block.launch()
```

> [!NOTE]
> Only dict type state is supported at this moment.

## Generate a translation dictionary placeholder

To build the transtion dictionary, we provide function `dump_blocks()` to dump all the i18n texts from the gradio blocks object.

This is an example of using yaml/json to persist the translation.


### JSON
```python
import gradio as gr
import gradio_i18n
import json

trans_file = "translations.json"
if not os.path.exists(trans_file):
    lang_store = {}
else:
    lang_store = json.load(open(trans_file))

# define your gradio block here....
# with gr.Blocks() as block:
#     ....
#     gradio_i18n.translate_blocks(block, lang_store)

collected_texts = gradio_i18n.dump_blocks(block, langs=["zh", "en"], include_translations=lang_store)
json.dump(collected_texts, open(trans_file, "w"), indent=2, ensure_ascii=False)
```

### YAML
```python
import gradio as gr
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
yaml.safe_dump(collected_texts, open(trans_file, "w"), allow_unicode=True)
```
