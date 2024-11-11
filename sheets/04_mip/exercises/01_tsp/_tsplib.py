"""
Provides some instances for the TSP.
"""

import gzip
import itertools
import re
import tarfile
import typing
from pathlib import Path

import networkx as nx


class TspLibGraphInstanceDb:
    def __init__(self, archive_path: Path = Path("./ALL_tsp.tar.gz")):
        self.archive_path = archive_path
        self.instance_names = [
            # Integer coordinate based instances <= 1_000 nodes
            "att48",
            "att532",
            "eil101",
            "eil51",
            "eil76",
            "gil262",
            "kroA100",
            "kroA150",
            "kroA200",
            "kroB100",
            "kroB150",
            "kroB200",
            "kroC100",
            "kroD100",
            "kroE100",
            "lin105",
            "lin318",
            "linhp318",
            "pr107",
            "pr124",
            "pr136",
            "pr144",
            "pr152",
            "pr226",
            "pr264",
            "pr299",
            "pr439",
            "pr76",
            "st70",
        ]

    def download(self):
        if not self.archive_path.exists():
            # download the file from the internet.
            import urllib.request

            urllib.request.urlretrieve(
                "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/ALL_tsp.tar.gz",
                self.archive_path,
            )
            # throw on failure
            assert self.archive_path.exists(), "Download failed."

    def _parse_points(self, lines: typing.Iterable[str]):
        points = []
        start_parsing = False
        for line in lines:
            if line.startswith("NODE_COORD_SECTION"):
                start_parsing = True
                continue
            if start_parsing:
                if line.startswith("EOF"):
                    break
                point_data = line.split(" ")
                if len(point_data) != 3:
                    msg = "Instance is not 2d-coordinate based."
                    raise ValueError(msg)
                x = float(point_data[1])
                y = float(point_data[2])
                points.append((x, y))
        if not start_parsing:
            msg = "Instance is not coordinate based."
            raise ValueError(msg)
        return points

    def _create_graph(self, points):
        g = nx.Graph()
        for i, p in enumerate(points):
            g.add_node(i, pos=p)

        def dist(a, b):
            return round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5)

        for v, w in itertools.combinations(range(len(points)), 2):
            g.add_edge(v, w, weight=dist(points[v], points[w]))
        assert g.number_of_nodes() == len(points)
        assert g.number_of_edges() == len(points) * (len(points) - 1) // 2
        return g

    def __getitem__(self, name):
        # The instance will be in "name.tsp.gz"
        with tarfile.open(self.archive_path, "r:gz") as t:
            f_ = t.extractfile(name + ".tsp.gz")
            assert f_ is not None
            f = gzip.GzipFile(fileobj=f_)
            lines = f.readlines()
            lines = [line.decode() for line in lines]  # to string
            return self._create_graph(self._parse_points(lines))

    def __iter__(self):
        yield from self.instance_names

    def deduce_number_of_nodes_from_name(self, instance_name):
        match = re.search(r"\d+$", instance_name)
        return int(match.group()) if match else None

    def selection(self, min_nodes: int, max_nodes: int):
        for instance_name in self:
            n = self.deduce_number_of_nodes_from_name(instance_name)
            assert n is not None
            if min_nodes <= n <= max_nodes:
                yield instance_name
