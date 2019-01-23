mkdir -p ./patches
git diff ${UPSTREAM_BRANCH}..${ORIGIN_BRANCH} --binary > ./patches/${UPSTREAM_BRANCH}-${ORIGIN_BRANCH}.patch
