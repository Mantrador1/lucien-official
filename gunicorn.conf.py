﻿# -*- coding: utf-8 -*-
import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "gthread"





