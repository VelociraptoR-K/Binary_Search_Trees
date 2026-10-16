from __future__ import annotations
import sys
from dataclasses import dataclass

# Лимит рекурсии на случай глубоких тестов
sys.setrecursionlimit(200000)


@dataclass
class Node:
    key: int
    left: Node | None = None
    right: Node | None = None


def insert(root: Node | None, key: int) -> Node:
    if root is None:
        return Node(key)
    if key == root.key:
        return root
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root


def find_min(root: Node | None) -> Node | None:
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left
    return current


def delete_node(root: Node | None, key: int) -> Node | None:
    if root is None:
        return None
    if key < root.key:
        root.left = delete_node(root.left, key)
        return root
    if key > root.key:
        root.right = delete_node(root.right, key)
        return root

    if root.left is None and root.right is None:
        return None
    if root.left is None:
        return root.right
    if root.right is None:
        return root.left

    succ = find_min(root.right)
    assert succ is not None
    root.key = succ.key
    root.right = delete_node(root.right, succ.key)
    return root


# Подсчет высоты
def get_height(root: Node | None) -> int:
    if root is None:
        return 0
    return 1 + max(get_height(root.left), get_height(root.right))


# Прямой обход: Корень -> Лево -> Право
def preorder_traversal(root: Node | None, result: list[str]) -> None:
    if root is not None:
        result.append(str(root.key))
        preorder_traversal(root.left, result)
        preorder_traversal(root.right, result)


def main() -> None:
    first_line = sys.stdin.readline()
    if not first_line:
        return
    q = int(first_line.strip())

    root: Node | None = None
    elements: set[int] = set()

    for _ in range(q):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0]

        if cmd == "add":
            x = int(parts[1])
            if x not in elements:
                root = insert(root, x)
                elements.add(x)
        elif cmd == "del":
            x = int(parts[1])
            if x in elements:
                root = delete_node(root, x)
                elements.remove(x)
        elif cmd == "exists":
            x = int(parts[1])
            print("YES" if x in elements else "NO")
        elif cmd == "height":
            print(get_height(root))
        elif cmd == "print":
            if root is None:
                print("Empty")
            else:
                res: list[str] = []
                preorder_traversal(root, res)
                print(" ".join(res))


if __name__ == "__main__":
    main()
