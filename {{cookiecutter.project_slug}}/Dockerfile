FROM python:3

ARG USER_NAME=app
ARG HOME_DIR=/home/${USER_NAME}
ARG APP_DIR=/home/${USER_NAME}/src
ARG ASSETS_DIR=/home/${USER_NAME}/assets
ARG SECRET_KEY=SUPERSECRET
ARG ENTRYPOINT=${APP_DIR}/scripts/init-server.sh

ENV PATH=${HOME_DIR}/.local/bin:$PATH
ENV SECRET_KEY=${SECRET_KEY}
ENV ENTRYPOINT=${ENTRYPOINT}

RUN python -m pip install --upgrade pip-tools pip
RUN useradd nginx -u 1005
RUN useradd -m -d ${HOME_DIR} ${USER_NAME} -u 1001 -G 1005

RUN mkdir -p ${APP_DIR}
RUN mkdir -p ${ASSETS_DIR}
RUN chown ${USER_NAME} -R ${APP_DIR}
RUN chown nginx -R ${ASSETS_DIR}
RUN chmod 770 -R ${ASSETS_DIR}

WORKDIR ${APP_DIR}
USER ${USER_NAME}

COPY --chown=${USER_NAME}:${USER_NAME} requirements/dev.txt ${APP_DIR}/requirements.txt
RUN python -m pip install -r ${APP_DIR}/requirements.txt

COPY --chown=${USER_NAME}:${USER_NAME} . ${APP_DIR}

RUN DATABASE_URL=sqlite:///tmp/test.db DEV=True python manage.py test -n

EXPOSE 8080

ENTRYPOINT "${ENTRYPOINT}"
