class Node:
    def __init__(self, image):
        self.image = image
        self.prev = None
        self.next = None

class Tracker:
    
    def __init__(self):
        self.head = None
        self.tail = self.head
        self.current = self.tail

    def append(self, image):
        
        if not self.head:
            self.head = Node(image)
            self.tail = self.head
            self.current = self.tail
        else:
            new_node = Node(image)

            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.current = self.tail
        


