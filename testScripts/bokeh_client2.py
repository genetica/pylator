from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

def modify_doc(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    

bokeh_app = Application(FunctionHandler(modify_doc))

def bkworker():
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    import threading
    server = Server({'/': bokeh_app})
    worker = threading.Thread(target=bkworker)
    worker.start()
    while input(">>")[0] != 'q':
        pass
    server.io_loop.stop()
    worker.join()

    