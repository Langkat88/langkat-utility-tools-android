import sys
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


try:
    from core.response_inference import generate_response
    IMPORT_ERROR = None
except Exception as e:
    generate_response = None
    IMPORT_ERROR = str(e)


class LaNgKaTAIApp(App):

    def build(self):
        self.title = "LaNgKaT AI"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        header = Label(
            text="LaNgKaT AI\nVersion 0.1",
            size_hint_y=None,
            height=dp(75),
            font_size=dp(23),
            bold=True,
            halign="center",
            valign="middle"
        )

        root.add_widget(header)

        self.scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(8)
        )

        self.chat_label = Label(
            text="LaNgKaT AI: Online\n\n",
            size_hint_y=None,
            font_size=dp(18),
            halign="left",
            valign="top",
            padding=(dp(8), dp(8))
        )

        self.chat_label.bind(
            texture_size=self.update_chat_size
        )

        self.scroll.add_widget(self.chat_label)
        root.add_widget(self.scroll)

        input_area = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(65),
            spacing=dp(8)
        )

        self.input_box = TextInput(
            hint_text="I-type ang message...",
            multiline=False,
            font_size=dp(18),
            padding=[dp(12), dp(12)],
            write_tab=False
        )

        self.input_box.bind(
            on_text_validate=self.send_message
        )

        send_button = Button(
            text="SEND",
            size_hint_x=None,
            width=dp(105),
            font_size=dp(18),
            bold=True
        )

        send_button.bind(
            on_release=self.send_message
        )

        input_area.add_widget(self.input_box)
        input_area.add_widget(send_button)

        root.add_widget(input_area)

        return root

    def update_chat_size(self, instance, value):
        self.chat_label.text_size = (
            self.scroll.width - dp(16),
            None
        )

        self.chat_label.height = (
            self.chat_label.texture_size[1] + dp(16)
        )

    def send_message(self, *args):

        user_text = self.input_box.text.strip()

        if not user_text:
            return

        self.input_box.text = ""

        self.chat_label.text += (
            f"You: {user_text}\n"
        )

        if user_text.lower() == "exit":
            self.stop()
            return

        if generate_response is None:
            response = (
                "Hindi ma-load ang LaNgKaT AI engine.\n"
                f"Error: {IMPORT_ERROR}"
            )
        else:
            try:
                response = generate_response(user_text)

                if not response:
                    response = (
                        "Hindi ko pa alam ang sagot. "
                        "Maaari mo akong turuan tungkol dito."
                    )

            except Exception as e:
                response = f"AI Error: {e}"

        self.chat_label.text += (
            f"LaNgKaT AI: {response}\n\n"
        )

        Clock.schedule_once(
            self.scroll_to_bottom,
            0.1
        )

    def scroll_to_bottom(self, *args):
        self.scroll.scroll_y = 0


if __name__ == "__main__":
    LaNgKaTAIApp().run()
