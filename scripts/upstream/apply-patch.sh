#!/usr/bin/env bash
git am -3 --ignore-whitespace < ./patches/${UPSTREAM_BRANCH}-${ORIGIN_BRANCH}.patch
