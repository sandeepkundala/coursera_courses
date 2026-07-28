import gradio as gr
from huggingface_hub import HfFolder

def add_numbers(Num1, Num2):
    return Num1 + Num2

def combine_lines(Line1, Line2):
    return Line1 + " " + Line2

# Define the interface
demo = gr.Interface(
    fn=add_numbers, 
    inputs=[gr.Number(), gr.Number()], # Create two numerical input fields where users can enter numbers
    outputs=gr.Number() # Create numerical output fields
)

demo2 = gr.Interface(
    fn=combine_lines, 
    inputs=[gr.Text(), gr.Text()], # Create two text input fields where users can enter string text
    outputs=gr.Text() # Create String/Text output fields
)

# Launch the interface
# demo.launch(server_name="127.0.0.1", server_port= 7860)
demo2.launch(server_name="127.0.0.1", server_port= 7860)
