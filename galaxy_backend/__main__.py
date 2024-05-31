from pathlib import Path
import sys


if __name__ == '__main__':
    sys.path.append(
        str(Path(__file__).parent.resolve())
    )
    from core import main
    main.main()

