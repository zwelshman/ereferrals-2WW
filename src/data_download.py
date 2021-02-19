import base64
def get_table_download_link(df, table):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe, table name
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV of {table}</a>'
    return href