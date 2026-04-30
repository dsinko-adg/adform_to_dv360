import streamlit as st
import re
import pandas as pd
import io

# Set up the page layout
st.set_page_config(page_title="Adform to DV360 Converter", page_icon="📊", layout="centered")

def process_excel(uploaded_file):
    # Read the Excel file, assuming row 8 contains headers (index 7 in pandas)
    df_input = pd.read_excel(uploaded_file, header=7)
    
    # Check if required columns exist to avoid cryptic KeyError
    required_cols = ['Ad name', 'Dimensions', 'Script', 'Destination URL']
    missing_cols = [col for col in required_cols if col not in df_input.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns in row 8: {', '.join(missing_cols)}. Please check the Adform export format.")

    # Map Adform columns to DV360 Bulk Import structure
    df_output = pd.DataFrame({
        "Creative name": df_input['Ad name'],
        "Dimensions (width x height)": df_input['Dimensions'],
        "Third-party tag": df_input['Script'],
        "Landing page URL": df_input['Destination URL'],
        "Expanding direction": "",
        "Expands on hover": "",
        "Requires HTML5": "",
        "Requires MRAID": "",
        "Requires ping for attribution": "",
        "Integration code (Optional)": "",
        "Notes (Optional)": ""
    })

    # Drop any empty rows (where Creative name is missing)
    df_output = df_output.dropna(subset=['Creative name'])
    
    return df_output

def main():
    st.title("📊 Adform to DV360 Bulk Converter")
    st.write("Upload your Adform export `.xlsx` file to convert it into a DV360 bulk import format.")

    # Change file uploader to accept Excel files
    uploaded_file = st.file_uploader("Upload Adform Excel File (.xlsx)", type=["xlsx", "xls"])

    if uploaded_file is not None:
        if st.button("Process File", type="primary"):
            with st.spinner("Reading Adform export and generating DV360 file..."):
                try:
                    # Process the Excel file
                    df = process_excel(uploaded_file)
                    
                    # Show a quick preview in the browser (first 5 rows)
                    st.subheader("Data Preview")
                    st.dataframe(df.head())

                    # Save the DataFrame to an Excel file in memory
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False)
                    excel_buffer.seek(0)

                    st.success(f"Data successfully converted! ({len(df)} tags processed)")
                    
                    # Provide the download button
                    st.download_button(
                        label="📥 Download DV360 Bulk File",
                        data=excel_buffer.getvalue(),
                        file_name="dv360_bulk_import.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                except Exception as e:
                    st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
