

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #string rep the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # string contained within tag
        self.children = children #list of HTMLNode(s) contained within
        self.props = props #dictionary of key-value pairs representing the attributes of the HTML tag.

    def __eq__(self, o_HTMLNode):
        if not isinstance(o_HTMLNode, HTMLNode):
            return False
        if self.tag == o_HTMLNode.text:
            if self.value == o_HTMLNode.value:
                if self.children == o_HTMLNode.children:
                    if self.props == o_HTMLNode.props:
                        return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props != None:
            props_str = ""
            for prop in self.props:
                props_str += f' {prop}="{self.props[prop]}"'
            return props_str
        return ""
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        rtn_str = ""
        if type(self.value) != str:
            raise ValueError
        if self.tag != None:
            if self.props != None:
                rtn_str += f"<{self.tag}{self.props_to_html()}>"
            else:
                rtn_str += f"<{self.tag}>"
        rtn_str += self.value
        if self.tag != None:
            rtn_str += f"</{self.tag}>"
        return rtn_str

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children is not None and not isinstance(children, (list, tuple)):
            children = [children]
        super().__init__(tag=tag, children=children, props=props, value=None)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        rtn_str = ""
        if type(self.tag) != str:
            raise Exception("Tag invalid")
        if self.children == None:
            raise Exception("children invalid")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"