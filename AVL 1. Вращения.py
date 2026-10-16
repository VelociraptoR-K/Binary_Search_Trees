from __future__ import annotations
import sys
from dataclasses import dataclass


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


def rotate_right(y: Node) -> Node:
    x = y.left
    assert x is not None
    y.left = x.right
    x.right = y
    return x


def rotate_left(x: Node) -> Node:
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    return y


# Рекурсивно ищет узел с ключом target и применяет к нему левый поворот
def apply_left_rotation(root: Node | None, target: int) -> Node | None:
    if root is None:
        return None
    if root.key == target:
        return rotate_left(root)
    if target < root.key:
        root.left = apply_left_rotation(root.left, target)
    else:
        root.right = apply_left_rotation(root.right, target)
    return root


# Рекурсивно ищет узел с ключом target и применяет к нему правый поворот
def apply_right_rotation(root: Node | None, target: int) -> Node | None:
    if root is None:
        return None
    if root.key == target:
        return rotate_right(root)
    if target < root.key:
        root.left = apply_right_rotation(root.left, target)
    else:
        root.right = apply_right_rotation(root.right, target)
    return root


def preorder_traversal(root: Node | None, result: list[str]) -> None:
    if root is not None:
        result.append(str(root.key))
        preorder_traversal(root.left, result)
        preorder_traversal(root.right, result)


def main() -> None:
    n_line = sys.stdin.readline()
    if not n_line: return
    n = int(n_line.strip())

    keys = list(map(int, sys.stdin.readline().split()))
    root: Node | None = None
    for k in keys:
        root = insert(root, k)

    m_line = sys.stdin.readline()
    if not m_line: return
    m = int(m_line.strip())

    for _ in range(m):
        line = sys.stdin.readline().strip()
        if not line: continue
        cmd, x_str = line.split()
        x = int(x_str)

        if cmd == "left":
            root = apply_left_rotation(root, x)
        elif cmd == "right":
            root = apply_right_rotation(root, x)

        res: list[str] = []
        preorder_traversal(root, res)
        print(" ".join(res))


if __name__ == "__main__":
    main()
