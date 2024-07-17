# Pro Actifs: Asset Management

## 📄 Description

💰 Discover an application dedicated to asset management, including features for savings simulation and mortgage calculation.

🤔 “How can I optimize my long-term savings?” or “What will my monthly repayments be for a mortgage?” These are questions many people ask. This application was developed to provide precise answers to these questions, offering detailed simulations and graphical visualizations.

This application allows you to analyze the evolution of savings with periodic contributions and interest rates, as well as calculate mortgage repayments, considering both principal and interest. It's an ideal tool for individuals and professionals looking to efficiently plan their personal finances.

👉 Access the app and start your analysis now at [coming soon].

![Image1](images/image1.png)

## Prerequisites
- Anaconda or Miniconda
- Docker (for Docker deployment)

## ⚒️ Installation

### Prerequisites
- Python 3.11
- Python libraries
    ```sh
    pip install -r requirements.txt
    ```

## 📝 Usage

### Running without Docker

1. **Clone the repository and navigate to the directory**
    ```bash
    git pull https://github.com/LudovicGardy/app_asset_management
    cd asset_management_repos/app_folder
    ```

2. **Environment setup**
    - Create and/or activate the virtual environment:
        ```bash
        conda create -n myenv python=3.11
        conda activate myenv
        ```
        or
        ```bash
        source .venv/bin/activate
        ```

3. **Launch the Streamlit App**
    - Run the Streamlit application:
        ```bash
        streamlit run main.py
        ```

### Running with Docker

1. **Prepare Docker environment**
    - Ensure Docker is installed and running on your system.

2. **Navigate to project directory**
    - For multiple containers:
        ```bash
        cd [path-to-app-folder-containing-docker-compose.yml]
        ```
    - For a single container:
        ```bash
        cd [path-to-app-folder-containing-Dockerfile]
        ```

3. **Build and start the containers**
    ```bash
    docker-compose up --build
    ```

    - The application will be accessible at `localhost:8501`.

    - ⚠️ If you encounter issues with `pymssql`, adjust its version in `requirements.txt` or remove it before building the Docker image.

## 👤 Author
- LinkedIn: [Ludovic Gardy](https://www.linkedin.com/in/ludovic-gardy/)
- Website: [https://www.sotisanalytics.com](https://www.sotisanalytics.com)
