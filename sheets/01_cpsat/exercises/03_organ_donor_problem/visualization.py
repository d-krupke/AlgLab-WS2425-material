import argparse
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
from _db_impl import SqliteTransplantDatabase
from data_schema import Donation, Donor, Recipient
from database import TransplantDatabase
from solution_basic import CrossoverTransplantSolver
from solution_small_cycles import CycleLimitingCrossoverTransplantSolver


def visualize_donations(
    donations: List[Donation], database: TransplantDatabase, basic: bool
):
    """
    Visualize the donations utilizing a directed graph drawing:

    In this directed graph, every node represents a patient and is labeled with their unique id.
    Edges ('a', 'b') in this graph represent donations from a donor representing patient 'a' directly
    to patient 'b'. All patients that do not receive a donation are marked with grey color.
    """

    def patient_to_node(patient: Recipient):
        return f"r_{patient.id}"

    def donor_to_node(donor: Donor):
        return f"d_{donor.id}"

    involved_donors = {donation.donor for donation in donations}
    involved_patients = {donation.recipient for donation in donations}

    patient_nodes = set()
    donor_nodes = set()
    donation_edges = []
    associaton_edges = []
    for donation in donations:
        # create recipient and donor nodes
        r_node = patient_to_node(donation.recipient)
        d_node = donor_to_node(donation.donor)
        patient_nodes.add(r_node)
        donor_nodes.add(d_node)
        # add edge for donation
        donation_edges.append((d_node, r_node))
        # add edge to represent association
        assoc_donors = (
            set(database.get_partner_donors(donation.recipient)) & involved_donors
        )
        assert len(assoc_donors) == 1
        associaton_edges.append((r_node, donor_to_node(assoc_donors.pop())))

    left_patients = set(database.get_all_recipients()) ^ involved_patients
    left_patient_nodes = {patient_to_node(p) for p in left_patients}

    # construct digraph
    full_donation_graph = nx.DiGraph()
    full_donation_graph.add_nodes_from(patient_nodes)
    full_donation_graph.add_nodes_from(donor_nodes)
    full_donation_graph.add_nodes_from(left_patient_nodes)
    full_donation_graph.add_edges_from(donation_edges)
    full_donation_graph.add_edges_from(associaton_edges)
    if basic:
        layout = nx.kamada_kawai_layout(full_donation_graph)
    else:
        layout = nx.fruchterman_reingold_layout(full_donation_graph)

    # create drawing, draw nodes and edges with different styles
    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw_networkx_nodes(
        full_donation_graph, pos=layout, nodelist=patient_nodes, node_color="pink"
    )
    nx.draw_networkx_nodes(
        full_donation_graph, pos=layout, nodelist=donor_nodes, node_color="lime"
    )
    nx.draw_networkx_nodes(
        full_donation_graph, pos=layout, nodelist=left_patient_nodes, node_color="gray"
    )
    nx.draw_networkx_labels(full_donation_graph, pos=layout)
    nx.draw_networkx_edges(full_donation_graph, pos=layout, edgelist=donation_edges)
    nx.draw_networkx_edges(
        full_donation_graph,
        pos=layout,
        edgelist=associaton_edges,
        arrows=False,
        style=":",
    )

    # create a custom legend
    custom_legend = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color,
            markersize=10,
            label=name,
        )
        for color, name in [
            ("pink", "Receiving Patient"),
            ("lime", "Donating Donor"),
            ("gray", "Non-Receiving Patient"),
        ]
    ]
    custom_legend += [
        plt.Line2D([0], [0], color="black", linestyle=style, label=name)
        for style, name in [("-", "Donation"), (":", "Association")]
    ]
    ax.legend(handles=custom_legend)

    plt.title(
        f"{len(database.get_all_recipients())} patients, {len(donations)} crossover donations"
    )
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualization script for visualizing solutions to the crossover transplant problem."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--basic", action="store_true", help="Select basic option")
    group.add_argument(
        "--cycle-limiting", action="store_true", help="Select cycle-limiting option"
    )
    args = parser.parse_args()

    # sqlite database
    db: TransplantDatabase = SqliteTransplantDatabase("./instances/20.db")

    # create solver based on arguments
    if args.basic:
        solver = CrossoverTransplantSolver(database=db)
    else:
        solver = CycleLimitingCrossoverTransplantSolver(database=db)

    if solution := solver.optimize(60.0):
        # visualize using graph
        visualize_donations(donations=solution.donations, database=db, basic=args.basic)
    else:
        print("No solution returned!")
