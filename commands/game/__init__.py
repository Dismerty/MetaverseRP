from . import exit
from . import info
from . import kick
from . import nonrp
from . import location

# GameChat импортируется в последнюю очередь,
# чтобы команды до GameChat регестрировались раньше
# и обработчик GameChat не перехватывал сообщения.
from . import GameChat