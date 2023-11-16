#!/bin/bash

# brew install nvsecurity/taps/nightvision
# brew update && brew upgrade nightvision
# nightvision login

rm openapi-spec.yml
rm .nightvision-scan.yml
NIGHTVISION_TARGET=http://127.0.0.1:5000
nightvision swagger-extract ./ -u ${NIGHTVISION_TARGET} --lang python
nightvision scan --api $NIGHTVISION_TARGET