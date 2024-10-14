# Algorithms Lab - Winter 2024/2025

_Instructor: [Dr. Dominik Krupke](https://www.ibr.cs.tu-bs.de/users/krupke/)
IBR, Algorithms Group_

Optimization problems are pervasive across numerous real-world applications
within computer science, ranging from
[route planning](https://en.wikipedia.org/wiki/Travelling_salesman_problem) to
[job scheduling](https://en.wikipedia.org/wiki/Job-shop_scheduling). Certain
problems, like the
[shortest path](https://en.wikipedia.org/wiki/Shortest_path_problem), can be
solved efficiently in theory and practice. However, a significant number of
these optimization problems are classified as
[NP-hard](https://en.wikipedia.org/wiki/NP-hardness), indicating that, for these
problems, there is no known algorithm capable of consistently solving every
instance efficiently to proven optimality. In such instances, heuristic
approaches, such as
[genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm), are
frequently employed as practical solutions. Yet, the question arises: Is it
possible to devise algorithms that yield optimal solutions within a feasible
timeframe for reasonably sized instances? This laboratory course is dedicated to
exploring three sophisticated techniques that hold the potential for computing
optimal solutions for a vast array of problems within practical limits. These
techniques include:

- **Constraint Programming** with
  [CP-SAT](https://developers.google.com/optimization/cp/cp_solver): This
  versatile methodology enables the definition of a problem’s constraints, upon
  which it employs a comprehensive suite of strategies, including the two
  techniques discussed below, to find optimal solutions.
- **SAT Solvers**: Renowned for their ability to resolve extensive logical
  formulas, these tools can be ingeniously adapted to address optimization
  challenges by transforming them into logical propositions.
- **Mixed Integer Programming (MIP)**: This approach is adept at solving
  optimization problems characterized by integer and continuous variables under
  linear constraints.

For algorithm engineers and operations researchers, mastering these techniques
opens the door to modeling and solving a wide spectrum of combinatorial
optimization problems. By the end of this course, you will have acquired the
skills to leverage these powerful methodologies, enabling you to approach
NP-hard problems not only with theoretical insight but with practical,
actionable solutions. This journey is not just about crafting elegant models but
also about utilizing robust solution engines to navigate the complexities of
NP-hard challenges effectively.

## Content

The class is organized into two main components: a series of exercises and an
in-depth final project, both of which are designed to enhance your proficiency
with key optimization techniques.

The exercise sheets will be conducted in pairs, while final projects will
require collaboration among groups of three to four students. To ensure
equitable team composition for the final projects, we may consider individual
performance in the exercises as a criterion for team formation. Our objective is
to create balanced teams by pairing students of comparable skill levels. This
approach is informed by our observation that teams with a mix of varying
abilities can sometimes lead to an imbalance, where more proficient students may
inadvertently overshadow their peers.

### Exercise Sheets Overview

To ensure you are thoroughly prepared for the project phase, this class will
begin with a series of exercise sheets. These exercises are carefully crafted to
either introduce you to new techniques or enhance your existing knowledge of
them. Designed with a hands-on approach, these tasks aim to provide you with
practical exposure to relevant tools and methodologies.

Each exercise sheet is allocated a two-week completion window. However, with new
sheets released on a weekly basis, you effectively have one week to work on each
exercise, with an additional week serving as a buffer. While the exercises are
designed to be completed within a few hours, the learning curve associated with
mastering new techniques may necessitate additional time. The time required to
complete each sheet may vary; for example, you might spend more time on the
initial sheet and less on subsequent ones, or vice versa, depending on your
familiarity with the topics covered.

|                  Sheet                  |           Time           |                                                                                                                                                 Content                                                                                                                                                 |
| :-------------------------------------: | :----------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| [Exercise Sheet 1A](./sheets/01_cpsat/) | 2024-10-15 to 2024-10-29 |                                                                                        Constraint Programming with CP-SAT - A Hello-World with CP-SAT, NetworkX, and Scalene. All nice and easy to get started.                                                                                         |
| [Exercise Sheet 1B](./sheets/01_cpsat/) | 2024-20-22 to 2024-11-05 |                                     Constraint Programming with CP-SAT - Here you will explore the use of CP-SAT, a declarative constraint programming solver. You will learn to define your problem mathematically, allowing CP-SAT to efficiently find solutions.                                     |
|   [Exercise Sheet 2](./sheets/02_bnb)   | 2024-10-29 to 2024-11-12 |                          DIY: Branch and Bound - This exercise delves into the foundational algorithm behind generic solvers like CP-SAT. Participants will gain insights into what these solvers require for optimal performance by exploring the Branch and Bound algorithm.                          |
|  [Exercise Sheet 3](./sheets/03_sat/)   | 2024-11-05 to 2023-11-19 |                                      SAT Solver - After the high-level interface provided by CP-SAT, this exercise demands a closer interaction with the core mechanics of a SAT solver. You will learn to translate complex problems into basic logical formulas.                                      |
|  [Exercise Sheet 4](./sheets/04_mip/)   | 2024-11-12 to 2024-11-26 | Mixed Integer Programming - Learn about Mixed Integer Programming (MIP), a technique favored by many optimization experts. Although not as expressive as CP-SAT, MIP offers better scalability and the opportunity to apply various optimization tricks thanks to an extensive mathematical foundation. |

> [!WARNING]
>
> These exercises are not traditional homework; they are the core of this course
> and should be approached accordingly. Each exercise sheet will require a full
> day of focused work, as they introduce new concepts and techniques you may not
> have encountered before. You will need to carefully study both the course
> material and the provided references to fully understand these concepts. Given
> the complexity, I expect you to ask more questions and seek assistance
> frequently.

### Final Project

In the latter part of the course, we will embark on a comprehensive final
project, marking an opportunity for you to apply the methodologies and
strategies discussed in the exercises to a concrete, real-world challenge. This
project phase, extending over several weeks, invites you to engage deeply with a
problem, under the mentorship of your tutor. The culmination of this endeavor
will be a presentation, wherein you will have the chance to exhibit the outcomes
of your efforts.

The essence of the project phase is to immerse you in the practical application
of optimization techniques, tackling a problem that demands a blend of
innovative thinking and strategic planning. You are encouraged to explore
diverse approaches to the problem, aiming to devise a persuasive and effective
solution.

Please note, as a five-credit course, you are expected to dedicate up to 150
hours in total to coursework. This allocation includes both the exercises and
the project, with no more than 50 hours slated for the exercises. Consequently,
a minimum of 100 hours should be devoted to the project, ensuring a deep and
productive engagement with the material and the challenge at hand.

## Prerequisites

For a successful experience in this course and to effectively work on the
projects, students are expected to meet the following prerequisites:

1. **Proficiency in Python**: The course's programming components will be
   exclusively conducted in Python. It is essential that you have a solid grasp
   of Python, as there will not be sufficient time to learn the language during
   the course.
2. **Algorithmic Foundations**:
   - Completion of _Algorithms and Data Structures 1_ is compulsory for
     foundational knowledge.
   - It is advisable to have also completed (or complete in parallel)
     _Algorithms and Data Structures 2_ and _Network Algorithms_ to be better
     prepared for the more complex topics.
   - Additionally, it is beneficial to have attended _Logic for Computer
     Scientist_ and _Theoretical Computer Science I+II_ to be familiar with
     NP-hardness and propositional logic.
3. **Unix-Based Operating System**:
   - Access to a Unix system, which could be in the form of a virtual machine,
     is required for the course. Students should possess a fundamental
     understanding of Unix command-line operations.
   - While most of the tools and software used in this course are compatible
     with Windows, support for Windows-specific issues cannot be guaranteed.
4. **Version Control with Git**:
   - A basic familiarity with Git is needed for version control purposes. While
     Git skills can be acquired swiftly, students are expected to learn them
     independently prior to or during the initial phase of the course.

Please ensure you meet these requirements to engage fully in the course
activities. If you have any questions or need clarification on the
prerequisites, feel free to reach out to us.

## Lectures to go next

This class is just a quick peek into solving NP-hard problems in practice, there
is more!

- _Algorithm Engineering (Master, infrequently)_ will teach you a superset of
  this class, with more details.
- _Mathematische Methoden der Algorithmik (Master)_ will teach you the
  theoretical background of Linear Programming and Mixed Integer Programming.
- _Approximation Algorithms (Master)_ will teach you theoretical aspects of how
  to approximate NP-hard problems with guarantees. While this takes a
  theoretical point of view, the theoretical understanding can improve your
  practical skills on understanding and solving such problems.

## References

- [Discrete Optimization Course](https://www.coursera.org/learn/discrete-optimization/):
  For those who are want to dive really deep into the topic, I recommend doing
  this free course on Coursera in parallel. It is very intense but also very
  rewarding. Probably one of the best courses I have ever seen.
- [In Pursuit of the Traveling Salesman](https://press.princeton.edu/books/paperback/9780691163529/in-pursuit-of-the-traveling-salesman):
  This amazing book is not a surprisingly good read, but also a great
  introduction to the field of optimization. It gives you a lot of the ideas
  that allow us to solve NP-hard problems in practice, while also gently
  introducing you to the way of thinking of an optimization expert.

## Found an error?

Please let us know by opening an issue! You can also create a pull request on a
separate branch, but as we have to do the changes in our internal repository
(which also contains solutions), from which the public repository is
automatically updated, it is easier for us if you open an issue and let us do
the changes.

## Are you an instructor?

If you are an instructor and want to use this material in your course, feel free
to do so! We are happy to share our material with you. If you have any
questions, feel free to reach out to us. To get the solutions, please contact us
directly from your official university email address, so we can verify that you
are an instructor and not a student.
