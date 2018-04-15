FROM debian:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y pypy curl unzip git
RUN curl -O https://pypi.python.org/packages/72/c2/c09362ab29338413ab687b47dab03bab4a792e2bbb727a1eb5e0a88e3b86/setuptools-39.0.1.zip && unzip setuptools-39.0.1.zip
RUN cd setuptools-39.0.1 && pypy bootstrap.py && pypy setup.py install
RUN cd ..
RUN curl https://pypi.python.org/packages/e0/69/983a8e47d3dfb51e1463c1e962b2ccd1d74ec4e236e232625e353d830ed2/pip-10.0.0.tar.gz | tar -zx
RUN cd pip-10.0.0 && pypy setup.py install
RUN cd ..
RUN curl https://pypi.python.org/packages/5d/c1/45947333669b31bc6b4933308dd07c2aa2fedcec0a95b14eedae993bd449/wheel-0.31.0.tar.gz | tar -zx
RUN cd wheel-0.31.0 && pypy setup.py install
RUN cd ..
RUN for f in easy_install easy_install-2.7 pip pip2 pip2.7; do mv /usr/local/bin/$f /usr/local/bin/pypy-$f; done
RUN pypy-pip install PyGLtools
RUN git clone https://github.com/billgreenwald/pgltools.git && mv pgltools /usr/local/bin/pgltools_files && ln -s /usr/local/bin/pgltools_files/sh/pgltools /usr/local/bin/pgltools
RUN rm -rf setuptools* pip-10.0.0 wheel-0.31.0 && apt-get clean
