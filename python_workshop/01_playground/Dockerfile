FROM python:3.13-slim-trixie

# Set the working directory to /app
WORKDIR /app

COPY . .

# Install Jupyter Notebook
RUN pip install jupyter

# Make port 8888 available to the world outside this container
EXPOSE 9999

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=9999", "--no-browser", "--allow-root"]
