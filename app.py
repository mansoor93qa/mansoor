import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.set_page_config(page_title="Customer Dashboard", layout="wide")
st.title("📊 Customer Dashboard: Data Visualizer")

# Upload Dataset
uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data Uploaded Successfully")
    
    st.subheader("📋 Preview of Dataset")
    st.dataframe(df.head())

    # Column Selection
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Plotting Options
    st.sidebar.header("⚙️ Plot Settings")
    plot_type = st.sidebar.selectbox("Select Plot Type", [
        "Histogram", "Boxplot", "Scatterplot", "Lineplot", "Barplot"
    ])
    
    seaborn_styles = ['white', 'dark', 'whitegrid', 'darkgrid', 'ticks']
seaborn_style = st.sidebar.selectbox("Seaborn Style", seaborn_styles)
sns.set_style(seaborn_style)

    sns.set_style(seaborn_style)

    st.sidebar.markdown("### Select Columns")

    x_axis = st.sidebar.selectbox("X-Axis", options=df.columns)
    y_axis = st.sidebar.selectbox("Y-Axis", options=numeric_cols, index=0) if plot_type in ["Scatterplot", "Lineplot", "Boxplot", "Barplot"] else None

    # Plot generation
    st.subheader(f"📈 Generated Plot: {plot_type}")
    fig, ax = plt.subplots()

    try:
        if plot_type == "Histogram":
            sns.histplot(data=df, x=x_axis, ax=ax, kde=True)
        elif plot_type == "Boxplot":
            sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif plot_type == "Scatterplot":
            sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif plot_type == "Lineplot":
            sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif plot_type == "Barplot":
            sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
        st.pyplot(fig)

        # Download plot button
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Download Plot",
            data=buf.getvalue(),
            file_name=f"{plot_type.lower()}_plot.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"❌ Error generating plot: {e}")

else:
    st.info("📤 Please upload a CSV file to begin.")
