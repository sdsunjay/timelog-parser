# Time Log HTML Table Parser

## Description

The `timelog.py` script provides functionality to parse, process, and reorder timelog data stored in HTML tables. The primary purpose is to calculate the time difference (in minutes) between start and end times for a given activity and reorder the table entries accordingly.

## Table Structure

The script expects the table to have the following column headings:

1. **Date**: The date of the activity.
2. **Start Time**: The time when the activity started.
3. **Stop Time**: The time when the activity stopped.
4. **Activity Code**: A unique code representing the activity.
5. **Activity Description**: A brief description of the activity.
6. **Delta Time**: The difference in minutes between the start and stop times.

### Example
```html
<table BORDER="3">
  <tbody>
    <tr>
        <td> Date </td>
        <td> Start </td>
        <td> Stop </td>
        <td> Activity Code </td>
        <td> Activity </td>
        <td> Delta Time </td>
    </tr>
    <tr>
        <td> 08/21/23 </td>
        <td> 23:10 </td>
        <td> 01:10 </td>
        <td> ADMIN </td>
        <td> Created this README </td>
        <td> xx </td>
    </tr>
    <tr>
        <td> 08/20/23 </td>
        <td> 16:10 </td>
        <td> 19:10 </td>
        <td> DEV </td>
        <td> Worked on timelog.py </td>
        <td> 180 </td>
    </tr>
   </tbody>
</table>
```

## Functions

1. **`time_delta(row, date_column, start_time_column, end_time_column)`**:
    - **Description**: Calculates the time difference in minutes between the start and end times for a given row.
    - **Parameters**: The row data, the indices for the date, start time, and end time columns.
    - **Returns**: The time difference in minutes.

2. **`create_final_table(table)`**:
    - **Description**: Converts a list of lists (table) into an HTML table string.
    - **Parameters**: A list of lists representing the table.
    - **Returns**: An HTML string representation of the table.

3. **`process_html(soup)`**:
    - **Description**: Parses an HTML table and returns its rows as lists.
    - **Parameters**: A BeautifulSoup object containing the HTML table.
    - **Returns**: A list of rows, where each row is a list of cell contents.

4. **`reorder_table(file_name, date_column, start_time_column, end_time_column)`**:
    - **Description**: Parses an HTML file containing a table, calculates the time delta for each row, and returns a reordered table.
    - **Parameters**: The file path of the HTML file, the indices for the date, start time, and end time columns.
    - **Returns**: An HTML string representing the reordered table.

## Usage

To use the `reorder_table()` function:

```python
final_table_html = reorder_table('timelogTable.html', 0, 1, 2)
with open('new.html', 'w') as f:
    f.write(final_table_html)
```

This example reads data from `timelogTable.html`, processes it, and writes the reordered table to `new.html`.

## Dependencies

- **BeautifulSoup**: Used for HTML parsing and processing.

## Note

Ensure that the provided HTML file follows the expected table structure mentioned above. Improperly formatted data may lead to unexpected results or errors.
