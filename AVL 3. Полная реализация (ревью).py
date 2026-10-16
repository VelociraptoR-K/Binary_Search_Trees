from __future__ import annotations
import sys
from dataclasses import dataclass

sys.setrecursionlimit(250000)

@dataclass
class AvlNode:
    key: int
    left: AvlNode | None = None
    right: AvlNode | None = None
    height: int = 1  # По условию задачи у нового листа высота равна 1


class AVLTree:
    def __init__(self) -> None:
        self.root: AvlNode | None = None

    def get_height(self, node: AvlNode | None) -> int:
        """Возвращает высоту узла (0 для пустого дерева)."""
        return 0 if node is None else node.height

    def _update_height(self, node: AvlNode) -> None:
        """Пересчитывает высоту узла на основе его детей."""
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def _balance_factor(self, node: AvlNode) -> int:
        """Вычисляет баланс узла по формуле: h(R) - h(L)."""
        return self.get_height(node.right) - self.get_height(node.left)

    def _rotate_right(self, y: AvlNode) -> AvlNode:
        """Малый правый поворот вокруг узла y."""
        x = y.left
        assert x is not None
        y.left = x.right
        x.right = y
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AvlNode) -> AvlNode:
        """Малый левый поворот вокруг узла x"""
        y = x.right
        assert y is not None
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        return y

    def _balance(self, node: AvlNode) -> AvlNode:
        """Проверяет баланс узла и выполняет необходимые повороты."""
        self._update_height(node)
        bf = self._balance_factor(node)

        # Перевес в правом поддереве
        if bf == 2:
            u = node.right
            assert u is not None
            if self._balance_factor(u) < 0:
                node.right = self._rotate_right(node.right)  # Большой левый поворот
            return self._rotate_left(node)

        # Перевес в левом поддереве
        if bf == -2:
            u = node.left
            assert u is not None
            if self._balance_factor(u) > 0:
                node.left = self._rotate_left(node.left)    # Большой правый поворот
            return self._rotate_right(node)

        return node

    def add(self, key: int) -> None:
        """Публичный метод вставки ключа"""
        self.root = self._insert(self.root, key)

    def _insert(self, node: AvlNode | None, key: int) -> AvlNode:
        if node is None:
            return AvlNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return self._balance(node)

    def delete(self, key: int) -> None:
        """Публичный метод удаления ключа"""
        self.root = self._delete(self.root, key)

    def _delete(self, node: AvlNode | None, key: int) -> AvlNode | None:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Узлы с 0 или 1 ребенком
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Узел с 2 детьми: ищем минимальный элемент в правом поддереве
            succ = node.right
            while succ.left is not None:
                succ = succ.left
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)

        return self._balance(node)

    def find_next(self, key: int) -> int | None:
        """Поиск минимального ключа >= X"""
        curr = self.root
        ans: int | None = None
        while curr is not None:
            if curr.key >= key:
                ans = curr.key
                curr = curr.left
            else:
                curr = curr.right
        return ans

    def find_prev(self, key: int) -> int | None:
        """Поиск максимального ключа <= X"""
        curr = self.root
        ans: int | None = None
        while curr is not None:
            if curr.key <= key:
                ans = curr.key
                curr = curr.right
            else:
                curr = curr.left
        return ans

    def get_preorder_list(self) -> list[str]:
        """Собирает ключи дерева для прямого обхода."""
        res: list[str] = []
        def _dfs(node: AvlNode | None) -> None:
            if node is not None:
                res.append(str(node.key))
                _dfs(node.left)
                _dfs(node.right)
        _dfs(self.root)
        return res


def main() -> None:
    # Читаем все команды сразу для максимального быстродействия ввода-вывода
    input_lines = sys.stdin.read().splitlines()
    if not input_lines:
        return

    tree = AVLTree()
    elements: set[int] = set()

    for line in input_lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0]

        if cmd == "add":
            x = int(parts[1])
            if x not in elements:
                tree.add(x)
                elements.add(x)
        elif cmd == "del":
            x = int(parts[1])
            if x in elements:
                tree.delete(x)
                elements.remove(x)
        elif cmd == "exists":
            x = int(parts[1])
            print("YES" if x in elements else "NO")
        elif cmd == "next":
            ans = tree.find_next(int(parts[1]))
            print(ans if ans is not None else "None")
        elif cmd == "prev":
            ans = tree.find_prev(int(parts[1]))
            print(ans if ans is not None else "None")
        elif cmd == "root":
            print(tree.root.key if tree.root else "Empty")
        elif cmd == "height":
            print(tree.get_height(tree.root))
        elif cmd == "print":
            if tree.root is None:
                print("Empty")
            else:
                print(" ".join(tree.get_preorder_list()))


if __name__ == "__main__":
    main()
