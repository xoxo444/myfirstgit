import gradio as gr
import os
import shutil

def query_bot(file, query, num_results):
    response = f"Processing your query: '{query}'\nResults requested: {num_results}"

    if file is not None and len(file) > 0:
        uploaded_file = file[0]  
        filename = os.path.basename(uploaded_file.name)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, filename)
        try:
            shutil.copy(uploaded_file.name, save_path)
            response += f"\n File saved as: {filename} in {script_dir}"
        except Exception as e:
            response += f"\n Error saving file: {str(e)}"

    return response

     
custom_css = """
body {
    margin: 0;
    padding: 0;
    background-color: #0f0f0f !important;
    font-family: 'Poppins', sans-serif;
    display: flex;
    justify-content: center;
}

.gradio-container {
    max-width: 900px;
    width: 95%;
    margin: 50px auto;
    padding: 20px;
    box-sizing: border-box;
}

#title {
    margin-bottom: 0px !important;  
    margin-top: 0px !important;      
    text-align: center;
    font-family: 'Roboto Slab', cursive !important;
    font-size: 32px;
    color: #ff69b4;
    font-weight: bold;
}

#title h2 {
    font-family: 'Playfair Display', serif !important;
    color: beige !important;
    font-size: 70px !important;
    text-align: center !important;
    margin-bottom: 20px !important;
}


#submit_btn {
    background-color: beige !important;
    color: black !important;
    width: 40px !important;
    height: 40px !important;
    text-align: center !important;
}

.gr-button {
    background-color: #ff69b4 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 6px 14px !important;   
    font-weight: bold !important;
    font-size: 14px !important;     
}

#file-upload {
    max-height: 200px;
    overflow-y: auto;
    padding-right: 8px;
}

#response-box {
    background-color: #1f1f1f;
    color: #ffffff;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 16px;
    margin-top: 12px;
    white-space: pre-wrap;
}

textarea, input[type=text] {
    color: black !important;
    border: 1px solid #ccc !important;
    border-radius: 8px !important;
    padding: 10px !important;
    background-color: white !important;
}

input[type=range]::-webkit-slider-thumb {
    background: black !important;
}

input[type=range]::-webkit-slider-runnable-track {
    background: #ffe6f0 !important;
}

input[type=range]::-moz-range-thumb {
    background: #ff69b4 !important;
}
"""

with gr.Blocks(css=custom_css, title="Resume Chatbot") as demo:
    gr.Markdown("##  Resume Chatbot", elem_id="title")

    with gr.Row():
        file_input = gr.File(label="📎 Attach File(s)", file_types=[".txt", ".pdf", ".docx"], file_count="multiple", elem_id="file-upload")

    query_input = gr.Textbox(label="📝 Enter your Query", placeholder="Type your query here...", lines=2, max_lines=4)
    results_slider = gr.Slider(1, 20, value=10, step=1, label=" How many results you want")

    with gr.Row():
        submit_button = gr.Button("Submit", elem_id="submit_btn")

    output = gr.Textbox(label=" 💬 Response", elem_id="response-box", lines=1, max_lines=10, interactive=False)

    submit_button.click(
        fn=query_bot,
        inputs=[file_input, query_input, results_slider],
        outputs=output
    )
    
     #HTML 
    gr.HTML("""
    <div style="text-align: center; margin-top: 10px;">
        <button onclick="copyResponse()" 
            style="padding: 8px 20px; background-color: beige; color: black; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">
             Copy Response
        </button>
    </div>
    <script>
        function copyResponse() {
            const textarea = document.querySelector('[id="response-box"] textarea');
            if (textarea) {
                textarea.select();
                document.execCommand('copy');
                alert('Response copied to clipboard!');
            }
        }
    </script>
    """)

demo.launch()
