FROM manimcommunity/manim:stable
USER root
RUN wget https://mirror.ctan.org/systems/texlive/tlnet/update-tlmgr-latest.sh && sh update-tlmgr-latest.sh -- --upgrade
RUN tlmgr install noto
RUN tlmgr install collection-fontsextra
