import streamlit as st
import re
import pandas as pd
import io

# Set up the page layout
st.set_page_config(page_title="Ad Tag Text to Excel", page_icon="📊", layout="centered")

def extract_info(input_text):
    # Use regular expressions to extract relevant information
    tag_pattern = r'Tag \d+\. "(.*?)" \(Line Item: (.*?), Size: (.*?)\)'
    serving_method_pattern = r'Serving method: 3\'rd party standard javascript tag:\n(.*?)Banner preview:'
    
    tag_matches = re.findall(tag_pattern, input_text, re.DOTALL)
    serving_method_matches = re.findall(serving_method_pattern, input_text, re.DOTALL)

    # Adding a quick safety check in case the regex parsing mismatches
    min_len = min(len(tag_matches), len(serving_method_matches))
    if len(tag_matches) != len(serving_method_matches):
        st.warning(f"⚠️ Warning: Found {len(tag_matches)} tags but {len(serving_method_matches)} serving methods. Check your text file for formatting irregularities.")

    # Create a list of dictionaries containing extracted information
    result = []
    for i in range(min_len):
        creative_name = tag_matches[i][0]  # Extract the creative name
        size = tag_matches[i][2].split(', Type:')[0]  # Extract the size without the type
        script = serving_method_matches[i].strip()  # Extract the script and clean up whitespace
        
        # Create a dictionary with the extracted information
        tag_info = {
            "Creative name": creative_name,
            "Dimensions (width x height)": size,
            "Third-party tag": script,
            "Landing page URL": "",
            "Expanding direction": "",
            "Expands on hover": "",
            "Requires HTML5": "",
            "Requires MRAID": "",
            "Requires ping for attribution": "",
            "Integration code (Optional)": "",
            "Notes (Optional)": "",
        }
        result.append(tag_info)
    
    return result

def main():
    st.title("📊 Ad Tag Text to Excel Converter")
    st.write("Upload a `.txt` file containing your ad tags to extract them into a formatted Excel sheet.")

    uploaded_file = st.file_uploader("Upload Input File (.txt)", type=["txt"])

    if uploaded_file is not None:
        if st.button("Process File", type="primary"):
            with st.spinner("Extracting tags and generating Excel file..."):
                try:
                    # Read the uploaded file
                    input_text = uploaded_file.read().decode("utf-8")
                    
                    # Extract the information
                    extracted_info = extract_info(input_text)
                    
                    if not extracted_info:
                        st.error("No valid tags found. Please ensure the text matches the expected format.")
                        return

                    # Create a Pandas DataFrame
                    df = pd.DataFrame(extracted_info)
                    
                    # Show a quick preview in the browser (first 5 rows)
                    st.subheader("Data Preview")
                    st.dataframe(df.head())

                    # Save the DataFrame to an Excel file in memory
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False)
                    excel_buffer.seek(0)

                    st.success(f"Data successfully extracted! ({len(extracted_info)} tags processed)")
                    
                    # Provide the download button
                    st.download_button(
                        label="📥 Download Excel File",
                        data=excel_buffer.getvalue(),
                        file_name="processed_ad_tags.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                except Exception as e:
                    st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
