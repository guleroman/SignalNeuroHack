FROM python:3-onbuild
RUN pip3 install --upgrade pip
RUN git clone  https://github.com/guleroman/SimpleDecisionDataHack.git /APII

EXPOSE 3334

ENTRYPOINT ["python3", "app.py"]
