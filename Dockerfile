# FROM jupyter/minimal-notebook:latest
FROM mcranmer/pysr:latest

RUN wget -q https://minlp.com/downloads/xecs/alamo/current/alamo-linux64.zip
RUN unzip -q alamo-linux64.zip
RUN wget -q https://gist.githubusercontent.com/IlyaOrson/cce96e9bfd440de1da7dbde5f1ac50c2/raw/e0478c5fc9f16dc786322e568cdada0611097138/alamolice.txt
RUN mv alamolice.txt alamo-linux64/
ADD https://api.github.com/repos/IlyaOrson/alamopy/git/ref/heads/main /.git-hashref
RUN git clone https://github.com/IlyaOrson/alamopy.git
RUN pip install --upgrade pip
RUN pip install --no-cache-dir simpy numpy matplotlib jupyterlab

WORKDIR /home/io/alamopy/

CMD python3 -m jupyter lab example.ipynb --ip 0.0.0.0 --port 8888 --no-browser --allow-root
