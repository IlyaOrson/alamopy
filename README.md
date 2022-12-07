# Symbolic Regression Demo

## Instructions

Try to open the `demo.ipynb` jupyter notebook simply by following this link to Binder `-->`
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IlyaOrson/alamopy/HEAD?labpath=demo.ipynb)

This should open a functional jupyter interface in your browser (after a couple of minutes of setup) where you can work directly.

Unfortunately this free service does not always work reliably, in which case the alternative will be to setup Docker locally.
You have done this before in the [CFD coil optimization setup](https://github.com/OptiMaL-PSE-Lab/symbolic_regression/blob/main/ml_course_documentation-2.pdf), so the following steps should be familiar.

### Docker setup

This process has been set up for you as a way to run symbolic regression packages on your own computer without manually configure them.
Note that whilst this seems long winded: be patient, and read all the steps.
This is significantly easier than installing all the relevant libraries yourself.

1. Download and [install Docker](https://docs.docker.com/get-docker/) for your operating system.
2. In a terminal, and in the desired location, clone the Git repository.
`git clone https://github.com/IlyaOrson/alamopy.git`
If Git is not installed, download and [install Git first](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

3. Then enter the Git repository: ```cd alamopy```
4. Build the Docker image: ```docker build --no-cache -t symbolic_regression```.
5. Run the Docker image as a container. This will also enable all the output files to be shared with your host machine.
- If you are on Mac or Linux run the following command:
`docker run -v $(pwd)/:/root/symbolic_regression/ -it -p 8888:8888 symbolic_regression`
- If you are in the Windows terminal run the following command:
`docker run -v /cd/:/root/symbolic_regression/ -it -p 8888:8888 symbolic_regression`
6. You should now be within the Docker container and should see something ending in #. Here enter the
following command to start a Jupyter notebook.
 `jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root`
7. The terminal will then prompt you with ```To access the notebook, open this file in a browser:
file:///root/.local/share/jupyter/runtime/nbserver-640-open.html
Or copy and paste one of these URLs:
http://41b527251408:8888/?token=044321e3fdb7493b611b493d...
or http://127.0.0.1:8888/?token=044321e3fdb7493b611b493d80d23...```
You can copy and paste any of these urls into your browser.
(*Note these URLs are just examples and they will not work for your machine*).
8. In your browser you should now see the jupyter notebook interface, where you can open the `demo.ipynb` and work your way through it.
