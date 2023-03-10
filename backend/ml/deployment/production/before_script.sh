apt update && apt install openssh-client rsync -y
mkdir -p ~/.ssh
echo "${VINGILOT_PRIVATE_KEY}" > ~/.ssh/uni_wuerzburg_cluster
chmod 600 ~/.ssh/uni_wuerzburg_cluster
echo "${VINGILOT_PUBLIC_KEY}" > ~/.ssh/uni_wuerzburg_cluster.pub
chmod 644 ~/.ssh/uni_wuerzburg_cluster.pub
echo -e "
  Host login6 \n\t
    Hostname login6.informatik.uni-wuerzburg.de \n\t
    StrictHostKeyChecking no \n\t
    User ${VINGILOT_USER} \n\t
    LogLevel ERROR \n\t
    IdentityFile ~/.ssh/uni_wuerzburg_cluster \n\n

  Host vingilot \n\t
    Hostname vingilot.informatik.uni-wuerzburg.de \n\t
    StrictHostKeyChecking no \n\t
    User ${VINGILOT_USER} \n\t
    ProxyCommand ssh login6 nc %h %p \n\t
    LogLevel ERROR \n\t
    IdentityFile ~/.ssh/uni_wuerzburg_cluster
" > ~/.ssh/config
chmod 600 ~/.ssh/config
ssh vingilot -t "
  if test -d /home/stud/tarasov/xtai_lab3/deployment.new; then rm -rf /home/stud/tarasov/xtai_lab3/deployment.new/*; fi;
  mkdir -p /home/stud/tarasov/xtai_lab3/deployment.new;
  if test -d /home/stud/tarasov/xtai_lab3/application.new; then rm -rf /home/stud/tarasov/xtai_lab3/application.new/*; fi;
  mkdir -p /home/stud/tarasov/xtai_lab3/application.new;
"
rsync -av backend/ml/deployment/production/* --exclude '*.sh' vingilot:/home/stud/tarasov/xtai_lab3/deployment.new
rsync -av backend/ml/requirements.* vingilot:/home/stud/tarasov/xtai_lab3/deployment.new
rsync -av --exclude docs --exclude README.md --exclude test --exclude deployment --exclude requirements.* backend/ml/* vingilot:/home/stud/tarasov/xtai_lab3/application.new