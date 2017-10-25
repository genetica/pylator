from bokeh.models.widgets import RadioGroup
from bokeh.layouts import widgetbox
from bokeh.layouts import layout
from bokeh.models.widgets import Slider
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure


output_file("slider.html")

p1 = figure()
p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

p2 = figure()
p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)

slider = Slider(start=0, end=10, value=1, step=.1, title="Stuff")
w1 = layout([[widgetbox(slider), p1]])

radio_group = RadioGroup(
        labels=["Option 1", "Option 2", "Option 3"], active=0)
w2 = layout([[widgetbox(radio_group), p2]])

tab1 = Panel(child=w1, title="circle")
tab2 = Panel(child=w2, title="line")

tabs = Tabs(tabs=[ tab1, tab2 ])

show(tabs)