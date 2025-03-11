#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	XML Schema validator and decoder
Summary(pl.UTF-8):	Biblioteka do sprawdzania poprawności i dekodowania schematów XML
Name:		python3-xmlschema
Version:	2.1.1
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/xmlschema/
Source0:	https://files.pythonhosted.org/packages/source/x/xmlschema/xmlschema-%{version}.tar.gz
# Source0-md5:	74757314884491c5d134a5df20c6d1b8
Patch0:		%{name}-remote-tests.patch
URL:		https://pypi.org/project/xmlschema/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-elementpath >= 3.0.0
BuildRequires:	python3-elementpath < 4
BuildRequires:	python3-lxml
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-elementpath >= 3.0.0
BuildRequires:	python3-elementpath < 4
BuildRequires:	python3-jinja2
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
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
%py3_build

%if %{with tests}
XMLSCHEMA_SKIP_REMOTE_TESTS=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m unittest
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/xmlschema-json2xml
%attr(755,root,root) %{_bindir}/xmlschema-validate
%attr(755,root,root) %{_bindir}/xmlschema-xml2json
%{py3_sitescriptdir}/xmlschema
%{py3_sitescriptdir}/xmlschema-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
