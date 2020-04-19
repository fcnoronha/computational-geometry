from . import brute_force
from . import bent_ott

children = [['bent_ott', 'Bent_ott', 'Bentley and\nOttmman'],
            ['brute_force', 'Brute_force', 'Forca\nBruta']]


__all__ = [a[0] for a in children]
