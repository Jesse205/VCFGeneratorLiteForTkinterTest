import re
import traceback
import webbrowser
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from tkinter import filedialog, Event
from tkinter.constants import *
from tkinter.ttk import *

from vcf_generator_lite.constants import URL_RELEASES, URL_SOURCE, APP_NAME, DEFAULT_INPUT_CONTENT, USAGE, URL_REPORT
from vcf_generator_lite.ui.about import open_about_window
from vcf_generator_lite.ui.base import BaseWindow, EVENT_EXIT
from vcf_generator_lite.util import dialog
from vcf_generator_lite.util.menu import MenuCascade, MenuCommand, MenuSeparator
from vcf_generator_lite.util.vcard import GenerateResult, VCardProcessor
from vcf_generator_lite.util.widget import get_auto_wrap_event
from vcf_generator_lite.widget.menu import TextContextMenu
from vcf_generator_lite.widget.scrolled_text import ScrolledText

MAX_INVALID_COUNT = 200

EVENT_ON_ABOUT_CLICK = "<<OnAboutClick>>"
EVENT_ON_CLEAN_QUOTES_CLICK = "<<OnCleanQuotesClick>>"
EVENT_ON_GENERATE_CLICK = "<<OnGenerateClick>>"


class MainWindow(BaseWindow):
    generate_button = None
    text_input = None
    text_context_menu = None
    progress_bar = None

    def on_init_window(self):
        self.anchor(CENTER)
        self.title(APP_NAME)
        self.set_minsize(400, 400)
        self.set_size(600, 600)
        self._create_widgets()
        self._create_menus()

    def _create_widgets(self):
        description_label = Label(self, text=USAGE, justify=LEFT)
        description_label.bind("<Configure>", get_auto_wrap_event(description_label))
        description_label.pack(fill=X, padx="10p", pady="10p")

        self.text_input = ScrolledText(self, undo=True, tabs="2c", tabstyle="wordprocessor")
        self.text_input.insert(0.0, DEFAULT_INPUT_CONTENT)
        self.text_input.edit_reset()
        self.text_input.pack(fill=BOTH, expand=True, padx="10p", pady=0)
        self.text_context_menu = TextContextMenu(self.text_input)
        self.text_context_menu.bind_to_widget()

        action_frame = Frame(self)
        action_frame.pack(fill=X)

        sizegrip = Sizegrip(action_frame)
        sizegrip.place(relx=1, rely=1, anchor=SE)

        self.progress_bar = Progressbar(action_frame, orient=HORIZONTAL, length=200)

        self.generate_button = Button(action_frame, text="生成", default=ACTIVE,
                                      command=lambda: self.event_generate(EVENT_ON_GENERATE_CLICK))
        self.generate_button.pack(side=RIGHT, padx="10p", pady="10p")

    def _create_menus(self):
        self.add_menus(
            MenuCascade(
                label="文件(&F)",
                items=[
                    MenuCommand(
                        label="退出(&X)",
                        command=self.quit,
                        accelerator="Alt + F4",
                    )
                ]
            ),
            MenuCascade(
                label="编辑(&E)",
                items=[
                    MenuCommand(
                        label="剪切(&T)",
                        command=lambda: self.focus_get().event_generate("<<Cut>>"),
                        accelerator="Ctrl + X",
                    ),
                    MenuCommand(
                        label="复制(&C)",
                        command=lambda: self.focus_get().event_generate("<<Copy>>"),
                        accelerator="Ctrl + C",
                    ),
                    MenuCommand(
                        label="粘贴(&P)",
                        command=lambda: self.focus_get().event_generate("<<Paste>>"),
                        accelerator="Ctrl + V",
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label="移除引号",
                        command=lambda: self.event_generate(EVENT_ON_CLEAN_QUOTES_CLICK),
                    ),
                ]
            ),
            MenuCascade(
                label="帮助(&H)",
                items=[
                    MenuCommand(
                        label="开源仓库(&O)",
                        command=lambda: webbrowser.open(URL_SOURCE),
                    ),
                    MenuCommand(
                        label="版本发布网址(&R)",
                        command=lambda: webbrowser.open(URL_RELEASES),
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label="提交反馈(&F)",
                        command=lambda: webbrowser.open(URL_REPORT),
                    ),
                    MenuCommand(
                        label="关于 VCF 生成器 Lite(&A)",
                        command=lambda: self.event_generate(EVENT_ON_ABOUT_CLICK),
                    )
                ]
            )
        )

    def set_text_content(self, content: str):
        self.text_input.replace(1.0, END, content)

    def get_text_content(self) -> str:
        return self.text_input.get(1.0, END)[:-1]

    def show_progress_bar(self):
        self.progress_bar.pack(side=LEFT, padx="10p", pady="10p")

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def set_progress(self, progress: float):
        self.progress_bar.configure(value=progress)

    def set_progress_determinate(self, value: bool):
        previous_value: bool = self.progress_bar.cget("mode") == "determinate"
        if previous_value != previous_value:
            return
        if value:
            self.progress_bar.configure(mode="determinate", maximum=1)
            self.progress_bar.stop()
        else:
            self.progress_bar.configure(mode="indeterminate", maximum=10)
            self.progress_bar.start()

    def set_generate_enabled(self, enabled: bool):
        self.generate_button.configure(state="normal" if enabled else "disabled")


