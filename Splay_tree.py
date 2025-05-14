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


class SplayTree:
    def __init__(self):
        self.root = None
        self.cost = 0

    def search(self, key):
        if self.root is None:
            return None
        current = self.root
        while key != current.val:
            parent = current
            if key < current.val:
                current = current.left
            elif key > current.val:
                current = current.right
            self.cost += 1
            if current is None:
                self.splay(parent)
                return None
        self.splay(current)
        return current

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
                    self.splay(node)
                    return
            elif key < current.val:
                temp = current
                current = current.left
                if current is None:
                    temp.left = node
                    node.parent = temp
                    self.splay(node)
                    return
            else:  # key == current.val
                self.splay(current)
                return

    def delete(self, key):
        if self.root is None:
            return None
        current = self.root
        while key != current.val:
            parent = current
            if key < current.val:
                current = current.left
            elif key > current.val:
                current = current.right
            if current is None:
                self.splay(parent)
        if current.left is None and current.right is None:  # The key is a leaf
            if current == self.root:
                self.root = None
                return
            if current == current.parent.left:
                current.parent.left = None
            elif current == current.parent.right:
                current.parent.right = None
            self.splay(current.parent)

        elif current.left is None and current.right is not None:
            if current == self.root:
                self.root = self.root.right
                self.root.parent = None
                return
            if current == current.parent.left:
                current.parent.left = current.right
                current.right.parent = current.parent
            elif current == current.parent.right:
                current.parent.right = current.right
                current.right.parent = current.parent
            self.splay(current.parent)

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
            self.splay(current.parent)

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
                self.splay(temp.parent)
                return
            temp.val = current.val
            current.right.parent = current.parent
            if current == current.parent.right:
                current.parent.right = current.right
            elif current == current.parent.left:
                current.parent.left = current.right
            self.splay(temp.parent)

    def show(self):
        if self.root is not None:
            self.root.display()

    def splay(self, p):
        if p is None:
            return
        while p != self.root:
            parent = p.parent
            grand = parent.parent
            # zig case
            if grand is None:
                self.rotate(p)
                self.cost += 0.05  # One rotation is done
            # zig-zig case
            elif (p == parent.left) == (parent == grand.left):
                self.rotate(parent)
                self.rotate(p)
                self.cost += 0.1  # Two rotations are done
            # zig-zag case
            else:
                self.rotate(p)
                self.rotate(p)
                self.cost += 0.1  # Two rotations are done

    def rotate(self, p):
        if p is None:
            return
        parent = p.parent
        grand = parent.parent
        if parent is None:  # The root is p
            return
        if grand is None:  # The root is parent
            if p == parent.left:
                parent.left, p.right = p.right, parent
                if parent.left is not None:
                    parent.left.parent = parent
                p.parent = None
                self.root = p
                parent.parent = p
            elif p == parent.right:
                parent.right, p.left = p.left, parent
                if parent.right is not None:
                    parent.right.parent = parent
                p.parent = None
                self.root = p
                parent.parent = p
            return

        # First case:
        if p == parent.left:
            parent.left, p.right = p.right, parent
            if parent.left is not None:
                parent.left.parent = parent
            parent.parent = p
            if parent == grand.left:
                grand.left, p.parent = p, grand
            elif parent == grand.right:
                grand.right, p.parent = p, grand
        # Second case
        elif p == parent.right:
            parent.right, p.left = p.left, parent
            if parent.right is not None:
                parent.right.parent = parent
            parent.parent = p
            if parent == grand.left:
                grand.left, p.parent = p, grand
            elif parent == grand.right:
                grand.right, p.parent = p, grand


if __name__ == "__main__":
    tree = SplayTree()
    tree.insert(9)
    # tree.show()
    # tree.insert(24)
    tree.insert(27)
    # tree.show()
    tree.insert(17)
    # tree.show()
    tree.insert(25)
    # tree.show()
    tree.insert(11)
    # tree.show()
    tree.insert(10)
    # tree.show()
    tree.insert(20)
    # tree.show()
    tree.insert(23)
    # tree.show()
    tree.insert(16)
    tree.show()
    tree.delete(20)
    tree.show()
    tree.cost = 0
    tree.search(27)
    tree.show()
    tree.search(9)
    print(tree.cost)
