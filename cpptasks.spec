Name:		cpptasks
Version:	1.0b5
Release:	3%{?dist}
Summary:	Compile and link task for ant

Group:		Development/Libraries

License:	ASL 2.0
URL:		http://ant-contrib.sourceforge.net/
Vendor:		Ant contrib project
Source0:	http://downloads.sourceforge.net/ant-contrib/cpptasks-1.0b5.tar.gz
Source1:	%{name}-README.fedora

BuildRequires:	ant 
BuildRequires:	ant-junit 
BuildRequires:	jpackage-utils 
BuildRequires:	junit
#BuildRequires:	mave

Requires:	ant 
Requires:	java
Requires:	jpackage-utils

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
	

%description
This ant task can compile various source languages and produce
executables, shared libraries (aka DLL's) and static libraries. Compiler
adaptors are currently available for several C/C++ compilers, FORTRAN,
MIDL and Windows Resource files.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	%{name}>=%{version}-%{release}
Requires:	jpackage-utils

%description	javadoc
Javadoc documentation for %{summary}.


#The manual for b5 has been moved to xdoc (doxia) format.
# This requires maven, which requires many dependencies which we don't have.
#%package	manual
#Summary:	Docs for %{name}
#Group:		Development/Documentation

#%description	manual
#User manual for %{summary}.

%prep
%setup -q -n %{name}-%{version}

#End of line conversion
%{__sed} -i 's/\r//' NOTICE 

#Check for exisiting jar files
JAR_files=""
for j in $(find -name \*.jar); do
if [ ! -L $j ] ; then
	JAR_files="$JAR_files $j"
	fi
done

if [ ! -z "$JAR_files" ] ; then
	echo "These JAR files should be deleted and symlinked to system JAR files: $JAR_files"
	exit 1
fi

cp -p %{SOURCE1} ./README.fedora

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
ant jars javadocs 

#In lieu of maven built docs, which requires clirr
#a URL is supplied in README.fedora
#mvn-jpp site

%install
rm -rf $RPM_BUILD_ROOT


# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}/ant/
install -Dpm 644 target/lib/%{name}.jar \
	$RPM_BUILD_ROOT%{_javadir}/ant/%{name}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}/ant/
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}.jar
popd

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

cp -pr target/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# manual - 
#install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

#Place a file into ant's config dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/
echo "%{name} ant/%{name}" > $RPM_BUILD_ROOT/%{_sysconfdir}/ant.d/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.fedora
%{_javadir}/ant/*.jar
%{_sysconfdir}/ant.d/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

#%files manual
#%defattr(-,root,root,-)
#%doc %{_docdir}/%{name}-%{version}

# -----------------------------------------------------------------------------

%changelog
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
