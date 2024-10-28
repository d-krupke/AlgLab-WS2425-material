"""
This code creates an interactive visualization of a branch and bound tree.
"""

from pathlib import Path
from typing import List, Optional

from jinja2 import Template
from pydantic import BaseModel

from .bnb_nodes import BnBNode
from .instance import Instance
from .relaxation import FractionalSolution


class BnBTree(BaseModel):
    node_id: int
    created_at: int
    processed_at: Optional[int] = None
    label: str
    color: str
    children: list["BnBTree"] = []


class BnBVisualization:
    def __init__(self, instance: Instance):
        self.root = None
        self.node_links = {}
        self.instance = instance
        self.node_detail_texts = {}
        self.iterations = []  # id of node processed in iteration

    def _get_node_color(self, node: BnBNode) -> str:
        if (
            node.relaxed_solution.is_fractionally_feasible()
            and node.relaxed_solution.is_integral()
        ):
            return "#20c997"
        return (
            "#adb5bd" if node.relaxed_solution.is_fractionally_feasible() else "#dc3545"
        )

    def on_new_node_in_tree(self, node: BnBNode):
        color = self._get_node_color(node)
        label = f"{node.relaxed_solution.value():.1f}"
        data = BnBTree(
            node_id=node.node_id,
            label=label,
            color=color,
            children=[],
            created_at=len(self.iterations),
        )
        if node.parent_id is None:
            assert self.root is None, "Root already exists."
            self.root = data
        else:
            self.node_links[node.parent_id].children.append(data)
        self.node_links[node.node_id] = data

    def on_node_processed(
        self,
        node: BnBNode,
        lb: float,
        ub: float,
        best_solution: Optional[FractionalSolution],
        heuristic_solutions: List[FractionalSolution],
    ):
        self.iterations.append(node.node_id)
        self.node_links[node.node_id].processed_at = len(self.iterations) - 1
        if node.parent_id is not None:
            assert self.node_links[node.parent_id].processed_at is not None
            assert (
                self.node_links[node.parent_id].processed_at
                < self.node_links[node.node_id].processed_at
            )
        with (Path(__file__).parent / "./templates/node.jinja2.html").open() as file:
            template_node_info = Template(file.read())
            node_info = template_node_info.render(
                node=node,
                lb=lb,
                ub=ub,
                heuristic_solutions=heuristic_solutions,
                best_solution=best_solution,
            )
            self.node_detail_texts[node.node_id] = node_info

    def visualize(self, path: str = "output.html"):
        if self.root is None:
            msg = "No nodes to visualize."
            raise ValueError(msg)
        with (
            Path(__file__).parent / "./templates/instance.jinja2.html"
        ).open() as file:
            template_instance = Template(file.read())
            instance_info = template_instance.render(instance=self.instance)
        with (Path(__file__).parent / "./templates/bnb.jinja2.html").open() as file:
            template = Template(file.read())
        with Path(path).open("w") as file:
            data = str(self.root.model_dump_json())
            file.write(
                template.render(
                    tree_data=data,
                    num_iterations=len(self.iterations) - 1,
                    iterations=self.iterations,
                    instance_info=instance_info,
                    node_details=self.node_detail_texts,
                )
            )
            print("Visualization saved to", path)
