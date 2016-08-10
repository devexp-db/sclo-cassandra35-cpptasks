%{?scl:%scl_package cpptasks}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}cpptasks
Version:	1.0b5
Release:	17%{?dist}
Summary:	Compile and link task for ant

License:	ASL 2.0
URL:		http://ant-contrib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ant-contrib/%{pkg_name}-%{version}.tar.gz
Source1:	%{pkg_name}-README.fedora

BuildRequires:	%{?scl_java_prefix}ant 
BuildRequires:	%{?scl_java_prefix}maven-local
BuildRequires:	%{?scl_mvn_prefix}maven-source-plugin
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
This ant task can compile various source languages and produce
executables, shared libraries (aka DLL's) and static libraries. Compiler
adaptors are currently available for several C/C++ compilers, FORTRAN,
MIDL and Windows Resource files.

%package        javadoc
Summary:	Javadoc for %{name}

%description	javadoc
Javadoc documentation for %{name}.

%prep
%{?scl_enable}
%setup -q -n %{pkg_name}-%{version}

find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

sed -i 's/\r//' NOTICE 

cp -p %{SOURCE1} ./README.fedora

# Use default compiler configuration
%pom_remove_plugin :maven-compiler-plugin

# Let xmvn generate javadocs
%pom_remove_plugin :maven-javadoc-plugin

# Fix dependency on ant
%pom_remove_dep ant:ant
%pom_remove_dep ant:ant-nodeps
%pom_remove_dep ant:ant-trax
%pom_add_dep org.apache.ant:ant

%mvn_file :%{pkg_name} ant/%{pkg_name}
%{?scl_disable}

%build
%{?scl_enable}
%mvn_build
%{?scl_disable}

%install
%{?scl_enable}
%mvn_install
%{?scl_disable}

# Place a file into ant's config dir
%{!?scl:mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/}
%{?scl:mkdir -p $RPM_BUILD_ROOT%{_root_sysconfdir}/ant.d/}
%{!?scl:echo "ant/%{pkg_name}" > $RPM_BUILD_ROOT/%{_sysconfdir}/ant.d/%{pkg_name}}
%{?scl:echo "ant/%{pkg_name}" > $RPM_BUILD_ROOT/%{_root_sysconfdir}/ant.d/%{pkg_name}}

%files -f .mfiles
%doc LICENSE NOTICE README.fedora
%{!?scl:%{_sysconfdir}/ant.d/%{pkg_name}}
%{?scl:%{_root_sysconfdir}/ant.d/%{pkg_name}}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Wed Aug 10 2016 Tomas Repik <trepik@redhat.com> - 1.0b5-17
- scl conversion
- added missing build dependency (maven-source-plugin)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0b5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Mat Booth <mat.booth@redhat.com> - 1.0b5-15
- Fix FTBFS

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0b5-12
- Use default compiler config and fix bad deps on ant.

* Sun Aug 11 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0b5-11
- Build with maven 3, update for newer guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 03 2009 D Haley <mycae@yahoo.com> - 1.0b5-5
- Req needs whitespace

* Thu Sep 03 2009 D Haley <mycae@yahoo.com> - 1.0b5-4
- tag bump

* Thu Sep 03 2009 D Haley <mycae@yahoo.com> - 1.0b5-3
- Remove excess BR
- Fix subpackage dep
- Fix doc installation 

* Fri Aug 28 2009 D Haley <mycae@yahoo.com> - 1.0b5-2
- Fix doc installation 
- Move to _javadir/ant/ rather than _javadir/
- Fix requires + buildrequires for both main and javadoc packages
- Add README.fedora source in lieu of  maven build 

* Sat Mar 14 2009 D Haley <mycae@yahoo.com> - 1.0b5-1
- Update to b5
- cpptasks now uses difficult mvn-doxia xdoc, so remove manual subpackage
- Add distribution jar check
- EOL conversion on NOTICE
- Change summary & format description
- Fix BuildRoot 
- Change licence to ASL 2.0 from Apache Software Licence 2.0
- Documentation to "Documentation" Group
