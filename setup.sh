#wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip
#unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xvzf geckodriver-v0.26.0-linux64.tar.gz && sudo ln -s $PWD/geckodriver /usr/local/bin/geckodriver
