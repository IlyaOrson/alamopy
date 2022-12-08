# Symbolic Regression Demo

## Instructions

Try to open the `demo.ipynb` jupyter notebook simply by following this link to Binder --->
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IlyaOrson/alamopy/HEAD?labpath=demo.ipynb)

This should open a functional jupyter interface in your browser (after a couple of minutes of setup) where you can work directly. **If this works you can ignore the rest of the instructions**.

Unfortunately this free service does not always work reliably, in which case the alternative will be to setup Docker locally.
You have done this before in the [CFD coil optimization setup](https://github.com/OptiMaL-PSE-Lab/symbolic_regression/blob/main/ml_course_documentation-2.pdf), so the following steps should be familiar.

### Docker setup

This process has been set up for you as a way to run symbolic regression packages on your own computer without you needing to manually set them up.
Whilst this seems long winded please be patient and read all the steps.
This is significantly easier than installing all the relevant libraries yourself.

- If you use Mac, [install the Docker Desktop app form Mac](https://docs.docker.com/desktop/install/mac-install/) and move to step 1 below.
- If you use Windows, you need to [Docker Desktop with the wsl backend](https://learn.microsoft.com/en-us/virtualization/windowscontainers/quick-start/quick-start-windows-10-linux) to run docker with a Linux backend. After the example in that link works you can move on to step 1 below.
- If you use Linux, [install Docker for your Linux distro](https://docs.docker.com/desktop/install/linux-install/), start the docker daemon in a terminal with `sudo dockerd`, keep that terminal open, and follow the instructions in another wsl terminal. This also works in WSL2 terminal.

1. Run the Docker image we prepared for the session as a container:
```
docker run -it -p 8888:8888 ilyaorson/symbolic_regression:latest python3 -m jupyter lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```
2. The terminal will then prompt you with the message below. Open the last url with your browser. (*Note these URLs are just examples and they will not work on your machine*).
```
[... ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[... ServerApp]

    To access the server, open this file in a browser:
        file:///home/ic/.local/share/jupyter/runtime/jpserver-1-open.html
    Or copy and paste one of these URLs:
        http://a313d60c6774:8888/lab?token=85a7920a5fd5accf9fef25038ea56669f9bd3fdd4466b0b2
     or http://127.0.0.1:8888/lab?token=85a7920a5fd5accf9fef25038ea56669f9bd3fdd4466b0b2
```
3. In your browser you should now see the jupyter notebook interface, where you can open the `demo.ipynb` and work your way through it. (Do not close the terminal while working on the notebook)
