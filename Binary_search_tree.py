from math import log2


class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.parent = None
        self.val = val

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height,
            and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class BST:
    def __init__(self):
        self.root = None
        self.cost = 0

    def search(self, key):
        if self.root is None:
            return None
        current = self.root
        while key != current.val:
            if key < current.val:
                current = current.left
            elif key > current.val:
                current = current.right
            self.cost += 1
            if current is None:
                return None
        return current

    # def height(self):
    #     temp = self.root
    #
    #     def height_(node):
    #         if node is None:
    #             return 0
    #         return max(height_(node.left), height_(node.right)) + 1
    #     return height_(temp)
    def depth(self, key):
        current = self.root
        depth = 0
        if current is None:
            return depth
        while key != current.val:
            if key < current.val:
                current = current.left
            elif key > current.val:
                current = current.right
            depth += 1
            if current is None:
                return depth
        return depth

    def insert(self, key):
        node = Node(key)
        if self.root is None:
            self.root = node
            return

        current = self.root
        while True:
            if key > current.val:
                temp = current
                current = current.right
                if current is None:
                    temp.right = node
                    node.parent = temp
                    return
            elif key < current.val:
                temp = current
                current = current.left
                if current is None:
                    temp.left = node
                    node.parent = temp
                    return
            else:  # key == current.val
                return

    def delete(self, key):
        current = self.search(key)
        if current is None:
            print(key, "Does not exist in the Tree")
            return
        if current.left is None and current.right is None:  # The key is a leaf
            if current == self.root:
                self.root = None
                return
            if current == current.parent.left:
                current.parent.left = None
            elif current == current.parent.right:
                current.parent.right = None

        elif current.left is None and current.right is not None:
            if current == self.root:
                self.root = self.root.right
                self.root.parent = None
                return
            # temp = current
            # current = current.right
            # current.parent = temp.parent
            if current == current.parent.left:
                current.parent.left = current.right
                current.right.parent = current.parent
            elif current == current.parent.right:
                current.parent.right = current.right
                current.right.parent = current.parent

        elif current.right is None and current.left is not None:
            if current == self.root:
                self.root = self.root.left
                self.root.parent = None
                return
            if current == current.parent.left:
                current.parent.left = current.left
                current.left.parent = current.parent
            elif current == current.parent.right:
                current.parent.right = current.left
                current.left.parent = current.parent

        elif current.left is not None and current.right is not None:
            #  We need to replace the node with its successor
            temp = current
            current = current.right
            while current.left is not None:
                current = current.left
            if current.right is None:
                temp.val = current.val
                if current == current.parent.left:
                    current.parent.left = None
                elif current == current.parent.right:
                    current.parent.right = None
                return
            temp.val = current.val
            current.right.parent = current.parent
            if current == current.parent.right:
                current.parent.right = current.right
            elif current == current.parent.left:
                current.parent.left = current.right

    def show(self):
        if self.root is not None:
            self.root.display()


if __name__ == "__main__":
    tree = BST()
    tree.insert(10)
    tree.insert(7)
    tree.insert(14)
    tree.insert(17)
    tree.insert(15)
    tree.insert(16)
    tree.insert(3)
    tree.insert(25)
    tree.insert(1)
    tree.show()
    print(tree.depth(1))
    print(tree.depth(16))
    tree.search(1)
    tree.search(16)
    tree.show()
    print(tree.cost)
#     r = tree.root
#     tree.insert(5)
#     tree.insert(3)
#     tree.insert(7)
#     tree.insert(6)
#     tree.insert(4)
#     tree.insert(9)
#     tree.insert(8)
#     # print(r.right.right.left.val) #??????????
#     tree.insert(5)
#     # print(tree.search(1))
#     # print(tree.search(8))
#     # tree.delete(11)
#     tree.show()
#     tree.delete(4)
#     # tree.show()
#     tree.delete(3)
#     # tree.show()
#     tree.delete(9)
#     # tree.show()
#     tree.delete(7)
#     tree.show()
#     # Check replacing two nodes(just changing val or changing the whole node)
