Name:       autotuned
Version:    0.5
Release:    1%{?dist}
Summary:    A simple auto script for tuned which set power mode for wifi adapters too
License:    GNU GPL3
URL:        https://www.thisistodo.org
#Sources
Source0:    autotuned.tar.xz
Source1:    README.md
#Requirements
Requires:   tuned
Requires:   bash
Requires:   iw
Requires:   systemd

#for systemctl and udev
Requires:       /usr/bin/systemctl
Requires:       /usr/bin/udevadm
Requires(post): /usr/sbin/iw
BuildArch:       noarch

%description
A simple auto script for tuned

%prep
%autosetup -n %{name}

%build
#We don't need to build anything here yet
%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/etc/udev/rules.d/
install -m 755 power.sh %{buildroot}/usr/bin/power
install -m 644 powersave.rules  %{buildroot}/etc/udev/rules.d/powersave.rules
install -m 644 power.service  %{buildroot}/etc/systemd/system/power.service
install -m 644 root-resume.service  %{buildroot}/etc/systemd/system/root-resume.service

%post
sed -i -e "s/@@WIFIDEV@@/$(/usr/sbin/iw dev | awk '$1=="Interface"{print $2}')/g" /usr/bin/power
systemctl daemon-reload
systemctl enable power.service
systemctl enable root-resume.service
systemctl start power.service
udevadm control --reload-rules

%preun
systemctl stop power.service
systemctl disable power.service
systemctl disable root-resume.service
 
%postun
systemctl daemon-reload
udevadm control --reload-rules
  
%files
%license LICENSE
%doc  AUTHORS 
/usr/bin/power
/etc/udev/rules.d/powersave.rules
/etc/systemd/system/power.service
/etc/systemd/system/root-resume.service

%changelog
* Thu Nov 01 2018 Akarshan Biswas <akarshan.biswas@gmail.com> - 0.5-1
- script now works on top of tuned

* Tue Jul 31 2018 Akarshan Biswas <akarshan.biswas@gmail.com> - 0.4-2
- Remove unsupported features and fix compatibility with intel cpus

* Wed Jun 20 2018 Akarshan Biswas <akarshan.biswas@gmail.com> - 0.3-1
- Set cpu on ac to be ondemand

* Tue Jun 5 2018 Akarshan Biswas <akarshan.biswas@gmail.com> - 0.2-4
- Set cpu on ac to be ondemand

* Thu May 10 2018 Akarshan Biswas <akarshan.biswas@gmail.com> - 0.2-3
- Fix wifi power saving mode

* Sat May 05 2018 Akarshan Biswas <akarshan.biswas@gmail.com>
- Initial release





