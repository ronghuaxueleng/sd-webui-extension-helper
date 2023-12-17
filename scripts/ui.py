import gradio as gr

import configparser
import os
from git import Repo

import shutil
from pathlib import Path
from modules import script_callbacks
from modules.paths_internal import extensions_dir

headers = ["扩展", "地址", "版本", "操作"]
datatype = ["str", "str", "str", "html"]


def config_parse(ini_path: str) -> str:
    config = configparser.ConfigParser()
    try:
        config.read(ini_path)  # 'gbk' codec can't decode byte 0xa6 in position 254: illegal multibyte sequence
    except:
        pass
    else:
        for section in config.sections():
            if 'remote' in section:
                if 'url' in config[section]:
                    return config[section]['url']
        return ''
    finally:
        pass  # 是否有异常时都会执行


def load_extension_list():
    template_values = []
    p = Path(extensions_dir)
    for x in p.iterdir():
        if x.is_dir():
            temp_list = list()
            temp_list.append(x.name)
            repo_path = os.path.join(extensions_dir, x.name)
            config_path = os.path.join(repo_path, '.git', 'config')
            if os.path.exists(config_path):
                url = config_parse(config_path)
                temp_list.append(url)
                repo = Repo(repo_path)
                temp_list.append(repo.active_branch.commit.name_rev)
                update_onclick = f'''update_extensions("{repo_path}")'''
                delete_onclick = f'''delete_extensions("{repo_path}")'''
                buttons = f"""
                        <div style='margin-top: 3px; text-align: center;'>
                            <button style='width: 102px;' class='secondary gradio-button svelte-cmf5ev' onclick='{update_onclick}'>更新</button>
                        </div>
                        <div style='margin-top: 3px; text-align: center;'>
                            <button style='width: 102px;' class='secondary gradio-button svelte-cmf5ev' onclick='{delete_onclick}'>删除</button>
                        </div>
                        """
                temp_list.append(buttons)
            template_values.append(temp_list)

    return template_values


def update_extensions(repo_path):
    if os.path.exists(repo_path):
        repo = Repo(repo_path)
        repo.git.pull()


def delete_extensions(repo_path):
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)


def ui_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Row(elem_id="prompt_main"):
            selected_text = gr.TextArea(elem_id='extension_path', visible=False)
            update_extensions_btn = gr.Button(elem_id='update_extensions_btn', visible=False)
            delete_extensions_btn = gr.Button(elem_id='delete_extensions_btn', visible=False)
        with gr.Row():
            with gr.Tab(label='扩展列表', elem_id="extension_list_tab"):
                with gr.Row():
                    datatable = gr.DataFrame(headers=headers,
                                             datatype=datatype,
                                             interactive=False,
                                             wrap=True,
                                             max_rows=10,
                                             show_label=True,
                                             overflow_row_behaviour="show_ends",
                                             value=load_extension_list(),
                                             elem_id="extension_list"
                                             )
                    update_extensions_btn.click(update_extensions, inputs=selected_text, outputs=datatable)
                    delete_extensions_btn.click(delete_extensions, inputs=selected_text, outputs=datatable)

        return [(ui, "扩展管理", "extensions_manager")]


script_callbacks.on_ui_tabs(ui_tab)
