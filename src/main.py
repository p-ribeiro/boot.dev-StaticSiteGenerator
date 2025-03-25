from src.block_markdown import markdown_to_html_node
from src.textnode import TextNode, TextType


def main():
    md =  """
# this is an h1

this is paragraph text

## this is an h2
"""
    x = markdown_to_html_node(md)
    html = x.to_html()
    print(html)
    
    
if __name__ == "__main__":
    main()