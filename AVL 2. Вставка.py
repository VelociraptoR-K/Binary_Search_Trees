from __future__ import annotations
import sys
from dataclasses import dataclass

sys.setrecursionlimit(200000)


@dataclass
class AvlNode:
    key: int
    left: AvlNode | None = None
    right: AvlNode | None = None
    height: int = 1


# Высота пустого дерева равна 0
def height(node: AvlNode | None) -> int:
    return 0 if node is None else node.height


def update(node: AvlNode) -> None:
    node.height = 1 + max(height(node.left), height(node.right))


# Применяем формулу: h(R) - h(L)
def balance_factor(node: AvlNode) -> int:
    return height(node.right) - height(node.left)


def rotate_right(y: AvlNode) -> AvlNode:
    x = y.left
    assert x is not None
    y.left = x.right
    x.right = y
    update(y)
    update(x)
    return x


def rotate_left(x: AvlNode) -> AvlNode:
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    update(x)
    update(y)
    return y


def avl_insert(root: AvlNode | None, key: int) -> AvlNode:
    if root is None:
        return AvlNode(key)
    if key == root.key:
        return root
    if key < root.key:
        root.left = avl_insert(root.left, key)
    else:
        root.right = avl_insert(root.right, key)

    update(root)
    bf = balance_factor(root)

    # Балансировка
    # Перевес Справа (bal == 2)
    if bf == 2:
        u = root.right
        assert u is not None
        if balance_factor(u) < 0:
            root.right = rotate_right(root.right)
        return rotate_left(root)

    # Перевес Слева (bal == -2)
    if bf == -2:
        u = root.left
        assert u is not None
        if balance_factor(u) > 0:
            root.left = rotate_left(root.left)
        return rotate_right(root)

    return root


def preorder_traversal(root: AvlNode | None, result: list[str]) -> None:
    if root is not None:
        result.append(str(root.key))
        preorder_traversal(root.left, result)
        preorder_traversal(root.right, result)


def main() -> None:
    first_line = sys.stdin.readline()
    if not first_line: return
    q = int(first_line.strip())

    root: AvlNode | None = None
    elements: set[int] = set()

    for _ in range(q):
        line = sys.stdin.readline().strip()
        if not line: continue
        parts = line.split()
        cmd = parts[0]

        if cmd == "add":
            x = int(parts[1])
            if x not in elements:
                root = avl_insert(root, x)
                elements.add(x)
        elif cmd == "exists":
            x = int(parts[1])
            print("YES" if x in elements else "NO")
        elif cmd == "root":
            print(root.key if root else "Empty")
        elif cmd == "height":
            print(height(root))
        elif cmd == "print":
            if root is None:
                print("Empty")
            else:
                res: list[str] = []
                preorder_traversal(root, res)
                print(" ".join(res))


if __name__ == "__main__":
    main()
