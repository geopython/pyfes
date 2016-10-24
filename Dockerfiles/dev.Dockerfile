FROM ricardogsilva/pyfes

RUN apk --no-cache add bash

COPY . .

RUN pip install --requirement requirements/dev.txt \
    && pip install --editable .