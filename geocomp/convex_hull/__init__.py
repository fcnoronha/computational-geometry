from . import jarvis
from . import graham

children = [['jarvis', 'find_ch', 'Jarvis'],
            ['graham', 'find_ch', 'Graham']]


__all__ = [a[0] for a in children]
