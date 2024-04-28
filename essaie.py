import streamlit as st

# Define the details for each bus line
bus_lines = [
    {"name": "Bus Line 1", "logo_path": "line_logo/1.png", "details": "Details for Bus Line 1..."},
    {"name": "Bus Line 2", "logo_path": "line_logo/1.png", "details": "Details for Bus Line 2..."},
    # Add details for other bus lines here
]

def main():
    st.title("Bus Line Gallery")

    # Display a gallery for all bus lines
    num_columns = 3  # Number of columns to display
    col_width = 1 / num_columns  # Column width

    for i in range(0, len(bus_lines), num_columns):
        row = bus_lines[i:i + num_columns]
        cols = st.columns(num_columns)
        for col, line in zip(cols, row):
            col.write(f"## {line['name']}")
            logo_clicked = col.image(line["logo_path"], use_column_width=True, caption=f"Click logo to see details")
            if logo_clicked:
                col.write(f"Details for {line['name']}:")
                col.write(line["details"])

if __name__ == "__main__":
    main()
