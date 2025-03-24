import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world",
            None,
            {"class": "greeting", "href": "https://localhost.com"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://localhost.com"'
        )
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "This is a div text",
            None,
            {"class": "greeting", "href": "https://localhost.com"}
        )
        
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "This is a div text"
        )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            {"class": "greeting", "href": "https://localhost.com"}
        )
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "This is a mad world",
            None,
            {"class": "primary"}
        )
        
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, This is a mad world, children: None, {'class': 'primary'})"
        )
    
    def test_leaf_node_without_props(self):
        node = LeafNode("p", "My paragraph")
        
        self.assertEqual(
            node.to_html(),
            "<p>My paragraph</p>"
        )
    
    def test_leaf_node_with_props(self):
        node = LeafNode("a", "My Website", {"href": "www.localhost.com"})
        
        self.assertEqual(
            node.to_html(),
            '<a href="www.localhost.com">My Website</a>'
        )
    
    def test_leaf_node_no_tag(self):
        node = LeafNode(None, "Hello Site")
        
        self.assertEqual(
            node.to_html(),
            'Hello Site'
        )
    
    def test_parent_node(self):
        node = ParentNode(
            "p",
            [LeafNode("a", "my website", {"href": "www.localhost.com"})],
            None
        )
        self.assertEqual(
            node.to_html(),
            '<p><a href="www.localhost.com">my website</a></p>'
        )
    
    def test_parent_node_with_parent_node(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b", 
                    [
                        LeafNode("a", "my website", {"href": "www.localhost.com"}),
                        LeafNode("i", "Italic Text")
                    ],
                    None
                )
            ],
            None
        )
        
        self.assertEqual(
            node.to_html(),
            '<p><b><a href="www.localhost.com">my website</a><i>Italic Text</i></b></p>'
        )