FROM python:3.13-alpine AS patcher

WORKDIR /work

COPY patches/apply_patches.py patches/offline-video.html /work/patches/
COPY site/original /work/site/original
COPY vendor/tdesign-icons-0.3.1.js /work/vendor/

RUN python /work/patches/apply_patches.py \
    --source /work/site/original/hub.gravastar.com \
    --output /work/site/patched/hub.gravastar.com \
    --vendor-script /work/vendor/tdesign-icons-0.3.1.js \
    --offline-video-template /work/patches/offline-video.html

FROM nginx:1.27-alpine

COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=patcher /work/site/patched/hub.gravastar.com /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/gravastar/connect || exit 1
