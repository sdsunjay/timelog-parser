import sys

from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def time_delta(row, date_column, start_time_column, end_time_column):
    """
    Calculate the time delta between start_time and end_time on a given date.

    Parameters:
    - row (list): A list representing a row of data, containing date and time info.
    - date_column (int): The index of the date in the list x.
    - start_time_column (int): The index of the start time in the list x.
    - end_time_column (int): The index of the end time in the list x.

    Returns:
    - timedelta: The time difference in minutes between start_time and end_time.
    """
    try:
        date_str = row[date_column]
        start_time_str = row[start_time_column]
        end_time_str = row[end_time_column]
        start_time = datetime.strptime(f"{date_str} {start_time_str}", '%m/%d/%y %H:%M')
        end_time = datetime.strptime(f"{date_str} {end_time_str}", '%m/%d/%y %H:%M')

        if end_time < start_time:
            end_time += timedelta(days=1)

        # Calculate the time difference in minutes
        delta_minutes = (end_time - start_time).total_seconds() / 60
        return int(delta_minutes)

    except Exception as e:
        print(f"Error parsing time data: {e}")
        return -1

def create_final_table(table:list) -> str:
    """
    Convert a list of lists into an HTML table string.

    Parameters:
    - table (list): A list of lists where each inner list represents a row of data.

    Returns:
    - str: An HTML string representation of the table.
    """
    # Create an empty table
    table_html = []
    table_html.append("<table>\n<tbody>\n")
    # table_html = BeautifulSoup('<table><tbody></tbody></table>', 'html5lib')
    # Iterate through the table list and add each row to the table
    for row in table:
        row_html = '\n\t'.join([f'<td>{cell}</td>' for cell in row])
        table_html.append(f"<tr>\n{row_html}\n</tr>\n")
    table_html.append("\n</tbody>\n</table>\n")
    # Get the final html
    return  str('\n'.join(table_html))

def sort_key(row: list, date_column: int, hour_column: int) -> datetime:
    """
    Construct a datetime object from the provided data based on specified columns.

    Parameters:
    - row (list): A list representing a row of data.
    - date_column (int): Index of the column containing the date.
    - hour_column (int): Index of the column containing the time.

    Returns:
    - datetime: A datetime object constructed from the date and time columns.
    """
    dt_string = f"{row[date_column]} {row[hour_column]}"
    return datetime.strptime(dt_string, '%m/%d/%y %H:%M')

def process_html(soup: BeautifulSoup) -> list:
    """
    Extract table data from the provided BeautifulSoup object.

    Parameters:
    - soup (BeautifulSoup): The parsed HTML content using BeautifulSoup.

    Returns:
    - list: A list of lists containing the extracted table data.
    """
    table = []
    # Process each <tr> element in the parsed HTML
    all_rows = soup.find_all('tr')
    for row in all_rows:
        cells = row.find_all(['th', 'td'])
        cell_content = [cell.get_text(strip=True) for cell in cells]
        row.clear()
        table.append(cell_content)
    return table

def reorder_table(file_name, date_column, start_time_column, end_time_column):
    """
    Parse an HTML file to extract tabular data, and calculate the time delta for each row.

    Parameters:
    - file_name (str): The path to the HTML file containing the table.
    - date_column (int): The index of the date column in the table.
    - start_time_column (int): The index of the start time column in the table.
    - end_time_column (int): The index of the end time column in the table.

    Returns:
    - list: A list of rows from the table, each row being a list of cell contents.
    - list: A list of headers from the table.
    - list: A list of calculated time deltas for each row.
    """
    return_boolean, original_table_html = extract_table_from_html(file_name)
    if not return_boolean:
        print(original_table_html)
        return ""

    soup = BeautifulSoup(original_table_html, 'html5lib')
    # remove the first row which are the headers
    table = process_html(soup)
    headers = table.pop(0)

    new_table = []

    for item in table:
        time_delta_in_minutes = time_delta(item, 0, 1, 2)
        if time_delta_in_minutes == -1:
            return ""
        new_table.append(item)
        if item[5] == "xx" or int(item[5]) != int(time_delta_in_minutes):
            print("{} {} {}".format(item[0], item[5], time_delta_in_minutes))
            item[5] = int(time_delta_in_minutes)
    # sort the data according to the selected column and reverse the order
    sorted_table = sorted(new_table, key=lambda x: sort_key(x, 0, 1), reverse=True)

    # add headers again
    sorted_table.insert(0, headers)
    # Reorder the rows of the table
    # table_html.tbody.clear()
    # for row in table:
    #    table_html.tbody.append(BeautifulSoup(f'<tr>{"".join(["<td>{cell}</td>" for cell in row])}</tr>', 'html.parser'))
    return create_final_table(sorted_table)

# Function to check if the file is an HTML file
def is_html_file(filename):
    return filename.endswith('.html') or filename.endswith('.htm')

def extract_table_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    start = content.find('<table')
    end = content.find('</table>', start)

    if start != -1 and end != -1:
        table_content = content[start:end + 8]  # 8 is the length of '</table>'
        return True, table_content
    else:
        return False, "Table tag not found."


if len(sys.argv) > 1:
    input_file = sys.argv[1]
    if is_html_file(input_file):
        # Main part of your script
        final_table_html = reorder_table(file_name=input_file, date_column=0, start_time_column=1, end_time_column=2)
        with open('new_timelog.html', 'w') as f:
            f.write(final_table_html)
    else:
        print(f"Error: The file '{input_file}' is not an HTML file.")
else:
    print("Error: No input file name provided.")
