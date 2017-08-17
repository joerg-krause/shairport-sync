Name:           shairport-sync
Version:        3.1
Release:        1%{?dist}
Summary:        AirTunes emulator. Shairport Sync adds multi-room capability with Audio Synchronisation.
# For a breakdown of the licensing, see LICENSES file
License:        MIT and BSD
URL:            https://github.com/mikebrady/shairport-sync
Source0:        https://github.com/mikebrady/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

%{?systemd_requires}
BuildRequires:  systemd
BuildRequires:  pkgconfig(libconfig)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libdaemon)
BuildRequires:  pkgconfig(avahi-core)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(soxr)
BuildRequires:  autoconf
BuildRequires:  automake

%description
Shairport Sync emulates an AirPort Express for the purpose of streaming audio
 from iTunes, iPods, iPhones, iPads and AppleTVs. Audio played by a Shairport
 Sync-powered device stays synchronised with the source and hence with similar
 devices playing the same source. Thus, for example, synchronised multi-room
 audio is possible without difficulty. (Hence the name Shairport Sync, BTW.)

Shairport Sync does not support AirPlay video or photo streaming.

%prep
%setup -q

%build
autoreconf -i -f
%configure --with-avahi --with-alsa --with-ssl=openssl --with-soxr
%make_build

%install
%make_install
rm %{buildroot}/etc/shairport-sync.conf.sample
install -p -m644 -D scripts/shairport-sync.service %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group %{name} &>/dev/null || groupadd --system %{name} >/dev/null
getent passwd %{name} &> /dev/null || useradd --system -c "%{name} User" \
        -d %{_localstatedir}/%{name} -m -g %{name} -s /sbin/nologin \
        -G audio %{name} >/dev/null

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%config /etc/shairport-sync.conf
/usr/bin/shairport-sync
/usr/share/man/man7/shairport-sync.7.gz
%{_unitdir}/%{name}.service
%doc README.md RELEASENOTES.md TROUBLESHOOTING.md
%license LICENSES

%changelog
* Thu Aug 17 2017 Bill Peck <bpeck@redhat.com> 3.1
- new backend offering synchronised PulseAudio support. 
- new optional loudness and convolution filters
- improvements in non-synchronised backends
- enhancements, stability improvements and bug fixes
* Fri Feb 24 2017 Mike Brady <mikebrady@eircom.net> 2.8.6
- Many changes including 8- 16- 24- and 32-bit output
* Fri Oct 21 2016 Mike Brady <mikebrady@eircom.net> 2.8.6
- Advertise self as ShairportSync rather than AirPort device 2.8.6
* Sun Sep 25 2016 Mike Brady <mikebrady@eircom.net> 2.8.5
- Bug fixes and small enhancements 2.8.5
* Sat May 28 2016 Mike Brady <mikebrady@eircom.net> 2.8.4
- Bug fixes and a few small enhancements 2.8.4
* Fri Apr 15 2016 Mike Brady <mikebrady@eircom.net> 2.8.2
- Stability improvements, bug fixes and a few special-purpose settings 2.8.2
* Wed Mar 02 2016 Mike Brady <mikebrady@eircom.net> 2.8.1
- Stability improvements and important bug fixes 2.8.1
* Sat Jan 30 2016 Mike Brady <mikebrady@eircom.net> 2.8.0
- Enhancements and bug fixes 2.8.0
* Sun Oct 18 2015 Mike Brady <mikebrady@eircom.net> 2.6
- Important enhancements and bug fixes 2.6
* Thu Aug 27 2015 Mike Brady <mikebrady@eircom.net> 2.4.1
- Minor bug fixes 2.4.1
* Thu Aug 27 2015 Mike Brady <mikebrady@eircom.net> 2.4
- Prepare for stable release 2.4
* Wed Aug 26 2015 Mike Brady <mikebrady@eircom.net> 2.3.13.1-1
- Harmonise release numbers
* Fri Jul 24 2015 Bill Peck <bill@pecknet.com> 2.3.7-1
- Initial spec file
