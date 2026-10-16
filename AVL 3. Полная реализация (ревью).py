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


def height(node: AvlNode | None) -> int:
    return 0 if node is None else node.height


def update(node: AvlNode) -> None:
    node.height = 1 + max(height(node.left), height(node.right))


def rotate(y: AvlNode, left: bool) -> AvlNode:
    x = y.right if left else y.left
    assert x is not None
    if left:
        y.right, x.left = x.left, y
    else:
        y.left, x.right = x.right, y
    update(y);
    update(x)
    return x


# Единая сжатая функция балансировки для вставки и удаления
def balance(node: AvlNode) -> AvlNode:
    update(node)
    bf = height(node.right) - height(node.left)
    if bf == 2:
        if height(node.right.right) - height(node.right.left) < 0:
            node.right = rotate(node.right, left=False)
        return rotate(node, left=True)
    if bf == -2:
        if height(node.left.right) - height(node.left.left) > 0:
            node.left = rotate(node.left, left=True)
        return rotate(node, left=False)
    return node


# Рекурсивная вставка и удаление с балансировкой (снизу-вверх)
def avl_insert(root: AvlNode | None, key: int) -> AvlNode:
    if root is None: return AvlNode(key)
    if key < root.key:
        root.left = avl_insert(root.left, key)
    elif key > root.key:
        root.right = avl_insert(root.right, key)
    return balance(root)


def avl_delete(root: AvlNode | None, key: int) -> AvlNode | None:
    if root is None: return None
    if key < root.key:
        root.left = avl_delete(root.left, key)
    elif key > root.key:
        root.right = avl_delete(root.right, key)
    else:
        if not root.left: return root.right
        if not root.right: return root.left
        # Поиск минимума в правом поддереве для замены (successor)
        succ = root.right
        while succ.left: succ = succ.left
        root.key = succ.key
        root.right = avl_delete(root.right, succ.key)
    return balance(root)


# Поиск соседей
def find_neighbor(root: AvlNode | None, key: int, is_next: bool) -> int | None:
    curr, ans = root, None
    while curr:
        cond = (curr.key >= key) if is_next else (curr.key <= key)
        if cond:
            ans = curr.key
            curr = curr.left if is_next else curr.right
        else:
            curr = curr.right if is_next else curr.left
    return ans


def preorder(root: AvlNode | None, res: list[str]) -> None:
    if root:
        res.append(str(root.key))
        preorder(root.left, res)
        preorder(root.right, res)


def main() -> None:
    lines = sys.stdin.read().splitlines()
    if not lines: return
    root, elements = None, set()

    for line in lines[1:]:
        if not line.strip(): continue
        parts = line.split()
        cmd = parts[0]

        if cmd == "add":
            x = int(parts[1])
            if x not in elements: root = avl_insert(root, x); elements.add(x)
        elif cmd == "del":
            x = int(parts[1])
            if x in elements: root = avl_delete(root, x); elements.remove(x)
        elif cmd == "exists":
            print("YES" if int(parts[1]) in elements else "NO")
        elif cmd == "next" or cmd == "prev":
            ans = find_neighbor(root, int(parts[1]), is_next=(cmd == "next"))
            print(ans if ans is not None else "None")
        elif cmd == "root":
            print(root.key if root else "Empty")
        elif cmd == "height":
            print(height(root))
        elif cmd == "print":
            if not root:
                print("Empty")
            else:
                res = []
                preorder(root, res)
                print(" ".join(res))


if __name__ == "__main__":
    main()
