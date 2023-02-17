ssh vingilot -t "
  cd ~/xtai_lab3/deployment.new && buildah bud --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ -t ${BACKEND_IMAGE_TAG} --layers .;
  buildah push --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ ${BACKEND_IMAGE_TAG};
  if test -f ~/xtai_lab3/deployment/kubernates.yaml; then kubectl -n ${VINGILOT_USER} delete ~/xtai_lab3/deployment/kubernates.yaml --all; rm -rf ~/xtai_lab3/deployment; fi;
  mv ~/xtai_lab3/deployment.new ~/xtai_lab3/deployment
  if test -d ./xtai_lab3/application; then rm -rf ./xtai_lab3/application; fi;
  mv ./xtai_lab3/application.new ./xtai_lab3/application
  kubectl -n ${VINGILOT_USER} create -f ~/xtai_lab3/deployment/kubernates.yaml
"