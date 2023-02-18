ssh vingilot -t "
  cd /home/stud/tarasov/xtai_lab3/deployment.new && buildah bud --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ -t ${BACKEND_IMAGE_TAG} --layers .;
  buildah push --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ ${BACKEND_IMAGE_TAG};
  if test -f /home/stud/tarasov/xtai_lab3/deployment/kubernates.yaml; then kubectl -n ${VINGILOT_USER} delete -f /home/stud/tarasov/xtai_lab3/deployment/kubernates.yaml --all; rm -rf /home/stud/tarasov/xtai_lab3/deployment; fi;
  mv /home/stud/tarasov/xtai_lab3/deployment.new /home/stud/tarasov/xtai_lab3/deployment
  if test -d /home/stud/tarasov/xtai_lab3/application; then rm -rf /home/stud/tarasov/xtai_lab3/application; fi;
  mv /home/stud/tarasov/xtai_lab3/application.new /home/stud/tarasov/xtai_lab3/application
  kubectl -n ${VINGILOT_USER} create -f /home/stud/tarasov/xtai_lab3/deployment/kubernates.yaml
"