#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	XML Schema validator and decoder
Summary(pl.UTF-8):	Biblioteka do sprawdzania poprawności i dekodowania schematów XML
Name:		python-xmlschema
Version:	1.0.18
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/xmlschema/
Source0:	https://files.pythonhosted.org/packages/source/x/xmlschema/xmlschema-%{version}.tar.gz
# Source0-md5:	f3e7f9002aeb9846af68f81c6ec82200
URL:		https://pypi.org/project/xmlschema/
%if %{with python2}
BuildRequires:	python-elementpath >= 1.3.0
BuildRequires:	python-elementpath < 1.4.0
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-elementpath >= 1.3.0
BuildRequires:	python3-elementpath < 1.4.0
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The xmlschema library is an implementation of XML Schema
(<http://www.w3.org/2001/XMLSchema>) for Python.

%description -l pl.UTF-8
Biblioteka xmlschema to implementacja XML Schema
(<http://www.w3.org/2001/XMLSchema>) dla Pythona.

%package -n python3-xmlschema
Summary:	XML Schema validator and decoder
Summary(pl.UTF-8):	Biblioteka do sprawdzania poprawności i dekodowania schematów XML
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-xmlschema
The xmlschema library is an implementation of XML Schema
(<http://www.w3.org/2001/XMLSchema>) for Python.

%description -n python3-xmlschema -l pl.UTF-8
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

%{__sed} -i -e 's/^SKIP_REMOTE_TESTS =.*/SKIP_REMOTE_TESTS = True/' xmlschema/tests/__init__.py

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python} xmlschema/tests/test_all.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} xmlschema/tests/test_all.py
%endif
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/xmlschema/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/xmlschema/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/xmlschema
%{py_sitescriptdir}/xmlschema-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-xmlschema
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/xmlschema
%{py3_sitescriptdir}/xmlschema-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
