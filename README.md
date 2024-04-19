# Deployment Commands

1. Create conda environment
    ```sh
        conda create -f environment.yml
    ```

2. Run streamlit app
    ```sh
        streamlit run statsupload.py --server.address 192.168.0.58 --server.port 8501
    ```