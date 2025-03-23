from multiprocessing import Value
from typing import List, Optional

class HTMLNode:
    def __init__(self, 
                 tag: Optional[str] = None, 
                 value: Optional[str] = None, 
                 children: Optional[List['HTMLNode']] = None,
                 props: Optional[dict[str,str]] = None):
        
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[List['HTMLNode']] = children
        self.props: Optional[dict[str, str]] = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for k,v in self.props.items():
            props_html += f" {k}=\"{v}\""
        return props_html

class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[dict[str,str]] = None):
        super().__init__(tag, value, None, props)
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self):
        if self.value is None:
            raise ValueError('All leaf nodes must have a value')
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
                
        
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List['HTMLNode'], props: Optional[dict[str, str]]):
        super().__init__(tag, None, children, props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode needs to have a tag.")
        
        if self.children is None:
            raise ValueError("ParentNode needs to have children")

        children_to_html = ""
        for c in self.children:
            children_to_html += c.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_to_html}</{self.tag}>"