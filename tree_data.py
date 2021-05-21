"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""

from __future__ import annotations
import os
from random import randint
import math

from typing import Tuple, List, Optional


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    data_size: the total size of all leaves of this tree.
    colour: The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    _root: the root value of this tree, or None if this tree is empty.
    _subtrees: the subtrees of this tree.
    _parent_tree: the parent tree of this tree; i.e., the tree that contains
        this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    data_size: int
    colour: (int, int, int)
    _root: Optional[object]
    _subtrees: List[AbstractTree]
    _parent_tree: Optional[AbstractTree]

    def __init__(self: AbstractTree, root: Optional[object],
                 subtrees: List[AbstractTree], data_size: int = 0) -> None:
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if self.is_empty():
            self.data_size = 0
            return

        if not subtrees:
            self.data_size = data_size

        else:
            ans = 0
            for child_tree in self._subtrees:
                ans += child_tree.data_size
                child_tree._parent_tree = self
            self.data_size = ans
        # 1. Initialize self.colour and self.data_size,
        # according to the docstring.
        # 2. Properly set all _parent_tree attributes in self._subtrees

    def is_empty(self: AbstractTree) -> bool:
        """Return True if this tree is empty."""
        return self._root is None

    def get_info(self: AbstractTree, rect: Tuple[int, int, int, int],
                 point: Tuple[int, int]) -> AbstractTree:
        """
        Given a rect with(x, y, width, height) and a point(x0, y0).
        Find the leaf where the point stands in the given rect.
        """
        width, height = rect[2], rect[3]
        x, y = rect[0], rect[1]

        if x <= point[0] <= x + width and y <= point[1] <= y + height \
                and not self._subtrees:
            return self

        child_ans = None
        if width > height:
            width_sum = 0
            for i in range(len(self._subtrees)):
                percentage = self._subtrees[i].data_size / self.data_size
                new_width = int(percentage * width)
                if i < (len(self._subtrees) - 1) and (
                        x + width_sum <= point[0] <= x + width_sum + new_width):
                    child_ans = self._subtrees[i].get_info(
                        (x + width_sum, y, new_width, height), point)
                if i == (len(self._subtrees) - 1) and (
                        x + width_sum <= point[0] <= x + width):
                    child_ans = self._subtrees[i]. \
                        get_info((rect[0] + width_sum, rect[1],
                                  width - width_sum, height), point)
                width_sum += new_width

        if width <= height:
            height_sum = 0
            for i in range(len(self._subtrees)):
                percentage = self._subtrees[i].data_size / self.data_size
                new_height = int(percentage * height)
                if i < len(self._subtrees) - 1 and (
                        y + height_sum <= point[-1] <= y + height_sum
                        + new_height):
                    child_ans = self._subtrees[i].\
                        get_info((x, y + height_sum, width, new_height), point)
                if i == len(self._subtrees) - 1 and\
                        (y + height_sum <= point[-1] <= y + height):
                    child_ans = self._subtrees[i]. \
                        get_info((x, y + height_sum, width,
                                  height - height_sum), point)
                height_sum += new_height

        return child_ans

    def parent_remove(self, item: AbstractTree) -> None:
        """
        Function used in event_loop for the situation when user click
        right mouse. This function will remove the item from the item's
         parent_tree's subtree if it is inside.
        """
        if self.is_leaf(item):
            self._subtrees.remove(item)
            return

        if self == item and not self._parent_tree:
            self._root = None
            return

        for child_tree in self._subtrees:
            child_tree.parent_remove(item)

    def change_size(self, size: int) -> int:
        """
        This function will be used in treemap_visualiser.
        This function will return the number after it multiplies 0.01
        """
        if self._root:
            return math.ceil(size * 0.01)
        return 0

    def is_leaf(self, selected: AbstractTree) -> bool:
        """
        return True if selected is a leaf, False otherwise
        """
        for child_tree in self._subtrees:
            if child_tree._root == selected._root and \
                    not child_tree._subtrees:
                return True
        return False

    def decrease_size(self, selected_leaf: AbstractTree, changes: int) -> None:
        """
        This function will decrease the data_size of the tree.
        The amount of the decreasing depends on changes.
        """
        if self.is_leaf(selected_leaf):
            self.data_size -= changes
            return
        for child_tree in self._subtrees:
            if child_tree._subtrees:
                child_tree.decrease_size(selected_leaf, changes)

    def increase_size(self, selected_leaf: AbstractTree, changes: int) -> None:
        """
        This function will increase the data_size of the tree.
        The amount of the increasing depends on changes.
        """
        if self.is_leaf(selected_leaf):
            self.data_size += changes
            return
        for child_tree in self._subtrees:
            if child_tree._subtrees:
                child_tree.increase_size(selected_leaf, changes)

    def size_decrease(self, item: AbstractTree) -> None:
        """
        This function will decrease the data_size of the tree, also change
        item's data_size to 0.
        The amount of the decreasing depends on the data_size of the item.
        """
        if self.is_leaf(item):
            self.data_size -= item.data_size
            item.data_size = 0
            return
        for child_tree in self._subtrees:
            child_tree.size_decrease(item)

    def generate_treemap(self: AbstractTree, rect: Tuple[int, int, int, int])\
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        if self.data_size == 0:
            return []

        if not self._subtrees and self.data_size > 0:
            return [(rect, self.colour)]

        width, height = rect[-2], rect[-1]
        ans = []
        if width > height:
            width_sum = 0
            for i in range(len(self._subtrees)):
                percentage = self._subtrees[i].data_size / self.data_size
                new_width = math.floor(percentage * width)
                if i < (len(self._subtrees) - 1):
                    child_ans = self._subtrees[i].generate_treemap(
                        (rect[0] + width_sum, rect[1], new_width, height))
                    ans.extend(child_ans)
                    width_sum += new_width

                elif i == len(self._subtrees) - 1:
                    final_width = width - width_sum
                    child_ans = self._subtrees[i].generate_treemap(
                        (rect[0] + width_sum, rect[1], final_width, height))
                    ans.extend(child_ans)

        if width <= height:
            height_sum = 0
            for i in range(len(self._subtrees)):
                percentage = self._subtrees[i].data_size / self.data_size
                new_height = math.floor(percentage * height)
                if i < len(self._subtrees) - 1:
                    child_ans = self._subtrees[i].generate_treemap(
                        (rect[0], rect[1] + height_sum, width, new_height))
                    ans.extend(child_ans)
                    height_sum += new_height

                if i == len(self._subtrees) - 1:
                    final_height = height - height_sum
                    child_ans = self._subtrees[i].generate_treemap(
                        (rect[0], rect[1] + height_sum, width, final_height))
                    ans.extend(child_ans)

        return ans

        # Read the handout carefully to help get started identifying base cases,
        # and the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # coordinates of a rectangle, as follows.
        # x, y, width, height = rect

    def __eq__(self, other: AbstractTree) -> bool:
        """
        return True if the root of two AbstractTrees equal to each other.
        """
        if isinstance(other, AbstractTree):
            return self._root == other._root
        return False

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        raise NotImplementedError

    def get_text(self, selected_leaf: AbstractTree, size: int) -> str:
        """
        Get the text(str) which will be used in event_loop to show the text.
        """
        ans_list = []
        ans_data = 0
        if not selected_leaf:
            return ''
        for child_tree in self._subtrees:
            if child_tree == selected_leaf and not child_tree._subtrees:
                ans_list.append(self._root)
                ans_list.append(child_tree._root)
                ans_data += size
                got = ''
                for item in ans_list:
                    got += self.get_separator() + str(item)
                return got[:] + '     ' + '(' + str(ans_data) + ')'

            if child_tree._subtrees:
                ans = child_tree.get_text(selected_leaf, size)
                if ans:
                    return ans
        return ''


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self: FileSystemTree, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.

        # root, internal nodes represent folders, the leaves represent regular
        #     files, data_size attribute for regular files as simply the size
        #     of the file, as reported by os.path.getsize.

        # Also remember to make good use of the superclass constructor!
        root = os.path.basename(path)
        subtrees = []

        if not os.path.isdir(path):
            data_size = os.path.getsize(path)
            AbstractTree.__init__(self, root, subtrees, data_size)

        elif os.path.isdir(path):
            subtrees_info = os.listdir(path)
            for info in subtrees_info:
                new_path = os.path.join(path, info)
                subtrees.append(FileSystemTree(new_path))
            AbstractTree.__init__(self, root, subtrees, 0)

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf."""
        return os.sep


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'extra-imports': ['os', 'random', 'math'],
            'generated-members': 'pygame.*'})
