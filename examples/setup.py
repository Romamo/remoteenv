from typing import Tuple, List

from remoteenv.zoo import ZooEnv


def split_text(text: str) -> List[Tuple[str, str]]:
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        yield tuple(line.split('=', 1))


s = """
DATABASE_DEFAULT_HOST=h2
mod/DATABASE_DEFAULT_HOST=h3
mod/h4/DATABASE_DEFAULT_HOST=h1
"""

envset = list(split_text(s))
env = ZooEnv('prefix', 'zoohost:2181')
env.start()
env.bulk_set(envset)
env.stop()
