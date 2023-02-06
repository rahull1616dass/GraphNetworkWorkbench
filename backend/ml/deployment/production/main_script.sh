ssh vingilot -t "
  cd ~xtai_lab3/deployment && buildah bud --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ -t ${BACKEND_IMAGE_TAG} --layers .;
  buildah push --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ ${BACKEND_IMAGE_TAG};
  kubectl -n ${VINGILOT_USER} create -f ~/xtai_lab3/deployment/kubernates.yaml
  "