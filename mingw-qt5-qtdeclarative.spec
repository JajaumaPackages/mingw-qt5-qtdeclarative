%?mingw_package_header

# Override the __debug_install_post argument as this package
# contains both native as well as cross compiled binaries
%global __debug_install_post %%{mingw_debug_install_post}; %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%%{?buildsubdir}" %{nil}

%global qt_module qtdeclarative
#%%global pre rc1

#%%global snapshot_date 20121111
#%%global snapshot_rev dd1d6b56

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        2%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtDeclarative component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://qt-project.org/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

# Make sure the QmlDevTools library is built as
# a shared library instead of a static library
Patch0:         qt5-build-qmldevtools-as-shared-library.patch

# QTBUG-51071 - Workaround to fix static builds
Patch1:         qt5-qtdeclarative-workaround-qtbug-50306.patch

# Make sure qmldevtools link against the system zlib
Patch2:         qt5-qtdeclarative-workaround-crashes-in-qtqml-code-related-to-dead-store-elimination.patch

# QTBUG-55482 - Workaround fixing crashes in QML
Patch3:         qt5-qtdeclarative-link-system-zlib.patch

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-qt5-qtbase >= 5.6.0
BuildRequires:  mingw32-qt5-qtbase-devel
BuildRequires:  mingw32-qt5-qtbase-static
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-qt5-qtbase >= 5.6.0
BuildRequires:  mingw64-qt5-qtbase-devel
BuildRequires:  mingw64-qt5-qtbase-static
BuildRequires:  mingw64-zlib

BuildRequires:  python


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtDeclarative component
BuildArch:      noarch

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.

%package -n mingw32-qt5-qmldevtools
Summary:       Qt5 for Windows build environment
Requires:      mingw32-qt5-%{qt_module} = %{version}-%{release}

%description -n mingw32-qt5-qmldevtools
Contains the files required to get various Qt tools built
which are part of the mingw-qt5-qttools package

%package -n mingw32-qt5-qmldevtools-devel
Summary:       Qt5 for Windows build environment
Requires:      mingw32-qt5-qmldevtools = %{version}-%{release}

%description -n mingw32-qt5-qmldevtools-devel
Contains the files required to get various Qt tools built
which are part of the mingw-qt5-qttools package

%package -n mingw32-qt5-%{qt_module}-static
Summary:       Static version of the mingw32-qt5-qtdeclarative library
Requires:      mingw32-qt5-qtdeclarative = %{version}-%{release}
Requires:      mingw32-qt5-qtbase-static
BuildArch:     noarch

%description -n mingw32-qt5-%{qt_module}-static
Static version of the mingw32-qt5-qtdeclarative library.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt for Windows - QtDeclarative component
BuildArch:      noarch

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.

%package -n mingw64-qt5-qmldevtools
Summary:       Qt5 for Windows build environment
Requires:      mingw64-qt5-%{qt_module} = %{version}-%{release}

%description -n mingw64-qt5-qmldevtools
Contains the files required to get various Qt tools built
which are part of the mingw-qt5-qttools package

%package -n mingw64-qt5-qmldevtools-devel
Summary:       Qt5 for Windows build environment
Requires:      mingw64-qt5-qmldevtools = %{version}-%{release}

%description -n mingw64-qt5-qmldevtools-devel
Contains the files required to get various Qt tools built
which are part of the mingw-qt5-qttools package

%package -n mingw64-qt5-%{qt_module}-static
Summary:       Static version of the mingw64-qt5-qtdeclarative library
Requires:      mingw64-qt5-qtdeclarative = %{version}-%{release}
Requires:      mingw64-qt5-qtbase-static
BuildArch:     noarch

%description -n mingw64-qt5-%{qt_module}-static
Static version of the mingw64-qt5-qtdeclarative library.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}
%patch0 -p1
%patch1 -p1
%patch2 -p0
#patch3 -p0


%build
MINGW_BUILDDIR_SUFFIX=_static %mingw_qmake_qt5 ../%{qt_module}.pro CONFIG+=static DEFINES+=QT_OPENGL_ES_2_ANGLE_STATIC
MINGW_BUILDDIR_SUFFIX=_static %mingw_make %{?_smp_mflags}

