import datetime
from asyncio import Future, ensure_future

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    Float,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.lexers import DynamicLexer, PygmentsLexer
from prompt_toolkit.search import start_search
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Label,
    MenuContainer,
    MenuItem,
    SearchToolbar,
    TextArea,
)
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous


class Cli:

    kb = KeyBindings()
    buffer = Buffer()

    def __init__(self):
        self.status_text = "text"
        self.background = "bg:ansired"
        self.window = Window(BufferControl(buffer=self.buffer))
        self.body = HSplit(
            [
                self.window,
                # A vertical line in the middle. We explicitly specify the width, to make
                # sure that the layout engine will not try to divide the whole width by
                # three for all these windows.
                # Display the Result buffer on the right.
                VSplit(
                        [
                            Window(
                                FormattedTextControl(self.get_status_text), style="class:status"
                            ),],height=1,style=self.get_background)

            ]
        )
        self.root_container = MenuContainer(body=self.body, menu_items=[MenuItem("File"), MenuItem("Edit")], key_bindings=self.kb)
        self.application = Application(
        layout=Layout(self.root_container, focused_element=self.window),
        key_bindings=self.kb,
        # Let's add mouse support!
        mouse_support=True,
        # Using an alternate screen buffer means as much as: "run full screen".
        # It switches the terminal to an alternate screen.
        full_screen=True,
        )

        @self.kb.add("m", eager=True)
        def _(event):
            "Focus menu."
            event.app.layout.focus(self.root_container.window)
            self.buffer.text += "menu focused\n"
            self.set_status_text("menu focused")
            self.set_background("bg:ansigreen")

        @self.kb.add("t", eager=True)
        def _(event):
            "Focus text."
            self.buffer.text += "text focused\n"
            event.app.layout.focus(self.root_container.window)
            self.set_status_text("text focused")
            self.set_background("bg:ansired")


        @self.kb.add("c-c", eager=True)
        def _(event):
            """
            Pressing Ctrl-Q or Ctrl-C will exit the user interface.

            Setting a return value means: quit the event loop that drives the user
            interface and return this value from the `Application.run()` call.

            Note that Ctrl-Q does not work on all terminals. Sometimes it requires
            executing `stty -ixon`.
            """
            event.app.exit()

    def set_status_text(self, text):
        self.status_text = text

    def get_status_text(self):
        return self.status_text

    def set_background(self, text):
        self.background = text

    def get_background(self):
        return self.background

  

    
    def run(self):
        # Run the interface. (This runs the event loop until Ctrl-Q is pressed.)
        self.application.run()



