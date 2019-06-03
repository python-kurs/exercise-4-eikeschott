import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Import both data tables into python using pandas. Set the index column to "MESS_DATUM" and parse the column values as dates. [1P]
garmisch=pd.read_csv("data/produkt_klima_tag_20171010_20190412_01550.txt", parse_dates=["MESS_DATUM"], index_col="MESS_DATUM", sep=";")
zugspitze=pd.read_csv("data/produkt_klima_tag_20171010_20190412_05792.txt", parse_dates=["MESS_DATUM"], index_col="MESS_DATUM", sep=";")

# Clip the tables to the year 2018: [1P]
garmisch = garmisch["2018"]
zugspitze = zugspitze["2018"]

# Resample the temperature data to monthly averages (" TMK") and store them in simple lists: [1P]
garmisch_agg = [garmisch[" TMK"].resample("1M").mean()]
zugspitze_agg = [zugspitze[" TMK"].resample("1M").mean()]

# Define a plotting function that draws a simple climate diagram
# Add the arguments as mentioned in the docstring below [1P]
# Set the default temperature range from -15°C to 20°C and the precipitation range from 0mm to 370mm [1P]
def create_climate_diagram(df, temp_col:str, prec_col:str, title:str, filename:str, temp_min:int=15, temp_max:int=20, prec_min:int=0, prec_max:int=370):
    """
    Draw a climate diagram.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with values to plot from
    temp_col : str
        Name of temperature column
    prec_col : str
        Name of precipitation column
    title : String
        The title for the figure
    filename : String
        The name of the output figure
    temp_min : Number
        The minimum temperature value to display
    temp_max : Number
        The maximum temperature value to display
    prec_min : Number
        The minimum precipitation value to display
    prec_max : Number
        The maximum precipitation value to display

    Returns
    -------
    The figure
    
    """
    fig = plt.figure(figsize=(10,8))
    plt.rcParams['font.size'] = 16

    ax2 = fig.add_subplot(111)
    ax1 = ax2.twinx()

    # Draw temperature values as a red line and precipitation values as blue bars: [1P]
    # Hint: Check out the matplotlib documentation how to plot barcharts. Try to directly set the correct
    #       x-axis labels (month shortnames).
    days = mdates.DayLocator(bymonthday=28)
    monthFmt = mdates.DateFormatter("%b")
    ax2.xaxis.set_major_locator(days)
    ax2.xaxis.set_major_formatter(monthFmt)
    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(monthFmt)
    
    df = df.loc[:,[temp_col,prec_col]].resample("1M").agg({temp_col:"mean",prec_col:"sum"})
    ax2.bar(df.index, height=df[prec_col], color="blue", width=20, label="Precipitation")
    ax1.plot(df[temp_col], color="r", label="Temperature")
    # Set appropiate limits to each y-axis using the function arguments: [1P]
    ax2.set_ylim(prec_min, prec_max)
    ax1.set_ylim(temp_min, temp_max)
    
    # Set appropiate labels to each y-axis: [1P]
    ax2.set_ylabel("Precipitation (mm)")
    ax1.set_ylabel("Temperature (°C)")
    
    # Give your diagram the title from the passed arguments: [1P]
    plt.title(title)
    
    # Save the figure as png image in the "output" folder with the given filename. [1P]
    fig.savefig(filename)
    return fig

# Use this function to draw a climate diagram for 2018 for both stations and save the result: [1P]
create_climate_diagram(df=garmisch, temp_col=" TMK", prec_col=" RSK", title="Garmisch", filename="Garmisch.png", temp_min=-15, temp_max=20, prec_min=0, prec_max=370)

create_climate_diagram(df=zugspitze, temp_col=" TMK", prec_col=" RSK", title="Zugspitze", filename="Zugspitze.png", temp_min=-15, temp_max=20, prec_min=0, prec_max=370)

