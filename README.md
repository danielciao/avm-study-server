# Flask Server

### Setup virtual environment

**Anaconda**

- conda create --name avm-server python=3.9 pip
- conda install --force-reinstall -y -q --name avm-server -c conda-forge --file requirements.txt
- conda activate avm-server
- conda deactivate
- conda env remove -n avm-server

**Install dependencies individually**

```bash
pip install boto3 fastparquet flasgger flask flask-cors gunicorn joblib openpyxl pandas python-dotenv scikit-learn scipy
```

### Start up server

At the server directory, run the following command:

```bash
flask run
```

Server will be running at localhost:3001. Swagger UI will be available at localhost:3001/apidocs/.
