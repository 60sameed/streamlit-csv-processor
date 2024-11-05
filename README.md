# Deployment Commands

1. Create conda environment
    ```sh
        conda create -n streamlit python=3.11
        conda activate streamlit
        pip install -r requirements.txt
    ```

2. Run streamlit app
    ```sh
        streamlit run main.py --server.address 0.0.0.0 --server.port 8501
    ```