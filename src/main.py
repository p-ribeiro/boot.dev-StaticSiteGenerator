from textnode import TextNode, TextType


def main():
    textNode = TextNode("This is a test text", TextType.BOLD, "localhost")
    print(textNode)
    
    
if __name__ == "__main__":
    main()