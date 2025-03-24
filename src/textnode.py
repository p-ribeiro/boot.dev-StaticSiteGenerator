from enum import Enum

from src.htmlnode import LeafNode

class TextType(Enum):
   TEXT = "text" 
   BOLD = "bold"
   ITALIC = "italic"
   CODE = "code"
   LINK = "link"
   IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str = url
       
    def __eq__(self, other: 'TextNode'):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
       return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
   
    def text_node_to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception("Not a valid TextType")
