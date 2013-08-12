Name:		cpptasks
Version:	1.0b5
Release:	12%{?dist}
Summary:	Compile and link task for ant

Group:		Development/Libraries

License:	ASL 2.0
URL:		http://ant-contrib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ant-contrib/cpptasks-1.0b5.tar.gz
Source1:	%{name}-README.fedora

BuildRequires:	ant 
BuildRequires:	maven-local

BuildArch:	noarch

%description
This ant task can compile various source languages and produce
executables, shared libraries (aka DLL's) and static libraries. Compiler
adaptors are currently available for several C/C++ compilers, FORTRAN,
MIDL and Windows Resource files.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description	javadoc
Javadoc documentation for %{summary}.

%prep
%setup -q

find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

sed -i 's/\r//' NOTICE 

cp -p %{SOURCE1} ./README.fedora

# Use default compiler configuration
%pom_remove_plugin :maven-compiler-plugin

# Fix dependency on ant
%pom_remove_dep ant:ant
%pom_remove_dep ant:ant-nodeps
%pom_remove_dep ant:ant-trax
%pom_add_dep org.apache.ant:ant

%mvn_file :%{name} ant/%{name}

%build
%mvn_build

%install
%mvn_install

# Place a file into ant's config dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/
echo "ant/%{name}" > $RPM_BUILD_ROOT/%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%doc LICENSE NOTICE README.fedora
%{_sysconfdir}/ant.d/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
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

* Sat Sep 02 2005 Anthony Green <green@redhat.com> - 0:1.0-0.b3.2jpp_1%{?dist}
- Remove "ghost" for javadocs and javadoc postprocessing.
- Place in Development/Libraries, not Development/Libraries/Java.
- Remove epoch references.
- Build into Fedora Extras.

* Mon Sep 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b3.2jpp
- Upgrade to Ant 1.6.X
- Build with ant-1.6.2
- Upgraded to 1.0.b3 and relaxed requirements on Thu Jul 15 2004 
by Ralph Apel <r.apel at r-apel.de> as 0:1.0-0.b3.1jpp

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b2.4jpp
- Build with ant-1.6.2
- Relax versioned BuildReq
- Drop junit runtime requirement

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b2.3jpp
- Also runtime dep to Ant 1.6.X

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.0-0.b2.2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b2.1jpp
- First JPackage release
