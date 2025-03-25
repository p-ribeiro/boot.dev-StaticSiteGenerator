from curses.ascii import HT
from enum import Enum
from pydoc import text
from typing import List
import re

from src.inline_markdown import text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.htmlnode import HTMLNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'

def block_to_block_type(block: str) -> BlockType:
    
    lines = block.split('\n')
    
    re_heading =  re.compile(r'^\#{1,6} ')
    re_code = re.compile(r'^\`{3}[^\`](.|\n)*[^\`]\`{3}$')
    re_quote = re.compile(r'^\>')
    re_unordered_list = re.compile(r'^- ')
    re_ordered_list = re.compile(r'^(\d+)\. ')
    
    if re_heading.match(block):
        return BlockType.HEADING
    
    if len(lines) > 1 and re_code.match(block):
        return BlockType.CODE

    if re_quote.match(block):
        for line in lines:
            if not re_quote.match(line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if re_unordered_list.match(block):
        for line in lines:
            if not re_unordered_list.match(line):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if re_ordered_list.match(block):
        i = 1
        for line in lines:
            match = re_ordered_list.match(line)
            if not match or i != int(match.group(1)):
                return BlockType.PARAGRAPH
            i+=1
        return BlockType.OLIST
        
    
    return BlockType.PARAGRAPH
    
 

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    block_strings = []
    
    for block in blocks:
        if block == "":
            continue
       
        block = block.strip()
        block_strings.append(block.strip())
    
    return block_strings


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    
    match(block_type):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text: str) -> List[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split('\n')
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block: str) -> HTMLNode:
    lvl = 0
    for c in block:
        if c == "#":
            lvl += 1
        else:
            break
    if lvl + 1 >= len(block):
        raise ValueError(f"invalid heading level: {lvl}")
    
    text = block[lvl+1:]
    children = text_to_children(text)
    return ParentNode(f"h{lvl}", children)

def code_to_html_node(block: str) -> HTMLNode:
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre",[code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)