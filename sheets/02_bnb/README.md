# Your own Branch and Bound Algorithm

After you have made some first experiences with solving the Knapsack and other
problems using CP-SAT as a black-box solver, we take a step back and look at
the fundamentals of solving NP-hard optimization problems in practice.

This exercise is designed to guide you through the process of implementing an
efficient branch and bound algorithm, specifically tailored to tackle the
Knapsack Problem. The term "efficient" here is defined by our ability to keep
the search tree as compact as possible, preventing exponential growth with the
addition of more items. Although it is not feasible to promise a consistently
small search tree, strategic decision-making can significantly mitigate its
expansion. Such optimization techniques are fundamental to modern solvers,
enabling them to address large-scale problems with remarkable efficiency. While
your implementation may not rival the capabilities of these advanced solvers,
this exercise aims to deepen your understanding of their underlying mechanics,
enhancing your proficiency in utilizing them effectively.

### Setting Up the Environment

This exercise will be conducted within a Jupyter notebook, providing a dynamic
and interactive coding environment. To prepare, install the necessary packages
by executing the following command in your terminal:

```bash
pip install -r requirements.txt
```

After installing the requirements, initiate the notebook by running:

```bash
jupyter-lab bnb.ipynb
```

For those unfamiliar with JupyterLab, a brief introduction is available through
this [Youtube video](https://youtu.be/p01wt-WB84c?si=qwCeY-ffKXpbQRr1), offering
insights into its features and functionalities.

> [!WARNING]
>
> The visualization will be written to `output.html` in the current directory.
> You can open it in JupyterLab or in your browser to explore the search tree.
> If the visualization does not render correctly, you may have to allow the
> javascript to run by trusting the file.