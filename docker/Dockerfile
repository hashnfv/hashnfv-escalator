FROM centos:7
LABEL escalator_image_version=1.0
ARG BRANCH
ENV BRANCH=${BRANCH:-master}
RUN yum -y update
RUN yum -y install centos-release-openstack-newton
RUN yum -y install \
  wget \
  coreutils \
  which \
  gawk \
  grep \
  git \
  intltool \
  make \
  rpm \
  rpm-build \
  python-sphinx \
  python2-oslo-sphinx \
  python2-oslo-messaging \
  python2-oslo-concurrency \
  python2-oslo-sphinx \
  python-devel \
  python-d2to1 \
  python-django-compressor \
  python-django-openstack-auth \
  python-django-pyscss \
  python-lesscpy \
  python-migrate \
  python-pint \
  python-routes
