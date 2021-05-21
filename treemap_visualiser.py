"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree, AbstractTree
from population import PopulationTree


# Screen dimensions and coordinates

ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree: AbstractTree) -> None:
    """Display an interactive graphical display of the given tree's treemap."""
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen: pygame.Surface, tree: AbstractTree,
                   text: str) -> None:
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    info = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))

    for data in info:
        pygame.draw.rect(screen, data[1], data[0])
        _render_text(screen, text)

    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen: pygame.Surface, text: str) -> None:
    """Render text at the bottom of the display."""
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen: pygame.Surface, tree: AbstractTree) -> None:
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.
    """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None
    size = 0

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            button = event.button
            rect = (ORIGIN[0], ORIGIN[1], WIDTH, TREEMAP_HEIGHT)
            get_point = tree.get_info(rect, event.pos)
            if button == 1 and selected_leaf != get_point:
                selected_leaf = get_point
                size = selected_leaf.data_size
            elif button == 1 and selected_leaf == get_point:
                selected_leaf = None
                size = 0

            if button == 3:
                tree.parent_remove(get_point)
                tree.size_decrease(get_point)
            elif button == 3 and get_point == selected_leaf:
                selected_leaf = None
                render_display(screen, tree, '')

            text = tree.get_text(selected_leaf, size)
            render_display(screen, tree, text)

        if event.type == pygame.KEYDOWN and selected_leaf:
            changes = tree.change_size(selected_leaf.data_size)
            if pygame.K_DOWN == event.key and selected_leaf.data_size - \
                    changes >= 1:
                selected_leaf.data_size -= changes
                tree.decrease_size(selected_leaf, changes)
            if pygame.K_DOWN == event.key and selected_leaf.data_size - \
                    changes < 1:
                selected_leaf.data_size = 1

            if pygame.K_UP == event.key:
                selected_leaf.data_size += changes
                tree.increase_size(selected_leaf, changes)
            text = tree.get_text(selected_leaf, selected_leaf.data_size)
            render_display(screen, tree, text)
        # Remember to call render_display if any data_sizes change,
        # as the treemap will change in this case.


def run_treemap_file_system(path: str) -> None:
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population() -> None:
    """Run a treemap visualisation for World Bank population data."""
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'extra-imports': ['pygame', 'tree_data', 'population'],
            'generated-members': 'pygame.*'})
