# standard
# none

# pypi
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# local
# none

# globals
DIAMONDS_DATA_FILE = "./diamonds.csv"
PLOTLY_OUTPUT_FILE = "./index.html"


def get_data():
    return pd.read_csv(DIAMONDS_DATA_FILE)


def main():
    # get data
    diamondData = get_data().round(decimals=3)

    # get figure
    fig = make_subplots(
        rows=2, cols=2,
        shared_xaxes=False,
        specs=[
            [{'type': 'surface'}, {'type': 'xy'}],
            [{'type': 'xy'}, {'type': 'xy'}]
            ],
        subplot_titles=(
            "Diamond Fracture Locations",
            "Population of Diamond Colors",
            "Diamond Price Against Diamond Weight",
            "Diamond Table-to-Depth Ratio by Clarity"
        )
    )

    # gather data for plotting
    # --- common calculations
    priceHi = max(diamondData.loc[:, "price"])
    priceLo = min(diamondData.loc[:, "price"])

    # --- plot 3
    depthTable = diamondData.loc[:, "table"] / diamondData.loc[:, "depth"]

    # plot data
    # --- figure in 1,1 position in page
    fig.add_trace(
        go.Scatter3d(
            x=diamondData.loc[:, "x"],
            y=diamondData.loc[:, "y"],
            z=diamondData.loc[:, "z"],
            mode='markers',
            marker={"colorscale": "viridis",
                    "color": diamondData.loc[:, "price"],
                    "colorbar": {"title": "Price"},
                    "cmax": priceHi,
                    "cmin": priceLo,
                    },
        ),
        row=1,
        col=1
    )
    fig.update_layout(
        scene={
            "xaxis": {"title": "X"},
            "yaxis": {"title": "Y"},
            "zaxis": {"title": "Z (depth)"},
        }
    )

    # --- figure in 1,2 position in page
    fig.add_trace(
        go.Histogram(
            x=diamondData.loc[:, "color"],
            showlegend=False,
            marker={"color": "blue"}
        ),
        row=1,
        col=2
    )
    fig['layout']['xaxis']['title'] = 'Diamond Color'

    # --- figure in 2,1 position in page
    fig.add_trace(
        go.Scatter(
            x=diamondData.loc[:, "carat"],
            y=diamondData.loc[:, "price"],
            mode='markers',
            marker={"colorscale": "viridis",
                    "color": diamondData.loc[:, "price"],
                    "cmax": priceHi,
                    "cmin": priceLo,
                    }
        ),
        row=2,
        col=1
    )
    fig['layout']['xaxis2']['title'] = 'Diamond Carat (units of 200 mg)'
    fig['layout']['yaxis2']['title'] = 'Price of Diamond (USD)'

    # --- figure in 2,2 position in page
    fig.add_trace(
        go.Scatter(
            x=diamondData.loc[:, "cut"],
            y=depthTable,
            mode='markers',
            marker={"colorscale": "Bluered",
                    "color": depthTable,
                    }
        ),
        row=2,
        col=2
        )
    # fig.add_trace(diamondPrice, row=2, col=2)
    fig['layout']['xaxis3']['title'] = 'Diamond Clarity'
    fig['layout']['yaxis3']['title'] = 'Price of Diamond (USD)'

    # finalize html and write file
    fig.update_traces(showlegend=False)
    fig.write_html(file=PLOTLY_OUTPUT_FILE,
                   full_html=False,
                   include_plotlyjs='cdn')


if __name__ == "__main__":
    main()
else:
    raise Exception("Sorry, this is not a module to be imported")
