# Taken from Layout Example in http://awesome-streamlit.org/

import io
from typing import List, Optional

import markdown
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly import express as px
from plotly.subplots import make_subplots

BACKGROUND_COLOR = 'white'
COLOR = 'black'

class Cell:
    '''A Cell can hold text, markdown, plots etc.'''

    def __init__(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None
    ):
        self.class_ = class_
        self.grid_column_start = grid_column_start
        self.grid_column_end = grid_column_end
        self.grid_row_start = grid_row_start
        self.grid_row_end = grid_row_end
        self.inner_html = ''

    def _to_style(self) -> str:
        return f'''
            .{self.class_} {{
                grid-column-start: {self.grid_column_start};
                grid-column-end: {self.grid_column_end};
                grid-row-start: {self.grid_row_start};
                grid-row-end: {self.grid_row_end};
            }}
            '''

    def text(self, text: str = ''):
        self.inner_html = text

    def markdown(self, text):
        self.inner_html = markdown.markdown(text)

    def dataframe(self, dataframe: pd.DataFrame):
        self.inner_html = dataframe.to_html()

    def plotly_chart(self, fig):
        self.inner_html = f'''
            <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
            <body>
                <p>This should have been a plotly plot.
                But since *script* tags are removed when inserting MarkDown/ HTML i cannot get it to workto work.
                But I could potentially save to svg and insert that.</p>
                <div id='divPlotly'></div>
                <script>
                    var plotly_data = {fig.to_json()}
                    Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
                </script>
            </body>
            '''

    def pyplot(self, fig=None, **kwargs):
        string_io = io.StringIO()
        plt.savefig(string_io, format='svg', fig=(2, 2))
        svg = string_io.getvalue()[215:]
        plt.close(fig)
        self.inner_html = '<div height="200px">' + svg + '</div>'

    def _to_html(self):
        return f'''<div class="box {self.class_}">{self.inner_html}</div>'''


class Grid:
    '''A (CSS) Grid'''

    def __init__(
        self,
        template_columns='1 1 1',
        gap='10px',
        background_color=BACKGROUND_COLOR,
        color=COLOR
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f'''
            <style>
                .wrapper {{
                display: grid;
                grid-template-columns: {self.template_columns};
                grid-gap: {self.gap};
                background-color: {self.background_color};
                color: {self.color};
                }}
                .box {{
                background-color: {self.color};
                color: {self.background_color};
                border-radius: 5px;
                padding: 20px;
                font-size: 150%;
                }}
                table {{
                    color: {self.color}
                }}
            </style>
            '''

    def _get_cells_style(self):
        return (
            '<style>'
            + '\n'.join([cell._to_style() for cell in self.cells])
            + '</style>'
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + '\n'.join([cell._to_html() for cell in self.cells])
            + '</div>'
        )

    def cell(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        cell = Cell(
            class_=class_,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell

class BlockContainerStyler:
    '''Block Container Styler'''

    def __init__(
        self,
        background_color=BACKGROUND_COLOR,
        color=COLOR
    ):
        self.background_color = background_color
        self.color = color

    def block_container_styler(self):
        '''Add selection section for setting setting the max-width and padding
        of the main block container'''
        st.sidebar.subheader('Block Container Styler')
        max_width_100_percent = st.sidebar.checkbox('Max-width: 100%?', False)
        if not max_width_100_percent:
            max_width = st.sidebar.slider('Select max-width in px', 100, 2000, 1100, 100)
        else:
            max_width = 1200
        dark_theme = st.sidebar.checkbox('Dark Theme?', False)
        padding_top = st.sidebar.number_input('Select padding top in rem', 0, 200, 1, 1)
        padding_right = st.sidebar.number_input('Select padding right in rem', 0, 200, 10, 1)
        padding_left = st.sidebar.number_input('Select padding left in rem', 0, 200, 1, 1)
        padding_bottom = st.sidebar.number_input('Select padding bottom in rem', 0, 200, 10, 1)
        
        if dark_theme:
            self.background_color = 'rgb(20,20,20)'
            self.color = 'white'
        else:
            self.background_color = 'white'
            self.color = 'black'

        self._set_block_container_style(
            max_width, max_width_100_percent,
            padding_top, padding_right, padding_left, padding_bottom
        )

    def set_default_block_container_style(
        self,
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10,
    ):
        self._set_block_container_style(
            max_width, max_width_100_percent,
            padding_top, padding_right, padding_left, padding_bottom,
        )

    def _set_block_container_style(
        self,
        max_width, max_width_100_percent,
        padding_top, padding_right, padding_left, padding_bottom,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                .reportview-container .main {{
                    color: {self.color};
                    background-color: {self.background_color};
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )
