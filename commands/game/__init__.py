from . import exit
from . import help
from . import info
from . import kick
from . import nonrp
from . import location
from . import locations

# GameChat импортируется в последнюю очередь,
# чтобы команды до GameChat регестрировались раньше
# и обработчик GameChat не перехватывал сообщения.
from . import GameChat