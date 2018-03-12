FROM centos:7.3.1611

#Enable the extras Repo
RUN yum -y install epel-release && \
    rm  -rf rm /var/log/lastlog

#Packages
RUN yum -y install audit-libs-devel.x86 \
                   autoconf.noarch \
                   automake \
                   bc \
                   e2fsprogs-devel \
                   e2fsprogs-devel.i686 \
                   file \
                   gcc.x86_64 \
                   gettext \
                   git.x86_64 \
                   krb5-devel \
                   krb5-devel.i686 \
                   lksctp-tools-devel \
                   libedit-devel.x86_64 \
                   make.x86_64 \
                   openldap-devel.x86_64 \
                   openldap-devel.i686 \
                   pam-devel.x86_64 \
                   pam-devel.i686 \
                   patch.x86_64 \
                   prelink.x86_64 \
                   python \
                   python-pip \
                   rpm-build \
                   rpm-sign \
                   ruby \
                   ruby-devel \
                   rubygems \
                   sudo \
                   tcp_wrappers-devel \
                   vim \
                   wget.x86_64 \
                   zlib.x86_64 \
                   zlib-devel.x86_64 \
                   zlib-devel.i686 && \
    rm  -rf rm /var/log/lastlog

RUN yum -y install glibc-devel.i686 \
                   libgcc.i686 \
                   zlib-devel.i686 && \
    rm  -rf rm /var/log/lastlog
#RUN yum -y install CUnit CUnit-devel
#installing the centos 6 CUnit packages because Centos 7 doesn't have i686 version
RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/Packages/c/CUnit-2.1.2-6.el6.i686.rpm
RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/Packages/c/CUnit-devel-2.1.2-6.el6.i686.rpm
RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/Packages/c/CUnit-2.1.2-6.el6.x86_64.rpm
RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/Packages/c/CUnit-devel-2.1.2-6.el6.x86_64.rpm
RUN yum localinstall -y CUnit*
#Fix locale info
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

#Python modules needed
RUN pip install pexpect
#Sudoers for wheel
COPY wheel-sudoers /etc/sudoers.d/

#Add non-root user and set it as default user/workdir
RUN groupadd -g 600 testuser
RUN useradd -s /bin/bash -G adm,wheel,systemd-journal -g testuser -u 600 -m testuser
WORKDIR /home/testuser/rpmbuild


#RPM macros
#COPY rpmmacros.template /tmp/
#RUN chmod 444 /tmp/rpmmacros.template

COPY . /home/testuser/rpmbuild/
RUN chown -R testuser:testuser /home/testuser/rpmbuild
#RUN chmod -R 755 /home/testuser/rpmbuild/scripts/*

#Entry point file
#ENTRYPOINT ["/home/testuser/rpmbuild/scripts/entrypoint.sh"]

#USER testuser
