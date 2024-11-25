import gradio as gr

from gradio_i18n import Translate
from gradio_i18n import gettext as _


def greet(name, gender, lang):
    return f"Hello {name} {gender} in {lang}!"


with gr.Blocks() as demo:
    with Translate(
        "translation.yaml", placeholder_langs=["en", "zh", "zh-Hant", "ja", "ko", "es", "fr", "de"]
    ) as lang:
        name = gr.Textbox(label=_("Name"), placeholder=_("Input your name here."))
        gender = gr.Radio(choices=[_("Male"), _("Female"), _("Unknown")])
        output = gr.Textbox(label=_("Greeting"))
        submit_btn = gr.Button(value=_("Submit"))

    submit_btn.click(greet, inputs=[name, gender, lang], outputs=output)

demo.launch()