def clean_quotes(text: str) -> str:
    return re.sub(r'"\s*(([^"\s][^"]*[^"\s])|[^"\s]?)\s*"', r'\1', text, flags=re.S)


class MainController:
    is_generating = False

    def __init__(self, window: MainWindow):
        self.window = window
        window.bind(EVENT_ON_ABOUT_CLICK, self.on_about_click)
        window.bind(EVENT_ON_CLEAN_QUOTES_CLICK, self.on_clean_quotes_click)
        window.bind(EVENT_ON_GENERATE_CLICK, self.on_generate_click)
        window.bind("<Control-S>", self.on_generate_click)
        window.bind("<Control-s>", self.on_generate_click)
        window.bind("<Return>", self.on_return_click)
        window.bind(EVENT_EXIT, self.on_exit)

    def on_about_click(self, _):
        open_about_window(self.window)

    def on_clean_quotes_click(self, _):
        self._clean_quotes()

    def on_return_click(self, event: Event):
        if event.widget is self.window.text_input:
            return
        self.window.generate_button.invoke()

    def on_generate_click(self, _):
        text_content = self.window.get_text_content()
        file_io = filedialog.asksaveasfile(parent=self.window, initialfile="phones.vcf",
                                           filetypes=[("vCard 文件", ".vcf")], defaultextension=".vcf")
        if file_io is None:
            return

        self.is_generating = True
        self.window.show_progress_bar()
        self.window.set_progress(0)
        self.window.set_progress_determinate(False)
        self.window.set_generate_enabled(False)

        def done(future: Future[GenerateResult]):
            file_io.close()
            self._show_generate_done_dialog(file_io.name, future.result())
            self.is_generating = False
            self.window.hide_progress_bar()
            self.window.set_generate_enabled(True)

        def on_update_progress(progress: float, determinate: bool):
            self.window.set_progress_determinate(determinate)
            if determinate:
                self.window.set_progress(progress)

        executor = ThreadPoolExecutor(max_workers=1)
        processor = VCardProcessor(executor)
        processor.add_progress_callback(on_update_progress)
        progress_future = processor.generate(text_content, file_io)
        progress_future.add_done_callback(done)
        executor.shutdown(wait=False)

    def on_exit(self, _):
        if self.is_generating:
            dialog.show_warning(self.window, "正在生成文件", "文件正在生成中，无法关闭窗口。请稍后重试。")
        else:
            self.window.destroy()

    def _show_generate_done_dialog(self, display_path: str, generate_result: GenerateResult):
        invalid_items = generate_result.invalid_items
        title_success = "生成 VCF 文件成功"
        title_failure = "生成 VCF 文件失败"
        title_partial_failure = "生成 VCF 文件部分成功"
        message_success_template = "已导出文件到“{path}”。"
        message_failure_template = "生成 VCF 文件时出现未知异常：\n\n{content}"
        message_partial_failure_template = "以下电话号码无法识别：\n{content}\n\n已导出文件到 {path}，但异常的号码未包含在导出文件中。"
        invalid_item_template = "第 {line} 行：{content}"
        ignored_template = "{content}... 等 {ignored_count} 个。"

        if generate_result.exceptions:
            formatted_exceptions = [
                "\n".join(traceback.format_exception(exception)) for exception in generate_result.exceptions
            ]
            dialog.show_error(self.window, title_failure,
                              message_failure_template.format(content="\n\n".join(formatted_exceptions)))
        elif len(invalid_items) > 0:
            content = '，'.join([
                invalid_item_template.format(line=item.line, content=item.content)
                for item in invalid_items[0:MAX_INVALID_COUNT]
            ])
            if (ignored_count := max(len(invalid_items) - MAX_INVALID_COUNT, 0)) > 0:
                content = ignored_template.format(content=content, ignored_count=ignored_count)
            dialog.show_warning(self.window, title_partial_failure, message_partial_failure_template.format(
                content=content,
                path=display_path
            ))
        else:
            dialog.show_info(self.window, title_success, message_success_template.format(path=display_path))

    def _clean_quotes(self):
        origin_text = self.window.get_text_content()
        self.window.set_text_content(clean_quotes(origin_text))


def create_main_window() -> tuple[MainWindow, MainController]:
    window = MainWindow()
    controller = MainController(window)
    return window, controller
