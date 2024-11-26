import gradio as gr

from gradio_i18n import Translate
from gradio_i18n import gettext as _


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
