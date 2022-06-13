import pandas_profiling as pp
from huggingface_hub.hf_api import create_repo, upload_file
from huggingface_hub.repository import Repository
import gradio as gr
import pandas as pd
import subprocess
import os
import tempfile

description = "This Space will profile a dataset file that you drag and drop and push the profile report to your Hugging Face account. 🌟 \n The value in dataset name field you'll enter will be used in the namespace of the Space that will be pushed to your profile, so you can use it to version the reports too! 🙌🏻 Feel free to open a discussion in case you have any feature requests. Dataset name you'll enter will be used for repository name so make sure it doesn't exist and it doesn't contain spaces."
title = "Dataset Profiler 🪄✨"
token = gr.Textbox(label = "Your Hugging Face Token")
username = gr.Textbox(label = "Your Hugging Face User Name")
dataset_name = gr.Textbox(label = "Dataset Name")
dataset = gr.File(label = "Dataset")
output_text = gr.Textbox(label = "Status")


def profile_dataset(dataset, username, token, dataset_name):

    df = pd.read_csv(dataset.name)
    profile = pp.ProfileReport(df, title=f"{dataset_name} Report")
    
    repo_url = create_repo(f"{username}/{dataset_name}", repo_type = "space", token = token, space_sdk = "static", private=False)
    
    profile.to_file("./index.html")
    upload_file(path_or_fileobj ="./index.html", path_in_repo = "index.html", repo_id =f"{username}/{dataset_name}", repo_type = "space", token=token)
    readme = f"---\ntitle: {dataset_name}\nemoji: ✨\ncolorFrom: green\ncolorTo: red\nsdk: static\npinned: false\ntags:\n- dataset-report\n---"    
    with open("README.md", "w+") as f:
        f.write(readme)
    upload_file(path_or_fileobj ="./README.md", path_in_repo = "README.md", repo_id =f"{username}/{dataset_name}", repo_type = "space", token=token)

    return f"Your dataset report will be ready at {repo_url}"

gr.Interface(profile_dataset,  title = title, description = description, inputs = [dataset, username, token, dataset_name], outputs=[output_text], enable_queue = True).launch(debug=True)
