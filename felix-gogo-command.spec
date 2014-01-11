%{?_javapackages_macros:%_javapackages_macros}
%if 0%{?fedora}
%else
%undefine __cp
%global __cp /bin/cp
%endif
%global project felix
%global bundle org.apache.felix.gogo.command
%global groupId org.apache.felix
%global artifactId %{bundle}

%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package %{project}-gogo-command}

Name:           %{?scl_prefix}%{project}-gogo-command
Version:        0.12.0
Release:        9.0%{?dist}
Summary:        Apache Felix Gogo Command


License:        ASL 2.0
URL:            http://felix.apache.org
Source0:        http://www.apache.org/dist/felix/%{bundle}-%{version}-project.tar.gz

Patch0:         felix-gogo-command-pom.xml.patch
Patch1:         java7compatibility.patch

BuildArch:      noarch

BuildRequires:  java
# This is to ensure we get OpenJDK and not GCJ
BuildRequires:  java-devel >= 1:1.7.0
BuildRequires:  maven-local
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  jpackage-utils
BuildRequires:  maven-install-plugin
BuildRequires:  mockito

BuildRequires:  felix-osgi-core
BuildRequires:  felix-framework
BuildRequires:  felix-osgi-compendium
BuildRequires:  %{?scl_prefix}felix-gogo-runtime
BuildRequires:  %{?scl_prefix}felix-gogo-parent
BuildRequires:  mvn(org.apache.felix:org.apache.felix.bundlerepository)
%{?scl:BuildRequires:	  %{?scl_prefix}build}

Requires:       felix-framework
Requires:       felix-osgi-compendium
Requires:       %{?scl_prefix}felix-gogo-runtime
Requires:       mvn(org.apache.felix:org.apache.felix.bundlerepository)
%{?scl:Requires: %scl_runtime}

%description
Provides basic shell commands for Gogo.

%package javadoc

Summary:        Javadoc for %{pkg_name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{pkg_name}.

%global POM %{_mavenpomdir}/JPP.%{project}-%{bundle}.pom

%prep
%setup -q -n %{bundle}-%{version} 
%patch0 -p1
%patch1 -p1

%build
mvn-rpmbuild install javadoc:aggregate

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{project}
install -m 644 target/%{bundle}-%{version}.jar \
        %{buildroot}%{_javadir}/%{project}/%{bundle}.jar

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{project}-%{bundle}.pom

%add_maven_depmap JPP.%{project}-%{bundle}.pom %{project}/%{bundle}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{pkg_name}
%__cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{pkg_name}

%files
%doc LICENSE
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%doc LICENSE
%{_javadocdir}/%{pkg_name}

%changelog
* Mon Aug 5 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-9
- Fix FTBS.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-7
- Initial SCLization.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.12.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-3
- Dependency to Java 7 added.
- Sources are patched to compile with OpenJDK 7.

* Tue Jan 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-2
- description formatting removed
- jar_repack removed
- license added to the javadoc

* Tue Jan 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-1
- Release 0.12.0
