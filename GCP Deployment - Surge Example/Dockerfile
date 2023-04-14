FROM python:3.9.2
WORKDIR /

COPY trainer /trainer

RUN pip install --upgrade pip
RUN pip install scikit-learn gcsfs numpy matplotlib google-cloud-storage joblib TensorFlow
#RUN pip install -r  trainer/requirements.txt
RUN pip install pandas
RUN pip list

# create virtual environment
#RUN python -m venv myenv
#ENV PATH="/myenv/bin:$PATH"

# install dependencies inside virtual environment
#RUN pip install -r /requirements.txt
RUN . /usr/local/bin
CMD ["python", "/trainer/task.py" ]