import inspect

import gradio as gr
from gradio.blocks import Block, BlockContext


class I18nString(str):
    def __str__(self):
        return self


def gettext(key: str):
    """Wrapper text string to return I18nString"""
    return I18nString(key)


def iter_i18n_fields(component: gr.components.Component):
    for name, value in inspect.getmembers(component):
        if isinstance(value, I18nString):
            yield name


def iter_i18n_components(block: Block):
    if isinstance(block, BlockContext):
        for component in block.children:
            for c in iter_i18n_components(component):
                yield c

    if any(iter_i18n_fields(block)):
        yield block


def dump_blocks(block: Block, langs=["en"], include_translations={}):
    """Dump all I18nStrings in the block to a dictionary"""
    components = list(iter_i18n_components(block))

    def get(lang, key):
        return include_translations.get(lang, {}).get(key, key)

    ret = {}

    for lang in langs:
        ret[lang] = {}
        for component in components:
            for field in iter_i18n_fields(component):
                value = "" + getattr(component, field)
                ret[lang][value] = get(lang, value)

    return ret


def translate_blocks(block: gr.Blocks, translation={}):
    """Translate all I18nStrings in the block"""
    if not isinstance(block, gr.Blocks):
        raise ValueError("block must be an instance of gradio.Blocks")

    components = list(iter_i18n_components(block))

    def get(lang, key):
        return translation.get(lang, {}).get(key, key)

    def set_lang(request: gr.Request):
        lang = request.headers["Accept-Language"].split(",")[0].split("-")[0].lower()
        if not lang:
            return

        outputs = []
        for component in components:
            fields = list(iter_i18n_fields(component))

            modified = {field: get(lang, getattr(component, field)) for field in fields}
            new_comp = component.__class__(**modified)
            outputs.append(new_comp)

        if len(outputs) == 1:
            return outputs[0]
        else:
            return outputs

    block.load(set_lang, None, outputs=components)

