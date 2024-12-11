import pandas as pd
from db import DBConn
from markupsafe import Markup
import plotly.graph_objs as go
from plotly.offline import plot


class Graphs:

    def __init__(self, datastore: DBConn) -> None:
        
        self.db = datastore


    def line_graph(self) -> Markup:
        
        df = pd.DataFrame(self.db.read_db())
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["total"]))
        fig.update_layout(title_text="Net Worth over Time")
        fig.update_xaxes(title_text="Dates")
        fig.update_yaxes(title_text="Value (£)")
        fig.update_layout(
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=10, r=10, b=20, t=25, pad=10),

        )
        fig.update_layout(
            barmode='stack',
            xaxis=dict(
                type='date',
                tickformat="%d/%m/%Y",
                tickangle=45
            ),
        )

        line_chart = plot(figure_or_data=fig,
                          include_plotlyjs=True,
                          output_type='div')
        
        return Markup(line_chart)


    def progress_graph(self) -> Markup:

        df = pd.DataFrame(self.db.read_db())
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

        current_total = df['total'].iloc[-1]

        fig = go.Figure()
        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=current_total,
            mode="gauge+number",
            title={'text': "Progress to Lean and Fat FIRE"},
            gauge={'axis': {'range': [None, 600000]},
                'steps': [
                    {'range': [0, 450000], 'color': "lightgray"},
                    {'range': [450000, 600000], 'color': "gray"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 600000}}))
        fig.update_layout(title_text="Progress Chart")
        fig.update_layout(
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=10, r=10, b=20, t=25, pad=5),
        )

        progress_chart = plot(figure_or_data=fig,
                              include_plotlyjs=True,
                              output_type='div')

        return Markup(progress_chart)


    def stacked_graph(self) -> Markup:

        df = pd.DataFrame(self.db.read_db())
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

        fig = go.Figure(data=[
            go.Bar(name='Axis', x=df['date'], y=df['axis']),
            go.Bar(name='Shares', x=df['date'], y=df['shares']),
            go.Bar(name='Pension', x=df['date'], y=df['pension']),
            go.Bar(name='LISA', x=df['date'], y=df['lisa']),
        ])
        fig.update_layout(barmode='stack')
        fig.update_layout(title_text="Breakdown over Time")
        fig.update_layout(
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=10, r=10, b=20, t=25, pad=5),
        )
        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))
        fig.update_layout(
            barmode='stack',
            xaxis=dict(
                type='date',
                tickformat="%d/%m/%Y",
                tickangle=45
            ),
        )

        stacked_chart = plot(figure_or_data=fig,
                             include_plotlyjs=True,
                             output_type='div')

        return Markup(stacked_chart)


    def treemap_plot(self) -> Markup:

        df = pd.DataFrame(self.db.read_db())
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

        data = {
            'name': ['Axis', 'Shares', 'Pension', 'LISA'],
            'number': [df['axis'].iloc[-1], df['shares'].iloc[-1], df['pension'].iloc[-1], df['lisa'].iloc[-1]]
        }
        df = pd.DataFrame.from_dict(data)

        parents = [''] * len(df['name'])

        fig = go.Figure(go.Treemap(labels=df['name'], values=df['number'], parents=parents))
        fig.update_layout(title_text="Latest Breakdown")
        fig.update_layout(
            autosize=False,
            width=450,
            height=500,
            margin=dict(l=10, r=10, b=20, t=25, pad=5),
        )

        treemap = plot(figure_or_data=fig,
                       include_plotlyjs=True,
                       output_type='div')

        return Markup(treemap)