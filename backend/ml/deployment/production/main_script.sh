ssh vingilot -t "
  cd /home/stud/tarasov/xtai_lab3/deployment.new && buildah bud --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ -t ${BACKEND_IMAGE_TAG} --layers . && cd /home/stud/tarasov;
  buildah push --runroot /tmp/${VINGILOT_USER}/.local/share/containers/runroot --root /tmp/${VINGILOT_USER}/.local/share/containers/storage/ ${BACKEND_IMAGE_TAG};
  if test -d /home/stud/tarasov/xtai_lab3/deployment/kubernates; then kubectl -n ${VINGILOT_USER} delete -f /home/stud/tarasov/xtai_lab3/deployment/kubernates -R --all; rm -rf /home/stud/tarasov/xtai_lab3/deployment; fi;
  mv /home/stud/tarasov/xtai_lab3/deployment.new /home/stud/tarasov/xtai_lab3/deployment;
  if test -d /home/stud/tarasov/xtai_lab3/application; then rm -rf /home/stud/tarasov/xtai_lab3/application; fi;
  mv /home/stud/tarasov/xtai_lab3/application.new /home/stud/tarasov/xtai_lab3/application;
  sleep 5;
  echo '
  CHATGPT_API_KEY=${CHAT_GPT_API_KEY}
  EXPERT_MODEL=${EXPERT_MODEL}
  ' > /home/stud/tarasov/xtai_lab3/application/.env;
  mkdir -p /home/stud/tarasov/xtai_lab3/redis_data;
  kubectl -n ${VINGILOT_USER} create -f /home/stud/tarasov/xtai_lab3/deployment/kubernates.yaml;
"