import pandas as pd
import plotly.graph_objects as go
from django.shortcuts import render
from .models import PowerData
import datetime

def data_display(request):
    plot_divs = []
    start_date = datetime.date.today().replace(day=1) 
    end_date = datetime.date.today() 
    available_days = pd.date_range(start_date, end_date, freq='D').strftime('%Y-%m-%d').tolist()

    if request.method == 'POST':
        selected_day = request.POST.get('selected_day')
        day_start = pd.to_datetime(selected_day)
        day_end = day_start + pd.DateOffset(days=1)
        
        data = PowerData.objects.filter(
            timestamp__range=(day_start, day_end)
        )
    else:
        day_start = pd.Timestamp(datetime.date.today())
        day_end = day_start + pd.DateOffset(days=1)
        data = PowerData.objects.filter(
            timestamp__range=(day_start, day_end)
        )

    # Check if any data exists for the selected day (or current day)
    if data.exists():
        # Assuming you've already fetched and processed the 'data' for the selected day
        df = pd.DataFrame.from_records(data.values('timestamp', 'current', 'voltage', 'power'))

        # Create plots (same as before)
        for y_data, title, y_axis_title in [
            (df['current'], 'Current', 'Amps'),
            (df['voltage'], 'Voltage', 'Volts'),
            (df['power'], 'Power', 'Watts')
        ]:
            fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=y_data, mode='lines', hovertemplate='<b>%{y:.2f} ' + y_axis_title + '</b><br>%{x|%H:%M}<extra></extra>')])
            fig.update_layout(title=title, xaxis_title='Time', yaxis_title=y_axis_title)
            plot_divs.append(fig.to_html(full_html=False))
    else:
        # Handle the case where no data is available for the selected day
        plot_divs.append("<p>No data available for the selected day.</p>") 
    

    return render(request, 'data_display.html', {'plot_divs': plot_divs, 'available_days': available_days})


