#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	XML Schema validator and decoder
Summary(pl.UTF-8):	Biblioteka do sprawdzania poprawności i dekodowania schematów XML
Name:		python3-xmlschema
Version:	3.4.5
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/xmlschema/
Source0:	https://files.pythonhosted.org/packages/source/x/xmlschema/xmlschema-%{version}.tar.gz
# Source0-md5:	5c58d8bf013208f8ed8137fbb020cdff
Patch0:		%{name}-remote-tests.patch
URL:		https://pypi.org/project/xmlschema/
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:61.0
%if %{with tests}
BuildRequires:	python3-elementpath >= 4.4.0
BuildRequires:	python3-elementpath < 5
BuildRequires:	python3-lxml
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-elementpath >= 4.4.0
BuildRequires:	python3-elementpath < 5
BuildRequires:	python3-jinja2
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The xmlschema library is an implementation of XML Schema
(<http://www.w3.org/2001/XMLSchema>) for Python.

%description -l pl.UTF-8
Biblioteka xmlschema to implementacja XML Schema
(<http://www.w3.org/2001/XMLSchema>) dla Pythona.

%package apidocs
Summary:	API documentation for Python xmlschema module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona xmlschema
Group:		Documentation

%description apidocs
API documentation for Python xmlschema module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona xmlschema.

%prep
%setup -q -n xmlschema-%{version}
%patch -P 0 -p1

%build
%py3_build_pyproject

%if %{with tests}
LC_ALL=C.UTF-8 \
PYTHONPATH=$(pwd) \
XMLSCHEMA_SKIP_REMOTE_TESTS=1 \
%{__python3} -m unittest
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/xmlschema-json2xml
%attr(755,root,root) %{_bindir}/xmlschema-validate
%attr(755,root,root) %{_bindir}/xmlschema-xml2json
%{py3_sitescriptdir}/xmlschema
%{py3_sitescriptdir}/xmlschema-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
