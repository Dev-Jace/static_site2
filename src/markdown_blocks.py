from enum import Enum
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes




def markdown_to_blocks(markdown):
    #input is a raw markdown file
    txt_blocks = []
    holder = markdown
    while len(holder) > 0:
        if len(holder.split("\n\n",1)[0]) > 0:
            txt_blocks.append(holder.split("\n\n",1)[0].strip())
        if len(holder.split("\n\n",1)) > 1:
            holder = holder.split("\n\n",1)[1]
        else:
            holder = ""

    return txt_blocks

#'''
#taken from lesson solutions and modified \/
class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    olist = "ordered list"
    ulist = "unordered list"

def block_to_block_type(block): # need to fix unordered list
    #paragraph
    #heading(s)
    #code
    #quote
    #unordered_list
    #ordered_list
    block_type = None
    if "# " in block:
        block_type = f"heading"
        return block_type
    if "```" in block:
        if block[0:3] == "```" and block[-3:] == "```":
            block_type = "code"
            return block_type
    if block[0] == ">":
        block_type = "quote"
        return block_type

    if block[0] == "*" or block[0] == "-":
        return "unordered list"
        if (block.count("*") == (block.count("\n")+1)) or (block.count("-") == (block.count("\n")+1)):
            block_type = "unordered list"
    if block[0:2] == "1.":
        lines = block.split("\n")
        i = 1
        for line in lines:
            if line[0:2] != f"{i}." :
                return "unordered list"
            i += 1
        block_type = "ordered list"
        return block_type
    
    block_type = "paragraph"

    return block_type

################

def markdown_to_html_nodes(markdown):
    
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_HTML_node(block))

    return children

def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_HTML_node(block))

    return ParentNode(tag= "div", children=children)

def block_to_HTML_node(block):
    block_type = block_to_block_type(block)
    if block_type[:7] == "heading":
        return heading_block_to_HTML_node(block)
    if block_type == "paragraph":#paragraph
        return paragraph_block_to_HTML_node(block) 
    if block_type == "code":#code
        return code_block_to_HTML_node(block)
    if block_type == "quote":#quote
        return quote_block_to_HTML_node(block)
    if block_type == "unordered list":#unordered_list
        return unordered_list_block_to_HTML_node(block)
    if block_type == "ordered list":#ordered_list
        return ordered_list_block_to_HTML_node(block)
    return "invalid block type"
        
'''     
def heading_block_to_HTML_node(block): #mostly working function
    heading_num = f"h{block.count("#")}"
    heading = block[block.count("#")+1:] #node -heading mark
    return LeafNode(tag=heading_num,value=heading)
'''
def heading_block_to_HTML_node(block): # Boots rewrite to catch italics/bolds
    heading_level = block.count("#")
    heading_text = block[heading_level+1:]  # Remove the #s and the space after
    
    # Process inline formatting in the heading text
    text_nodes = text_to_textnodes(heading_text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    
    # Create a parent node with the processed text
    return ParentNode(tag=f"h{heading_level}", children=html_nodes)

def paragraph_block_to_HTML_node(block):
    child = []
    lines = block.split("\n")
    nodes = text_to_textnodes(" ".join(lines))
    for node in nodes:
        child.append(text_node_to_html_node(node))
    return ParentNode(tag="p", children=child)

def code_block_to_HTML_node(block):
    code_text = LeafNode(tag="code", value= block[4:-4])
    return ParentNode(tag="pre",children=code_text)

def quote_block_to_HTML_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

    #return LeafNode(tag= "blockquote", value=block[1:])


def unordered_list_block_to_HTML_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ordered_list_block_to_HTML_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

    
#'''