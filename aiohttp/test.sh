#!/usr/bin/env bash

#wrk -c100 -t1 -d5s http://127.0.0.1:8080/test

#wrk -c100 -t1 -d15s --latency http://127.0.0.1:8080/test_basic_db

wrk -c100 -t1 -d15s --latency http://127.0.0.1:8080/test_medium_db
