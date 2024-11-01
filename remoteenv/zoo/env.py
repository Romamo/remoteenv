from typing import List, Tuple

import kazoo
from kazoo.client import KazooClient


class ZooEnv:
    def __init__(self, prefix, hosts):
        self._prefix = prefix
        self._zk = KazooClient(hosts=hosts)

    def start(self) -> bool:
        if not self._zk.connected:
            try:
                self._zk.start()
            except kazoo.handlers.threading.KazooTimeoutError:
                return False
        return True

    def stop(self):
        if self._zk.connected:
            self._zk.stop()

    def dump(self) -> List[Tuple[str, str]]:
        # recursively dump all nodes
        def dump_node(path):
            try:
                children = self._zk.get_children(path)
            except kazoo.exceptions.NoNodeError:
                return
            for child in children:
                data, stat = self._zk.get(f"{path}/{child}")
                if data != b'':
                    if path == f"/{self._prefix}":
                        # print(f"{child}={data.decode()}, {stat.version}, {stat.numChildren} -> {path[2 + len(self._prefix):]}/{child} [{len(path)}")
                        yield child, data.decode()
                    else:
                        # print(f"{path}/{child}={data.decode()}, {stat.version}, {stat.numChildren} -> {path[2+len(self._prefix):]}/{child} [{len(path)}")
                        yield f"{path[2+len(self._prefix):]}/{child}", data.decode()
                for t in dump_node(f"{path}/{child}"):
                    yield t

        for t in dump_node(f"/{self._prefix}"):
            yield t

    def bulk_delete(self, exclude: List[str] = None):
        for k, v in self.dump():
            if k not in exclude:
                print(f"delete {k}")
                self._zk.delete(f"/{self._prefix}/{k}", recursive=True)

    def set(self, key, value):
        path = f"/{self._prefix}/{key}"

        try:
            current, stat = self._zk.get(path)
            if current.decode() != value:
                self._zk.set(path, value.encode())
        except kazoo.exceptions.NoNodeError:
            self._zk.create(path, value.encode(), makepath=True)

    def bulk_set(self, pairs: List[Tuple[str, str]], delete_others=True):
        for k, v in pairs:
            # print(f"{k}={v}")
            self.set(k, v)

        if delete_others:
            self.bulk_delete(exclude=[k[0] for k in pairs])

    def read(self, *paths) -> List[Tuple[str, str]]:
        for path in [f"/{self._prefix}"] + [f"/{self._prefix}/{p}" for p in paths] if paths else []:
            try:
                children = self._zk.get_children(path)
            except kazoo.exceptions.NoNodeError:
                continue
            for child in children:
                data, stat = self._zk.get(f"{path}/{child}")
                # print(f"{path}: {child}={data.decode()}")
                yield child, data.decode()
