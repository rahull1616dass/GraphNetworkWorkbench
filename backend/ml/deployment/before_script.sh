mkdir -p ~/.ssh
echo "${VINGILOT_PRIVATE_KEY}" > ~/.ssh/uni_wuerzburg_cluster
chmod 600 ~/.ssh/uni_wuerzburg_cluster
echo "${VINGILOT_PUBLIC_KEY}" > ~/.ssh/uni_wuerzburg_cluster.pub
chmod 644 ~/.ssh/uni_wuerzburg_cluster.pub
echo -e "Host login6 \n\t Hostname login6.informatik.uni-wuerzburg.de \n\t StrictHostKeyChecking no \n\t User ${VINGILOT_USER} \n\t LogLevel ERROR \n\t IdentityFile ~/.ssh/uni_wuerzburg_cluster" > ~/.ssh/config
echo -e "Host vingilot \n\t Hostname vingilot.informatik.uni-wuerzburg.de \n\t StrictHostKeyChecking no \n\t User ${VINGILOT_USER} \n\t ProxyCommand ssh login6 nc %h %p \n\t LogLevel ERROR \n\t IdentityFile ~/.ssh/uni_wuerzburg_cluster" >> ~/.ssh/config
chmod 600 ~/.ssh/config
ssh vingilot -t "mkdir -p ./xtai_lab3/deployment; cd ./xtai_lab3/deployment && if test -f ./kubernates.yaml; then kubectl -n ${VINGILOT_USER} delete -f ./kubernates.yaml; fi"
scp ./backend/ml/deployment/Dockerfile ./backend/ml/deployment/kubernates.yaml vingilot:./xtai_lab3/deployment
scp -r ./backend/ml/src vingilot:./xtai_lab3/application