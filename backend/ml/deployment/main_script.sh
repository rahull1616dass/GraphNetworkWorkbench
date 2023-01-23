ssh vingilot -t "
  buildah bud --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ -t ${BACKEND_IMAGE_TAG} --layers -f ~/xtai_lab3/deployment/Dockerfile;
  buildah push --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ ${BACKEND_IMAGE_TAG}
  "