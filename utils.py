import plotly.express as px
import plotly.graph_objects as go

def plot_trend_line(df, x_col, y_col, title, x_label, y_label, color_col=None):
    """
    Creates a line chart using Plotly Express.
    """
    fig = px.line(df, x=x_col, y=y_col, title=title, color=color_col, markers=True)
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="plotly_dark",
        hovermode="x unified"
    )
    return fig

def plot_bar_chart(df, x_col, y_col, title, x_label, y_label, color_col=None):
    """
    Creates a bar chart using Plotly Express.
    """
    fig = px.bar(df, x=x_col, y=y_col, title=title, color=color_col)
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="plotly_dark"
    )
    return fig

def format_large_number(num):
    """
    Formats large numbers (e.g., 1,000,000 -> 1M).
    """
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)
