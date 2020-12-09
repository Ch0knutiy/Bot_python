FROM rasa/rasa:latest-full

WORKDIR /app
USER root
RUN pip install pymorphy2
RUN pip install --upgrade spacy==2.1.9
USER 1001

EXPOSE 5005
ENTRYPOINT [ "rasa" ]
CMD ["--help" ]
