#!/bin/bash/env python3

from sqlalchemy import create_engine

import config
import models

if __name__ == '__main__':
    engine = create_engine(config.DB_URI)
    models.Base.metadata.create_all(engine)
