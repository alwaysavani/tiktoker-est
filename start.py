# Save this file as token_counter.py
import reflex as rx
import tiktoken

# Define the state for the application.
# This class holds all the variables and functions that can be updated or called from the frontend.
class State(rx.State):
    """The app's state."""
    text_input: str = ""
    token_count: int = 0
    is_counting: bool = False
    error_message: str = ""

    # Load the tiktoken encoding. This is done once when the state is initialized.
    # The 'cl100k_base' encoding is widely used for modern models.
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception:
        encoding = None
        error_message = "tiktoken encoding could not be loaded."

    def estimate_tokens(self):
        """Calculates the number of tokens in the text input."""
        # Set a loading state and reset the count
        self.is_counting = True
        self.token_count = 0
        self.error_message = ""

        if not self.encoding:
            self.error_message = "Error: Tokenization library not available."
            self.is_counting = False
            return

        # Check if the input text is empty
        if not self.text_input:
            self.token_count = 0
            self.is_counting = False
            return

        try:
            # Use tiktoken to encode the text and get the number of tokens
            tokens = self.encoding.encode(self.text_input)
            self.token_count = len(tokens)
        except Exception as e:
            self.error_message = f"Failed to count tokens: {e}"
        finally:
            self.is_counting = False

# Define the user interface (UI) components.
# This function describes how the page looks and binds UI elements to state variables.
def index():
    return rx.center(
        rx.card(
            rx.text("Python Token Counter", font_size="2em", font_weight="bold", text_align="center"),
            rx.text(
                "Enter text below to get an accurate token count.",
                color="#a0aec0",
                text_align="center",
                margin_bottom="1.5em",
            ),
            rx.text_area(
                placeholder="Paste your text here...",
                on_change=State.set_text_input,  # Binds the input to the state variable
                height="200px",
                width="100%",
            ),
            rx.hstack(
                rx.button(
                    "Count Tokens",
                    on_click=State.estimate_tokens, # Binds the button click to the state function
                    is_loading=State.is_counting, # Shows a loading spinner while counting
                    loading_text="Counting...",
                    width="100%",
                ),
                width="100%",
                margin_top="1em"
            ),
            rx.cond(
                State.token_count > 0, # Conditional rendering based on token_count
                rx.box(
                    rx.text("Estimated Token Count:", color="#a0aec0", font_size="0.8em"),
                    rx.text(State.token_count.to_string(), font_size="2.5em", font_weight="extrabold"),
                    text_align="center",
                    padding_top="1em",
                )
            ),
            rx.cond(
                State.error_message,
                rx.box(
                    rx.text(State.error_message, color="red.500", text_align="center"),
                    padding_top="1em",
                )
            ),
            width="100%",
            max_width="600px",
            background_color="#2d3748",
            padding="2.5rem",
            border_radius="1.5rem",
            box_shadow="lg",
            border="1px solid #4a5568",
        ),
        width="100%",
        height="100vh",
        background_color="#1a202c",
        color="#e2e8f0",
        padding="1rem"
    )

# Add a style to the app for a global font and a better look.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
    ),
)
app.add_page(index)
