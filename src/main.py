# -*- coding utf-8 -*-

from world import World

def main() -> int:

    program: World
    program = World()
    program.run()

    return 0

if __name__ == '__main__':
    raise SystemExit(main())