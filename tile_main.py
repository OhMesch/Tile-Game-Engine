import tile_level_editor
import tile_renderer
import tile_terrain


def main():
    block_size = 15
    window_width = 500
    window_height = 500
    ren = tile_renderer.Renderer(window_width, window_height, block_size)
    ret = tile_level_editor.loop(ren, window_width, window_height, block_size)
    if ret == 'q':
        print("you have closed with the quit button")
    else:
        print('wat')

main()