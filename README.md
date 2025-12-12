# simple-tsp: A simple TSP solver using numpy and LNS

Welcome to `simple-tsp`, a highly efficient solver for the Traveling Salesman Problem (TSP) using the Large Neighborhood Search (LNS) algorithm. This project is for demonstration purposes, to show how complex optimization problems can be tackled in milliseconds with minimal code.

![](/tsp_plot/tsp_plot.gif)

## Important

No Copilot/Cursor/GPT/Claude etc was used for creating the code in this project (although they will very soon scrape and have it 😄)

## Features

-   Solves TSP for 17 cities in just 700 milliseconds on my machine.
-   Written in concise Python code (less than 80 lines).
-   Demonstrates significant improvements over exhaustive search methods.

## Requirements

Having `uv` installed on your machine

## Installation

1.  Clone the repository:

    ``` bash
    git clone https://github.com/nickgiki/simple-tsp.git
    cd simple-tsp
    ```

2.  Create a new venv using `uv`

    ``` bash
    uv venv -p 3.13
    ```

3.  Activate the environment

    on MacOS

    ``` bash
    source .venv/bin/activate
    ```

    on Windows

    ``` bash
    .venv\Scripts\activate
    ```

## Usage

Run the solver with the following command:

``` bash
python src/lns_tsp.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.