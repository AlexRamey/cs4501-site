FROM tp33/django

RUN pip install --upgrade pip && pip install selenium && apt-get update && apt-get install -y --no-install-recommends libfontconfig

COPY phantomjs /usr/local/bin/phantomjs.exe

RUN mv /usr/local/bin/phantomjs.exe /usr/local/bin/phantomjs
