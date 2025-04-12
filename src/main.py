from textnode import TextNode, TextType
from copystatic import refresh_public
from gencontent import generate_page, generate_pages_recursive

import os, shutil, sys

from inline_markdown import extract_markdown_links #temp for testing

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"
git_dir = "https://github.com/Dev-Jace/static_site2/"

def main():
    basepath = sys.argv

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
        
    print("Copying static to public...")
    refresh_public(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath,
    )

main()