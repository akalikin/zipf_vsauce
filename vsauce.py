import re, string
from collections import Counter
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
pattern = re.compile("(<(.*?)>)+|(\d+)|(\r\n)")
table = string.maketrans("", "")
sub = "subtitles.srt"
lines = [line.replace('\n', '').replace('\r', '').translate(table, string.punctuation) for line in open(sub) if not pattern.match(line)]
words = [word for line in lines for word in line.split()]
data = sorted(Counter(words).items(), key=lambda (k, v): v, reverse=True)

source = ColumnDataSource(
        data=dict(
            x=range(0,len(data)),
            y=[v for (k,v) in data],
            desc=[k for (k,v) in data],
        )
    )

hover = HoverTool(
        tooltips=[
            ("index", "$index"),
            ("desc", "@desc"),
        ]
    )

p = figure(plot_width=900, plot_height=450, tools=[hover, 'box_zoom', 'resize', 'pan', 'reset', 'save', 'wheel_zoom'],
           title="Mouse over the dots")

p.circle('x', 'y', source=source)
output_file('graph.html')
show(p)