MINGW_BUILDDIR_SUFFIX=_shared %mingw_qmake_qt5 ../%{qt_module}.pro
MINGW_BUILDDIR_SUFFIX=_shared %mingw_make %{?_smp_mflags}


%install
MINGW_BUILDDIR_SUFFIX=_static %mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT/static
MINGW_BUILDDIR_SUFFIX=_shared %mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Move the static libraries from the static tree to the main tree
mv $RPM_BUILD_ROOT/static%{mingw32_libdir}/*.a $RPM_BUILD_ROOT%{mingw32_libdir}
mv $RPM_BUILD_ROOT/static%{mingw64_libdir}/*.a $RPM_BUILD_ROOT%{mingw64_libdir}

# Clean up the static trees as we've now merged all interesting pieces
rm -rf $RPM_BUILD_ROOT/static

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete

# The .dll's are installed in both %%{mingw32_bindir} and %%{mingw32_libdir}
# One copy of the .dll's is sufficient
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*.dll
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*.dll

# Prevent file conflict with mingw-qt4
mv $RPM_BUILD_ROOT%{mingw32_bindir}/qmlplugindump.exe $RPM_BUILD_ROOT%{mingw32_bindir}/qmlplugindump-qt5.exe
mv $RPM_BUILD_ROOT%{mingw64_bindir}/qmlplugindump.exe $RPM_BUILD_ROOT%{mingw64_bindir}/qmlplugindump-qt5.exe

# Remove unneeded files
rm -f $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libQt5QmlDevTools.la
rm -f $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/pkgconfig/Qt5QmlDevTools.pc
rm -f $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libQt5QmlDevTools.la
rm -f $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/pkgconfig/Qt5QmlDevTools.pc

# Create a list of .dll.debug files which need to be excluded from the main packages
# Note: the .dll.debug files aren't created yet at this point (as it happens after
# the %%install section). Therefore we have to assume that all .dll files will
# eventually get a .dll.debug counterpart
find $RPM_BUILD_ROOT%{mingw32_datadir}/qt5 | grep .dll| sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw32-qt5-%{qt_module}.excludes
find $RPM_BUILD_ROOT%{mingw64_datadir}/qt5 | grep .dll| sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw64-qt5-%{qt_module}.excludes


# Win32
%files -n mingw32-qt5-%{qt_module} -f mingw32-qt5-%{qt_module}.excludes
%{mingw32_bindir}/Qt5Qml.dll
%{mingw32_bindir}/Qt5Quick.dll
%{mingw32_bindir}/Qt5QuickParticles.dll
%{mingw32_bindir}/Qt5QuickTest.dll
%{mingw32_bindir}/Qt5QuickWidgets.dll
%{mingw32_bindir}/qml.exe
%{mingw32_bindir}/qmleasing.exe
%{mingw32_bindir}/qmlplugindump-qt5.exe
%{mingw32_bindir}/qmlprofiler.exe
%{mingw32_bindir}/qmlscene.exe
%{mingw32_bindir}/qmltestrunner.exe
%{mingw32_includedir}/qt5/QtQml/
%{mingw32_includedir}/qt5/QtQmlDevTools/
%{mingw32_includedir}/qt5/QtQuick/
%{mingw32_includedir}/qt5/QtQuickParticles/
%{mingw32_includedir}/qt5/QtQuickTest/
%{mingw32_includedir}/qt5/QtQuickWidgets/
%{mingw32_libdir}/libQt5Qml.dll.a
%{mingw32_libdir}/libQt5Quick.dll.a
%{mingw32_libdir}/libQt5QuickParticles.dll.a
%{mingw32_libdir}/libQt5QuickTest.dll.a
%{mingw32_libdir}/libQt5QuickWidgets.dll.a
%{mingw32_libdir}/cmake/Qt5Qml/
%{mingw32_libdir}/cmake/Qt5Quick/
%{mingw32_libdir}/cmake/Qt5QuickTest/
%{mingw32_libdir}/cmake/Qt5QuickWidgets/
%{mingw32_libdir}/pkgconfig/Qt5Qml.pc
%{mingw32_libdir}/pkgconfig/Qt5Quick.pc
%{mingw32_libdir}/pkgconfig/Qt5QuickTest.pc
%{mingw32_libdir}/pkgconfig/Qt5QuickWidgets.pc
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_debugger.dll
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_inspector.dll
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_local.dll
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_native.dll
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_profiler.dll
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_server.dll
%{mingw32_libdir}/qt5/plugins/qmltooling/qmldbg_tcp.dll
%{mingw32_datadir}/qt5/qml/Qt/labs/folderlistmodel/
%{mingw32_datadir}/qt5/qml/Qt/labs/settings/
%{mingw32_datadir}/qt5/qml/QtQml/
%{mingw32_datadir}/qt5/qml/QtQuick.2/
%{mingw32_datadir}/qt5/qml/QtQuick/
%{mingw32_datadir}/qt5/qml/QtTest/
%{mingw32_datadir}/qt5/qml/builtins.qmltypes
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_qml.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_qml_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_qmldevtools_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_qmltest.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_qmltest_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_quick.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_quick_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_quickparticles_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_quickwidgets.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_quickwidgets_private.pri

# These folders are not used by qtdeclarative itself, but
# by other Qt5 components which depend on qtdeclarative
%dir %{mingw32_datadir}/qt5/qml/
%dir %{mingw32_datadir}/qt5/qml/Qt/
%dir %{mingw32_datadir}/qt5/qml/Qt/labs/

%files -n mingw32-qt5-qmldevtools
%{_prefix}/%{mingw32_target}/bin/qt5/qmlimportscanner
%{_prefix}/%{mingw32_target}/bin/qt5/qmllint
%{_prefix}/%{mingw32_target}/bin/qt5/qmlmin
%{_prefix}/%{mingw32_target}/lib/libQt5QmlDevTools.so

%files -n mingw32-qt5-qmldevtools-devel
%{_prefix}/%{mingw32_target}/lib/libQt5QmlDevTools.so.5*

%files -n mingw32-qt5-%{qt_module}-static
%{mingw32_libdir}/libQt5Qml.a
%{mingw32_libdir}/libQt5Quick.a
%{mingw32_libdir}/libQt5QuickParticles.a
%{mingw32_libdir}/libQt5QuickTest.a
%{mingw32_libdir}/libQt5QuickWidgets.a


# Win64
%files -n mingw64-qt5-%{qt_module} -f mingw64-qt5-%{qt_module}.excludes
%{mingw64_bindir}/Qt5Qml.dll
%{mingw64_bindir}/Qt5Quick.dll
%{mingw64_bindir}/Qt5QuickParticles.dll
%{mingw64_bindir}/Qt5QuickTest.dll
%{mingw64_bindir}/Qt5QuickWidgets.dll
%{mingw64_bindir}/qml.exe
%{mingw64_bindir}/qmleasing.exe
%{mingw64_bindir}/qmlplugindump-qt5.exe
%{mingw64_bindir}/qmlprofiler.exe
%{mingw64_bindir}/qmlscene.exe
%{mingw64_bindir}/qmltestrunner.exe
%{mingw64_includedir}/qt5/QtQml/
%{mingw64_includedir}/qt5/QtQmlDevTools/
%{mingw64_includedir}/qt5/QtQuick/
%{mingw64_includedir}/qt5/QtQuickParticles/
%{mingw64_includedir}/qt5/QtQuickTest/
%{mingw64_includedir}/qt5/QtQuickWidgets/
%{mingw64_libdir}/libQt5Qml.dll.a
%{mingw64_libdir}/libQt5Quick.dll.a
%{mingw64_libdir}/libQt5QuickParticles.dll.a
%{mingw64_libdir}/libQt5QuickTest.dll.a
%{mingw64_libdir}/libQt5QuickWidgets.dll.a
%{mingw64_libdir}/cmake/Qt5Qml/
%{mingw64_libdir}/cmake/Qt5Quick/
%{mingw64_libdir}/cmake/Qt5QuickTest/
%{mingw64_libdir}/cmake/Qt5QuickWidgets/
%{mingw64_libdir}/pkgconfig/Qt5Qml.pc
%{mingw64_libdir}/pkgconfig/Qt5Quick.pc
%{mingw64_libdir}/pkgconfig/Qt5QuickTest.pc
%{mingw64_libdir}/pkgconfig/Qt5QuickWidgets.pc
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_debugger.dll
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_inspector.dll
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_local.dll
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_native.dll
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_profiler.dll
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_server.dll
%{mingw64_libdir}/qt5/plugins/qmltooling/qmldbg_tcp.dll
%{mingw64_datadir}/qt5/qml/Qt/labs/folderlistmodel/
%{mingw64_datadir}/qt5/qml/Qt/labs/settings/
%{mingw64_datadir}/qt5/qml/QtQml/
%{mingw64_datadir}/qt5/qml/QtQuick.2/
%{mingw64_datadir}/qt5/qml/QtQuick/
%{mingw64_datadir}/qt5/qml/QtTest/
%{mingw64_datadir}/qt5/qml/builtins.qmltypes
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_qml.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_qml_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_qmldevtools_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_qmltest.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_qmltest_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_quick.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_quick_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_quickparticles_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_quickwidgets.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_quickwidgets_private.pri

# These folders are not used by qtdeclarative itself, but
# by other Qt5 components which depend on qtdeclarative
%dir %{mingw64_datadir}/qt5/qml/
%dir %{mingw64_datadir}/qt5/qml/Qt/
%dir %{mingw64_datadir}/qt5/qml/Qt/labs/

%files -n mingw64-qt5-qmldevtools
%{_prefix}/%{mingw64_target}/bin/qt5/qmlimportscanner
%{_prefix}/%{mingw64_target}/bin/qt5/qmllint
%{_prefix}/%{mingw64_target}/bin/qt5/qmlmin
%{_prefix}/%{mingw64_target}/lib/libQt5QmlDevTools.so

%files -n mingw64-qt5-qmldevtools-devel
%{_prefix}/%{mingw64_target}/lib/libQt5QmlDevTools.so.5*

%files -n mingw64-qt5-%{qt_module}-static
%{mingw64_libdir}/libQt5Qml.a
%{mingw64_libdir}/libQt5Quick.a
%{mingw64_libdir}/libQt5QuickParticles.a
%{mingw64_libdir}/libQt5QuickTest.a
%{mingw64_libdir}/libQt5QuickWidgets.a


%changelog
* Thu Aug 25 2016 Martin Bříza <mbriza@redhat.com> - 5.6.0-2
- Fix crashes in the QML engine related to dead store elimination

* Mon Mar 28 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1

* Thu Aug  6 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 21 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Mon Dec 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0
- Added -static subpackages (RHBZ #1123776)

* Sat Sep 20 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul  6 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Sun Jan 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-4
- Don't carry .dll.debug files in main package

* Mon Jan  6 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-3
- Dropped manual rename of import libraries

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-2
- Removed BR: mingw{32,64}-qt5-qtjsbackend (unnecessary as of Qt 5.2)

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.rc1
- Update to 5.2.0 RC1

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1

* Fri Aug  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-2
- Make sure the QmlDevTools library is built as a shared library
- Added mingw{32,64}-qt5-qmldevtools-devel subpackages

* Thu Jul 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0
- Added mingw{32,64}-qt5-qmldevtools subpackages
- Changed URL to http://qt-project.org/

* Sun May 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2
- Own the folders %%{mingw32_datadir}/qt5/qml, %%{mingw32_datadir}/qt5/qml/Qt,
  %%{mingw32_datadir}/qt5/qml/Qt/labs, %%{mingw64_datadir}/qt5/qml,
  %%{mingw64_datadir}/qt5/qml/Qt and %%{mingw64_datadir}/qt5/qml/Qt/labs

* Sat Feb  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1

* Thu Jan  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-1
- Update to Qt 5.0.0 Final

* Sun Nov 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1.git20121111.dd1d6b56
- Update to 20121111 snapshot (rev dd1d6b56)
- Rebuild against latest mingw-qt5-qtbase
- Dropped pkg-config rename hack as it's unneeded now
- Dropped upstreamed patch

* Wed Sep 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial release

