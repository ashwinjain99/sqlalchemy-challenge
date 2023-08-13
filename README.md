# SurfsUP
## Part 1: Analyzing and Exploring the Climate Data: A Pythonic Approach with SQLAlchemy, Pandas, and Matplotlib
- Connect to the SQLite database using SQLAlchemy's create_engine() function.
- Use automap_base() to reflect the tables into classes and save references to the classes named "station" and "measurement." This allows to work with the database tables as Python classes.
- Create a SQLAlchemy session to interact with the database.
### Perform a precipitation analysis:
- Find the most recent date in the dataset.
- Query the previous 12 months of precipitation data.
- Load the results into a Pandas DataFrame and plot the data as a chart.
- Print summary statistics for the precipitation data.
### Perform a station analysis:
- Calculate the total number of stations in the dataset.
- Find the most active stations based on the number of observations.
- Calculate the lowest, highest, and average temperatures for the most active station.
- Query the previous 12 months of temperature observation (TOBS) data for the most active station.
- Plot the temperature observations as a histogram.
## Part 2: Flask API Routes for Climate Data Analysis
- `/`: The homepage that lists all the available routes for the API.

- `/api/v1.0/precipitation`: Returns the last 12 months of precipitation data in a JSON format. The data is organized as a dictionary with dates as keys and precipitation values as values.

- `/api/v1.0/stations`: Returns a JSON list of all the stations available in the dataset.

- `/api/v1.0/tobs`: Queries and returns a JSON list of temperature observations for the most-active station for the previous year.

- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returns a JSON list containing the minimum, average, and maximum temperature for a specified start date or a start-end date range.

  - For a specified start date, the API calculates TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.

  - For a specified start date and end date, the API calculates TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
