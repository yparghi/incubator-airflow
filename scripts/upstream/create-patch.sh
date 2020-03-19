mkdir -p ./patches
git format-patch ${UPSTREAM_BRANCH}..${ORIGIN_BRANCH} --binary --stdout > ./patches/${UPSTREAM_BRANCH}-${ORIGIN_BRANCH}.patch
